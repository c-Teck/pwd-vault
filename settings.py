#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 06:53:59 2021

@author: cybree
"""

# settings.py
## importing the load_dotenv from the python-dotenv module
from dotenv import load_dotenv
 
## using existing module to specify location of the .env file
from pathlib import Path
import os
 
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
 
# retrieving keys and adding them to the project
# from the .env file through their key names
if not os.getenv("SALT"):
    print("EMpty")

def check_func(Func_to_check):

#DOMAIN = os.getenv("DOMAIN")
#EMAIL = os.getenv("EMAIL")
