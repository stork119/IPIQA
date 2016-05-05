#! /usr/bin/python

"""
rpy2- GET READY TO WORK (EASY)

I. Required installed software:
- R
- pip

II. Pre-installation procedures:
1. Adding new variables in the system variable field:
- R_USER (username)
- R_HOME (path/to/installed/r) / (or just add your R path to your system PATHS)

III. Example rpy2 installation:
1. Download pre-compiled binary package for Windows (http://www.lfd.uci.edu/~gohlke/pythonlibs/)
2. In command line type:
    py -m pip install rpy2

IV. R packages' installation. [list of needed packages will show up soon]

... You can just use the code below by running this script. [source: http://rpy2.readthedocs.io/]

"""

import rpy2.robjects.packages as rpackages

packnames = ('ggplot2', 'hexbin') # R package names

if all(rpackages.isinstalled(x) for x in packnames):
    have_tutorial_packages = True
else:
    have_tutorial_packages = False

if not have_tutorial_packages:
    # import R's utility package
    utils = rpackages.importr('utils')
    # select a mirror for R packages
    utils.chooseCRANmirror(ind=1) # select the first mirror in the list
if not have_tutorial_packages:
    # R vector of strings
    from rpy2.robjects.vectors import StrVector
    # file
    packnames_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
    if len(packnames_to_install) > 0:
        utils.install_packages(StrVector(packnames_to_install))
