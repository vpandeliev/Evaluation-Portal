'''
Contains:
    run_tests - which replaces the default Django test runner
'''

import os, os.path, re
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test.simple import *


def _find_all_app_modules():
    '''Uses _find_app_modules on every app in INSTALLED_APPS'''
    mods = []
    for app_path in settings.INSTALLED_APPS:
        if app_path.startswith('django'):
            continue
        else:
            mods.extend(_find_app_modules(app_path))
    return mods
    

def _find_app_modules_given_label(app_label):
    mods = []
    for app_path in settings.INSTALLED_APPS:
        if app_label == app_path.split('.')[-1]:
            mods.extend(_find_app_modules(app_path))
    return mods


def _find_app_modules(app_path):
    '''Find modules under an app.
    
    Does not search recursively.
    
    Returns a list of imported modules, including the app package.
    '''
    mods = []
    i = app_path.rfind('.')
    assert i != -1, 'Cannot test %s' % app_path
    package_name = app_path[:i]
    label = app_path[i+1:]
    app = __import__(package_name, {}, {}, [label])
    try:
        mods.append(getattr(app, label))
    except AttributeError:
        # app_path does not refer to a package
        return []
    app_dir = mods[0].__path__[0]    
    for name in os.listdir(app_dir):
        dir_name = os.path.join(app_dir, name)
        if name.endswith('.py') and name != '__init__.py':
            name = name[:-3]
            mod = __import__(app_path, {}, {}, [name])
            mods.append(getattr(mod, name))                
        elif os.path.isdir(dir_name) and not os.path.islink(dir_name):
            mods += _find_app_modules('.'.join([app_path, name]))
    return mods


def inject_dummy_get_tests():
    def get_tests(app_module):
        '''Stupid get_tests that always returns None.

        This function is injected into django.test.simple because our
        test runner already finds the tests module (and because the
        default implementation breaks our runner).
        '''
        return None
    import django.test.simple
    django.test.simple.get_tests = get_tests


def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    """
    Run the unit tests for all the test labels in the provided list.
    Labels must be of the form:
     - app.TestClass.test_method
        Run a single specific test method
     - app.TestClass
        Run all the test methods in a given class
     - app
        Search for doctests and unittests in the named application.

    When looking for tests, the test runner will look in the models and
    tests modules for the application.
    
    A list of 'extra' tests may also be provided; these tests
    will be added to the test suite.
    
    Returns the number of tests that failed.
    """
    # Custom setup
    inject_dummy_get_tests()
    
    setup_test_environment()
    
    settings.DEBUG = False    
    suite = unittest.TestSuite()
    
    if test_labels:
        for label in test_labels:
            if '.' in label:
                suite.addTest(build_test(label))
            else:
                for mod in _find_app_modules_given_label(label):
                    t = build_suite(mod)
                    suite.addTest(t)
    else:
        for mod in _find_all_app_modules():
            suite.addTest(build_suite(mod))
    
    for test in extra_tests:
        suite.addTest(test)

    suite = reorder_suite(suite, (TestCase,))

    old_name = settings.DATABASE_NAME
    from django.db import connection
    connection.creation.create_test_db(verbosity, autoclobber=not interactive)
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    connection.creation.destroy_test_db(old_name, verbosity)
    
    teardown_test_environment()
    
    return len(result.failures) + len(result.errors)
