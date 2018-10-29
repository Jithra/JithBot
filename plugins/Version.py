from util import Events
import discord

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events():
        return [Events.Command('version', desc = 'prints the current version')]

    async def handle_command(self, message_object, command, args):
        if command == 'version':
            await self.print_version(message_object)

    async def print_version(self, message_object):
        await self.pm.client.send_message(message_object.channel, 'My current version is FG25 Ver3.0.1 Rev2.1')
