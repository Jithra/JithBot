USE [db_discord]
GO
/****** Object:  StoredProcedure [dbo].[manage_table]    Script Date: 10/29/2018 10:31:00 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROC [dbo].[manage_table] @serverID VARCHAR(100), @servername VARCHAR(1000)
AS 

DECLARE @idtest VARCHAR(100), @count INT;
DECLARE @nametest VARCHAR(100), @oldname VARCHAR(100), @newname VARCHAR(100);
SET @servername = 'tbl' + @servername;
SELECT @idtest = (SELECT ServerID FROM tblServerID WITH (NOLOCK) WHERE ServerID = @serverID)
SELECT @nametest = (SELECT ServerName FROM tblServerID WITH (NOLOCK) WHERE ServerID = @serverID)


/*Handler to create table if no entry exists for serverid and name. If servername is null, its safe to create table based off servername. */
IF (OBJECT_ID(@servername) IS NULL) AND (@idtest IS NULL) AND (@nametest IS NULL)
BEGIN
EXECUTE ('USE db_discord CREATE TABLE ' + @servername + '( EntryID INT IDENTITY (1,1), UserChannel VARCHAR(100), UserName VARCHAR(100), UserID VARCHAR(20), UserMessage VARCHAR(1000), MessageTime DATETIME)');
INSERT INTO tblServerID (ServerID, ServerName) 
VALUES (@serverid, @servername);
END

/*Handler to create table and assign it a unique name if there is no ID entry in the routing table, but there is already a table named after servername*/
ELSE IF OBJECT_ID(@servername) IS NOT NULL AND @idtest IS NULL
BEGIN
SET @count = 2
SET @newname = @servername
		WHILE OBJECT_ID(@newname) IS NOT NULL
	    BEGIN
		    SET @newname = @servername
		    SET @newname = @newname + (CONVERT(VARCHAR,@count))
			SET @count = @count + 1
		END
EXECUTE ('USE db_discord CREATE TABLE ' + @newname + '( EntryID INT IDENTITY (1,1), UserChannel VARCHAR(100), UserName VARCHAR(100), UserID VARCHAR(20), UserMessage VARCHAR(1000), MessageTime DATETIME)');
INSERT INTO tblServerID (ServerID, ServerName)
VALUES (@serverid, @newname);
END

/*Handler to rename a server if it already has an entry ID but servername has changed. Also checks to make sure the new name is not already in use.*/
ELSE IF(OBJECT_ID(@servername) IS NULL) AND @idtest IS NOT NULL
BEGIN
	SELECT @oldname = (SELECT ServerName FROM tblServerID WITH (NOLOCK) WHERE ServerID = @serverID)
	SET @newname = @servername
	EXEC sp_rename @oldname, @newname
	UPDATE tblServerID 
	SET ServerName = @newname
	WHERE ServerID = @serverID;
END

/*If all of the above checks fail, give the server a new unique name and update the routing table. This shouldn't exist, but i'm paranoid.*/
ELSE IF OBJECT_ID(@servername) IS NOT NULL AND @idtest IS NOT NULL AND @nametest NOT LIKE '%' + @servername + '%'
BEGIN
	SET @count = 2
	SET @newname = @servername
	SET @oldname = @nametest

		WHILE OBJECT_ID(@newname) IS NOT NULL
	    BEGIN
		    SET @newname = @servername
		    SET @newname = @newname + (CONVERT(VARCHAR,@count))
			SET @count = @count + 1
		END

	EXEC sp_rename @oldname, @newname
	UPDATE tblServerID 
	SET ServerName = @newname
	WHERE ServerID = @serverID;
END



