import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DiscordOauth:
    client_id = os.getenv('id')
    client_secret = os.getenv('token')
    redirect_uri = "https://broken.mrnoodle1.repl.co/login"
    scope = "identify%20email%20guilds"
    discord_login_url = "https://discord.com/api/oauth2/authorize?client_id=730093014222897182&redirect_uri=https%3A%2F%2Fbroken.mrnoodle1.repl.co%2Fdashboard&response_type=code&scope=identify%20guilds%20email"
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api"
    api_endpoint = 'https://discord.com/api/v6'

    # Get access token
    @staticmethod
    def get_access_token(code):
        access_token_url = DiscordOauth.discord_token_url

        access_token = requests.post(
            access_token_url,
            data={
                'client_id': DiscordOauth.client_id,
                'client_secret': DiscordOauth.client_secret,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': DiscordOauth.redirect_uri,
                'scope': DiscordOauth.scope

            }
        ).json()

        return access_token.get('access_token')

    #Get user
    @staticmethod
    def get_user(access_token):
        user_object = requests.get(
            url=f'{DiscordOauth.api_endpoint}/users/@me',
            headers={'Authorization': 'Bearer %s' % access_token}
        ).json()

        return user_object

    # Get user current guild
    @staticmethod
    def get_user_current_guild(access_token):
        user_guild_object = requests.get(
            url=f'{DiscordOauth.api_endpoint}/users/@me/guilds',
            headers={'Authorization': 'Bearer %s' % access_token}
        ).json()

        return user_guild_object