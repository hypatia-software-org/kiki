import json
import os
import time

from slackclient import SlackClient


# Slack Client Constants
API_KEY=""
USER=""
NAME="Aurora"


class Aurora(SlackClient):
    """The Slack bot, Aurora, itself.

    A Slack client is basically a user in a Slack
    team chat. Aurora gives this "Slack Client,"
    special responses, abilities, e.g., sending
    an introduction message to new users.

    """

    def __init__(self, key, user, name):
        """Set Aurora's API key, ..

        Args:
            key (str): Slack API key
            user (str):
            name (str):

        """

        SlackClient.__init__(self, key)
        self.user = user
        self.name = name

    def is_user_message(self, event):
        """Check whether the given event is a message
        and isn't from the bot.

        Args:
            event (dict):

        """

        return event.get("type") == "message" and event["user"] != self.user

    def is_join(self, event):
        """Check whether given event has a channel join event.

        Args:
            event:

        """

        return event.get("subtype") == "group_join"

    def unjson(self, bstring):
        """Decodes bytes to UTF-8 and then decode the string
        from JSON.

        Args:
            bstring:

        """

        return json.loads(bstring.decode("utf_8"))

    def greet(self, event):
        """Greet new user with prewritten paragraph.

        Args:
            event (dict):

        """

        user_id = self.unjson(self.api_call("users.info", user=event['user']))
        username = user_id['user']['name']

        try:
            path = os.path.dirname(os.path.realpath(__file__)) + "/greeting.txt"
            paragraph = open(path).read().format(username, self.name)
            self.rtm_send_message(event['user']['name'], paragraph) 

        except FileNotFoundError:
            print("Greeting file not found! {}".format(path))

    def run(self):

        if not self.rtm_connect():
            print("Connection to RTM failed.")

            return None

        while True:
            response = self.rtm_read()

            for event in response:
                if self.is_join(event):
                    self.greet(event) 

            time.sleep(1)


aurora = Aurora(API_KEY, USER, NAME)
aurora.run()
