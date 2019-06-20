import getopt
from coapthon import defines
from coapthon.client.helperclient import HelperClient

client = None

def main():
  global client
  server_address = (defines.ALL_COAP_NODES, 5683)
  operation = "GET"
  path = "water"
  
  client = HelperClient(server_address)
  response = client.get(path)
  print(response.pretty_print())
  client.stop()
  
if __name__ == "__main__":
  main()