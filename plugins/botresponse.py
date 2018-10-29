from util import Events
import discord
import re
import random

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events(): #im putting this here because plugin manager is making me :(
        return [Events.Message("test")]

    async def handle_message(self, message_object): #tell the bot how to respond to various messages

        if message_object.author.name != 'JithBot' and message_object.author.id != '398266752829489152':
            if re.search("DEUS VULT", message_object.content) is not None:
                await self.pm.client.send_message(message_object.channel, random.choice(['FOR JERUSALEM', 'FOR THE HOLY LAND', 'GOD WILLS IT', 'DEUS VULT', 'WE SHALL TAKE BACK WHAT IS OURS']))

            elif re.search("roh roh", message_object.content.lower()) is not None: #Respond to "Roh Roh"
                await self.pm.client.send_message(message_object.channel,'Fight the powa!')

            elif (re.search("hello jithbot", message_object.content.lower()) is not None) or (re.search("hi jithbot", message_object.content.lower()) is not None): #Respond to "Hello Jithbot"
                await self.pm.client.send_message(message_object.channel,'Hello.')

            elif re.search("i{1,}'{0,}m{1,} {0,}g{1,}(a|e){1,}(y|i){1,}", message_object.content.lower()) is not None: #Respond to "I'm gay"
                await self.pm.client.send_message(message_object.channel,'Please tell me more about how your sexuality makes you a special snowflake.')

            elif re.search("i{1,}'{0,}m{1,} {0,} s{1,}l{1,}e{1,}p{1,}y{1,}", message_object.content.lower()) is not None: #Respond to "I'm sleepy."
                await self.pm.client.send_message(message_object.channel,'Then go to sleep you autistic parrot.')

            elif re.search("w{1,}o{1,}", message_object.content.lower()) is not None and re.search("\ww{1,}o{1,}", message_object.content.lower()) is None and re.search("w{1,}o{1,}\w", message_object.content.lower()) is None: #Respond to 'wo'
                await self.pm.client.send_message(message_object.channel,'Studies show that people who omit letters from words have LOTS OF SEX')
