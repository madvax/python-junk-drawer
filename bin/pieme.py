#!/usr/bin/env python

# Quick utility to create pie chart images from command line data 
# This is a quick an dirty solution. 
# You have to provide four numbers and an output file name.

from pylab import *
import sys, os

VERSION = "1.0.0"                               # Version for this library
FIRST   = 0                                     # First list index
LAST    = -1                                    # Last list index
ME      = os.path.split(sys.argv[FIRST])[LAST]  # Name of this file


def usage():
   print "%s, Version %s" %(ME, VERSION)
   print "Summary: Utility to create pie chart images from command line data"
   print ""
   print "Usage: %s PercentPassing OutputFilename" %ME
   print ""
   print "Note: Both arguments are required" 
   print ""
   print "Return Codes:"
   print "  0 - Success"
   print "  1 - Bad or missing command line arguments"
   print "  2 - Output file already exists"
   print "  3 - Otherwise unable to create output file, see folder permissions"
   print "  Any other code represents a general failure"
   print ""
   return


# Get the command line data
if len(sys.argv) != 3:
   usage()
   exit(1)

percentPassing = float(sys.argv[1])
percentFailing = float(100.00 - percentPassing) 

# make a square figure and axes
plt.figure(1, figsize=(6,6))
ax = axes([0.1, 0.1, 0.8, 0.8])

# The slices will be ordered and plotted counter-clockwise.
labels  = ['Passed', 'Failed']
fracs   = [percentPassing, percentFailing]
colors  = ["green", "red"]
explode = (0, 0.05)
pie(fracs             , 
    explode     = explode  , 
    labels      = labels   ,
    autopct     = '%1.0f%%', 
    shadow      = True     , 
    startangle  = 90       ,
    colors      = colors   )
title('Test Result Summary', bbox={'facecolor':'0.8', 'pad':5})


if os.path.isfile(sys.argv[2]):
   sys.stderr.write("\nERROR -- Cannot overwrite %s\n\n" %sys.argv[2])
   exit(2)
else:
   try:
      savefig(sys.argv[2])
   except:
      sys.stderr.write("\nERROR -- Unable to save image %s\n\n" %sys.argv[2])
      # show()
      exit(3)
exit(0)
