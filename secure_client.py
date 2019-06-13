''' System '''
import socket
import tempfile
import random
import os
import getopt
import sys

''' DTLS '''
import ssl
from coapthon import defines
from dtls.wrapper import wrap_client

''' CoAPthon '''
from coapthon.messages.request import Request
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

CA_CERT_VALID = """-----BEGIN CERTIFICATE-----
MIICCzCCAXQCCQCwvSKaN4J3cTANBgkqhkiG9w0BAQUFADBKMQswCQYDVQQGEwJV
UzETMBEGA1UECBMKV2FzaGluZ3RvbjETMBEGA1UEChMKUmF5IENBIEluYzERMA8G
A1UEAxMIUmF5Q0FJbmMwHhcNMTQwMTE4MjEwMjUwWhcNMjQwMTE2MjEwMjUwWjBK
MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjETMBEGA1UEChMKUmF5
IENBIEluYzERMA8GA1UEAxMIUmF5Q0FJbmMwgZ8wDQYJKoZIhvcNAQEBBQADgY0A
MIGJAoGBAN/UYXt4uq+YdTDnm7WPCu+0B50kJXWU3sSS+WAAhr3BHh7qa7UTiRXy
yGYysgvtwriETAZRckzd+hdblNRUWXGJdRvtyx94nLpPpI8p4djBrJ5IMPqK5SgW
ZP4XTWs694VtUBAvHCX+Ly+t0O5Rw3NmqxY1MakooqU9t+wL0H0TAgMBAAEwDQYJ
KoZIhvcNAQEFBQADgYEANemjvYCJrTc/6im0DmDC6AW8KrLG0xj31HWpq1dO9LG7
mlVFgbVtbcuCZgA78kxgw1vN6kBBLEsAJC8gkg++AO/w3a4oP+U9txAr9KRg6IGA
FiUohuWbjKBnQEpceoECgrymooF3ayzke/vf3wcMYy153uC+H4t96Yc5T066c4o=
-----END CERTIFICATE-----
"""

CA_CERT_WRONG = """-----BEGIN CERTIFICATE-----
MIIE6jCCBFOgAwIBAgIDEIGKMA0GCSqGSIb3DQEBBQUAME4xCzAJBgNVBAYTAlVT
MRAwDgYDVQQKEwdFcXVpZmF4MS0wKwYDVQQLEyRFcXVpZmF4IFNlY3VyZSBDZXJ0
aWZpY2F0ZSBBdXRob3JpdHkwHhcNMTAwNDAxMjMwMDE0WhcNMTUwNzAzMDQ1MDAw
WjCBjzEpMCcGA1UEBRMgMmc4YU81d0kxYktKMlpENTg4VXNMdkRlM2dUYmc4RFUx
CzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMRIwEAYDVQQHEwlTdW5u
eXZhbGUxFDASBgNVBAoTC1lhaG9vICBJbmMuMRYwFAYDVQQDEw13d3cueWFob28u
Y29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6ZM1jHCkL8rlEKse
1riTTxyC3WvYQ5m34TlFK7dK4QFI/HPttKGqQm3aVB1Fqi0aiTxe4YQMbd++jnKt
djxcpi7sJlFxjMZs4umr1eGo2KgTgSBAJyhxo23k+VpK1SprdPyM3yEfQVdV7JWC
4Y71CE2nE6+GbsIuhk/to+jJMO7jXx/430jvo8vhNPL6GvWe/D6ObbnxS72ynLSd
mLtaltykOvZEZiXbbFKgIaYYmCgh89FGVvBkUbGM/Wb5Voiz7ttQLLxKOYRj8Mdk
TZtzPkM9scIFG1naECPvCxw0NyMyxY3nFOdjUKJ79twanmfCclX2ZO/rk1CpiOuw
lrrr/QIDAQABo4ICDjCCAgowDgYDVR0PAQH/BAQDAgTwMB0GA1UdDgQWBBSmrfKs
68m+dDUSf+S7xJrQ/FXAlzA6BgNVHR8EMzAxMC+gLaArhilodHRwOi8vY3JsLmdl
b3RydXN0LmNvbS9jcmxzL3NlY3VyZWNhLmNybDCCAVsGA1UdEQSCAVIwggFOgg13
d3cueWFob28uY29tggl5YWhvby5jb22CDHVzLnlhaG9vLmNvbYIMa3IueWFob28u
Y29tggx1ay55YWhvby5jb22CDGllLnlhaG9vLmNvbYIMZnIueWFob28uY29tggxp
bi55YWhvby5jb22CDGNhLnlhaG9vLmNvbYIMYnIueWFob28uY29tggxkZS55YWhv
by5jb22CDGVzLnlhaG9vLmNvbYIMbXgueWFob28uY29tggxpdC55YWhvby5jb22C
DHNnLnlhaG9vLmNvbYIMaWQueWFob28uY29tggxwaC55YWhvby5jb22CDHFjLnlh
aG9vLmNvbYIMdHcueWFob28uY29tggxoay55YWhvby5jb22CDGNuLnlhaG9vLmNv
bYIMYXUueWFob28uY29tggxhci55YWhvby5jb22CDHZuLnlhaG9vLmNvbTAfBgNV
HSMEGDAWgBRI5mj5K9KylddH2CMgEE8zmJCf1DAdBgNVHSUEFjAUBggrBgEFBQcD
AQYIKwYBBQUHAwIwDQYJKoZIhvcNAQEFBQADgYEAp9WOMtcDMM5T0yfPecGv5QhH
RJZRzgeMPZitLksr1JxxicJrdgv82NWq1bw8aMuRj47ijrtaTEWXaCQCy00yXodD
zoRJVNoYIvY1arYZf5zv9VZjN5I0HqUc39mNMe9XdZtbkWE+K6yVh6OimKLbizna
inu9YTrN/4P/w6KzHho=
-----END CERTIFICATE-----
"""

