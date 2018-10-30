from PluginManager import PluginManager
from util import jithsql
from util import Events
import discord
import re
import pyodbc

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events():
        return [Events.Message("logging")]

    async def handle_message(self, message_object):

         if message_object.content.startswith(self.pm.botPreferences.commandPrefix) is False:
             #format server name, user name, and message contents to make them all SQL friendly.
            ServerName = jithsql.sanitize_inputs(message_object, 'server')
            UserName = jithsql.sanitize_inputs(message_object, 'author')
            UserMessage = jithsql.sanitize_inputs(message_object, 'content')
            ServerID = str(message_object.server.id)
            UserID = str(message_object.author.id)
            UserChannel = '#' + str(message_object.channel)
            sql = "EXEC insert_into_table '" + ServerName + "','" + ServerID + "','" + UserName + "','" + UserMessage + "','" + UserChannel + "','" + UserID + "';"
            connection = jithsql.parse_connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            cursor.execute("COMMIT;")
            del cursor
            connection.close
