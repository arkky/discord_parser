# Parser of discord

I present to the whole world the discord parser

## Features

- Gathers metadata about the guild
- Read each message in different channels
- Collects users in the entire guild

## Usage

1) You need to get your authorization token discord (**authorization** header)
![Semantic description of image](/imgs/discord_authorization_token.png "Discord token")
<!-- blank line -->
<br>

2) You need to be a member of the guild you plan to parse
3) You need to get the guild id (first ID of the url)
<br>

![Semantic description of image](/imgs/guild_id.png "Guild id")

<!-- blank line -->
<br>

4) Insert guild id and your authorization token discord into main.py variables
<!-- blank line -->
<br>

![Semantic description of image](/imgs/insert_ids.png "Insert IDS")

<br>

5) python3 main.py
6) SWAG

### P.S.

It's possible that you could get your discord account temporarily banned if you're parsing a huge amount of messages, so it makes sense to set timeouts between parsing or have multiple accounts.