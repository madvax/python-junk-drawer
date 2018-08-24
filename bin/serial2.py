#! /usr/bin/env python

#!c:\Python27\Python.exe

# SUMARY: This script transmits data via the system's communications port.

# THEORY OF OPERATION:
# This scripts sends data from one serial-connected ZigBee device to another. 
# The transmission is "one way" and no response is expected or processed by 
# this script.
# The duration of the transmission is specified by either the -t or --time 
# options supplied on the command line at the time of invocation. The 'time'
# option takes an integer argument specifying the seconds to transmit. The 
# default transmission time is 10 seconds, see SECONDS_TO_RUN variable. 
# Messages will be transmitted over the ZigBee RF channel at intervals 
# specified by the -i or --interval option. The 'interval' option takes a 
# floating-point argument specifying the number of seconds between individual 
# message transmission throughout the session. The default interval is 0.25 or 
# 250 milliseconds. It is the burden of the user to ensure that the Serial BAUD 
# Rate can support the message interval.
# This script support 'most' serial port parameters for connecting to the ZigBee 
# device. Please see the help display or usage() function for details on serial 
# connection parameters supported by this script.
# 
# NOTES: 
#  1.) This script requires the site package "PySerial" to execute
#  2.) This script automatically detects devices connected to Communication ports
#  3.) Exit codes other than zero indicate known execution failures, see help      
#  4.) This script executes multi-threaded tasks, please don't edit unless you 
#      understand multi threading in Python.     

# For support using this script please contact:
#     H. Wilson, harold.wilson@netscout.com,  719-272-8796

# ==============================================================================
# Standard Library imports 
import sys 
import os
import time 
from getopt import getopt
from thread import start_new_thread

# ==============================================================================
# Local Site Package Imports
try:
   import serial 
except:
   sys.stderr.write("\n\n")   
   sys.stderr.write("ERROR -- Unable to import the PySerial Site Package\n")
   sys.stderr.write("         Try any of these options to install PySerial:\n")
   sys.stderr.write("           Option 1.) pip install pyserial\n")
   sys.stderr.write("           Option 2.) easy_install -U pyserial\n")
   sys.stderr.write("           Option 3.) Download the archive from http://pypi.python.org/pypi/pyserial.\n")
   sys.exit(11)
   

# ==============================================================================
# Dictionary of Globals 
VERSION        = "0.1"
DEBUG          = False   # Flag for debug operation
VERBOSE        = False   # Flag for verbose operation 
FIRST          = 0       # First element in a list 
LAST           = -1      # Last element in a list
ME             = os.path.split(sys.argv[FIRST])[LAST]        # Name of this file
MY_PATH        = os.path.dirname(os.path.realpath(__file__)) # Path for this file
BAUD_RATES     = ["2400","4800","9600","14400","19200","38400","57600","115200"] 
DATA_BITS      = ["5", "6", "7", "8"]
PARITY         = ["none", "odd", "even", "mark", "space"]
STOP_BITS      = ["1", "1.5", "2"]
FLOW_CONTROL   = ["none", "Xon/Xoff", "hardware"]
COM_PORTS      = []
SECONDS_TO_RUN = 10    # Time in seconds to run communications
INTERVAL       = 0.25  # Time is seconds to wait between messages sent
TIME_IS_UP     = False # Flag for thread to use, indicates comms should stop 

# ==============================================================================
# Native functions 

