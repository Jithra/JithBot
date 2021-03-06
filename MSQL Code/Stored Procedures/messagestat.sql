USE [db_discord]
GO
/****** Object:  StoredProcedure [dbo].[messagestat]    Script Date: 10/29/2018 11:11:24 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO
ALTER PROC [dbo].[messagestat] @word VARCHAR(100), @serverid VARCHAR(100)
AS 
BEGIN
SET NOCOUNT ON
SET QUOTED_IDENTIFIER OFF
IF OBJECT_ID('tempdb..#jbdev') IS NOT NULL DROP TABLE tempdb..#jbdev
CREATE TABLE #jbdev
(
	UserName VARCHAR(100),
	WordCount INT
)

IF OBJECT_ID('tempdb..#wordcount') IS NOT NULL DROP TABLE tempdb..#wordcount
CREATE TABLE #wordcount
(
	UserName VARCHAR(100),
	MessageCount INT
)
EXECUTE('
INSERT INTO #jbdev
SELECT tm.[User Name], tm.[Fuck Count]
FROM(
	SELECT UserName AS ''User Name'', COUNT(UserMessage) AS ''Fuck Count''
	FROM tblAggregateDiscordLogs(NOLOCK)
	WHERE UserMessage LIKE ''%' + @word + '%''
	AND ServerID = ''' + @serverid + '''
	GROUP BY UserName
)tm

INSERT INTO #wordcount
SELECT tm2.[User Name], tm2.[Word Count]
FROM(
	SELECT UserName AS ''User Name'', COUNT(UserMessage) AS ''Word Count''
	FROM tblAggregateDiscordLogs(NOLOCK)
	WHERE ServerID = ''' + @serverid + '''
	GROUP BY UserName
) tm2


SELECT MAX(j.UserName) AS ''UserName'', MAX(MessageCount) AS ''Message Count'', MAX(WordCount) AS ''' + @word + ' count'', CONVERT(VARCHAR,ROUND(CONVERT(FLOAT,MAX(WordCount)) / CONVERT(FLOAT,MAX(MessageCount)) * 100, 2, 1)) + ''%'' AS ''' + @word + ' Percentage''
FROM #jbdev j (NOLOCK)
INNER JOIN #wordcount w (NOLOCK) ON j.UserName = w.UserName
GROUP BY w.UserName
ORDER BY MAX(WordCount) DESC');
END
