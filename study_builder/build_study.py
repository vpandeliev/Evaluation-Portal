#!/usr/bin/env python
"""
    Something descriptive
    
    TODO:
        1) create an xml schema for acceptable settings.xml files and validate 
            against it (verify_study_directory())
            
        2) verify that the Tangra django directory is valid 
            (verify_django_directory())
"""
import os, sys, getopt

from study_builder import StudySettings


# Required command line options. These are set by process_options()
study_settings_dir = None
django_root_dir = None


def usage(msg):
    """ Prints a usage message to stdout."""
    if (msg):
        sys.stderr.write("{0}\n".format(msg.strip()))
        
    sys.stderr.write("usage: a b c d e f g.\n")
    sys.exit(1)


def verify_study_directory(dir):
    """ Verifies that the study directory has the correct structure. exit()s with
    a useful error message if something out of the ordinary is found.
    """
    print "OooooooOooOOOooooh yeeeeeeeaaaaaah! Verified study directory."


def verify_django_directory(dir):
    """ Verifies that the django directory has the correct structure. exit()s 
    with a useful error message if something out of the ordinary is found.
    """
    print "OooooooOooOOOooooh yeeeeeeeaaaaaah! Verified django directory."


def process_options():
    """Process command line options."""
    global study_settings_dir, django_root_dir
    
    optlist, args = getopt.getopt(sys.argv[1:], "s:d:")
    for opt, arg in optlist:
        if opt == "-s":
            study_settings_dir = arg
        elif opt == "-d":
            django_root_dir = arg
        else:
            usage("Unhandled option.")
    
    if not study_settings_dir:
        usage("Study settings directory (-s) is required.")
    
    if not django_root_dir:
        usage("Django root directory (-d) is required.")


if __name__ == "__main__":
    process_options()
    verify_study_directory(study_settings_dir)
    verify_django_directory(django_root_dir)
    
    settings = StudySettings(study_settings_dir)
    
    print(settings)







