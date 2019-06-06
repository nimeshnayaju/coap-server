import getopt
import socket
import sys

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

def usage():
  print("client.py -o <operation> -p <path> [-P] <payload>")

def main(argv):
  operation = None
  path = None
  payload = None
  try:
    opts, args = getopt.getopt(argv[1:], "ho:p:P:", ["help", "operation=", "path=" "payload="])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit(2)
    elif opt in ("-o", "--operation"):
      operation = arg
    elif opt in ("-p", "--path"):
      path = arg
    elif opt in ("-P", "--payload"):
      payload = arg
    else:
      usage()
      sys.exit(2)

  host, port, path = parse_uri(path)
  try:
    host = socket.gethostbyname(host)
  except socket.gaierror:
    pass
  
  client = HelperClient(server=(host, port))

  if operation == "GET":
    response = client.get(path)
    print(response.pretty_print())
    client.stop()
  elif operation == "POST":
    response = client.post(path, payload)
    print(response.pretty_print())
    client.stop()
  elif operation == "PUT":
    response = client.put(path, payload)
    print(response.pretty_print())
    client.stop()
  elif operation == "DELETE":
    response = client.delete(path)
    print(response.pretty_print())
    client.stop()
  else:
    print("Operation not recognized")
    usage()
    sys.exit(2)
  
if __name__ == "__main__":
  main(sys.argv)