import json
from random import randint

import threading
import logging
import time

from coapthon import defines
from coapthon.resources.resource import Resource

logger = logging.getLogger(__name__)

''' Generates dummy values (emulates behaviour of a sensor) '''
def dummyvalues(metername, numbers): # metername - identifier of meter, number - number of dummy values to generate
  values = []
  for i in range(1, numbers + 1):
    keyname = keyname = metername + " meter " + str(i)
    values.append({'meterName': keyname, 'value': str(randint(1,65535))})
  return values


class ElectricityResource(Resource):
  def __init__(self, name="Electricity", coap_server=None):
    super(ElectricityResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=False)
    self.resource_type = "rt1"
    self.content_type = "application/json"
    self.interface_type = "if1"
    self.payload = str(randint(1, 100)) + " Watts"
    self.period = 5
    self.update(True)

  ''' Returns a JSON object with the values of 10 Electricity's meters '''
  def render_GET(self, request):
    return self
  
  def render_PUT(self, request):
    self.edit_resource(request)
    return self

  def render_POST(self, request):
    res = self.init_resource(request, ElectricityResource())
    return res
  
  def render_DELETE(self, request):
    return True

  def update(self, first=False):
    self.payload = str(randint(1, 100)) + " Watts"
    if not self._coap_server.stopped.isSet():
      timer = threading.Timer(self.period, self.update)
      timer.start()

      if not first and self._coap_server is not None:
        logger.debug("Periodic Update")
        self._coap_server.notify(self)
        self.observe_count += 1
        print(self.payload)

class WaterResource(Resource):
  def __init__(self, name="Water", coap_server=None):
    super(WaterResource, self).__init__(name, coap_server, visible=True, observable=False, allow_children=True)
    self.resource_type = "rt1"
    self.content_type = "application/json"
    self.interface_type = "if1"
    self.payload = (defines.Content_types["application/json"], json.dumps({'output': dummyvalues("Water", 20)}))

  ''' Returns a JSON object with the values of 20 Water's meters '''
  def render_GET(self, request):
    return self
  
  def render_PUT(self, request):
    self.edit_resource(request)
    return self

  def render_POST(self, request):
    res = self.init_resource(request, WaterResource())
    return res
  
  def render_DELETE(self, request):
    return True


class AllMetersResource(Resource):
  def __init__(self, name="Allmeters", coap_server=None):
    super(AllMetersResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
    self.resource_type = "rt1"
    self.content_type = "application/json"
    self.interface_type = "if1"
    self.payload = (defines.Content_types["application/json"], json.dumps({'electricity': dummyvalues("Electricity", 10), 'water': dummyvalues("Water", 20)}))

  ''' Returns a JSON object with the values of 10 Electricity's meters and 20 Water's meters '''
  def render_GET(self, request):
    return self
  
  def render_PUT(self, request):
    self.edit_resource(request)
    return self

  def render_POST(self, request):
    res = self.init_resource(request, ElectricityResource())
    return res
  
  def render_DELETE(self, request):
    return True