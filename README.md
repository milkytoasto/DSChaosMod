# DSChaosMod

## What is this?

DSChaosMod is a repository for adding a sort of 'Twitch integration' to Dark Souls, wherein viewers can vote in a streamer's chat to interact with their gameplay.

Visit the [Wiki](https://github.com/milkytoasto/DSChaosMod/wiki) for specific details on contributing to this application.

## Project Structure

The repository is broken up into two major parts, with much of the logic being handled by the server portion.

- TwitchVotingOverlay containing an html file with some basic styling meant to be used as a browser source. In the scripts for this html file is the logic for interacting with the sever part over websockets.
- TwitchVoting Server containing many different handlers that work alongside one another, offering a websocket server that transmits messages to the overlay for display. Inside this server are:
  - Bots containing the base logic for bots such as one for Twitch. As of this writing, the only bot in there is the Twitch bot. Any future platforms such as YouTube or the like should get one under here.
  - ChaosHandler which handles the memory editing portion of the application. Effects are performed by reading/writing to the game's memory via the pymem package.
  - ConfigHandler for reading/writing to config files for the app, such as user settings for the effects and Twitch integration settings.
  - ServerGUI, containing the files relating the the application's user interface.
  - VotingHandler which handles the actual logic pertaining to the voting state.
  - WebsocketHandler for handling logic as it pertains to the websocket server.
  
All of these parts rely on one another in one way or another, and communicate with each other's modules asynchronously.

## Installing

1. Clone the repository using `git clone https://github.com/milkytoasto/DSChaosMod.git`
2. Go into the project root directory with `cd DSChaosMod`
3. `python -m pip install pipenv` to get the pipenv dependency
4. `pipenv install --dev` to get both base and dev dependencies
5. `pipenv run pre-commit install` to install the pre-commit hooks
6. (Optional) `pipenv run pre-commit run -a` to run the pre-commit hooks. This will make sure they are operating as expected.

And that should be all you need to get started on development. There is more planned with the mod as it is still in the early stages, so this is subject to change.

At this time I would recommend running `git update-index --assume-unchanged .\TwitchVotingServer\config.ini` to prevent committing any secrets you may store in there.

## Usage

Currently there is a gui server that can be run by running the `server.py` file. A sample `client.py` file has been added to receive and print the messages the websocket server broadcasts.

To run the websocket server, press `Initialize Websocket Server`

`Connect to Twitch` will initialize the tasks to connect to Twitch as well as the actual voting handler.

`Stop` will stop the voting handler as well as the Twitch bot.
