#import python lib
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from math import factorial

#import own functions
from updateGame import inputGameResults, catchGroupStage, catchTeamInfo, addQuaterFinals, catchQF, updateQF

class Header:
    def __init__(self) -> None:
        self.group = QListWidgetItem("Gruppe")
        self.rank1 = QListWidgetItem("1. in Gruppe")
        self.rank2 = QListWidgetItem("2. in Gruppe")
        self.teamX = QListWidgetItem("Team 1")
        self.teamY = QListWidgetItem("Team 2")
        self.TeamName = QListWidgetItem("Team Name")
        self.cupsX = QListWidgetItem("Cups")
        self.cupsY = QListWidgetItem("Cups")
        self.rank = QListWidgetItem("Platz")
        self.points = QListWidgetItem("Punkte")
        pass

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bierpong Tunier")
        self.setGeometry(0, 0, 2000, 800)

        # user can change this Variables
        self.groupNumber = 4
        self.teamsPerGroup = 4

        #TODO make this beautifull
        self.allCupColsTeamInfo = []
        self.allCupColsGroupStage = []
        self.allCupColsSF = []
        self.allCupColsQF = []
        self.allCupColsFinals = []
        
        self.UiComponents()

        self.show()

    def _groupOverview(self, tableGeometry, teamInfo):
        rank = QListWidget(self)
        teamName = QListWidget(self)
        cups = QListWidget(self)
        points = QListWidget(self)
    
        # creating table
        distancToBorder = 25
        tableHigh = self.teamsPerGroup * 22
        rank.setGeometry(tableGeometry, distancToBorder, 50, tableHigh)
        tableGeometry += 50
        teamName.setGeometry(tableGeometry, distancToBorder, 150, tableHigh)
        tableGeometry += 150
        cups.setGeometry(tableGeometry, distancToBorder, 50, tableHigh)
        tableGeometry += 50
        points.setGeometry(tableGeometry, distancToBorder, 60, tableHigh)
        tableGeometry += 205

        # set headers
        groupHeader = Header()
        rank.addItem(groupHeader.rank)
        teamName.addItem(groupHeader.TeamName)
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
        self.allCupColsTeamInfo.append(rank)
        self.allCupColsTeamInfo.append(cups)
        self.allCupColsTeamInfo.append(points)
        return tableGeometry

    def _createGroupTable(self, tableGeometry, infoGroupStages, numberOfGames):
        col1TeamNameX = QListWidget(self)
        col2TeamNameY = QListWidget(self)
        col3GroupStageCups = QListWidget(self)
        col4GroupStageCups = QListWidget(self)
        
        # creating table
        distanceToGroupOverview = 50 + ((self.teamsPerGroup) * 21)
        tableHigh = (numberOfGames * 21)
        col1TeamNameX.setGeometry(tableGeometry, distanceToGroupOverview, 235, tableHigh)
        tableGeometry += 150
        col2TeamNameY.setGeometry(tableGeometry, distanceToGroupOverview, 150, tableHigh)
        tableGeometry += 150
        col3GroupStageCups.setGeometry(tableGeometry, distanceToGroupOverview, 50, tableHigh)
        tableGeometry += 50
        col4GroupStageCups.setGeometry(tableGeometry, distanceToGroupOverview, 50, tableHigh)
        tableGeometry += 100

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
        self.allCupColsGroupStage.append(col3GroupStageCups)
        self.allCupColsGroupStage.append(col4GroupStageCups)
        return tableGeometry

    def _createTableKO(self, tableGeometry, distanceToTable, tableHeigh, numberOfGames, tableID):
        col1 = QListWidget(self)
        col2 = QListWidget(self)
        col3 = QListWidget(self)
        col4 = QListWidget(self)

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
        self.allCupColsSF.append(col1)
        self.allCupColsSF.append(col2)
        self.allCupColsSF.append(col3QFcups)
        self.allCupColsSF.append(col4QFcups)

    def _addAllCupColsQF(self, col1, col2, col3QFcups, col4QFcups):
        self.allCupColsQF.append(col1)
        self.allCupColsQF.append(col2)
        self.allCupColsQF.append(col3QFcups)
        self.allCupColsQF.append(col4QFcups)

    def _addAllCupColsFinals(self, col1, col2, col3Final, col4Final):
        self.allCupColsFinals.append(col1)
        self.allCupColsFinals.append(col2)
        self.allCupColsFinals.append(col3Final)
        self.allCupColsFinals.append(col4Final)

    def fillQuaterFinalsTable(self):
        _, groupWinnerFirst, groupWinnerSecond = catchTeamInfo(self.groupNumber)
        
        rank1VSrank2 = 1
        for groupCounter in range(0, len(self.allCupColsQF), 4):
            for _ in range(2):
                self.allCupColsQF[groupCounter].addItem(groupWinnerFirst[0][0])
                self.allCupColsQF[groupCounter+1].addItem(groupWinnerSecond[rank1VSrank2][0])
                self.allCupColsQF[groupCounter+2].addItem("0")
                self.allCupColsQF[groupCounter+3].addItem("0")

                addQuaterFinals(groupWinnerFirst[0][0], groupWinnerSecond[rank1VSrank2][0], 0 , 0)
                
                groupWinnerFirst.pop(0)
                if (rank1VSrank2 == 1 or len(groupWinnerSecond) < 2) and len(groupWinnerSecond) > 1:
                    groupWinnerSecond.pop(1)
                    rank1VSrank2 = 0
                elif rank1VSrank2 == 0:
                    groupWinnerSecond.pop(0)
                    rank1VSrank2 = 1

    #TODO dont use a table for short textes
    def resultUserInput(self):
        # info Text for the User
        col0 = QListWidget(self)
        col1 = QListWidget(self)
        col2 = QListWidget(self)
        col3 = QListWidget(self)
        col4 = QListWidget(self)
        col0.setGeometry(0, 600, 150, 22)
        col1.setGeometry(50, 600, 150, 22)
        col2.setGeometry(200, 600, 150, 22)
        col3.setGeometry(350, 600, 50, 22)
        col4.setGeometry(400, 600, 50, 22)
        group = QListWidgetItem("group")
        team1 = QListWidgetItem("Team 1")
        team2 = QListWidgetItem("Team 2")
        cupsTeam1 = QListWidgetItem("Cups")
        cupsTeam2 = QListWidgetItem("Cups")
        col0.addItem(group)
        col1.addItem(team1)
        col2.addItem(team2)
        col3.addItem(cupsTeam1)
        col4.addItem(cupsTeam2)

        # userInput
        self.group = QLineEdit(self)
        self.team1Name = QLineEdit(self)
        self.team2Name = QLineEdit(self)
        self.team1Result = QLineEdit(self)
        self.team2Result = QLineEdit(self)
        self.resultGroup = QPushButton('hinzufügen', self)
        self.resultQF = QPushButton('hinzufügen VF', self)
        self.resultFinal = QPushButton('hinzufügen Final', self)

        self.group.setGeometry(0, 622, 170, 22)
        self.team1Name.setGeometry(50, 622, 150, 22)
        self.team2Name.setGeometry(200, 622, 150, 22)
        self.team1Result.setGeometry(350, 622, 50, 22)
        self.team2Result.setGeometry(400, 622, 50, 22)
        self.resultGroup.setGeometry(450, 622, 100, 22)
        self.resultQF.setGeometry(450, 644, 150, 22)
        self.resultFinal.setGeometry(450, 666, 150, 22)
    
        # buttons
        self.resultGroup.clicked.connect(self.inputResultGroupButton)
        self.resultQF.clicked.connect(self.inputResultQFbutton)
        self.resultFinal.clicked.connect(self.inputResultQFbutton) # This button is not rdy for the final Table

        self.resultGroup = QPushButton('start KO-Phase', self)
        self.resultGroup.setGeometry(600, 622, 150, 22)
        self.resultGroup.clicked.connect(self.startQFButton)
        self.show()

        self.resultQF = QPushButton('start Finale', self)
        self.resultQF.setGeometry(600, 644, 150, 22)
        self.resultQF.clicked.connect(self.startFinalsButton)
        self.show()

    # method for components

    def updateTables(self):
        numberOfGames = factorial(self.teamsPerGroup - 1)

        # delete columns Team Info
        for groupCounter in range(len(self.allCupColsTeamInfo)):
            for gameCounter in range(self.teamsPerGroup):
                QListWidget.takeItem(self.allCupColsTeamInfo[groupCounter], 1)
        # delete columns Group Stage
        for groupCounter in range(len(self.allCupColsGroupStage)):
            for gameCounter in range(numberOfGames):
                QListWidget.takeItem(self.allCupColsGroupStage[groupCounter], 1)

        # fill columns Team Info
        teamInfo, _, _ = catchTeamInfo(self.groupNumber)
        # print(teamInfo)
        for groupCounter in range(0, len(self.allCupColsTeamInfo), 3):
            for gameCounter in range(self.teamsPerGroup):
                self.allCupColsTeamInfo[groupCounter].addItem(str(teamInfo[0][gameCounter][3]))
                self.allCupColsTeamInfo[groupCounter+1].addItem(str(teamInfo[0][gameCounter][1]))
                self.allCupColsTeamInfo[groupCounter+2].addItem(str(teamInfo[0][gameCounter][2]))
            teamInfo.pop(0)
        # fill columns Group Stage
        allGroupStages = catchGroupStage(self.groupNumber)
        for groupCounter in range(0, len(self.allCupColsGroupStage), 2):
            for gameCounter in range(numberOfGames):
                self.allCupColsGroupStage[groupCounter].addItem(str(allGroupStages[0][gameCounter][2]))
                self.allCupColsGroupStage[groupCounter+1].addItem(str(allGroupStages[0][gameCounter][3]))
            allGroupStages.pop(0)

    def inputResultGroupButton(self):
        numberOfGames = factorial(self.teamsPerGroup - 1)
        groupValue = self.group.text()
        team1NameValue = self.team1Name.text()
        team2NameValue = self.team2Name.text()
        team1ResultValue = self.team1Result.text()
        team2ResultValue = self.team2Result.text()

        # only for tests!!!
        allGroupNames = ["groupA", "groupB", "groupC", "groupD"]
        allGroupStages = catchGroupStage(self.groupNumber)
        for idx, group in enumerate(allGroupNames):
            for i in range(numberOfGames):
                inputGameResults(group, allGroupStages[idx][i][0], allGroupStages[idx][i][1], "8", "10")

        # inputGameResults(groupValue, team1NameValue, team2NameValue, team1ResultValue, team2ResultValue)
        self.updateTables()
        
        self.group.setText("")
        self.team1Name.setText("")
        self.team2Name.setText("")
        self.team1Result.setText("")
        self.team2Result.setText("")

    def startQFButton(self):
        self.fillQuaterFinalsTable()
        # in the case of a program crash
        self.updateQFtable()

    def startFinalsButton(self):
        self.fillFinalsTable()
        # in the case of a program crash
        self.updateFinalsTable()

    def inputResultQFbutton(self):
        team1NameValue = self.team1Name.text()
        team2NameValue = self.team2Name.text()
        team1ResultValue = self.team1Result.text()
        team2ResultValue = self.team2Result.text()

        updateQF(team1NameValue, team2NameValue, team1ResultValue, team2ResultValue)
        self.updateQFtable()    

        self.team1Name.setText("")
        self.team2Name.setText("")
        self.team1Result.setText("")
        self.team2Result.setText("")

    def updateQFtable(self):
        for _ in range(2):
            for gameCounter in range(2):
                    QListWidget.takeItem(self.allCupColsQF[gameCounter + 2], 1)
                    QListWidget.takeItem(self.allCupColsQF[gameCounter + 6], 1)

        qfTable = catchQF()
        print(qfTable)
        for i in range(2):
            self.allCupColsQF[2].addItem(str(qfTable[i][2]))
            self.allCupColsQF[3].addItem(str(qfTable[i][3]))
        for i in range(2, 4):
            self.allCupColsQF[6].addItem(str(qfTable[i][2]))
            self.allCupColsQF[7].addItem(str(qfTable[i][3]))
    
    def UiComponents(self):
        tableGeometry = 95
        numberOfGames = factorial(self.teamsPerGroup - 1)
        
        # Create Group Overview
        teamInfo, _, _ = catchTeamInfo(self.groupNumber)
        for _ in range(self.groupNumber):
            tableGeometry = self._groupOverview(tableGeometry, teamInfo)
        tableGeometry = 50

        # Create Group Stage table
        infoGroupStages = catchGroupStage(self.groupNumber)
        for _ in range(self.groupNumber):
            tableGeometry = self._createGroupTable(tableGeometry, infoGroupStages, numberOfGames)

        # Create Quater Final table
        if self.groupNumber >= 4:
            tableGeometry = 500
            distanceToGroupStage = ((50 + ((self.teamsPerGroup) * 21)) + (50 + numberOfGames * 21))
            tableHeigh = 3 * 21
            for _ in range(2):
                tableGeometry = self._createTableKO(tableGeometry, distanceToGroupStage, tableHeigh, numberOfGames, "qf")

        # Create Semi Final table
        if self.groupNumber >= 2:
            tableGeometry = 500
            distanceToQFStage = distanceToGroupStage + tableHeigh + 50
            tableHeigh = 2 * 21
            for _ in range(2):
                tableGeometry = self._createTableKO(tableGeometry, distanceToQFStage, tableHeigh, numberOfGames, "sf")

        # Create Final table
        tableGeometry = 50
        distanceToSF = distanceToQFStage + tableHeigh + 50
        tableHeigh = 2 * 21
        for _ in range(2):
            tableGeometry = self._createTableKO(tableGeometry, distanceToSF, tableHeigh, numberOfGames, "final")

        self.resultUserInput()


# create pyqt5 app
App = QApplication(sys.argv)
# create the instance of our Window
window = Window()
# start the app
sys.exit(App.exec())
