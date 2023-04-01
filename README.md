This is a python package for the Timeular API. 

This is for learning purposes only. 

Use this as a guide to build your own with the timeular-api-start respository


Steps I took: 

Created folders
Added __init__.py where appropriate (required in any folder that is imported)
Added my .py files where I wanted them
Created setup.py file
Created .gitignore file (https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore)
Created requirements.txt (pip freeze > requirements.txt)

Ipython and Black
    I like to add these for my personal preference and ease of use, but the package doesn't actually require them. 

    Ipython for testing and running functions
    Black for formatting files

/tests 
    tried working with pytest

logging
    I added logging to all the files, and created a submodule that sets up the logger everytime the package is imported, just pushes logs to a local file. 

    Used the __init__.py to do this. 

After making a change: 
$ black src
$ black tests
$ pytest
$ pip install -e .
$ ipython
: from joesTime import api
: from joesTime.utils import entry