import sqlite3 as sql

def _incCups(group, teamX, cupsX, teamY, cupsY, cur):
    cur.execute("UPDATE " + group + " SET cups = cups + (?) WHERE team_name = (?)", (cupsX, teamX))
    cur.execute("UPDATE " + group + " SET cups = cups + (?) WHERE team_name = (?)", (cupsY, teamY))

def _incPoints(group, teamX, cupsX, teamY, cupsY, cur):
    points = 3
    if cupsX > cupsY:
        if cupsX < 10:
            points = 2
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (points, teamX))
    elif cupsX < cupsY:
        if cupsY < 10:
            points = 2
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (points, teamY))
    else:
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (1, teamX))
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (1, teamY))

def _calcRank(group, cur):
    # first prio = points than highest number of cups
    cur.execute("SELECT * FROM " + group + " ORDER BY points DESC, cups DESC")
    teamInfo = cur.fetchall()

    for i in range(len(teamInfo)):
        cur.execute("UPDATE " + group + " SET rank = (?) WHERE team_name = (?)", (i + 1, teamInfo[i][0]))

def insertWinnerQF(teamXname, teamYname, teamXresult, teamYresult, xFinalsTable):
    cur, conn = _openDB()
    winnerTeam = teamXname
    if int(teamXresult) < int(teamYresult):
        winnerTeam = teamYname
    cur.execute("UPDATE " + xFinalsTable + " \
                        SET winner = (?)\
                        WHERE team_name1 = (?) AND team_name2 = (?)", (winnerTeam, teamXname, teamYname))
    _closeDB(conn)
    
def _calcGroupWinner(teamInfo):
    groupWinnerFirst = []
    groupWinnerSecond = []

    for groupCounter in range(len(teamInfo)):
        for teamCounter in range(len(teamInfo[1])):
            if teamInfo[groupCounter][teamCounter][3] == 1:
                groupWinnerFirst.append(teamInfo[groupCounter][teamCounter])
            elif teamInfo[groupCounter][teamCounter][3] == 2:
                groupWinnerSecond.append(teamInfo[groupCounter][teamCounter])

    return groupWinnerFirst, groupWinnerSecond

def addEight(teamX, teamY, cupsX, cupsY, xFinalTable):
    cur, conn = _openDB()
    cur.execute("SELECT COUNT(*) FROM " + xFinalTable)
    teamNumber = cur.fetchall()
    # TODO Error Handling
    if int(teamNumber[0][0]) < 8:
        cur.execute("INSERT INTO " + xFinalTable + " (team_name1, team_name2, result_for_team1, result_for_team2, winner) VALUES (?,?,?,?,'x')", (teamX, teamY, cupsX, cupsY))
    _closeDB(conn)

def addQF(teamX, teamY, cupsX, cupsY, xFinalTable):
    cur, conn = _openDB()
    cur.execute("SELECT COUNT(*) FROM " + xFinalTable)
    teamNumber = cur.fetchall()
    # TODO Error Handling
    if int(teamNumber[0][0]) < 4:
        cur.execute("INSERT INTO " + xFinalTable + " (team_name1, team_name2, result_for_team1, result_for_team2, winner) VALUES (?,?,?,?,'x')", (teamX, teamY, cupsX, cupsY))
    _closeDB(conn)

def addSF(teamX, teamY, cupsX, cupsY, xFinalTable):
    cur, conn = _openDB()
    cur.execute("SELECT COUNT(*) FROM " + xFinalTable)
    teamNumber = cur.fetchall()
    # TODO Error Handling
    if int(teamNumber[0][0]) < 2:
        cur.execute("INSERT INTO " + xFinalTable + " (team_name1, team_name2, result_for_team1, result_for_team2, winner) VALUES (?,?,?,?,'x')", (teamX, teamY, cupsX, cupsY))
    _closeDB(conn)

def addFinals(teamX, teamY, cupsX, cupsY, xFinalTable):
    cur, conn = _openDB()
    cur.execute("SELECT COUNT(*) FROM " + xFinalTable)
    teamNumber = cur.fetchall()
    # TODO Error Handling
    if int(teamNumber[0][0]) < 2:
        cur.execute("INSERT INTO " + xFinalTable + " (team_name1, team_name2, result_for_team1, result_for_team2) VALUES (?,?,?,?)", (teamX, teamY, cupsX, cupsY))
    _closeDB(conn)

