#  __init__.py
#
#  Copyright 2017  <pi@picroft>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
 
from os.path import dirname
 
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
 
import requests
from requests.auth import HTTPBasicAuth
import json

from fuzzywuzzy import fuzz

__author__ = 'ralf'

LOGGER = getLogger(__name__)

class SkillSymcon(MycroftSkill):

    def __init__(self):
        super(SkillSymcon, self).__init__(name="SkillSymcon")
 
        self.url = self.config.get('url')
        self.username = self.config.get('username')
        self.password = self.config.get('password')
        self.testid = self.config.get('testid')
        self.scriptid = self.config.get('scriptid')
 
    def initialize(self):
        self.__build_get_intent()
  
    def symconClient(self, method, param):
        auth=HTTPBasicAuth(self.username,self.password)
        headers = {'content-type': 'application/json'}          
        payload = {"method": method, "params": param, "jsonrpc": "2.0", "id": "0"}
        req = requests.post(self.url, auth=auth, data=json.dumps(payload), headers=headers, stream=True)
 
        if req.status_code == 200:
            json_response = req.json()
            return json_response
        else:
            self.speak_dialog("speakValue",{"temperature":temperature})
            pass

    def get_itemDictionary(self):
        try:
            itemDictionary = json.loads(symcon.symconClient("IPS_RunScriptWait",[self.scriptid])['result'])
            return itemDictionary       
        except:
            raise ValueError("Dictionary not found")

    def get_room(self, message):
        try:
            room = message.data.get("room", None)
            if room:
                return room, room
        except:
            raise ValueError("Room not found")

    def get_attribute(self, message):
        try:
            attribute = message.data.get("attribute", None)
            if attribute:
                return attribute, attribute
        except:
            raise ValueError("Attribute not found")

    def findItemName(self, messageItem):
        bestScore = 0
        score = 0
        bestItem = None		
        
        try:
            for itemName, itemLabel in itemDictionary.items():
                score = fuzz.ratio(messageItem, itemName)
                LOGGER.info("Score: {}; Item: {}".format(score,itemName))
                if score > bestScore:
                    bestScore = score
                    bestItem = itemLabel
        except KeyError:
                    pass
                    
        return bestItem

    def __build_get_intent(self):
        intent = IntentBuilder("SymconGetIntent").\
            require("getKeyword").\
            require("attribute").\
            optional("room").\
            build()
        self.register_intent(intent, self.handle_symcon_get_intent)
         
    def handle_symcon_test_intent(self, message):
        self.speak_dialog("welcome")
  
    def handle_symcon_get_intent(self, message):
        room = message.data.get('room')
        LOGGER.info("Room: {}, Attribute: {}".format(message.data.get('room'),message.data.get('attribute')))
        #value = self.symconClient("GetValue",[item['objectID']])
        #LOGGER.info(value['result'])
        #self.speak_dialog("speakValue",{"room":item['room'],"attribute":item['attribute'],"value":value['result']})
 
    def stop(self):
        pass
 
def create_skill():
    return SkillSymcon()
