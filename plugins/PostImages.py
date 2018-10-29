from util import Events
import glob
import os
import random


class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events():
        return [Events.Command("two", desc="Two?"),
                Events.Command("two?", desc="An alternative for 'two'"),
                Events.Command("kyouko", desc="Post an image of Kyouko")]

    async def handle_command(self, message_object, command, args):
        if command == "two" or command == "two?":
            await self.post_image(message_object, "two")
        if command == "kyouko":
            await self.post_image(message_object, "kyouko")

    async def post_image_to_user(self, message_object, user, type, message):
        files = glob.glob(os.getcwd() + "/images/" + type + "/" + '*.gif')
        files.extend(glob.glob(os.getcwd() + "/images/" + type + "/" + '*.png'))
        files.extend(glob.glob(os.getcwd() + "/images/" + type + "/" + '*.jpg'))
        file = random.choice(files)

        await self.pm.client.delete_message(message_object)

        if user is None or user == "":
            await self.pm.client.send_message(message_object.channel, "Please specify a target to " + type + ".")
            return

        await self.pm.client.send_message(message_object.channel,
                                          "**" + user + "** " + message)
        await self.pm.client.send_file(message_object.channel, file)

    async def post_image(self, message_object, type):
        files = glob.glob(os.getcwd() + "/images/" + type + "/" + '*.gif')
        files.extend(glob.glob(os.getcwd() + "/images/" + type + "/" + '*.png'))
        files.extend(glob.glob(os.getcwd() + "/images/" + type + "/" + '*.jpg'))
        file = random.choice(files)
        await self.pm.client.send_file(message_object.channel, file)
