USE [db_discord]
GO
/****** Object:  StoredProcedure [dbo].[insert_into_table]    Script Date: 10/29/2018 10:31:10 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROC [dbo].[insert_into_table] (@servername VARCHAR(100), @serverID VARCHAR(100), @username VARCHAR(100), @usermessage VARCHAR(1000), @userchannel VARCHAR(100), @userid VARCHAR(50))
AS
BEGIN
/*Set @servername to the value that matches the server ID in tblServerID*/
EXECUTE ('INSERT INTO tblAggregateDiscordLogs (ServerName, ServerID, UserChannel, UserName, UserMessage, MessageTime, UserID) VALUES (''' + @servername + ''',''' + @serverID + ''',''' + @userchannel + ''',''' + @username + ''',''' + @usermessage + ''',' + 'GETDATE()' + ',''' + @userid + ''')')
END 