import getopt
import sys

from coapthon.server.coap import CoAP
from resources import ElectricityResource, WaterResource, AllMetersResource
from exampleresources import BasicResource

class CoAPServer(CoAP):
  def __init__(self, host, port, multicast=False):
    CoAP.__init__(self, (host, port), multicast)

    '''Adding resources to the server along with the HTTP endpoints for the resource '''
    self.add_resource('electricitymeters/', ElectricityResource())
    self.add_resource('watermeters/', WaterResource())
    self.add_resource('allmeters/', AllMetersResource())
    self.add_resource('basic/', BasicResource())

    print("CoAP server starting on " + host + ":" + str(port))
    print(self.root.dump())

def usage():
  print("server.py -i <ip address> -p <port>")

def main(argv):
  ip = "0.0.0.0"
  port = 5683
  multicast = False
  try:
    opts, args = getopt.getopt(argv[1:], "hi:p:m", ["ip=", "port=", "multicast"])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit(2)
    elif opt in ("-i", "--ip"):
      ip = arg
    elif opt in ("-p", "--port"):
      port = int(arg)
    elif opt in ("-m", "--multicast"):
      multicast = bool(arg)
    else:
      usage()
      sys.exit(2)
  
  server = CoAPServer(ip, port, multicast) 
  try:
    server.listen(10)
  except KeyboardInterrupt:
    print("Server shutting down....")
    server.close()


if __name__ == '__main__':
  main(sys.argv)