#!/usr/bin/env python

import sys
import io
import math

class smartboard_driver():

  def transformBasis(self, xy):
    #translation
    xy[0] = xy[0] - self.transform_xy[0]
    xy[1] = xy[1] - self.transform_xy[1]

    #rotation
    xy2 = []
    xy2.append(xy[0] * math.cos(self.transform_theta) + xy[1] * math.sin(self.transform_theta))
    xy2.append(-(xy[1] * math.cos(self.transform_theta) - xy[0] * math.sin(self.transform_theta)))
    return xy2

  def validPacket(self, inp):
    ok = True
    if(len(inp) != 64):
      ok = False
    for x in range(0, 8):
      if(x == 0):
        if(inp[8*x] != '\xa6' or inp[8*x+1] != '\x00' or inp[8*x+2] != '\xa0' or inp[8*x+3] != '\xff'):
          ok = False
      else:
        if(inp[8*x] != '\xa7' or inp[8*x+1] != '\x00' or inp[8*x+2] != '\xa0' or inp[8*x+3] != '\xff'):
          ok = False
    return ok

  def isNop(self, inp):
    nop = True
    for x in range(0, 8):
      if(inp[8*x+4] != '\xff'  or inp[8*x+5] != '\xff' or inp[8*x+6] != '\xff' or inp[8*x+7] != '\xff'):
        nop = False
    return nop


  def prepareCsv(self, inp):
    bytes = []
    for x in range(0, 8):  
      bytes.append(ord(inp[8*x+4]))
	
    #ako je paket ima netocne podatke ili je prazan vrati same nule ...
    if(bytes[0] == 2 or (self.isNop(inp))):
      return "0;0;0;0;0;0"

    xy = [(bytes[2] << 8) + bytes[1], (bytes[4] << 8) + bytes[3]]
    xy = self.transformBasis(xy)
  
    string = str(bytes[0]) + ";" + str(xy[0]) + ";" + str(xy[1]) + ";" + str(bytes[5]) + ";" + str(bytes[6]) + ";" + str(bytes[7])
    return string

  def run(self):

    buf = []
    try:
      byte = self.input_file.read(1)
      while byte != "":
        if len(buf) == 0 and byte == '\xa6':
          buf.append(byte)
        elif len(buf) > 0 and len(buf) < 64:
          buf.append(byte)
        
        byte = self.input_file.read(1)
 
        if len(buf) == 64:
          if(self.validPacket(buf)):
            if(self.update != None):
              self.update(self.prepareCsv(buf))
            else:
              print self.prepareCsv(buf)
          del buf[:] 

    except KeyboardInterrupt:
      pass

  
  def __init__(self, input_file):

    self.transform_xy = [1035, 17515]
    self.transform_theta = math.pi / 4
    self.input_file = input_file
    self.update = None

#ako se pokrece kao samostalna aplikacija
if __name__ == '__main__':

  if(len(sys.argv) == 1):
    input_file_name = '/dev/usb/hiddev0'
  else:
    input_file_name = sys.argv[1]

  # --> stdin
  #input_file = io.open(sys.stdin.fileno(), mode='rb', closefd=False)
  # --> datoteka
  input_file = open(input_file_name, 'rb')

  sb = smartboard_driver(input_file)

  sb.run()
      

