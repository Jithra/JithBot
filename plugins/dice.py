from util import Events
import discord
import re
import random

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events(): #im putting this here because plugin manager is making me :(
        return [Events.Command("roll", desc="rolls the dice")]

    async def handle_command(self, message_object, command, args):
        if command == "roll":
            await self.pm.client.send_message(message_object.channel, 'Brooke is running a test and this command does nothing')