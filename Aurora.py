from slackclient import SlackClient
import json
import os
import time

API_KEY=""
USER=""
NAME="Aurora"

class Aurora(SlackClient):
    def __init__(self, key, user, name):
        SlackClient.__init__(self, key)
        self.user = user
        self.name = name

    # Checks whether the given event is a message, and isn't from the bot.
    def is_user_message(self, ev):
        if "type" in ev and ev['type'] == "message" and ev['user'] != self.user:
            return True
        else:
            return False

    # Checks whether the given event was a channel join event.
    def is_join(self, ev):
        if "subtype" in ev and ev['subtype'] == "group_join":
            return True
        else:
            return False

    # Decodes bytes to utf-8 and then decodes the string from json.
    def unjson(self, bstring):
        return json.loads(bstring.decode("utf_8"))

    # Greet a new user with a prewritten paragraph.
    def greet(self, ev):
        user_id = self.unjson(self.api_call("users.info", user = ev['user']))
        username = user_id['user']['name']
        try:
            path = os.path.dirname(os.path.realpath(__file__)) + "/greeting.txt"
            paragraph = open(path).read().format(username, self.name)
            self.rtm_send_message(ev['channel'], paragraph) 
        except FileNotFoundError:
            print("Greeting file not found! {}".format(path))

    def run(self):
        if self.rtm_connect():
            while True:
                response = self.rtm_read()
    
                for event in response:
                    if self.is_join(event):
                        self.greet(event) 

                time.sleep(1)
        else:
            print("Connection to RTM failed.")

aurora = Aurora(API_KEY, USER, NAME)
aurora.run()
