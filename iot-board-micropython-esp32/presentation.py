import util.octopus as octopus
from util.pinout import set_pinout
from lib.microWebSrv import MicroWebSrv
from machine import PWM

print ("Running MAIN")

pinout = set_pinout()

FET = None
if pinout.MFET_PIN is not None:
    FET = PWM(MFET_PIN, freq=2000)
    FET.duty(0)

RELAY = pinout.RELAY_PIN

@MicroWebSrv.route('/led/pwm', "POST")
def _httpTest123(httpClient, httpResponse):
    print("LED PWM Call")

    data = httpClient.ReadRequestContent()
    print(data)

    if FET is None:
        httpResponse.WriteResponse(code=500, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = "MFET is not defined, check setup()")
        return

    
    try:
        value = int(data)
        MFET.value(value)
    except Exception as e:
        print("Exception: {0}".format(e))
        raise
    finally:
        httpResponse.WriteResponseOk(None)

    httpResponse.WriteResponse(code=204, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = None)

@MicroWebSrv.route('/relay', "POST")
def _httpTest123(httpClient, httpResponse):
    if RELAY is None:
        httpResponse.WriteResponse(code=500, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = "RELAY is not defined, check setup()")
        return
    
    data = httpClient.ReadRequestContent()
    try:
        value = int(data)
        RELAY.value(value)
    except Exception as e:
        print("Exception: {0}".format(e))
        raise
    finally:
        httpResponse.WriteResponseOk(None)

    httpResponse.WriteResponse(code=204, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = None)


octopus.w_connect()
octopus.web_server()
