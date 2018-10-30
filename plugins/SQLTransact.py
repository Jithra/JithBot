from util import Events
from util import jithsql
import discord
import re
import textwrap
import pyodbc

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm

    @staticmethod
    def register_events(): #im putting this here because plugin manager is making me :(
        return [Events.Command("transact", desc='execute sql code'),
                Events.Command("select", desc='execute sql code'),
                Events.Command("messagestat", desc='execute sql code')]

    async def handle_command(self, message_object, command, args):
        if command == 'transact' and message_object.author.name == "Jithra" and message_object.author.id == '130942288510582784':
            await self.process_transaction(message_object, command)

        if command == 'select' and message_object.author.name == "Jithra" and message_object.author.id == '130942288510582784':
            await self.process_selection(message_object, command)

        if command == 'messagestat':
            await self.process_messagestat(message_object, command)


    async def process_transaction(self, message_object, command):
        connection = jithsql.parse_connection()
        cursor = connection.cursor()
        sql = jithsql.remove_command(command, message_object)
        cursor.execute(sql)
        cursor.execute("COMMIT;")
        connection.close
        del cursor
        await self.pm.client.send_message(message_object.channel, 'Command(s) completed successfully.')
        return()

    async def process_selection(self, message_object, command):
        connection = jithsql.parse_connection()
        cursor = connection.cursor()
        sql = jithsql.remove_command(command, message_object)
        cursor.execute(sql)
        outputMessage = jithsql.format_output(cursor)
        cursor.execute("COMMIT;")
        connection.close
        del cursor
        await self.pm.client.send_message(message_object.channel, outputMessage)
        return()


    async def process_messagestat(self, message_object, command):
        messageBody = jithsql.remove_command(command, message_object)
        connection = jithsql.parse_connection()
        cursor = connection.cursor()

        if (messageBody.startswith('"') and messageBody.endswith('"')):
            messageBody = jithsql.messagestat_formatting(messageBody)
            sql = ('EXEC messagestatliteral "' + messageBody + '", "' + str(message_object.server.id) + '"')
        else:
            messageBody = jithsql.messagestat_formatting(messageBody)
            sql = ('EXEC messagestat "' + messageBody + '", "' + str(message_object.server.id) + '"')

        cursor.execute(sql)
        outputMessage = jithsql.format_output(cursor)
        cursor.execute("COMMIT;")
        connection.close
        del cursor
        await self.pm.client.send_message(message_object.channel, outputMessage)
        return()
