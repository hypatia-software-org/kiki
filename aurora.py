from slacker import *
from time import sleep
import requests

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class Bot(Slacker):

    def __init__(self, key):
        """Set bot's API key and load userlist.

        Args:
            key (str): Slack API key
        """

        Slacker.__init__(self, key)
        self.userlist = self.load_userlist()

    def load_userlist(self):
        """Load userlist from textfile 'userlist'.
        
        Returns:
            set: The user IDs read from userlist file.

        """

        try:

            with open("userlist", "r") as userlist:

                return set(uid.strip() for uid in userlist.readlines())

        except IOError:
            print("File not found... using empty userlist.")

            return set()

    def learn_users(self, uids):
        """Iterate over user ids and append them to 
        the file 'userlist'.

        Args:
            uids (set): Set of IDs to append (strs).

        """

        with open("userlist", "a") as userlist:

            for user in uids:
                userlist.write("{}\n".format(user))

    def with_channel(self, uid, callback):
        """Opens an IM channel with a user and
        calls a callback with the new channel ID
        and finally closes the channel when done.

        Args:
            uid (str): User ID to open a channel for.
            callback (function): Function to pass the channel ID to.

        Returns:
            bool: True if able to open IM session, False if unable
                to open session, e.g., user is disabled.

        Raises:
            slacker.Error: Raises an error if a user cannot be
                messaged, and it's for a reason beyond their
                account being disabled or being a bot.

        """

        try:
            channel = self.im.open(uid)
            callback(channel.body["channel"]["id"])
            self.im.close(channel.body["channel"]["id"])

            return True

        except Error as e:

            if e.message in ("user_disabled", "cannot_dm_bot"):

                return False

            else:

                raise e

    def send_greeting(self, channel):
        """Send the new member greeting in greeting.txt to the user.

        Args:
            channel (str): Channel to send to.

        """
        try:
            
            with open("greeting.txt", "r") as greeting:
                self.chat.post_message(channel, greeting.read(), as_user=True)

        except FileNotFoundError:
            print("Greeting file not found!")

    # NOTES: YIKES! REFACTOR!!!
    # We need to start using more decorators.
    def run(self):

        try:
            while True:
                response = self.users.list()
                users = set(user["id"] for user in response.body["members"])

                if not self.userlist:
                    print("No users defined. Learning users.")
                    self.learn_users(users)
                    print("Done.")

                else:

                    for user in (users ^ self.userlist):

                        if self.with_channel(user, self.send_greeting):
                            print("Learning {}...".format(user))
                            self.learn_users(users ^ self.userlist)
                   
                self.userlist = users
                sleep(1)

        except requests.exceptions.HTTPError as e:

            if e.response.status_code == 504:

                pass

            else:

                raise e


if __name__ == "__main__":
    bot_config = configparser.ConfigParser()
    bot_config.read("bot_config.ini")
    api_key = bot_config.get("bot", "apikey")

    bot = Bot(api_key)
    bot.run()