#------------------------------------------------------------------------------- usage()
def usage():
   """ usage() Displays a usage message on standard output""" 
   print "\n%s, Version %s, Serial Driver." %(ME,VERSION)
   print ""
   print "SUMARY: "
   print "This script transmits data via the system's communications port" 
   print ""
   print "\nUSAGE: %s [OPTIONS]" %ME
   print ""
   print "OPTIONS:"
   print "   -h --help          Show this help message"
   print "   -v --verbose       Print verbose output to stdout"
   print "   -g --debug         Print debugging informatio to stdout"
   print "   -t --time=         Time to run (in seconds), Default: %d"                  %SECONDS_TO_RUN
   print "   -i --interval      Inteval between messages (floating point), Default: %s" % INTERVAL
   print "   -c --comport=      Serial Communications port:\n                      %s"  %COM_PORTS
   print "   -b --baud=         Serial BAUD rate:\n                      %s"            %BAUD_RATES
   print "   -d --datasize=     Serial Data Size:\n                      %s"            %DATA_BITS
   print "   -p --parity=       Serial Parity:\n                      %s"               %PARITY
   print "   -s --stopbits=     Serial Stop Bits:\n                      %s"            %STOP_BITS
   print "   -f --flow control= Serial Flow Control:\n                      %s"         %FLOW_CONTROL
   print ""
   print "Default connection parameters:"
   print "   {port,baud,data,parity,stop,flow}"
   print "   {%s,%s,%s,%s,%s,%s}" %(comPort     ,  
                                    baud        ,
                                    dataSize    ,
                                    parity      ,
                                    stopBits    ,
                                    flowControl )
   print ""
   print "EXIT CODES:"
   print "  0 - Successful completion of the task"   
   print "  1 - Bad or missing command line options/arguments"   
   print "  2 - Bad Serial Communications port specified"   
   print "  3 - Bad Serial BAUD Rate specified"   
   print "  4 - Bad Serial Data size specified"   
   print "  5 - Bad Serial Parity specified"   
   print "  6 - Bad Serial Stop Bits specified"   
   print "  7 - Bad Serial Flow Control specified"   
   print "  8 - Bad Session Time-to-run value specified"   
   print "  9 - Bad Session Message Interval specified"   
   print " 10 - Unable to open a serial session"   
   print " 11 - Unable to import the PySerial site package"   
   print " 12 - Unable to initialize the serial data size on this system"   
   print " 13 - Unable to initialize the serial stop bits on this system"   
   print " 14 - Unable to initialize the serial parity on this system"   
   print " 15 - Unable to identify any devices conected to any com ports"

# ------------------------------------------------------------------------------ showError()                                    
def showError(message, additionalInfo = None): 
   """ showError(message, additionalInfo = None) --> None
       Prints clean consistent error messages on stderr. """
   sys.stderr.write("\n\n")
   sys.stderr.write("ERROR -- %s\n" %str(message))
   if additionalInfo: sys.stderr.write("         %s\n" %str(additionalInfo))
   sys.stderr.flush()
   return None

# ------------------------------------------------------------------------------ runTest   
def runTest():
   """  runTest() --> None
        Executes the timed serial communications in a seperate execution thread.  
   """
   global TIME_IS_UP
   try:
      if DEBUG: print "Entered %s thread" %ME 

      counter = 0   
      while not TIME_IS_UP: 
         counter += 1
         msg = "Test String: %4d" %counter
         msg += "\r\n"         
         ser.write(msg)
         if VERBOSE: print msg   
         time.sleep(INTERVAL)    
      time.sleep(1) # Allow time to finish the last message         
      ser.close()
      if DEBUG: print "Leaving %s thread" %ME
      time.sleep(1) # Allow time to close the serial port
   except Exception as e:
      showError("Error in execution thread:", str(e) )
   finally:
      return None

# ------------------------------------------------------------------------------
# Get a list of valid com ports for this system 
if os.name == 'nt':  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports
else:
    raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))
ports =  comports()
for n, (port, desc, hwid) in enumerate(ports, 1):
   COM_PORTS.append(port)
   # sys.stdout.write("{:20}\n".format(port))
   # sys.stdout.write("    desc: {}\n".format(desc))
   # sys.stdout.write("    hwid: {}\n".format(hwid))

# ------------------------------------------------------------------------------   
# Check to see that we have at least one usable com port or notify and quit
if len(COM_PORTS) < 1:
   showError("Unable to identify any usable com ports"      , 
             "Please ensure that your device is connected." )
   sys.exit(15)

# ------------------------------------------------------------------------------   
# Default Values for Serial Connections
comPort     = COM_PORTS[FIRST]    #  COM1 or maybe /dev/ttyS0 
baud        = BAUD_RATES[2]       #  9600
dataSize    = DATA_BITS[LAST]     #     8
parity      = PARITY[FIRST]       #  none
stopBits    = STOP_BITS[FIRST]    #     1
flowControl = FLOW_CONTROL[FIRST] #  none

# ------------------------------------------------------------------------------
# Validate the command line arguments
try: arguments = getopt(sys.argv[1:]           , 
                        "hvgi:t:c:b:d:p:s:f:"  , 
                        [ 'help'         ,
                          'verbose'      , 
                          'debug'        , 
                          'time'         ,
                          'interval'
                          'comport='     ,
                          'baud='        ,                         
                          'datasize='    ,
                          'parity='      ,
                          'stopbits='    , 
                          'flowcontrol=' ]     )   
