from util import Events
import discord
import re
import pyodbc

class Plugin(object):
    def __init__(self, pm):
        self.pm = pm
        self.server = 'localhost\FORTUNABASE'
        self.database = 'db_discord'
        self.uid = 'jithbotdev'
        self.pwd = 'jbdev'
        self.driver= '{ODBC Driver 13 for SQL Server}'

    @staticmethod
    def register_events():
        return [Events.Message("logging")]

    async def handle_message(self, message_object):

         if message_object.author.id != '295674371907780619':
             #format server name, user name, and message contents to make them all SQL friendly.
            ServerName = await self.format_text(message_object, 'server')
            ServerID = str(message_object.server.id)
            UserID = str(message_object.author.id)
            UserName = await self.format_text(message_object, 'author')
            UserMessage = await self.format_text(message_object, 'content')
            UserChannel = '#' + str(message_object.channel)
            sql = "EXEC insert_into_table '" + ServerName + "','" + ServerID + "','" + UserName + "','" + UserMessage + "','" + UserChannel + "','" + UserID + "';"
            connection = pyodbc.connect('DRIVER='+self.driver+ ';SERVER='+self.server+';PORT=1443;DATABASE='+self.database+';UID='+self.uid+';PWD='+ self.pwd)
            cursor = connection.cursor()
            cursor.execute(sql)
            cursor.execute("COMMIT;")
            del cursor
            connection.close

	#uses regex to format messages to prevent syntax conflicts with SQL server. (Side note, ' is replaced with ''''' due to how the insert_into_table sproc parses an EXEC statement.)
    async def format_text(self, message_object, pointer):
        text = str(getattr(message_object, pointer))

        if pointer == 'server':
            text = re.sub(' ', '_', text)
            text = re.sub('[\W]', '', text)
        else:
            text = re.sub("'", "''''", text)

        return(str(text))
