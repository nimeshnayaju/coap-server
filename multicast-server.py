from coapserver import CoAPServer
from resources import WaterResource
import threading

def main():
  server = CoAPServer("0.0.0.0", 5683, multicast=True)

if __name__ == "__main__":
  main()