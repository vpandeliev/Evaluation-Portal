#!/usr/bin/env python
"""
    Something descriptive goes here
    
    TODO:
        1) create an xml schema for acceptable settings.xml files and validate 
            against it (verify_study_directory())
            
        2) verify that the Tangra django directory is valid 
            (verify_django_directory())
"""
import os, sys, getopt

from study_builder import StudySettings


def verify_study_directory(study_dir):
    """ Verifies that the study directory has the correct structure. exit()s with
    a useful error message if something out of the ordinary is found.
    """
    print "OooooooOooOOOooooh yeeeeeeeaaaaaah! Didn't verify study directory."


def get_study_settings(study_dir):
    verify_study_directory(study_dir)
    settings = StudySettings(study_dir)
    return settings








