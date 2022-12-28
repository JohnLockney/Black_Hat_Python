#!/usr/bin/env python
"""
Extending Burp Proxy
Page 97

###############################################################
# Note: download jython .jar from
# https://www.jython.org/download.html

###############################################################
## jython import error: 12/27/22

# jython-standalone-2.7.4.jar
# burp community v2022.12.4
# Startup warning: Your JRE appears to be 17.0.5 from Debian Burp has not been fully tested on this platform
## Import Error:
java.lang.Exception: Extension class is not a recognized type
	at burp.i6d.S(Unknown Source)
	at burp.i6d.z(Unknown Source)
	at burp.dp8.I(Unknown Source)
	at burp.bsl.e(Unknown Source)
	at burp.rm2.lambda$panelLoaded$0(Unknown Source)
	at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:539)
	at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136)
	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
	at java.base/java.lang.Thread.run(Thread.java:833)

"""


from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import list, ArrayList

import random

class BurpExtender(IBurpExtender, IIntruderPaylaodGeneratorFactory):
    def registerExtendercallbacks(self, callbacks):
        self.callbacks = callbacks
        self._helpers  = callbacks.getHelpers()

        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return

    def getGeneratorName(self):
        return "BHP Payload Generator"

    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)

class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attach):
        self.extender = extender
        self.helpers  = extender._helpers
        self._attack  = attack
        self.mayx_payloads  = 10
        sxelf.num_iterations = 0

        return

    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True

    def getNextPayload(self, current_payload):
        # convert into a string
        payload = self.mutate_payload(payload)

        # increase the number of of fuzzing attempts
        self.num_iterations += 1

        return payload

    def reset(self):
        self.num_iterations = 0
        return

    def mutate_payload(self, original_payload):
        '''# pick a simple mutator or even call an external script'''
        picker = random.randint(1,3)

        # select a random offset in teh payload to mutate
        offset = random.randint(0,len(original_payload) -1)

        front, back = original_payload[:offset], original_payload[offset:]

        # random offset insert a SQL injection attempt
        if picker == 1:
            front += "'"

            # jam an XSS attempt in
        elif picker == 2:
            front += "<script>alert('BHP!');</script>"

        # repeat a random chunk of the original payload
        elif picker == 3:
            chunk_length = random.randint(0, len(back)-1)
            repeater = random.randint(1,10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]

        return front + back


