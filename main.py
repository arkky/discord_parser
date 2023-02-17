import requests


class Parser:
    # the parser collects from all channels of the guild all messages of users for the role of everyone who has permissions to view messages
    # and then collects information about each user
    def __init__(self, authorization_token: str, guild_id: str):
        # the parser needs to be given your authentication token and guild id
        # your authentication token via web discord in the networks panel in the browser as a request header
        # guild id can be obtained from the web discord or via the discord API
        self.guild_id = guild_id
        self.headers = {"authorization": authorization_token} # you may need to add some user-agent, but so far it works
        
        self.get_everyone_permissions()
        self.get_guild()
        self.everyone_can_read = self.check_permissions(self.everyone_permissions)
    
    def get_guild(self) -> None:
        # get some metadata. in fact, you can get more metadata from the guild
        # so you can refer to the discord API for clarification
        response = requests.get(f"https://discord.com/api/v9/guilds/{self.guild_id}", headers=self.headers)
        data = response.json()
        
        guild_name = data['name']
        region = data['region']
        verification_level = data['verification_level']
        language = data['preferred_locale']
        
        self.meta_info = {
            "guild_name": guild_name,
            "guild_id": self.guild_id,
            "region": region,
            "verification_level": verification_level,
            "language": language,
        }
    
    def get_everyone_permissions(self) -> None:
        # get all permissions from the guild for each role
        roles = self.get_roles()
        for role in roles:
            if role['name'] == '@everyone':
                self.everyone_id = role['id']
                self.everyone_permissions = int(role['permissions'])
                break
    
    def get_roles(self) -> dict:
        # get all roles from guild
        response = requests.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/roles", headers=self.headers)
        return response.json()
    
    def get_channels(self) -> dict:
        # get all channels from guild
        response = requests.get(f"https://discord.com/api/v9/guilds/{self.guild_id}/channels", headers=self.headers)
        return response.json()
    
    def get_messages(self, channel_id: str, limit: int = 100, before_id: int = 9223372036854775806) -> dict:
        # get all messages from the channel in a chunk of 100 units (limit=100)
        length_messages = limit
        info_users = {}

        while length_messages >= limit:
            try:
                response = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}&before={before_id}", headers=self.headers)
                messages = response.json()

                if "code" in messages:
                    raise Exception("print messages")

                length_messages = len(messages)
                print("Length messages:", length_messages)
                
                if length_messages:

                    for message in messages:
                        username = message['author']['username']
                        discriminator = message['author']['discriminator']

                        nickname = username + "#" + discriminator
                        id_member = message['author']['id']

                        info_users[nickname] = id_member

                    before_id = messages[-1]['id']
                    print(f"Before_id: {before_id}")

                if length_messages != limit:
                    break

            except Exception as e:
                print(e)
                print(messages)
                break
                
        return info_users
    
    def get_id_channels(self):
        # the logic of work is as follows: we are looking for all channels for a regular user with the role of everyone
        # Then we check the channel's rights to view messages, if they are, then fine
        channels = self.get_channels()
        id_channels = []
        for channel in channels:

            if channel['type'] == 0:

                if channel['permission_overwrites']:
                    everyone_flag = False

                    for permission in channel['permission_overwrites']:
                        allow = int(permission['allow'])
                        deny = int(permission['deny'])

                        if permission['id'] == self.everyone_id:
                            everyone_flag = True

                            if self.everyone_can_read:
                                if not self.check_permissions(deny):
                                    id_channels.append(channel['id'])
                            else:
                                if self.check_permissions(allow):
                                    id_channels.append(channel['id'])

                        if everyone_flag:
                            break

                else:
                    if self.everyone_can_read:
                        id_channels.append(channel['id'])

        return id_channels
    
    @staticmethod
    def check_permissions(permissions):
        answer = False
        if int(permissions) & 0x400:
            answer = True
        return answer
    
    def get_all_users_from_guild(self):
        info_users = {}
        id_channels = self.get_id_channels()
        for id_channel in id_channels:
            temp_info_users = self.get_messages(id_channel)
            info_users.update(temp_info_users)
        
        result_data = {'users': info_users, 'meta': self.meta_info}
        return result_data
    

if __name__ == "__main__":
    DISCORD_TOKEN = "<YOUR DISCORD TOKEN>"
    GUILD_ID = "<YOUR GUILD ID>"
    giga_discord_parser = Parser(DISCORD_TOKEN, GUILD_ID)

    data = giga_discord_parser.get_all_users_from_guild()

    # save all users with unique nicknames and ids
    with open(f"data_{data['meta']['guild_id']}.txt", "w") as f:
        for meta in data['meta']:
            f.write(f"{meta}: {data['meta'][meta]}\n")
        f.write("---"*15 + "\n")
        f.write(f"user_id:nickname\n\n")
        for user in data['users']:
            f.write(f"{data['users'][user]}:{user}\n")