KEY_CERT_VALID = """-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBANjL+g7MpTEB40Vo
2pxWbx33YwgXQ6QbnLg1QyKlrH6DEEotyDRWI/ZftvWbjGUh0zUGhQaLzF3ZNgdM
VkF5j0wCgRdwPon1ct5wJUg6GCWvfi4B/HlQrWg8JDaWoGuDcTqLh6KYfDdWTlWC
Bq3pOW14gVe3d12R8Bxu9PCK8jrvAgMBAAECgYAQFjqs5HSRiWFS4i/uj99Y6uV3
UTqcr8vWQ2WC6aY+EP2hc3o6n/W1L28FFJC7ZGImuiAe1zrH7/k5W2m/HAUM7M9p
oBcp7ZVMFU6R00cQWVKCpQRCpNHnn+tVJdRGiHRj9836/u2z3shBxDYgXJIR787V
SlBXkCcsi0Clem5ocQJBAPp/0tF4CpoaOCAnNN+rDjPNGcH57lmpSZBMXZVAVCRq
vJDdH9SIcb19gKToCF1MUd7CJWbSHKxh49Hr+prBW8cCQQDdjrH8EZ4CDYvoJbVX
iWFfbh6lPwv8uaj43HoHq4+51mhHvLxO8a1AKMSgD2cg7yJYYIpTTAf21gqU3Yt9
wJeZAkEAl75e4u0o3vkLDs8xRFzGmbKg69SPAll+ap8YAZWaYwUVfVu2MHUHEZa5
GyxEBOB6p8pMBeE55WLXMw8UHDMNeQJADEWRGjMnm1mAvFUKXFThrdV9oQ2C7nai
I1ai87XO+i4kDIUpsP216O3ZJjx0K+DS+C4wuzhk4IkugNxck5SNUQJASxf8E4z5
W5rP2XXIohGpDyzI+criUYQ6340vKB9bPsCQ2QooQq1BH0wGA2fY82Kr95E8KhUo
zGoP1DtpzgwOQg==
-----END PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIICDTCCAXYCCQCxc2uXBLZhDjANBgkqhkiG9w0BAQUFADBKMQswCQYDVQQGEwJV
UzETMBEGA1UECBMKV2FzaGluZ3RvbjETMBEGA1UEChMKUmF5IENBIEluYzERMA8G
A1UEAxMIUmF5Q0FJbmMwHhcNMTQwMTE4MjEwMjUwWhcNMjQwMTE2MjEwMjUwWjBM
MQswCQYDVQQGEwJVUzETMBEGA1UECBMKV2FzaGluZ3RvbjEUMBIGA1UEChMLUmF5
IFNydiBJbmMxEjAQBgNVBAMTCVJheVNydkluYzCBnzANBgkqhkiG9w0BAQEFAAOB
jQAwgYkCgYEA2Mv6DsylMQHjRWjanFZvHfdjCBdDpBucuDVDIqWsfoMQSi3INFYj
9l+29ZuMZSHTNQaFBovMXdk2B0xWQXmPTAKBF3A+ifVy3nAlSDoYJa9+LgH8eVCt
aDwkNpaga4NxOouHoph8N1ZOVYIGrek5bXiBV7d3XZHwHG708IryOu8CAwEAATAN
BgkqhkiG9w0BAQUFAAOBgQBw0XUTYzfiI0Fi9g4GuyWD2hjET3NtrT4Ccu+Jiivy
EvwhzHtVGAPhrV+VCL8sS9uSOZlmfK/ZVraDiFGpJLDMvPP5y5fwq5VGrFuZispG
X6bTBq2AIKzGGXxhwPqD8F7su7bmZDnZFRMRk2Bh16rv0mtzx9yHtqC5YJZ2a3JK
2g==
-----END CERTIFICATE-----
"""

