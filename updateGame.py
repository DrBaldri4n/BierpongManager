import sqlite3

def _incCups(group, teamX, cupsX, teamY, cupsY, cur):
    cur.execute("UPDATE " + group + " SET cups = cups + (?) WHERE team_name = (?)", (cupsX, teamX))
    cur.execute("UPDATE " + group + " SET cups = cups + (?) WHERE team_name = (?)", (cupsY, teamY))

def _incPoints(group, teamX, cupsX, teamY, cupsY, cur):
    if cupsX > cupsY:
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (3, teamX))
    elif cupsX < cupsY:
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (3, teamY))
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

def _printGroupStage(groupNumber, allGroupNames):
    for i in range(groupNumber):
        cur.execute("SELECT * FROM " + allGroupNames[i] + "_group_stage")
        print(allGroupNames[i], cur.fetchall())

def inputGameResults(group, teamX, teamY, cupsX, cupsY):
    cur, conn = _openDB()

    cur.execute("UPDATE " + group + "_group_stage SET result_for_team1 = " + cupsX + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    cur.execute("UPDATE " + group + "_group_stage SET result_for_team2 = " + cupsY + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
    _incPoints(group, teamX, int(cupsX), teamY, int(cupsY), cur)
    _incCups(group, teamX, cupsX, teamY, cupsY, cur)
    _calcRank(group, cur)

    _closeDB(conn)

def _closeDB(conn):
    conn.commit()
    conn.close()

def _openDB():
    conn = sqlite3.connect('beerpong.db')
    cur = conn.cursor()
    return cur, conn
