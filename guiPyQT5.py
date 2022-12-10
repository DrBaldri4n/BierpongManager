import sys
from PyQt5 import QtWidgets, QtGui # test with gui commit
from math import factorial

from updateGame import inputGameResults, catchGroupStage, addQF, catchQF, updateKOtabelDB,\
                       insertWinnerQF, catchWinner, addSF, addFinals

class Header:
    def __init__(self) -> None:
        self.group = QtWidgets.QListWidgetItem("Gruppe")
        self.rank1 = QtWidgets.QListWidgetItem("1. in Gruppe")
        self.rank2 = QtWidgets.QListWidgetItem("2. in Gruppe")
        self.teamX = QtWidgets.QListWidgetItem("Team 1")
        self.teamY = QtWidgets.QListWidgetItem("Team 2")
        self.teamName = QtWidgets.QListWidgetItem("Team Name")
        self.cupsX = QtWidgets.QListWidgetItem("Cup")
        self.cupsY = QtWidgets.QListWidgetItem("Cup")
        self.rank = QtWidgets.QListWidgetItem("Platz")
        self.points = QtWidgets.QListWidgetItem("Punkte")
        pass

class KOWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bierpong Tunier: KO Phase")
        self.setGeometry(0, 0, 1920, 1080)
        self.lable = QtWidgets.QWidget(self)
        self.lable.setStyleSheet("background-image : url(beerpong.png)")
        self.lable.resize(1920, 1080)

        self.groupNumber = 8
        self.teamsPerGroup = 4

        #TODO make this beautifull
        self._allCupColsTeamInfo = []
        self._allCupColsGroupStage = []
        self._allCupColsSF = []
        self._allCupColsQF = []
        self._allCupColsFinals = []

        self._gamePhase = "quater_finals"

        self.uiComponents1()
        self.show()

    def _createTableKO(self, tableGeometry, distanceToTable, tableHeigh, tableID):
        col1 = QtWidgets.QListWidget(self)
        col2 = QtWidgets.QListWidget(self)
        col3 = QtWidgets.QListWidget(self)
        col4 = QtWidgets.QListWidget(self)
        # creating table
        col1.setGeometry(tableGeometry, distanceToTable, 150, tableHeigh)
        tableGeometry += 150
        col2.setGeometry(tableGeometry, distanceToTable, 150, tableHeigh)
        tableGeometry += 150
        col3.setGeometry(tableGeometry, distanceToTable, 50, tableHeigh)
        tableGeometry += 50
        col4.setGeometry(tableGeometry, distanceToTable, 50, tableHeigh)
        # set header
        finalHeader = Header()
        col1.addItem(finalHeader.rank1)
        col2.addItem(finalHeader.rank2)
        col3.addItem(finalHeader.cupsX)
        col4.addItem(finalHeader.cupsY)
        # needed to update later cups in the table
        if tableID == "qf":
            self._addAllCupColsQF(col1, col2, col3, col4)
            tableGeometry += 100
        if tableID == "sf":
            self._addAllCupColsSF(col1, col2, col3, col4)
            tableGeometry += 100
        elif tableID == "final":
            self._addAllCupColsFinals(col1, col2, col3, col4)
            tableGeometry += 325
            
        return tableGeometry

    def _addAllCupColsSF(self, col1, col2, col3QFcups, col4QFcups):
        self._allCupColsSF.append(col1)
        self._allCupColsSF.append(col2)
        self._allCupColsSF.append(col3QFcups)
        self._allCupColsSF.append(col4QFcups)

    def _addAllCupColsQF(self, col1, col2, col3QFcups, col4QFcups):
        self._allCupColsQF.append(col1)
        self._allCupColsQF.append(col2)
        self._allCupColsQF.append(col3QFcups)
        self._allCupColsQF.append(col4QFcups)

    def _addAllCupColsFinals(self, col1, col2, col3Final, col4Final):
        self._allCupColsFinals.append(col1)
        self._allCupColsFinals.append(col2)
        self._allCupColsFinals.append(col3Final)
        self._allCupColsFinals.append(col4Final)


    def fillQFtable(self):
        _, groupWinnerFirst, groupWinnerSecond = catchGroupStage(self.groupNumber, "teamInfo")
        
        rank1VSrank2 = 1
        for groupCounter in range(0, len(self._allCupColsQF), 4):
            for _ in range(2):
                self._allCupColsQF[groupCounter].addItem(groupWinnerFirst[0][0])
                self._allCupColsQF[groupCounter+1].addItem(groupWinnerSecond[rank1VSrank2][0])
                self._allCupColsQF[groupCounter+2].addItem("0")
                self._allCupColsQF[groupCounter+3].addItem("0")

                addQF(groupWinnerFirst[0][0], groupWinnerSecond[rank1VSrank2][0], 0 , 0)
                
                groupWinnerFirst.pop(0)
                if (rank1VSrank2 == 1 or len(groupWinnerSecond) < 2) and len(groupWinnerSecond) > 1:
                    groupWinnerSecond.pop(1)
                    rank1VSrank2 = 0
                elif rank1VSrank2 == 0:
                    groupWinnerSecond.pop(0)
                    rank1VSrank2 = 1

    def fillSFtable(self):
        winnerQF = catchWinner("quater_finals")
        
        for groupCounter in range(0, len(self._allCupColsSF), 4):
            self._allCupColsSF[groupCounter].addItem(winnerQF[0][0])
            self._allCupColsSF[groupCounter+1].addItem(winnerQF[len(winnerQF)-1][0])
            self._allCupColsSF[groupCounter+2].addItem("0")
            self._allCupColsSF[groupCounter+3].addItem("0")

            addSF(winnerQF[0][0], winnerQF[len(winnerQF)-1][0], 0 , 0, "semi_finals")
            
            winnerQF.pop(0)
            winnerQF.pop(len(winnerQF)-1)

    def fillFinaltable(self):
        winnerSF = catchWinner("semi_finals")
        loserSF = catchWinner("quater_finals")
        # filter the loser teams
        for j in range(len(winnerSF)):
            for i in range(len(loserSF)):
                if loserSF[i] == winnerSF[j]:
                    loserSF.pop(i)
                    break
        for i in range(len(loserSF)):
            winnerSF.append(loserSF[i]) 
        # add the Teams in the Table
        for i in range(0, len(self._allCupColsFinals), 4):
            self._allCupColsFinals[i].addItem(winnerSF[len(winnerSF)-2][0]) # losing teams are at the end of the winnerSF[list]
            self._allCupColsFinals[i+1].addItem(winnerSF[len(winnerSF)-1][0])
            self._allCupColsFinals[i+2].addItem("0")
            self._allCupColsFinals[i+3].addItem("0")

            addSF(winnerSF[len(winnerSF)-2][0], winnerSF[len(winnerSF)-1][0], 0 , 0, "semi_finals")
            addFinals(winnerSF[len(winnerSF)-2][0], winnerSF[len(winnerSF)-1][0], 0 , 0, "finals")
            
            winnerSF.pop(len(winnerSF)-1)
            winnerSF.pop(len(winnerSF)-1)

    def updateKOtable(self, _xFinalTable):
        if _xFinalTable == "quater_finals":
            # clear cup columns
            for _ in range(2):
                for gameCounter in range(2):
                        QtWidgets.QListWidget.takeItem(self._allCupColsQF[gameCounter + 2], 1)
                        QtWidgets.QListWidget.takeItem(self._allCupColsQF[gameCounter + 6], 1)
            # insert new number of cups in columns
            qfTable = catchQF(self._gamePhase)
            for i in range(2):
                self._allCupColsQF[2].addItem(str(qfTable[i][2]))
                self._allCupColsQF[3].addItem(str(qfTable[i][3]))
            for i in range(2, 4):
                self._allCupColsQF[6].addItem(str(qfTable[i][2]))
                self._allCupColsQF[7].addItem(str(qfTable[i][3]))
        elif _xFinalTable == "semi_finals":
            # clear cup columns
            for gameCounter in range(2):
                QtWidgets.QListWidget.takeItem(self._allCupColsSF[gameCounter + 2], 1)
                QtWidgets.QListWidget.takeItem(self._allCupColsSF[gameCounter + 6], 1)
            # insert new number of cups in columns
            sfTable = catchQF(_xFinalTable)
            self._allCupColsSF[2].addItem(str(sfTable[0][2]))
            self._allCupColsSF[3].addItem(str(sfTable[0][3]))
            self._allCupColsSF[6].addItem(str(sfTable[1][2]))
            self._allCupColsSF[7].addItem(str(sfTable[1][3]))
        elif _xFinalTable == "finals":
            # clear cups columns
            for gameCounter in range(2):
                QtWidgets.QListWidget.takeItem(self._allCupColsFinals[gameCounter + 2], 1)
                QtWidgets.QListWidget.takeItem(self._allCupColsFinals[gameCounter + 6], 1)
            # insert new number of cups in columns
            finalTable = catchQF(_xFinalTable)
            self._allCupColsFinals[2].addItem(str(finalTable[0][2]))
            self._allCupColsFinals[3].addItem(str(finalTable[0][3]))
            self._allCupColsFinals[6].addItem(str(finalTable[1][2]))
            self._allCupColsFinals[7].addItem(str(finalTable[1][3]))

    def inputResultbutton(self):
        teamXnameValue = self.teamXname.text()
        teamYnameValue = self.teamYname.text()
        team1ResultValue = self.teamXresult.text()
        team2ResultValue = self.teamYresult.text()

        if self._gamePhase == "quater_finals":
            # only for tests!!!!
            # teamX = ["Team4", "Team9", "Team14", "Team19"]
            # teamY = ["Team8", "Team3", "Team18", "Team13"]
            # for i in range(4):
            #     updateQF(teamX[i], teamY[i], "2", "8", self.gamePhase)
            #     insertWinnerQF(teamX[i], teamY[i], "2", "8" , self.gamePhase)
            insertWinnerQF(teamXnameValue, teamYnameValue, team1ResultValue, team2ResultValue, self._gamePhase)
            updateKOtabelDB(teamXnameValue, teamYnameValue, team1ResultValue, team2ResultValue, self._gamePhase)
            self.updateKOtable("quater_finals")    
        elif self._gamePhase == "semi_finals":
            updateKOtabelDB(teamXnameValue, teamYnameValue, team1ResultValue, team2ResultValue, self._gamePhase)
            insertWinnerQF(teamXnameValue, teamYnameValue, team1ResultValue, team2ResultValue, self._gamePhase)
            self.updateKOtable(self._gamePhase)
        elif self._gamePhase == "finals":
            updateKOtabelDB(teamXnameValue, teamYnameValue, team1ResultValue, team2ResultValue, self._gamePhase)
            self.updateKOtable(self._gamePhase)

        self.teamXname.setText("")
        self.teamYname.setText("")
        self.teamXresult.setText("")
        self.teamYresult.setText("")

    def _startSFbutton(self):
        self.fillSFtable()
        # to avoid table overflowing
        self.resultQF.hide()
        # nicer user interface  
        self._gamePhase = "semi_finals"
        # in the case of a program crash
        self.updateKOtable("semi_finals")

    def _startFinalbutton(self):
        self.fillFinaltable()
        # to avoid table overflowing
        self.resultSF.hide()
        # nicer user interface  
        self._gamePhase = "finals"
        # in the case of a program crash
        self.updateKOtable("finals")

    def _userInput(self):
        # Headers
        teamXnameLable = QtWidgets.QLabel("Team1", self)
        teamXnameLable.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        teamXnameLable.setGeometry(175, 828, 150, 23)
        teamYnameLable = QtWidgets.QLabel("Team2", self)
        teamYnameLable.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        teamYnameLable.setGeometry(325, 828, 150, 23)
        teamXresultLable = QtWidgets.QLabel("Cups", self)
        teamXresultLable.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        teamXresultLable.setGeometry(435, 828, 50, 23)
        teamYresultLable = QtWidgets.QLabel("Cups", self)
        teamYresultLable.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        teamYresultLable.setGeometry(485, 828, 50, 23)

        self.groupLable.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        # userInput
        self.teamXname = QtWidgets.QLineEdit(self)
        self.teamXname.setGeometry(130, 850, 150, 23)
        self.teamYname = QtWidgets.QLineEdit(self)
        self.teamYname.setGeometry(280, 850, 150, 23)
        self.teamXresult = QtWidgets.QLineEdit(self)
        self.teamXresult.setGeometry(430, 850, 50, 23)
        self.teamYresult = QtWidgets.QLineEdit(self)
        self.teamYresult.setGeometry(480, 850, 50, 23)
        # buttons
        self.resultGroup = QtWidgets.QPushButton('hinzufügen', self)
        self.resultGroup.setGeometry(530, 850, 150, 23)
        self.resultGroup.clicked.connect(self.inputResultbutton)
        self.resultSF = QtWidgets.QPushButton('start Finale', self)
        self.resultSF.setGeometry(530, 872, 150, 23)
        self.resultSF.clicked.connect(self._startFinalbutton)
        self.resultQF = QtWidgets.QPushButton('start Halb Finale', self)
        self.resultQF.setGeometry(530, 872, 150, 23)
        self.resultQF.clicked.connect(self._startSFbutton)

    def uiComponents1(self):
        tableGeometry = 75
        posYaxis = 100
        numberOfGames = factorial(self.teamsPerGroup - 1)

        # Create Quater Final table
        if self.groupNumber >= 4:
            tableGeometry = 500
            distanceToGroupStage = ((posYaxis + ((self.teamsPerGroup) * 23)) + (50 + numberOfGames * 23))
            tableHeigh = 3 * 23
            self.groupLable = QtWidgets.QLabel("Viertelfinale", self)
            self.groupLable.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
            self.groupLable.setGeometry(tableGeometry + 355, distanceToGroupStage - 35, 150, 23)
            for _ in range(2):
                tableGeometry = self._createTableKO(tableGeometry, distanceToGroupStage, tableHeigh, "qf")

        self.fillQFtable()
        # Create Semi Final table
        if self.groupNumber >= 2:
            tableGeometry = 500
            tableHeigh = 2 * 23
            distanceToQFStage = distanceToGroupStage + tableHeigh + 95
            self.groupLable = QtWidgets.QLabel("Halbfinale", self)
            self.groupLable.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
            self.groupLable.setGeometry(tableGeometry + 365, distanceToQFStage - 35, 150, 23)
            for _ in range(2):
                tableGeometry = self._createTableKO(tableGeometry, distanceToQFStage, tableHeigh, "sf")
        # Create Final table
        tableGeometry = 50
        distanceToSF = distanceToQFStage + tableHeigh + 75
        tableHeigh = 2 * 23
        self.groupLable = QtWidgets.QLabel("Finale", self)
        self.groupLable.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
        self.groupLable.setGeometry(tableGeometry + 835, distanceToSF - 35, 150, 23)
        for _ in range(2):
            tableGeometry = self._createTableKO(tableGeometry, distanceToSF, tableHeigh, "final")

        self._userInput()

    

class GroupStageWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bierpong Tunier")
        self.setGeometry(0, 0, 1920, 1080)
        self.lable = QtWidgets.QWidget(self)
        self.lable.setStyleSheet("background-image : url(beerpong.png)")
        self.lable.resize(1920, 1080)

        # user can change this Variables
        self.groupNumber = 8
        self.teamsPerGroup = 4

        # #TODO make this beautifull
        self._allCupColsTeamInfo = []
        self._allCupColsGroupStage = []
        self._allCupColsSF = []
        self._allCupColsQF = []
        self._allCupColsFinals = []
        # needed to make the buttons disappear
        self._gamePhase = "group_phase"
    
        self.uiComponents()
        self.show()

    def showNewWindow(self, checked):
        if self.w is None:
            self.w = KOWindow()
        self.w.show()

    def _groupOverview(self, tableGeometry, yAxis, teamInfo):
        rank = QtWidgets.QListWidget(self)
        teamName = QtWidgets.QListWidget(self)
        cups = QtWidgets.QListWidget(self)
        points = QtWidgets.QListWidget(self)
        # creating table
        tableHigh = self.teamsPerGroup * 26
        rank.setGeometry(tableGeometry, yAxis, 50, tableHigh)
        tableGeometry += 50
        teamName.setGeometry(tableGeometry, yAxis, 150, tableHigh)
        tableGeometry += 150
        cups.setGeometry(tableGeometry, yAxis, 50, tableHigh)
        tableGeometry += 50
        points.setGeometry(tableGeometry, yAxis, 60, tableHigh)
        tableGeometry += 205
        # set headers
        groupHeader = Header()
        rank.addItem(groupHeader.rank)
        teamName.addItem(groupHeader.teamName)
        cups.addItem(groupHeader.cupsX)
        points.addItem(groupHeader.points)
        # fill columns
        for i in range(self.teamsPerGroup):
            rank.addItem(str(teamInfo[0][i][3]))
            teamName.addItem(teamInfo[0][i][0])
            cups.addItem(str(teamInfo[0][i][1]))
            points.addItem(str(teamInfo[0][i][2]))
        teamInfo.pop(0)
        # needed to update Rank, Cups and Points
        self._allCupColsTeamInfo.append(rank)
        self._allCupColsTeamInfo.append(cups)
        self._allCupColsTeamInfo.append(points)
        return tableGeometry

    def creatColTime(self, tableGeometry, distanceToGroupOverview, tableHigh, numberOfGames):
        col0time = QtWidgets.QListWidget(self)
        # creating table
        col0time.setGeometry(tableGeometry - 47, distanceToGroupOverview, 47, tableHigh)
        # fill time col
        timeSlots = ["", "18:00", "18:15", "18:30", "18:45", "19:00", "19:15"]
        for i in range(numberOfGames + 1):
            col0time.addItem(timeSlots[i])

    def _createGroupTable(self, tableGeometry, infoGroupStages, numberOfGames, posYaxis):
        col1TeamNameX = QtWidgets.QListWidget(self)
        col2TeamNameY = QtWidgets.QListWidget(self)
        col3GroupStageCups = QtWidgets.QListWidget(self)
        col4GroupStageCups = QtWidgets.QListWidget(self)
        # creating table
        distanceToGroupOverview = posYaxis + ((self.teamsPerGroup) * 23) # befor = 150 + ((self.teamsPerGroup) * 23)
        tableHigh = (numberOfGames * 23)
        # create static TimeSlots table (not in the end version!!!)
        self.creatColTime(tableGeometry, distanceToGroupOverview, tableHigh, numberOfGames)

        col1TeamNameX.setGeometry(tableGeometry, distanceToGroupOverview, 150, tableHigh)
        tableGeometry += 150
        col2TeamNameY.setGeometry(tableGeometry, distanceToGroupOverview, 150, tableHigh)
        tableGeometry += 150
        col3GroupStageCups.setGeometry(tableGeometry, distanceToGroupOverview, 35, tableHigh)
        tableGeometry += 35
        col4GroupStageCups.setGeometry(tableGeometry, distanceToGroupOverview, 35, tableHigh)
        tableGeometry += 110
        # set headers
        groupStageHeader = Header()
        col1TeamNameX.addItem(groupStageHeader.teamX)
        col2TeamNameY.addItem(groupStageHeader.teamY)
        col3GroupStageCups.addItem(groupStageHeader.cupsX)
        col4GroupStageCups.addItem(groupStageHeader.cupsY)
        # fill columns 
        for i in range(numberOfGames):
            col1TeamNameX.addItem(infoGroupStages[0][i][0])
            col2TeamNameY.addItem(infoGroupStages[0][i][1])
            col3GroupStageCups.addItem(str(infoGroupStages[0][i][2]))
            col4GroupStageCups.addItem(str(infoGroupStages[0][i][3]))            
        infoGroupStages.pop(0)
        # needed to update cups in the table
        self._allCupColsGroupStage.append(col3GroupStageCups)
        self._allCupColsGroupStage.append(col4GroupStageCups)
        return tableGeometry

    def updateTeamInfoTables(self):
        numberOfGames = factorial(self.teamsPerGroup - 1)
        # clear cup columns Team Info
        for groupCounter in range(len(self._allCupColsTeamInfo)):
            for gameCounter in range(self.teamsPerGroup):
                QtWidgets.QListWidget.takeItem(self._allCupColsTeamInfo[groupCounter], 1)
        # fill Cup columns Team Info
        teamInfo, _, _ = catchGroupStage(self.groupNumber, "teamInfo")
        for groupCounter in range(0, len(self._allCupColsTeamInfo), 3):
            for gameCounter in range(self.teamsPerGroup):
                self._allCupColsTeamInfo[groupCounter].addItem(str(teamInfo[0][gameCounter][3]))
                self._allCupColsTeamInfo[groupCounter+1].addItem(str(teamInfo[0][gameCounter][1]))
                self._allCupColsTeamInfo[groupCounter+2].addItem(str(teamInfo[0][gameCounter][2]))
            teamInfo.pop(0)

        # clear cup columns Group Stage
        for groupCounter in range(len(self._allCupColsGroupStage)):
            for gameCounter in range(numberOfGames):
                QtWidgets.QListWidget.takeItem(self._allCupColsGroupStage[groupCounter], 1)
        # fill cup columns Group Stage
        allGroupStages = catchGroupStage(self.groupNumber, "groupStage")
        for groupCounter in range(0, len(self._allCupColsGroupStage), 2):
            for gameCounter in range(numberOfGames):
                self._allCupColsGroupStage[groupCounter].addItem(str(allGroupStages[0][gameCounter][2]))
                self._allCupColsGroupStage[groupCounter+1].addItem(str(allGroupStages[0][gameCounter][3]))
            allGroupStages.pop(0)

    def _userInput(self):
        # Headers
        self.groupLable = QtWidgets.QLabel("Gruppe", self)
        self.groupLable.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
        self.groupLable.setGeometry(60, 828, 70, 23)
        teamXnameLable = QtWidgets.QLabel("Team1", self)
        teamXnameLable.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        teamXnameLable.setGeometry(175, 828, 150, 23)
        teamYnameLable = QtWidgets.QLabel("Team2", self)
        teamYnameLable.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        teamYnameLable.setGeometry(325, 828, 150, 23)
        teamXresultLable = QtWidgets.QLabel("Cups", self)
        teamXresultLable.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        teamXresultLable.setGeometry(435, 828, 50, 23)
        teamYresultLable = QtWidgets.QLabel("Cups", self)
        teamYresultLable.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        teamYresultLable.setGeometry(485, 828, 50, 23)

        self.groupLable.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        # userInput
        self.group = QtWidgets.QComboBox(self)
        self.group.setGeometry(50, 850, 80, 23)
        groupChoice = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
        self.group.addItems(groupChoice)
        self.teamXname = QtWidgets.QLineEdit(self)
        self.teamXname.setGeometry(130, 850, 150, 23)
        self.teamYname = QtWidgets.QLineEdit(self)
        self.teamYname.setGeometry(280, 850, 150, 23)
        self.teamXresult = QtWidgets.QLineEdit(self)
        self.teamXresult.setGeometry(430, 850, 50, 23)
        self.teamYresult = QtWidgets.QLineEdit(self)
        self.teamYresult.setGeometry(480, 850, 50, 23)
        # buttons
        self.resultGroup = QtWidgets.QPushButton('hinzufügen', self)
        self.resultGroup.setGeometry(530, 850, 150, 23)
        self.resultGroup.clicked.connect(self.inputResultbutton)
        self.resultGroup = QtWidgets.QPushButton('start Viertel Finale', self)
        self.resultGroup.setGeometry(530, 872, 150, 23)
        self.resultGroup.clicked.connect(self._startQFbutton)
        self.w = None
        self.resultGroup.clicked.connect(self.showNewWindow)

    def inputResultbutton(self):
        groupValue = self.group.currentText()
        teamXnameValue = self.teamXname.text()
        teamYnameValue = self.teamYname.text()
        team1ResultValue = self.teamXresult.text()
        team2ResultValue = self.teamYresult.text()

        if self._gamePhase == "group_phase":
            numberOfGames = factorial(self.teamsPerGroup - 1)
            # only for tests!!!
            # allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"] # should change variable 
            # allGroupStages = catchGroupStage(self.groupNumber, "groupStage")
            # for idx, group in enumerate(allGroupNames):
            #     for i in range(numberOfGames):
            #         inputGameResults(group, allGroupStages[idx][i][0], allGroupStages[idx][i][1], "10", "8")

            inputGameResults(groupValue, teamXnameValue, teamYnameValue, team1ResultValue, team2ResultValue)
            self.updateTeamInfoTables()

        self.teamXname.setText("")
        self.teamYname.setText("")
        self.teamXresult.setText("")
        self.teamYresult.setText("")

    def _startQFbutton(self):
        self.fillQFtable()
        # to avoid table overflowing
        self.resultGroup.hide()
        self.group.hide()
        # nicer user interface
        self.groupLable.hide()
        self._gamePhase = "quater_finals"
        # in the case of a program crash
        self.updateKOtable("quater_finals") 

        # start new Window for KO stage
        self.w = None
        self.showNewWindow()
        
    def setGroupOverviewInTable(self, allGroupNames, teamInfo, counter, yAxis, tableGeometry):
        # set table Header
        self.groupLable = QtWidgets.QLabel(allGroupNames[counter], self)
        self.groupLable.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        self.groupLable.setGeometry(tableGeometry + 110, yAxis - 25, 100, 23)
        #  set Tabel
        tableGeometry = self._groupOverview(tableGeometry, yAxis, teamInfo)
        return tableGeometry

    def setGroupStageInTable(self, allGroupNames, infoGroupStages, numberOfGames, tableGeometry, counter, posYaxis):
        self.groupLable = QtWidgets.QLabel(allGroupNames[counter], self)
        self.groupLable.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        self.groupLable.setGeometry(tableGeometry + 160, posYaxis, 100, 23)
        tableGeometry = self._createGroupTable(tableGeometry + 15, infoGroupStages, numberOfGames, posYaxis)
        return tableGeometry

    def uiComponents(self):
        allGroupNames = ["Gruppe A", "Gruppe B", "Gruppe C", "Gruppe D", "Group E", "Group F", "Group G", "Group H"] # should change variable
        tableGeometry = 75
        posYaxis = 100
        numberOfGames = factorial(self.teamsPerGroup - 1)
        # Create Group Overview
        teamInfo, _, _ = catchGroupStage(self.groupNumber, "teamInfo")
        for counter in range(self.groupNumber):
            if self.groupNumber > 4 and counter == (self.groupNumber // 2):
                tableGeometry = 75
                posYaxis += self.teamsPerGroup * 26 + 50
            tableGeometry = self.setGroupOverviewInTable(allGroupNames, teamInfo, counter, posYaxis, tableGeometry) # TODO change yAxis to posYaxis
        tableGeometry = 60
        posYaxis += 50
        # Create Group Stage table
        infoGroupStages = catchGroupStage(self.groupNumber, "groupStage")
        for counter in range(self.groupNumber):
            if self.groupNumber > 4 and counter == (self.groupNumber // 2):
                tableGeometry = 60
                posYaxis += numberOfGames * 23 + 50
            tableGeometry = self.setGroupStageInTable(allGroupNames, infoGroupStages, numberOfGames, tableGeometry, counter, posYaxis)

        self._userInput()


# create pyqt5 app
App = QtWidgets.QApplication(sys.argv)
# create the instance of our Window
window = GroupStageWindow()
# start the app
sys.exit(App.exec())