client = None

def usage():  # pragma: no cover
    print "Command:\tcoapclient.py -o -p [-P] [-u]"
    print "Options:"
    print "\t-o, --operation=\tGET|PUT|POST|DELETE|DISCOVER|OBSERVE"
    print "\t-p, --path=\t\tPath of the request"
    print "\t-P, --payload=\t\tPayload of the request"
    print "\t-f, --payload-file=\tFile with payload of the request"
    print "\t-u, --proxy-uri-header=\tProxy-Uri CoAP Header of the request"


def client_callback(response):
  print("Callback")

def client_callback_observe(response):  # pragma: no cover
  global client
  print("Callback Observe")
  print (response.pretty_print())
  check = True
  while check:
    chosen = raw_input("Stop observing? [Y/N]: ")
    if chosen != "" and not (chosen == "n" or chosen == "N" or chosen == "y" or chosen == "Y"):
      print("Unrecognized choice")
      continue
    elif chosen == "y" or chosen == "Y":
      while True:
        rst = raw_input("Send RST message? [Y/N]: ")
        if rst != "" and not (rst == "n" or rst == "N" or rst == "y" or rst == "Y"):
          print("Unrecognized choice")
          continue
        elif rst == "" or rst == "y" or rst == "Y":
          client.cancel_observing(response, True)
        else:
          client.cancel_observing(response, False)
        check = False
        break
    else:
      break

