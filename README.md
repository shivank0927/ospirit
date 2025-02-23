# ospirit discord bot

A basic discord bot with several functionalities.

## Features and Functionalities:

- **Moderation Commands**:
  - `kick`: Kicks a user from the server.
  - `ban`: Bans a user from the server.
  - `unban`: Unbans a user from the server.
  - `purge`: Deletes a specific number of messages from a channel.
  - `mute`: Temporarily mutes a user for a set period.
  - `createcategory`: Creates a new category in the server.
  - `createchannel`: Creates a new channel in the server.
  - `logs`: Sets up and manages a log system to track all moderation activities, deleted/edited messages, and user join events.

- **Member Commands**:
  - `channelstats`: Provides statistics for a channel such as message counts and activity metrics.
  - `about`: Provides detailed information about a user.
  - `avatar`: Fetches and displays the avatar of a user.
  - `ping`: Checks the bot’s latency to the server.
  - `quote`: Provides a random or specific quote when requested by a user.
  - `caption`: Returns a formatted embed of a message referenced by command user.

## Installation
- The bot is not hosted online, to use the code you have to clone the repository and install the dependencies.

- Clone the repository and install the provided dependencies from `dependencies.txt`:

```sh
git clone https://github.com/shivank0927/ospirit

cd ospirit

pip install -r requirements.txt
