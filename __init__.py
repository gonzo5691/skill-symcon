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

__author__ = 'ralf'

LOGGER = getLogger(__name__)

class SymconSkill(MycroftSkill):

    #~ __init__
    #~ This is the constructor for the class, called when a new object is created.
    #~ In it you should call the constructor of the MycroftSkill class using super and initialize
    #~ any member variable to the values you need. In the Hello World skill, this looks like
    def __init__(self):
            super(SkillSymcon, self).__init__(name="SkillSymcon")

    #~ This is where you build each intent you want to create. For the Hello World skill, this looks like
    #~
    #~ def initialize(self):
    #~     thank_you_intent = IntentBuilder("ThankYouIntent").\
    #~     require("ThankYouKeyword").build()
    #~     self.register_intent(thank_you_intent, self.handle_thank_you_intent)
    #~     ...
    #~
    #~ This creates an intent named thank_you_intent that requires a ThankYouKeyword,
    #~ which is one of the phrases in the ThankYouKeyword.voc files.
    #~ You can also require defined regex entities, such as Location in the regex example.
    #~ It then registers that the function handle_thank_you_intent is what should be called
    #~ if the ThankYouKeyword is found. All of the other intents are registered in the same way.
    def initialize(self):
        self.load_vocab_files(join(dirname(__file__), 'vocab', self.lang))
        self.load_regex_files(join(dirname(__file__), 'regex', self.lang))
        self.__build_test_intent()
        self.__build_get_intent()

    def __build_test_intent(self):
        intent = IntentBuilder("SymconTestIntent").\
            require("SymconKeyword").build()
        self.register_intent(intent, self.handle_symcon_test_intent)

    def __build_get_intent(self):
        intent = IntentBuilder("SymconGetIntent").\
            require("SymconGetKeyword").build()
        self.register_intent(intent, self.handle_symcon_get_intent)
        
    #~ handle_
    #~ This is where you tell Mycroft to actually do what you want him to do.
    #~ This can range from something like a call to an API to opening an application.
    #~ In the Hello World skill, each intent simply tells Mycroft to speak from the dialog file..
    #~
    #~ def handle_thank_you_intent(self, message):
    #~  self.speak_dialog("welcome")
    #~
    #~ This simply tells Mycroft to randomly select one of the pieces of dialogue from the
    #~ welcome.dialog file and speak it. In your skill, you can include as many ways of phrasing
    #~ what he says as you want.
    #~
    #~ Note that in most Mycroft skills, the handle_intent function will include an API call or something
    #~ else with a potential failure case, so it is best to enclose what you want to run in a try/except block.
    #~ Note also that it always takes two arguments, self and message, even if you never use message.
    def handle_symcon_test_intent(self, message):
        self.speak_dialog("welcome")

    def handle_symcon_get_intent(self, message):
        self.host = SkillSymcon(self.config.get('host'))
        self.username = SkillSymcon(self.config.get('username'))
        LOGGER.debug("username: %s" % username)
        self.password = SkillSymcon(self.config.get('password'))
        self.testid = SkillSymcon(self.config.get('testid'))
        url = self.host
        auth=HTTPBasicAuth(self.username,self.password)
        headers = {'content-type': 'application/json'}
        payload = {"method": "GetValueFloat", "params": [self.testid], "jsonrpc": "2.0", "id": "0"}
        r = requests.post(url, auth=auth, data=json.dumps(payload), headers=headers, stream=True)
        
        decoded = json.loads(r.text)
        temperature = (decoded["result"])
    
        self.speak_dialog("speakValue",{"temperature":temperature})

    #~ stop
    #~ This function is used to determine what Mycroft does if stop is said while this skill is running.
    #~ In the Hello World skill, since Mycroft is saying simple phrases,
    #~ the stop function just contains the word pass:
    #~
    #~ def stop(self)
        #~ pass
    #~ The keyword pass does nothing when executed.
    #~ It is simply used when code is required syntactically but you do not want any code to run.
    #~ For an example of a skill that uses the stop function, look at the NPR News skill.
    def stop(self):
        pass

def create_skill():
    return SkillSymcon()
