import sqlite3 as sql

class Databank:
    def _incCups(self, group, teamX, cupsX, teamY, cupsY, cur):
        cur.execute("UPDATE " + group + " SET cups = cups + (?) WHERE team_name = (?)", (cupsX, teamX))
        cur.execute("UPDATE " + group + " SET cups = cups + (?) WHERE team_name = (?)", (cupsY, teamY))

    def _incPoints(self, group, teamX, cupsX, teamY, cupsY, cur):
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

    def _calcRank(self, group, cur):
        # first prio = points than highest number of cups
        cur.execute("SELECT * FROM " + group + " ORDER BY points DESC, cups DESC")
        teamInfo = cur.fetchall()

        for i in range(len(teamInfo)):
            cur.execute("UPDATE " + group + " SET rank = (?) WHERE team_name = (?)", (i + 1, teamInfo[i][0]))

    def insertWinnerQF(self, teamXname, teamYname, teamXresult, teamYresult, xFinalsTable):
        db = Databank()
        cur, conn = db._openDB()
        winnerTeam = teamXname
        if int(teamXresult) < int(teamYresult):
            winnerTeam = teamYname
        cur.execute("UPDATE " + xFinalsTable + " \
                            SET winner = (?)\
                            WHERE team_name1 = (?) AND team_name2 = (?)", (winnerTeam, teamXname, teamYname))
        db._closeDB(conn)
        
    def _calcGroupWinner(self, teamInfo):
        groupWinnerFirst = []
        groupWinnerSecond = []

        for groupCounter in range(len(teamInfo)):
            for teamCounter in range(len(teamInfo[1])):
                if teamInfo[groupCounter][teamCounter][3] == 1:
                    groupWinnerFirst.append(teamInfo[groupCounter][teamCounter])
                elif teamInfo[groupCounter][teamCounter][3] == 2:
                    groupWinnerSecond.append(teamInfo[groupCounter][teamCounter])

        return groupWinnerFirst, groupWinnerSecond

    def addEight(self, teamX, teamY, cupsX, cupsY, xFinalTable):
        db = Databank()
        cur, conn = db._openDB()
        cur.execute("SELECT COUNT(*) FROM " + xFinalTable)
        teamNumber = cur.fetchall()
        # TODO Error Handling
        if int(teamNumber[0][0]) < 8:
            cur.execute("INSERT INTO " + xFinalTable + " (team_name1, team_name2, result_for_team1, result_for_team2, winner) VALUES (?,?,?,?,'x')", (teamX, teamY, cupsX, cupsY))
        db._closeDB(conn)

    def addQF(self, teamX, teamY, cupsX, cupsY, xFinalTable):
        db = Databank()
        cur, conn = db._openDB()
        cur.execute("SELECT COUNT(*) FROM " + xFinalTable)
        teamNumber = cur.fetchall()
        # TODO Error Handling
        if int(teamNumber[0][0]) < 4:
            cur.execute("INSERT INTO " + xFinalTable + " (team_name1, team_name2, result_for_team1, result_for_team2, winner) VALUES (?,?,?,?,'x')", (teamX, teamY, cupsX, cupsY))
        db._closeDB(conn)

    def addSF(self, teamX, teamY, cupsX, cupsY, xFinalTable):
        db = Databank()
        cur, conn = db._openDB()
        cur.execute("SELECT COUNT(*) FROM " + xFinalTable)
        teamNumber = cur.fetchall()
        # TODO Error Handling
        if int(teamNumber[0][0]) < 2:
            cur.execute("INSERT INTO " + xFinalTable + " (team_name1, team_name2, result_for_team1, result_for_team2, winner) VALUES (?,?,?,?,'x')", (teamX, teamY, cupsX, cupsY))
        db._closeDB(conn)

    def addFinals(self, teamX, teamY, cupsX, cupsY, xFinalTable):
        db = Databank()
        cur, conn = db._openDB()
        cur.execute("SELECT COUNT(*) FROM " + xFinalTable)
        teamNumber = cur.fetchall()
        # TODO Error Handling
        if int(teamNumber[0][0]) < 2:
            cur.execute("INSERT INTO " + xFinalTable + " (team_name1, team_name2, result_for_team1, result_for_team2) VALUES (?,?,?,?)", (teamX, teamY, cupsX, cupsY))
        db._closeDB(conn)

    def updateKOtabelDB(self, teamX, teamY, cupsX, cupsY, xFinalsTable, idx):
        db = Databank()
        cur, conn = db._openDB()
        cur.execute("SELECT * FROM " + xFinalsTable)
        oldData = cur.fetchall()
        cur.execute("UPDATE '" + xFinalsTable + "' SET team_name1 = '" + teamX + "', team_name2 = '" + teamY + "' WHERE team_name1 = '" + oldData[idx][0] + "' AND team_name2 = '" + oldData[idx][1] + "'")
        cur.execute("UPDATE " + xFinalsTable + " SET result_for_team1 = " + cupsX + ", result_for_team2 = " + cupsY + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
        cur.execute("SELECT * FROM " + xFinalsTable)
        newData = cur.fetchall()
        db._closeDB(conn)

    def updateGameResult(self, teamX, teamY, cupsX, cupsY, xFinalsTable):
        db = Databank()
        cur, conn = db._openDB()
        cur.execute("SELECT * FROM " + xFinalsTable)
        cur.execute("UPDATE " + xFinalsTable + " SET result_for_team1 = " + cupsX + ", result_for_team2 = " + cupsY + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
        
        db._closeDB(conn)

    def catchGroupStage(self, groupNumber, infoORstage):
        db = Databank()
        cur, conn = db._openDB()
        allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
        allGroupStages = []

        if infoORstage == "groupStage": # catch Group Stage
            for i in range(groupNumber):
                cur.execute("SELECT * FROM " + allGroupNames[i] + "_group_stage")
                allGroupStages.append(cur.fetchall())
            db._closeDB(conn)
            return allGroupStages 
        else: # catch Team Info
            for i in range(groupNumber):
                cur.execute("SELECT * FROM " + allGroupNames[i])
                allGroupStages.append(cur.fetchall())
            groupWinnerFirst, groupWinnerSecond = db._calcGroupWinner(allGroupStages)
            db._closeDB(conn)
            return allGroupStages, groupWinnerFirst, groupWinnerSecond

    def catchQF(self, xFinalsTable):
        db = Databank()
        cur, conn = db._openDB()
        cur.execute("SELECT * FROM " + xFinalsTable)
        x = cur.fetchall()
        db._closeDB(conn)
        return x

    def catchWinner(self, xFinalsTable):
        db = Databank()
        cur, conn = db._openDB()
        cur.execute("SELECT winner FROM " + xFinalsTable)
        winner = cur.fetchall()
        db._closeDB(conn)
        return winner

    def inputGameResults(self, group, teamX, teamY, cupsX, cupsY):
        db = Databank()
        cur, conn = db._openDB()
        
        cur.execute("SELECT result_for_team1, result_for_team2 FROM " + group + "_group_stage WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
        oldResult = cur.fetchall()
        # delete old result if existing
        # oldResult TeamX        oldResult TeamY
        if oldResult[0][0] != 0 or oldResult[0][1]:            
            db.deleteInputDB(group, teamX, teamY, oldResult[0][0], oldResult[0][1])

        if int(cupsX) + int(cupsY) != 0:
            cur.execute("UPDATE " + group + "_group_stage SET result_for_team1 = " + cupsX + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
            cur.execute("UPDATE " + group + "_group_stage SET result_for_team2 = " + cupsY + " WHERE team_name1 = '" + teamX + "' AND team_name2 = '" + teamY + "'")
            db._incPoints(group, teamX, int(cupsX), teamY, int(cupsY), cur)
            db._incCups(group, teamX, cupsX, teamY, cupsY, cur)
            db._calcRank(group, cur)

        db._closeDB(conn)

    def deleteInputDB(self, groupValue, teamXname, teamYname, teamXResult, teamYResult):
        db = Databank()
        cur, conn = db._openDB()
        points = -3

        # set cups = 0 in GroupStage
        cur.execute("UPDATE " + groupValue + "_group_stage SET result_for_team1 = 0 WHERE team_name1 = '" + teamXname + "' AND team_name2 = '" + teamYname + "'")
        cur.execute("UPDATE " + groupValue + "_group_stage SET result_for_team2 = 0 WHERE team_name1 = '" + teamXname + "' AND team_name2 = '" + teamYname + "'")
        if int(teamXResult) ==  int(teamYResult):
            # set cups = 0 in TeamInfo Table
            db._incCups(groupValue, teamXname, str(int(teamXResult) * (-1)), teamYname, str(int(teamYResult) * (-1)), cur)
            # set points = 0 in TeamInfo Table
            cur.execute("UPDATE " + groupValue + " SET points = points + (?) WHERE team_name = (?)", (-1, teamXname))
            cur.execute("UPDATE " + groupValue + " SET points = points + (?) WHERE team_name = (?)", (-1, teamYname))
            db._closeDB(conn)
            return
        winner = teamXname
        if int(teamXResult) < int(teamYResult):
            if int(teamYResult) < 10:
                points = -2
            # filter winner in this game
            winner = teamYname
            # set Cups AND Points = 0 from the winner in TeamInfo Table
            db._incCups(groupValue, teamXname, str(int(teamXResult) * (-1)), teamYname, str(int(teamYResult) * (-1)), cur)
            cur.execute("UPDATE " + groupValue + " SET points = points + (?) WHERE team_name = (?)", (points, winner))
            db._closeDB(conn)
            return

        # set Cups AND Points = 0 from the winner in TeamInfo Table
        if int(teamXResult) < 10:
            points = -2
        db._incCups(groupValue, teamXname, str(int(teamXResult) * (-1)), teamYname, str(int(teamYResult) * (-1)), cur)
        cur.execute("UPDATE " + groupValue + " SET points = points + (?) WHERE team_name = (?)", (points, teamXname))

        db._closeDB(conn)
        return

    def _closeDB(self, conn):
        conn.commit()
        conn.close()

    def _openDB(self):
        conn = sql.connect('beerpong.db')
        cur = conn.cursor()
        return cur, conn