def updateKOtabelDB(teamX, teamY, cupsX, cupsY, xFinalsTable):
    cur, conn = _openDB()
    cur.execute("UPDATE " + xFinalsTable + " SET result_for_team1 = " + cupsX + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    cur.execute("UPDATE " + xFinalsTable + " SET result_for_team2 = " + cupsY + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    _closeDB(conn)

def catchGroupStage(groupNumber, infoORstage):
    cur, conn = _openDB()
    allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
    allGroupStages = []

    if infoORstage == "groupStage": # catch Group Stage
        for i in range(groupNumber):
            cur.execute("SELECT * FROM " + allGroupNames[i] + "_group_stage")
            allGroupStages.append(cur.fetchall())
        _closeDB(conn)
        return allGroupStages 
    else: # catch Team Info
        for i in range(groupNumber):
            cur.execute("SELECT * FROM " + allGroupNames[i])
            allGroupStages.append(cur.fetchall())
        groupWinnerFirst, groupWinnerSecond = _calcGroupWinner(allGroupStages)
        _closeDB(conn)
        return allGroupStages, groupWinnerFirst, groupWinnerSecond

def catchQF(xFinalsTable):
    cur, conn = _openDB()
    cur.execute("SELECT * FROM " + xFinalsTable)
    quaterFinalsTable = cur.fetchall()
    _closeDB(conn)
    return quaterFinalsTable

def catchWinner(xFinalsTable):
    cur, conn = _openDB()
    cur.execute("SELECT winner FROM " + xFinalsTable)
    winner = cur.fetchall()
    _closeDB(conn)
    return winner

def inputGameResults(group, teamX, teamY, cupsX, cupsY):
    cur, conn = _openDB()
    
    cur.execute("SELECT result_for_team1, result_for_team2 FROM " + group + "_group_stage WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    oldResult = cur.fetchall()
    # delete old result if existing
      # oldResult TeamX        oldResult TeamY
    if oldResult[0][0] != 0 or oldResult[0][1]:            
        deleteInputDB(group, teamX, teamY, oldResult[0][0], oldResult[0][1])

    if int(cupsX) + int(cupsY) != 0:
        cur.execute("UPDATE " + group + "_group_stage SET result_for_team1 = " + cupsX + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
        cur.execute("UPDATE " + group + "_group_stage SET result_for_team2 = " + cupsY + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
        _incPoints(group, teamX, int(cupsX), teamY, int(cupsY), cur)
        _incCups(group, teamX, cupsX, teamY, cupsY, cur)
        _calcRank(group, cur)

    _closeDB(conn)

def deleteInputDB(groupValue, teamXname, teamYname, teamXResult, teamYResult):
    cur, conn = _openDB()
    points = -3

    # set cups = 0 in GroupStage
    cur.execute("UPDATE " + groupValue + "_group_stage SET result_for_team1 = 0 WHERE team_name1 = '" + teamXname + "' AND team_name2 = '" + teamYname + "'")
    cur.execute("UPDATE " + groupValue + "_group_stage SET result_for_team2 = 0 WHERE team_name1 = '" + teamXname + "' AND team_name2 = '" + teamYname + "'")
    if int(teamXResult) ==  int(teamYResult):
        # set cups = 0 in TeamInfo Table
        _incCups(groupValue, teamXname, str(int(teamXResult) * (-1)), teamYname, str(int(teamYResult) * (-1)), cur)
        # set points = 0 in TeamInfo Table
        cur.execute("UPDATE " + groupValue + " SET points = points + (?) WHERE team_name = (?)", (-1, teamXname))
        cur.execute("UPDATE " + groupValue + " SET points = points + (?) WHERE team_name = (?)", (-1, teamYname))
        _closeDB(conn)
        return
    winner = teamXname
    if int(teamXResult) < int(teamYResult):
        if int(teamYResult) < 10:
            points = -2
        # filter winner in this game
        winner = teamYname
        # set Cups AND Points = 0 from the winner in TeamInfo Table
        _incCups(groupValue, teamXname, str(int(teamXResult) * (-1)), teamYname, str(int(teamYResult) * (-1)), cur)
        cur.execute("UPDATE " + groupValue + " SET points = points + (?) WHERE team_name = (?)", (points, winner))
        _closeDB(conn)
        return

    # set Cups AND Points = 0 from the winner in TeamInfo Table
    if int(teamXResult) < 10:
        points = -2
    _incCups(groupValue, teamXname, str(int(teamXResult) * (-1)), teamYname, str(int(teamYResult) * (-1)), cur)
    cur.execute("UPDATE " + groupValue + " SET points = points + (?) WHERE team_name = (?)", (points, teamXname))

    _closeDB(conn)
    return

def _closeDB(conn):
    conn.commit()
    conn.close()

def _openDB():
    conn = sql.connect('beerpong.db')
    cur = conn.cursor()
    return cur, conn
