#!/usr/bin/env python

# Encrypts or decrypts a file with an eight bit key.
# The default key is 113 or binary 01110001 or hex 0x71
# Valid keys are greater than 0 and less than 255.
# Output file will be overwritten or created if necessary

# If the file is encrypted the script will decrypt it and if the 
# file is decrypted then, the script will encrypt it. No need to 
# specify the operation. 

# Default key is 113, default output file is "./a.txt"

# Intended for files the require only weak encryption.

# H. Wilson, January 2019

# -----------------------------------------------------------------------------
# Standard Library imports
import sys, os
from getopt import getopt

# -----------------------------------------------------------------------------
# Some useful variables
VERSION = "1.0.0"
VERBOSE = False
DEBUG   = False
FIRST   = 0
LAST    = -1
ME      = os.path.split(sys.argv[FIRST])[LAST]        # Name of this file
MY_PATH = os.path.dirname(os.path.realpath(__file__)) # Path for this file
PASSED  = "\033[32mPASSED\033[0m" # \
FAILED  = "\033[31mFAILED\033[0m" #  > Linux-specific colorization
ERROR   = "\033[31mERROR\033[0m"  # /
KEY              = 113     # Default key
input_file_name  = ""      # No default input file
output_file_name = "a.txt" # default output file

# ----------------------------------------------------------------------------- usage()
def usage():
   """usage() - Prints the usage message on stdout. """
   print "\n\n%s, Version %s, Encrypt/decrypt script. " %(ME,VERSION)
   print "Encrypts or decrypts the input file using an eight-bit key "
   print " "
   print "USAGE: %s [OPTIONS] " %ME
   print " "
   print "OPTIONS: "
   print "   -h --help     Display this message. "
   print "   -v --verbose  Runs the program in verbose mode, default: %s. " %VERBOSE
   print "   -d --debug    Runs the program in debug mode (implies verbose). "
   print "   -k --key=     Key to be used for encrypt/decrypt, default: %s. " %KEY 
   print "                 Valid keys are > 0 and < 255. "
   print "   -i --input=   Input file name, REQUIRED. "  
   print "   -o --output=  Output file name, default is \"%s\". " %output_file_name
   print " "
   print "EXIT CODES: "
   print "    0 - Successful completion of the program. "
   print "    1 - Bad or missing command line arguments. "
   print "    2 - Invalid key, key must be an integer. "
   print "    3 - Invalid key, key must be an integer between 0 and 255. "
   print "    4 - Input file not supplied, use -i or --input options. "
   print "    5 - Unable tocreate the output file, check file/folder permissions. "
   print "    6 - Main Program cannot be imported by another script. "
   print " " 
   print "EXAMPLES: " 
   print "    TODO - I'll make some examples up later. "
   print " "
   pass

# ----------------------------------------------------------------------------- main
if __name__ == "__main__":
 
   # Process the command line arguments 
   try:
      arguments = getopt(sys.argv[1:]        ,
                         'hvdk:o:i:'         ,
                         ['help'         ,
                          'verbose'      ,
                          'debug'        ,
                          'key='         ,
                          'input='       ,
                          'output='      ]   )
   except:
      sys.stderr.write("ERROR -- Bad or missing command line argument(s)\n\n")
      usage()
      sys.exit(1)
   # --- Check for a help option
   for arg in arguments[0]:
      if arg[0]== "-h" or arg[0] == "--help":
         usage()
         sys.exit(0)
   # --- Check for a verbose option
   for arg in arguments[0]:
      if arg[0]== "-v" or arg[0] == "--verbose":
         VERBOSE = True
   # --- Check for a debug option
   for arg in arguments[0]:
      if arg[0]== "-d" or arg[0] == "--debug":
         DEBUG   = True
         VERBOSE = True
   # --- Check for an input file option
   for arg in arguments[0]:
      if arg[0]== "-i" or arg[0] == "--input":
         input_file_name = arg[1]
         # While we are here, lets see if the input file exists
         if  not os.path.isfile(input_file_name):
             sys.stdout.write("ERROR -- Input file supplied \"%s\" does not exist." %input_file_name)
             sys.stdout.write("\n\n")
             sys.exit(3)
   # --- Check for an output file option
   for arg in arguments[0]:
      if arg[0]== "-o" or arg[0] == "--output":
         output_file_name = arg[1]
   # --- Check for a "key" option
   for arg in arguments[0]:
      if arg[0]== "-k" or arg[0] == "--key":
         try:
            candidate_key = int(arg[1])
         except:
            sys.stderr.write("ERROR -- Invalid key, key must be an integer between 0 and 255")
            sys.stderr.write("\n\n")
            sys.exit(2)
         if candidate_key < 255 and candidate_key > 0:
            KEY = candidate_key
         else:
            sys.stderr.write("ERROR -- Invalid key, key must be an integer between 0 and 255")
            sys.stderr.write("\n\n")
            sys.exit(3)

   # --------------------------------------------------------------------------
   # Verify that an input file was provided
   if input_file_name == "":
      sys.stdout.write("ERROR -- Input file not supplied. Use -i or --input")
      sys.stdout.write("\n\n")
      sys.exit(4)

   # --------------------------------------------------------------------------
   # Open the input file 
   input_file_text = open(input_file_name, 'r').read() 
   if VERBOSE: print input_file_text

   # --------------------------------------------------------------------------
   # Modify (encrypt/decrypt) the input file text with the key
   # Through the miracle of XOR encryption, if the file is encrypted it will 
   # be decrypted and if the file is decrypted it will automatically be encrypted.
   output_file_text = ""
   for character in input_file_text:                # *** ***************************** ***
      output_file_text += chr(ord(character) ^ KEY) # *** Per-character encrypt/decrypt ***
   if VERBOSE: print output_file_text               # *** ***************************** *** 

   # --------------------------------------------------------------------------
   # Write the output file 
   try:
      f = open(output_file_name, 'w')
      f.write(output_file_text)  
      f.close()
   except Exception as e:
      sys.stderr.write("ERROR -- Unable to write to the output file. Check permissions\n")
      sys.stderr.write(str(e))
      sys.stderr.write("\n\n")
      sys.exit(5)
      
   # --------------------------------------------------------------------------
   # TODO: verify that output file exists   
   if VERBOSE: print "--=[ TASK COMPLETE ]=--"
   sys.exit(0)

else:

   sys.stderr.write("ERROR -- Main Program cannot be imported by another script\n\n")
   sys.exit(6)
   
   
   
