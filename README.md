# ospirit Discord Bot

The **ospirit Discord Bot** is designed to provide a wide array of moderation tools and member-based commands, enhancing server management and user engagement. It integrates various functionalities such as user warnings, kicks, bans, message deletions, and other moderation tools, along with commands specifically for server members to manage their profiles, settings, and activities.

## Features and Functionalities:

- **Moderation Tools**:
  - `kick`: Kicks a user from the server.
  - `ban`: Bans a user from the server.
  - `timeout`: Temporarily mutes a user for a set period.
  - **Purge Command**: Deletes a specific number of messages from a channel.
  - **Avatar Check**: Fetches the avatar of a user.
  - **About User Command**: Provides information about a user.

- **Log System Setup**:
  - Automatically creates a `moderation` category and a `logs` channel to redirect all moderation commands, deleted/edited messages, and track when someone joins the server using an invite from someone else.

- **Channel and Category Management**:
  - Tracks and logs when channels or categories are created.
  - Provides channel statistics such as message counts and other key metrics.

- **Server Member Commands**:
  - Allows members to manage their profiles and settings.
  - Provides a random or specific quote when requested by a user.

- **Ping Check Command**: Checks the bot’s latency to the server.

With ospirit, you can ensure smooth moderation and provide enhanced interaction for members within your server.

## Installation

Clone the repository and install the provided dependencies from `requirements.txt`:

```sh
git clone https://github.com/shivank0927/ospirit

cd ospirit

pip install -r requirements.txt