except Exception as e:
   showError("Bad command line argument(s)\n", str(e))
   usage()
   sys.exit(1)         

# ------------------------------------------------------------------------------
# Check the command line options
# --- Check for a help option
for arg in arguments[FIRST]:
   if arg[FIRST]== "-h" or arg[FIRST] == "--help":
      usage()
      sys.exit(0)
# --- Check for a verbose option
for arg in arguments[FIRST]:
   if arg[FIRST]== "-v" or arg[FIRST] == "--verbose":
      VERBOSE = True               
# --- Check for a debug option
for arg in arguments[FIRST]:
   if arg[FIRST]== "-g" or arg[FIRST] == "--debug":
      DEBUG   = True
      VERBOSE = True   
# --- Check for a aerial communications port option
for arg in arguments[FIRST]:
   if arg[FIRST]== "-c" or arg[FIRST] == "--comport":
      if arg[LAST] in COM_PORTS:
         comPort = arg[LAST] 
      else: 
         showError("Bad comport specified: \'%s\'\n" %arg[LAST] ,
                   "Valid Values are: %s"            %COM_PORTS )
         sys.exit(2)          
# --- Check for a serial baud rate option                   
for arg in arguments[FIRST]:
   if arg[FIRST]== "-b" or arg[FIRST] == "--baud":
      if arg[LAST] in BAUD_RATES:
         baud = arg[LAST]
      else:
         showerror("Bad baud specified \'%s\'\n" %arg[LAST]  ,
                   "Valid Values are: %s"        %BAUD_RATES )
         sys.exit(3)          
# --- Check for a serial data size option
for arg in arguments[FIRST]:
   if arg[FIRST]== "-d" or arg[FIRST] == "--datasize":
      if arg[LAST] in DATA_BITS:
         dataSize = arg[LAST]
      else: 
         showError("Bad data size specified \'%s\'\n" %arg[LAST]  ,
                   "Valid Values are: %s"             %DATA_BITS  )
         sys.exit(4)          
# --- Check for a serial parity option
for arg in arguments[FIRST]:
   if arg[FIRST]== "-p" or arg[FIRST] == "--parity":
      if arg[LAST] in PARITY:
         parity = arg[LAST]
      else: 
         showError("Bad parity specified \'%s\'\n" %arg[LAST]  ,
                   "Valid Values are: %s"          %PARITY  )
         sys.exit(5)          
# --- Check for serial stop bits option
for arg in arguments[FIRST]:
   if arg[FIRST]== "-s" or arg[FIRST] == "--stopbits":
      if arg[LAST] in STOP_BITS:
         stopBits = arg[LAST]
      else: 
         showError("Bad stop bits specified \'%s\'\n" %arg[LAST]  ,
                   "Valid Values are: %s"             %STOP_BITS  )
         sys.exit(6)          
# --- Check for a serial flow control option
for arg in arguments[FIRST]:
   if arg[FIRST]== "-f" or arg[FIRST] == "--flowcontrol":
      if  arg[LAST] in FLOW_CONTROL:
         flowControl = arg[LAST]
      else: 
         showError("Bad flow control specified \'%s\'\n" %arg[LAST]     ,
                   "Valid Values are: %s"                %FLOW_CONTROL  )
         sys.exit(7)          
# --- Check for a time-to-run option
for arg in arguments[FIRST]:
   if arg[FIRST]== "-t" or arg[FIRST] == "--time":
      try:
         SECONDS_TO_RUN = int(arg[LAST])
      except Exception as e:
         showError("Invalid time to run specified using \'%s %s\', must be an integer" %(arg[FIRST], arg[LAST]))
         sys.exit(8)
# --- Check for an interval between messages option
for arg in arguments[FIRST]:
   if arg[FIRST]== "-i" or arg[FIRST] == "--interval":
      try:
         INTERVAL = float(arg[LAST])
      except Exception as e:
         showError("Invalid interval specified using \'%s %s\', must be an integer" %(arg[FIRST], arg[LAST]))
         sys.exit(9)
         
