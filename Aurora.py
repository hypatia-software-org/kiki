from slacker import *
from time import sleep

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

        except FileNotFoundError:
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

        """

        channel = self.im.open(uid)
        callback(channel.body["channel"]["id"])
        self.im.close(channel.body["channel"]["id"])

    def send_test(self, channel):
        """Send the string 'test' to a channel.

        Args:
            channel (str): Channel to send to.

        """

        self.chat.post_message(channel, "<3 This bot loves you <3", as_user=True)

    def run(self):

        while True:
            response = self.users.list()
            users = set(user["id"] for user in response.body["members"])

            if not self.userlist:
                print("No users defined. Learning users.")
                self.learn_users(users)
                print("Done.")

            else:

                for user in (users ^ self.userlist):
                    self.with_channel(user, self.send_test)
                    print("Learning {}...".format(user))
                    self.learn_users(users ^ self.userlist)
               
            self.userlist = users
            sleep(1)


if __name__ == "__main__":
    bot_config = configparser.ConfigParser()
    bot_config.read("bot_config.ini")
    api_key = bot_config.get("bot", "apikey")

    bot = Bot(api_key)
    bot.run()
