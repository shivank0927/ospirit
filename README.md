# ospirit Discord Bot

The **ospirit Discord Bot** is designed to provide a wide array of moderation tools and member-based commands, enhancing server management and user engagement. It integrates various functionalities such as user warnings, kicks, bans, message deletions, and other moderation tools, along with commands specifically for server members to manage their profiles, settings, and activities.

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

## Installation

Clone the repository and install the provided dependencies from `requirements.txt`:

```sh
git clone https://github.com/shivank0927/ospirit

cd ospirit

pip install -r requirements.txt
