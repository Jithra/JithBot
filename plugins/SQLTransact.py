from util import Events
import discord
import re
import textwrap
import pyodbc

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm
        self.server = 'localhost\FORTUNABASE'
        self.database = 'db_discord'
        self.uid = 'jithbotdev'
        self.pwd = 'jbdev'
        self.driver= '{ODBC Driver 13 for SQL Server}'
        self.literalFlag = 0

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
        connection = self.parse_connection()
        cursor = connection.cursor()
        sql = self.remove_command(command, message_object)
        cursor.execute(sql)
        cursor.execute("COMMIT;")
        connection.close
        del cursor
        await self.pm.client.send_message(message_object.channel, 'Command(s) completed successfully.')
        return()

    async def process_selection(self, message_object, command):
        connection = self.parse_connection()
        cursor = connection.cursor()
        sql = self.remove_command(command, message_object)
        cursor.execute(sql)
        outputMessage = self.format_output(cursor)
        cursor.execute("COMMIT;")
        connection.close
        del cursor
        await self.pm.client.send_message(message_object.channel, outputMessage)
        return()


    async def process_messagestat(self, message_object, command):
        messageBody = self.remove_command(command, message_object)
        messageBody = self.messagestat_formatting(messageBody)
        connection = self.parse_connection()
        cursor = connection.cursor()

        if (self.literalFlag == 1):
            sql = ('EXEC messagestatliteral "' + messageBody + '", "' + str(message_object.server.id) + '"')
            cursor.execute(sql)

        else:
            sql = ('EXEC messagestat "' + messageBody + '", "' + str(message_object.server.id) + '"')
            cursor.execute(sql)

        outputMessage = self.format_output(cursor)
        cursor.execute("COMMIT;")
        connection.close
        del cursor
        await self.pm.client.send_message(message_object.channel, outputMessage)
        return()

    def parse_connection(self):
        connection = pyodbc.connect('DRIVER='+self.driver+';PORT=1433;SERVER='+self.server+';PORT=1443;DATABASE='+self.database+';UID='+self.uid+';PWD='+ self.pwd)
        return(connection)

    def remove_command(self, command, message_object):
        message_object.content = re.split(command, message_object.content)
        return(message_object.content[1])


    def messagestat_formatting(self, messageBody):
        messageBody = messageBody[1:]
        messageBody = re.sub(' ', '_', messageBody)
        messageBody = re.sub("'", "''", messageBody)
        self.literalFlag = 0

        if (messageBody.startswith('"') and messageBody.endswith('"')):
            messageBody = messageBody[1:]
            messageBody = messageBody[:-1]
            print(messageBody)
            self.literalFlag = 1

        return(messageBody)

    def format_output(self, cursor):
        #assign all the contents of the cursor to sqlOutput
        sqlOutput = cursor.fetchall()
		#assign rowOutput to a blank value so it can be used with the += function
        rowOutput = ''
        columnHeaders = ''
		#format each row and column so that it has a uniform length of 20 - also change the date format that ODBC outputs by default
        for row in sqlOutput:
            for column in row:
                columnBody = str(column)
                columnBody = re.sub("(?P<year>[0-9]{4,})-(?P<month>[0-9]{1,})-(?P<day>[0-9]{1,}) (?P<hour>[0-9]{1,}):(?P<minute>[0-9]{1,}):(?P<second>[0-9]{1,}).[0-9]{1,6}", "\g<year>-\g<month>-\g<day> \g<hour>:\g<minute>:\g<second>", columnBody)

                if len(columnBody) >= 20:
                    columnBody = textwrap.shorten(columnBody, width = 20)

                while len(columnBody) < 20:
                    columnBody += ' '

                rowOutput += columnBody

            rowOutput += '\n'

	    #format the column headers in a similar fashion as the rows
        for column in cursor.description:
            columnHeader = str(column[0])

            while len(columnHeader) < 20:
                columnHeader += ' '
            columnHeaders += columnHeader
        columnHeaders += '\n'

        for columns in columnHeaders:
            columnHeaders += '-'

        columnHeaders = re.sub('_',' ', columnHeaders)
        outputMessage = '```TSQL\n' + columnHeaders + '\n' + rowOutput + '```'

        return(outputMessage)
