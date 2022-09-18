# DSChaosMod

Installing
---

1. Clone the repository using `git clone https://github.com/milkytoasto/DSChaosMod.git`
2. Go into the project root directory with `cd DSChaosMod`
3. `python -m pip install pipenv` to get the pipenv dependency
4. `pipenv install --dev` to get both base and dev dependencies
5. `pipenv run pre-commit install` to install the pre-commit hooks

And that should be all you need to get started on development. There is more planned with the mod as it is still in the early stages, so this is subject to change.

At this time I would recommend running `git update-index --assume-unchanged .\TwitchVotingServer\config.ini` to prevent committing any secrets you may store in there.

Usage
---

Currently there is a gui server that can be run by running the `server.py` file. A sample `client.py` file has been added to receive and print the messages the websocket server broadcasts.

To run the websocket server, press `Initialize Websocket Server`

`Connect to Twitch` will initialize the tasks to connect to Twitch as well as the actual voting handler.

`Stop` will stop the voting handler as well as the Twitch bot.
