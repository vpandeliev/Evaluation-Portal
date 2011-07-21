from django.conf import settings

import os



def get_user_study_dir():
    """
        Returns a relative path to the user studies directory.
        
        TODO: Find a more robust way to the user_studies directory
    """
    return settings.ROOT_PATH + "/portal/user_studies"


def get_user_study_names():
    """
        Returns a list of the base names of all available study directories
    """
    module_dir = get_user_study_dir()
    files = ["{0}/{1}".format(module_dir, f) for f in os.listdir(module_dir)]
    study_dirs = [f for f in files if os.path.isdir(f)]
    
    return [os.path.basename(d) for d in study_dirs]


def get_study_directory(base_name):
    """Returns a full path to the studies directory for the study with the given
    directory name
    """
    return settings.ROOT_PATH + "/portal/user_studies/" + base_name