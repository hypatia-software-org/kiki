# Slack Bot Aurora

This bot sends a private message (defined in a text file) to a user
that's new to your team!

## Usage

`greeting.txt` contains the text sent to new users. It's modified with
`format` to include the user's username and the bot's name.

A file (`userfile`) is used as a database for detecting new users. It
is updated when new users are detected.

# Dependencies

`pip install -r requirements.txt`

  * `slacker`
