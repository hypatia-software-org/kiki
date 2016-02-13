# Kiki: Greets newbies on a Slack team

Kiki sends a private message (`greeting.txt`) to
people who are new to your Slack team!

Kiki was named after Kiki, from Kiki's Delivery Service.

## Usage

  1. Create `greeting.txt`, this will be
     the text sent to new users.
  2. Enter your Slack bot API key into `bot_config.example.ini`
  3. `pip install -r requirements.txt`

A file (`userfile`) is used as a database for detecting new users. It
is updated when new users are detected.
