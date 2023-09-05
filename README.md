# jsondb-bot

A simple discord bot to record json data.

## Usage

1. Setup the environment. In `.env`:

```
DISCORD_TOKEN=[your bot token]
DBFILE=[database file]
```

2. Install and run the application
```bash
pip install git+https://github.com/jimmy-zx/jsondb-bot.git
python -m jsondb_bot
```

## Bot commands

| Name | Function |
|-|-|
| `$ping` | Ping the bot. The bot will send `pong` in the same channel. |
| `$dmping` | Ping the bot. The bot will send `pong` by DM to the sender. |
| `$reg$[data]` | Append some json data in the sender's storage. |
| `$dereg` | Delete all data saved by the sender. |
| `$check` | Check the data saved by the sender. |

## Database format

The data is stored as a dict that maps user ID to a list of saved data.

## Notes

- DO NOT USE AS A PUBLIC BOT.
No security/rate limiting mechanisms has been implemented.
