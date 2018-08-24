#!/usr/bin/env python

# This script disconnects the existing android adb connection 
# and establishes a new conection to the android device via adb

# Standard library imports 
import sys
import time 
import os
from getopt import getopt 

# Dictionary 
VERSION             = "1.2.0" # Version for this script
DEBUG               = False   # Flag for debug operation
VERBOSE             = False   # Flag for verbose operation
FIRST               = 0       # First list index
LAST                = -1      # Last list index
ME                  = os.path.split(sys.argv[FIRST])[LAST]        # Name of this file
MY_PATH             = os.path.dirname(os.path.realpath(__file__)) # Path for this file
LIBRARY_PATH        = os.path.join(MY_PATH, "../lib")             # Custom library path
CONFIGURATION_NAME  = "testmaster.conf"                           # Configuration file name 
CONFIGURATION_PATH  = os.path.join(MY_PATH, "../etc")             # Configuration file path
CONFIGURATION_FILE  = os.path.join(CONFIGURATION_PATH, CONFIGURATION_NAME)
ANDROID_ADB         = "/home/test/Android/Sdk/platform-tools/adb"
ANDROID_DEVICES     = ANDROID_ADB + " devices"    # \
ANDROID_DISCONNECT  = ANDROID_ADB + " disconnect" #  > Some useful adb commands 
ANDROID_CONNECT     = ANDROID_ADB + " connect"    # / 
DELAY               = 2 # Generic number of seconds to wait 

# Custom Library Imports 
sys.path.append(LIBRARY_PATH)
try:
   import ns_Command
   if DEBUG: print "Successfully imported the \"ns_Command\" library, version %s" %ns_Command.VERSION
except Exception as e:
   print "ERROR -- Unale to import the \"ns_Command\" library"
   print e
   sys.exit(2)

# Native Functions 

# ------------------------------------------------------------------------------ usage()
def usage():
   """ usage() --> 0 Prints the usage statement to stdout """
   print ""
   print "%s, Version %s" %(ME, VERSION)
   print ""
   print "SUMMARY: Reconnects to the Android Device via ADB"
   print ""
   print "USAGE: %s [OPTIONS]" %ME
   print ""
   print "OPTIONS:"
   print " -h --help               Display this help message. "
   print " -d --debug              Executes the script in 'debug' mode (interactive)."
   print " -v --verbose            Generates verbose output on stdout. "
   print ""
   print "NOTE: Uses the testmaster config file for connection parameters"
   print ""
   print "EXIT CODES:"
   print "   0  Successful completion of %s " %ME
   print "   1  Bad or missing command line arguments "
   print "   2  Unable to import one or more custom libraries"
   print "   3  Unable to read configuration file %s" %CONFIGURATION_FILE
   print "   4  Unableto establish a connection to the Android Device"
   print ""
   print "EXAMPLES: "
   print "  TODO: Add Examples\n\n"
   return None

# ------------------------------------------------------------------------------ configFile2dictionary()
def configFile2dictionary(configFile, delimeter=' '):
   """ configFile2dictionary(configFile) --> {configurations...}
       Given a configuration file, this function returns a dictionary of
       key-value pairs from that file. """
   # TODO: Encrypt the configuration file . . . maybe 
   configurations = {}
   try:
      confFileData = open(configFile, 'r').read()
      for line in confFileData.split('\n'):
         line = line.strip()     # Clean up leading and trailing whitespace
         if len(line) < 1:
            pass                 # Skip blank lines
         elif line[FIRST] == '#':
            pass                 # Skip comment lines
         elif line.find(delimeter) == -1:
            pass                 # Skip mal-formed lines (lines without an equal sign character'=')
         else:
            line  = line.strip() # Clean up the whitespace
            key   = line.split(delimeter, 1)[FIRST].strip()
            value = line.split(delimeter, 1)[LAST].strip()
            configurations[key] = value
   except Exception as e:
      print "Unable to read from configurations file %s" %configFile
      configurations = {} # Trust no one. If there was a problem then flush the data
   return configurations

# Parse command line arguments 

try:
   arguments = None
   try:
      arguments = getopt( sys.argv[1:] ,
                          "hdv"        ,
                          ['help'   ,
                           'debug'  ,
                          'verbose' ]  )
   except:
      print "ERROR -- %s bad or missing command line arguments." %ME
      usage()               
      sys.exit(1)
   # Check for a help switch option
   for arg in arguments[0]:
      if arg[0]== "-h" or arg[0] == "--help":
         usage()
         sys.exit(0)
   # Check for a Verbose switch option
   for arg in arguments[0]:
      if arg[0]== "-v" or arg[0] == "--verbose":
         VERBOSE = True
   # Check for Debug option. Debug implies Verbose
   for arg in arguments[0]:
      if arg[0]== "-d" or arg[0] == "--debug":
         DEBUG   = True
         VERBOSE = True 
except Exception as e:
      print "ERROR -- %s bad or missing command line arguments." %ME
      print e                       
      sys.exit(1)                

# Read the configuration file  
configs = {}
try:
   configs = configFile2dictionary(CONFIGURATION_FILE)
except Exception as e:
   print "ERROR -- Unable to read the configuration file %s" %CONFIGURATION_FILE
   print e
   sys.exit(3)
if DEBUG:
   print "Using IP Address \"%s\"" %configs["rhw_ip_address"]
   print "Using IP Port    \"%s\"" %configs["rhw_port_number"]

if DEBUG: print "Disconnecting ...", 
c = ns_Command.Command(ANDROID_DISCONNECT)
c.run()
if DEBUG: print "Done" 
time.sleep(DELAY)
if DEBUG: print "Connecting ...",
connectionString =  "%s %s:%s" %(ANDROID_CONNECT, configs["rhw_ip_address"], configs["rhw_port_number"])
c = ns_Command.Command(connectionString)
c.run()
if DEBUG: print "Done" 
time.sleep(DELAY)
c = ns_Command.Command(ANDROID_DEVICES)
c.run()
if DEBUG: print c.returnResults()["output"]

# Check to see if we are actually connected 
if "%s:%s" %(configs["rhw_ip_address"], configs["rhw_port_number"]) in c.returnResults()["output"]:
   if VERBOSE: print "Successfully connected to the Android Device" 
   returnCode = 0
else: 
   print "ERROR -- Unable to connect to device at %s:%s" %(configs["rhw_ip_address"], configs["rhw_port_number"])
   returnCode = 4