def main():
  global client

  operation = None
  path = None
  payload = None
  proxy_uri = None

  try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:p:P:f:", ["help", "operation=", "path=", "payload=", "payload-file=", "proxy-uri-header="])
  except getopt.GetoptError as err:
    print(str(err))
    usage()
    sys.exit(2)

  for opt, arg in opts:
    if opt in("-o", "--operation"):
      operation = arg
    elif opt in ("-p", "--path"):
      path = arg
    elif opt in ("-P", "--payload"):
      payload = arg
    elif opt in ("-f", "--payload-file"):
      with open(arg, "r") as f:
        payload = f.read()
    elif opt in ("-u", "--proxy-uri-header"):
      proxy_uri = arg
    elif opt in ("-h", "--help"):
      usage()
      sys.exit()
    else:
      usage()
      sys.exit(2)

  if operation is None:
    print("Operation must be specified")
    usage()
    sys.exit(2)
  
  if path is None:
    print("Path must be specified")
    usage()
    sys.exit(2)
  
  if not path.startswith("coap://"):
    print("Path must conform to coap://host[:port]/path")
    usage()
    sys.exit(2)
  
  if proxy_uri and not proxy_uri.startswith("http://") and not proxy_uri.startswith("https://"):
    print("Proxy-Uri header must conform to http[s]://host[:port]/path")
    usage()
    sys.exit(2)

  host, port, path = parse_uri(path)

  try:
    tmp = socket.gethostbyname(host)
    host = tmp
  except socket.gaierror:
    pass
  
  server_address = (host, port)
  current_mid = random.randint(1, 1000)

  pem = setUpPems()

  ''' Set up a client side DTLS socket '''
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock = wrap_client(sock,
                     cert_reqs=ssl.CERT_REQUIRED,
                     ca_certs=pem['CA_CERT'],
                     ciphers="RSA",
                     do_handshake_on_connect=True)

  ''' Connect CoAP client to the newly created socket '''
  client = HelperClient(server_address,
                        sock=sock,
                        cb_ignore_read_exception=_cb_ignore_read_exception,
                        cb_ignore_write_exception=_cb_ignore_write_exception)


  if operation == "GET":
    if path is None:
      print("Path needs to be specified for a GET request")
      usage()
      sys.exit(2)
    
    req = Request()
    req.code = defines.Codes.GET.number
    req.uri_path = "/" + path + "/"
    req.type = defines.Types["CON"]
    req._mid = current_mid
    req.destination = server_address
    req.add_if_none_match()

    received_message = client.send_request(req)
    print(received_message.pretty_print())
    client.stop()

  elif operation == "OBSERVE":
    if path is None:
      print("Path needs to be specified for a GET request")
      usage()
      sys.exit(2)
    req = Request()
    req.observe = 0
    req.code = defines.Codes.GET.number
    # req.proxy_uri = "coap://" + host + ":" + str(port) + "/" + path
    req.uri_path = "/" + path + "/"
    req.type = defines.Types["CON"]
    req._mid = current_mid
    req.destination = server_address

    client.send_request(req, client_callback_observe)
    # client.observe(path, client_callback_observe)
    
def setUpPems():
  def createPemFile(fname, content):
    with open(fname, mode='w') as f:
      f.write(content)
    f.close()
    return fname

  tmp_dir = tempfile.mkdtemp()

  pem = dict()
  pem['SERVER_KEY'] = createPemFile(os.path.join(tmp_dir, 'serverkey.pem'), KEY_CERT_VALID)
  pem['CA_CERT'] = createPemFile(os.path.join(tmp_dir, 'ca_cert.pem'), CA_CERT_VALID)
  pem['CA_CERT_WRONG'] = createPemFile(os.path.join(tmp_dir, 'ca_cert_wrong.pem'), CA_CERT_WRONG)

  return pem


def _cb_ignore_write_exception(self, exception, client):
  """
  In the CoAP client write method, different exceptions can arise from the DTLS stack. Depending on the type of exception, a
  continuation might not be possible, or a logging might be desirable. With this callback both needs can be satisfied.

  note: Default behaviour of CoAPthon without DTLS if no _cb_ignore_write_exception would be called is with "return True"

  :param exception: What happened inside the DTLS stack
  :param client: Reference to the running CoAP client
  :return: True if further processing should be done, False processing should be stopped
  """
  return False

def _cb_ignore_read_exception(self, exception, client):
  """
  In the CoAP client read method, different exceptions can arise from the DTLS stack. Depending on the type of exception, a
  continuation might not be possible, or a logging might be desirable. With this callback both needs can be satisfied.

  note: Default behaviour of CoAPthon without DTLS if no _cb_ignore_read_exception would be called is with "return False"

  :param exception: What happened inside the DTLS stack
  :param client: Reference to the running CoAP client
  :return: True if further processing should be done, False processing should be stopped
  """
  return False


if __name__ == "__main__":
  main()