# ------------------------------------------------------------------------------
# Check to see what we are setting from either default values and/or command 
# line options       
if DEBUG:
   print "COM PORT CONNECTION PARAMS:"
   print "   {port,baud,data,parity,stop,flow}"
   print "   {%s,%s,%s,%s,%s,%s}" %(comPort     ,  
                                    baud        ,
                                    dataSize    ,
                                    parity      ,
                                    stopBits    ,
                                    flowControl ) 

# ------------------------------------------------------------------------------                                    
# Initialize the serial port
# Prep the arguments for the serial connection call. All arguments start out 
# as strings but, some need to be cast to ints or floats.  
# --- BAUD
baud  = int(baud)
# --- DATA SIZE
if dataSize   == '5':
   dataSize = serial.FIVEBITS
elif dataSize == '6':
   dataSize = serial.SIXBITS
elif dataSize == '7':
   dataSize = serial.SEVENBITS
elif dataSize == '8':
   dataSize = serial.EIGHTBITS
else:
   showError("Unable to initialize the data size  value \'%s\'" %dataSize ,
              "Valid Values are %s" %DATA_BITS                            )
   sys.exit(12)              
# --- STOP BITS
if stopBits == "1" :
   stopBits = serial.STOPBITS_ONE
elif stopBits == "2":
   stopBits = serial.STOPBITS_TWO
elif stopBit == "1.5":
   stopBits = serial.STOPBITS_ONE_POINT_FIVE
else:
   showError("Unable to initialize the stop bits value \'%s\'" %stopBits ,
              "Valid Values are %s" %STOP_BITS                           )
   sys.exit(13)              
# --- PARITY
p = {"none"  : serial.PARITY_NONE  , 
     "odd"   : serial.PARITY_ODD   ,
     "even"  : serial.PARITY_EVEN  ,
     "mark"  : serial.PARITY_MARK  ,
     "space" : serial.PARITY_SPACE }
try:
   parity = p[parity]
except:
   showError("Unable to initialize the parity value \'%s\'" %parity ,
              "Valid Values are %s" %PARITY                           )
   sys.exit(14)              
# --- FLOW CONTROL - Map hardware and software flow controls 
XonXoff = False
RTSCTS  = False
DSRDTR  = False
if flowControl == "Xon/Xoff":   # Software flow control 
   XonXoff = True               #
elif flowControl == "hardware": # Hardware flow control (extra wires needed)
   RTSCTS = True                # 
   DSRDTR = True                #
else:                           # Anything else is ignored 
   pass                         # 

# ------------------------------------------------------------------------------   
# Create the serial port connection using the initialized connection parameters 
try:  
   ser = serial.Serial( port     = comPort  ,
                        baudrate = baud     ,
                        parity   = parity   ,
                        stopbits = stopBits ,
                        bytesize = dataSize ,
                        xonxoff  = XonXoff  , 
                        rtscts   = RTSCTS   ,
                        dsrdtr   = DSRDTR   )
except Exception as e:
   showError("Unable to initialize the comm port '%s'" %str(comPort))
   print str(e)
   print "\n\n"
   sys.exit(10)
                     
                     
# ------------------------------------------------------------------------------
# Check to see of the serial com port is up and working                
time.sleep(1) # Some systems may need a second to start the port 
params = [comPort, baud, parity, stopBits, dataSize]                     
if not ser.isOpen():
   showError("Unable to open a serial session on %s" %commPort, "Com Port Params:\n%s" %params)
   sys.exit(10)
else:
   if DEBUG:
      print "Serial Port Initialized "

# ------------------------------------------------------------------------------
# Start the clock for the comunications session 
startTimeSeconds = int(time.time())
elapTimeSeconds  = int(time.time()) - startTimeSeconds
# Start the timed thread for the comunications session, see: runTest()    
start_new_thread(runTest, ())
# Wait here for the clock to run out
while (elapTimeSeconds < SECONDS_TO_RUN ):
    time.sleep(1) # Tick, Tock 
    elapTimeSeconds  = int(time.time()) - startTimeSeconds 
# Time is up! Set the flag to exit the thread
TIME_IS_UP = True
time.sleep(3) # Allow time for the thread to finish cleanly 
# ------------------------------------------------------------------------------
# Clean up after our selves
if ser.isOpen():
   if DEBUG: print "Closing Serial Port" 
   ser.close()
else:
   if DEBUG: print "Serial Port already closed"
# So long and thanks for all the fish! 
if VERBOSE: print "--=[ TAK COMPLETE ]=-"    
sys.exit(0)
