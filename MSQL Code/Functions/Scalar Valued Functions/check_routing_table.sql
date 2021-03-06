USE [db_discord]
GO
/****** Object:  UserDefinedFunction [dbo].[check_routing_table]    Script Date: 10/29/2018 11:13:23 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER FUNCTION [dbo].[check_routing_table] (@serverID VARCHAR(100), @servername VARCHAR(100))
RETURNS BIT
AS
BEGIN

DECLARE @idtest VARCHAR(100), @nametest VARCHAR(100);
DECLARE @result BIT;
SELECT @idtest = (SELECT ServerID FROM tblServerID WITH (NOLOCK) WHERE ServerID = @serverID);
SELECT @nametest = (SELECT ServerName FROM tblServerID WITH (NOLOCK) WHERE ServerID = @serverID);

	IF ((@idtest = @serverID) AND (@nametest LIKE '%' + @servername + '%'))
	BEGIN
		SET @result = 1;
	END

	ELSE
	BEGIN
		SET @result = 0;
    END

RETURN @result
END