# Discord Bot
A general purpose discord bot built with discord.py api wrapper in python.

## Features
* Moderation commands
* Web search
* Miscellaneous commands 
* Music support (coming soon)

## Running
#### Create a bot user on the discord developer portal
Follow the steps given in the link below and create a bot user
[click here](https://discordpy.readthedocs.io/en/stable/discord.html)

#### Make sure to get python 3.9 or higher
This runtime is required to run the bot

#### Set up environment variables for the project
To run this project, you will need to add the following environment variables to your .env file<br />
`TOKEN`<br />
This is the token authorized by discord to your bot account

#### Setup a virtual environment
1. Install the virtual environment maker tool
    ```bash
    pip install virtualenv
    ```

2. Create a virtual environment (you could name the environment anything)
    ```bash
    virtualenv venv
    ```

3. Activate virtual environment 
    (for linux and mac)
    ```bash
    source ./venv/Scripts/activate
    ```
    (for windows)
    ```powershell
    ./venv/Scripts/activate
    ```

#### Install required packages
```bash
pip install -r requirements.txt
```
#### Run the instance of the bot
```bash
python main.py
```

> Your bot would be up and ready but remember that the bot is hosted temporarily on your local machine and would be down once you exit the code or close the terminal

## Documentation
- [discord developer portal official documentation](https://discord.com/developers/docs/intro)
- [discordpy official documentation](https://discordpy.readthedocs.io/en/stable/)

## Acknowledgements
 - [Awesome open-source discord bots made with discordpy](https://opensourcelibs.com/libs/discord-py)
 - [Host a discord bot 24/7 for free](https://medium.com/analytics-vidhya/how-to-host-a-discord-py-bot-on-heroku-and-github-d54a4d62a99e)