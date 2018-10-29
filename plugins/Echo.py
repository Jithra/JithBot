from util import Events
import discord
import re

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events():
        return [Events.Command('echo', desc = 'Make JithBot say something.')]

    async def handle_command(self, message_object, command, args):
        if command == 'echo':
            await self.echo_test(message_object, command)

    async def echo_test(self, message_object,command):
        message = re.split(command, message_object.content)
        message = re.split('`', message[1])
        channel = re.sub('\W','', message[0])
        await self.pm.client.delete_message(message_object)
        await self.pm.client.send_message(discord.Object(id = str(channel)), str(message[1]))
        return()
