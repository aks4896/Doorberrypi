# Author: 
# Description: 
#
#
#


import serial
import time, sys, re
from optparse import OptionParser


def main():
  #configure serial interfaces and handle prompts
  parser = OptionParser(usage="%prog -p SERIALPORT", version="%prog 0.1")
  parser.set_defaults(
     port = "/dev/ttyUSB0",
     baud = 9600,
  )
  parser.add_option("-p", dest="port", action="store", 
    help='Serial interface (Default is /dev/ttyUSB0)')
  parser.add_option("-b", dest="baud", action="store",
    help='Set the baud rate (Default is 9600)')

  (options, args) = parser.parse_args()
  #Validate input here
  #if options.port:
    #check that port exists, is unlocked, and accessible to the user

  #if not options.baud == 9600 or 19200 or 38400 or 56600:
  #  print("Invalid baud rate")
  #  exit()

  #TODO turn this into it's own process

  print("Connecting to %s at %s" % (options.port, options.baud))
  try:
    ser = serial.Serial(options.port, options.baud, timeout=.5)
    if ser.isOpen(): print("Connection successful...")
    if test(ser): print("Communication test successful...")
    else: sys.exit()
    ser.readlines() # clear the buffer
    ser.write('$')  # scanning mode
  except:
    print("Could not connect to %s" % options.port)
    sys.exit()

  buffer = []

  while True:
    #print(ser.inWaiting())
    if ser.inWaiting() > 39:
      buffer = ser.readlines()
      serialread = buffer[:2] #take only the last 2 items
      print(ivalidate(serialread))

      ###
      #  interface with next portion of code here
      ###


    else:
      time.sleep(.5)  ##TODO make more elegant
    ##TODO search for properly formatted ibuttons or bail
    ## if invalid ibuttons come in that wait
    ## TODO add security here :)
  ser.close()

def ivalidate(ibuttons):
  #validate the input from a user
  ipattern = re.compile('^!,([A-F0-9]{16})')
  for i in ibuttons:
    imatch = ipattern.match(i)
    if imatch: return imatch.group(0)[2:] #strip the first two chars
    else: return None
  

def test(ser):
  #make sure connection is good
  try:
    ser.write('r') #send a reset signal
    time.sleep(1) #give it a second to respond
    response = ser.readlines()
    if 'N\r\n' in response: #valid response
      return True
    else:
      return False
  except:
    return False
    
    
def alert():
  #send alerts when something goes wrong
  print("yay. alert")

if __name__ == "__main__":
  main()
