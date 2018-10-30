import BotPreferences
import discord
import re
import textwrap
import pyodbc

server = 'localhost\FORTUNABASE'
database = 'db_discord'
uid = 'jithbotdev'
pwd = 'jbdev'
driver= '{ODBC Driver 13 for SQL Server}'

def parse_connection():
    """
    Constructs the connection based on the given variables.
    In the future, I plan to have this pull from a config file
    """
    connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+uid+';PWD='+ pwd)
    return(connection)

def remove_command(command, message_object):
    """
    Separates the command and the command prefix from the message body,
    as these are not needed for SQL functions
    """
    message_object.content = re.sub('\\' + BotPreferences.BotPreferences.commandPrefix + command, '', message_object.content)
    if message_object.content.startswith(' '):
        message_object.content = message_object.content[1:]
    return(message_object.content)


def messagestat_formatting(messageBody):
    """
    Formats the message body for messagestat functions.
    This mostly involves replacing spaces with underscores
    and doubling up on quotations so that SQL server
    ignores them
    """
    messageBody = re.sub(' ', '_', messageBody)
    messageBody = re.sub("'", "''", messageBody)
    if messageBody.startswith('"') and messageBody.endswith('"'):
        messageBody = messageBody[1:]
        messageBody = messageBody[:-1]
    return(messageBody)


def format_output(cursor):
    """
    This function is a giant mess and I need to fix
    it at some point. This basically formats the output
    so that it looks like SQLcmd, rather than the
    mess that odbc spits out when returning data
    from SQL
    """
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

def sanitize_inputs(message_object, pointer):
    """
    doubles up on quotation marks to get through two layers of manual
    string executions. There is probably a better way to do this, but i'm dumb
    """
    input = str(getattr(message_object, pointer))
    input = re.sub("'", "''''", input)
    return(input)
