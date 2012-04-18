#! /usr/bin/env python 

'''
read a changelog, and get the package name

parses a changelog with this 1st line
"openmolar-namespace (2.0.5-2~unstable0) unstable; urgency=low"

usage python version_name.py [DEBFOLDER[ (full)

if full...
output is "openmolar-namespace_2.0.5-2~unstable" (withoug quotes)
else
output is "openmolar-namespace_2.0.5"
'''


import os
import re 
import sys

curdir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(sys.argv[1], "changelog")

try:
    f = open(filepath)
    data = f.read()
    f.close()

    matches = re.match("(.*) \((.*)-(.*)\)", data).groups()
    
    debname = "%s_%s"% (matches[0], matches[1])
    
    if "full" in sys.argv:
    	debname += "-%s"% matches[2]
    print (debname)

except:
    sys.exit("unable to parse changelog %s"% filepath)

