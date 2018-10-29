server = 'localhost\FORTUNABASE'
database = 'db_discord'
uid = 'jithbotdev'
pwd = 'jbdev'
driver= '{ODBC Driver 13 for SQL Server}'

def parse_connection(self):
        connection = pyodbc.connect('DRIVER='+self.driver+';PORT=1433;SERVER='+self.server+';PORT=1443;DATABASE='+self.database+';UID='+self.uid+';PWD='+ self.pwd)
        return(connection)

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
