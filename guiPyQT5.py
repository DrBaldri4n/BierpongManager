#import python lib
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from math import factorial

#import own functions
from updateGame import inputGameResults, catchGroupStage, catchTeamInfo, calcRank


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        # setting title
        self.setWindowTitle("Bierpong Tunier")
        # setting geometry
        self.setGeometry(0, 0, 2000, 800)
        # needed to update the tables
        self.allCupColsTeamInfo = []
        self.allCupColsGroupStage = []
        self.allCupColsQuaterFinals = []
        # calling method
        self.UiComponents()
        # showing all the widgets
        self.show()

    def groupOverview(self, tableGeometry, teamInfo):
        rank = QListWidget(self)
        teamName = QListWidget(self)
        cups = QListWidget(self)
        points = QListWidget(self)
    
        rank.setGeometry(tableGeometry, 25, 50, (self.teamsPerGroup) * 22)
        tableGeometry += 50
        teamName.setGeometry(tableGeometry, 25, 150, (self.teamsPerGroup) * 22)
        tableGeometry += 150
        cups.setGeometry(tableGeometry, 25, 50, (self.teamsPerGroup)  * 22)
        tableGeometry += 50
        points.setGeometry(tableGeometry, 25, 60, (self.teamsPerGroup)  * 22)
        tableGeometry += 205

        # set headers
        rankHeader = QListWidgetItem("Platz")
        TeamNameHeader = QListWidgetItem("Team Name")
        cupsHeader = QListWidgetItem("Cups")
        pointsHeader = QListWidgetItem("Punkte")
        rank.addItem(rankHeader)
        teamName.addItem(TeamNameHeader)
        cups.addItem(cupsHeader)
        points.addItem(pointsHeader)

        # fill columns
        for i in range(self.teamsPerGroup):
            rank.addItem(str(teamInfo[0][i][3]))
        for i in range(self.teamsPerGroup):
            teamName.addItem(teamInfo[0][i][0])
        for i in range(self.teamsPerGroup):
            cups.addItem(str(teamInfo[0][i][1]))
        for i in range(self.teamsPerGroup):
            points.addItem(str(teamInfo[0][i][2]))
        teamInfo.pop(0)

        # needed to update Rank, Cups and Points
        self.allCupColsTeamInfo.append(rank)
        self.allCupColsTeamInfo.append(cups)
        self.allCupColsTeamInfo.append(points)

        return tableGeometry
        

    def createGroupTable(self, tableGeometry, numberOfGames, allGroupStages):
        # creating table
        col1 = QListWidget(self)
        col2 = QListWidget(self)
        self.col3QF = QListWidget(self)
        self.col4QF = QListWidget(self)
        
        distanceTogroupOverview = 50 + ((self.teamsPerGroup) * 22)
        col1.setGeometry(tableGeometry, distanceTogroupOverview, 235, numberOfGames * 22)
        tableGeometry += 150
        col2.setGeometry(tableGeometry, distanceTogroupOverview, 150, numberOfGames * 22)
        tableGeometry += 150
        self.col3QF.setGeometry(tableGeometry, distanceTogroupOverview, 50, numberOfGames * 22)
        tableGeometry += 50
        self.col4QF.setGeometry(tableGeometry, distanceTogroupOverview, 50, numberOfGames * 22)
        tableGeometry += 100

        # set headers
        team1 = QListWidgetItem("Team 1")
        team2 = QListWidgetItem("Team 2")
        self.cupsTeam1 = QListWidgetItem("Cups")
        self.cupsTeam2 = QListWidgetItem("Cups")

        # fill columns 
        col1.addItem(team1)
        for i in range(numberOfGames):
            col1.addItem(allGroupStages[0][i][0])

        col2.addItem(team2)
        for i in range(numberOfGames):
            col2.addItem(allGroupStages[0][i][1])

        self.col3QF.addItem(self.cupsTeam1)
        for i in range(numberOfGames):
            self.col3QF.addItem(str(allGroupStages[0][i][2]))

        self.col4QF.addItem(self.cupsTeam2)
        for i in range(numberOfGames):
            self.col4QF.addItem(str(allGroupStages[0][i][3]))
        
        allGroupStages.pop(0)

        # needed to update the tables
        self.allCupColsGroupStage.append(self.col3QF)
        self.allCupColsGroupStage.append(self.col4QF)

        return tableGeometry

    def createQuaterFinalsTable(self, tableGeometry, numberOfGames):
        # creating table
        col1 = QListWidget(self)
        col2 = QListWidget(self)
        self.col3QF = QListWidget(self)
        self.col4QF = QListWidget(self)

        distanceToGroupStage = ((50 + ((self.teamsPerGroup) * 22)) + (50 + numberOfGames * 22))

        col1.setGeometry(tableGeometry, distanceToGroupStage, 150, 3 * 22)
        tableGeometry += 150
        col2.setGeometry(tableGeometry, distanceToGroupStage, 150, 3 * 22)
        tableGeometry += 150
        self.col3QF.setGeometry(tableGeometry, distanceToGroupStage, 50, 3 * 22)
        tableGeometry += 50
        self.col4QF.setGeometry(tableGeometry, distanceToGroupStage, 50, 3 * 22)
        tableGeometry += 100

        # header
        rank1 = QListWidgetItem("1. in Gruppe")
        rank2 = QListWidgetItem("2. in Gruppe")
        self.cupsRank1 = QListWidgetItem("Cups")
        self.cupsRank2 = QListWidgetItem("Cups")
        col1.addItem(rank1)
        col2.addItem(rank2)
        self.col3QF.addItem(self.cupsRank1)
        self.col4QF.addItem(self.cupsRank2)

        self.allCupColsQuaterFinals.append(col1)
        self.allCupColsQuaterFinals.append(col2)
        self.allCupColsQuaterFinals.append(self.col3QF)
        self.allCupColsQuaterFinals.append(self.col4QF)

        return tableGeometry

    # fill columns TODO
    def fillQuaterFinalsTable(self):
        _, groupWinnerFirst, groupWinnerSecond = catchTeamInfo(self.groupNumber)
        print(groupWinnerFirst, groupWinnerSecond)
        
        rank1VSrank2 = 1
        for groupCounter in range(0, len(self.allCupColsQuaterFinals), 4):
            for _ in range(2):
                self.allCupColsQuaterFinals[groupCounter].addItem(groupWinnerFirst[0][0])
                self.allCupColsQuaterFinals[groupCounter+1].addItem(groupWinnerSecond[0 + rank1VSrank2][0])
                self.allCupColsQuaterFinals[groupCounter+2].addItem("0")
                self.allCupColsQuaterFinals[groupCounter+3].addItem("0")
                groupWinnerFirst.pop(0)

                # .pop index out of range... but not fatal
                if rank1VSrank2 == 1 or len(groupWinnerSecond) < 2:
                    groupWinnerSecond.pop(1)
                    rank1VSrank2 = 0
                elif rank1VSrank2 == 0:
                    groupWinnerSecond.pop(0)
                    rank1VSrank2 = 1
                

                print(groupWinnerFirst, groupWinnerSecond)

        

    def resultUserInput(self):

        #TODO dont use a table for small textes
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
        self.button = QPushButton('hinzufügen', self)

        self.group.setGeometry(0, 622, 150, 22)
        self.team1Name.setGeometry(50, 622, 150, 22)
        self.team2Name.setGeometry(200, 622, 150, 22)
        self.team1Result.setGeometry(350, 622, 50, 22)
        self.team2Result.setGeometry(400, 622, 50, 22)
        self.button.setGeometry(450, 622, 80, 22)
    
        # buttons
        self.button.clicked.connect(self.inputResultButton)

        self.button = QPushButton('start KO-Phase', self)
        self.button.setGeometry(600, 622, 150, 22)
        self.button.clicked.connect(self.startQuaterFinalsButton)
        self.show()



    # method for components

    def updateTables(self):

        # delete columns Team Info
        for groupCounter in range(len(self.allCupColsTeamInfo)):
            for gameCounter in range(self.teamsPerGroup):
                QListWidget.takeItem(self.allCupColsTeamInfo[groupCounter], 1)
        # delete columns Group Stage
        for groupCounter in range(len(self.allCupColsGroupStage)):
            for gameCounter in range(self.numberOfGames):
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
            for gameCounter in range(self.numberOfGames):
                self.allCupColsGroupStage[groupCounter].addItem(str(allGroupStages[0][gameCounter][2]))
                self.allCupColsGroupStage[groupCounter+1].addItem(str(allGroupStages[0][gameCounter][3]))
            allGroupStages.pop(0)

    def inputResultButton(self):
        groupValue = self.group.text()
        team1NameValue = self.team1Name.text()
        team2NameValue = self.team2Name.text()
        team1ResultValue = self.team1Result.text()
        team2ResultValue = self.team2Result.text()


        # only for tests!!!
        allGroupNames = ["groupA", "groupB", "groupC", "groupD"]
        allGroupStages = catchGroupStage(self.groupNumber)
        for idx, group in enumerate(allGroupNames):
            for i in range(self.numberOfGames):
                inputGameResults(group, allGroupStages[idx][i][0], allGroupStages[idx][i][1], "8", "10")

    
        # inputGameResults(groupValue, team1NameValue, team2NameValue, team1ResultValue, team2ResultValue)
        self.updateTables()
        
        self.group.setText("")
        self.team1Name.setText("")
        self.team2Name.setText("")
        self.team1Result.setText("")
        self.team2Result.setText("")

    def startQuaterFinalsButton(self):
        self.fillQuaterFinalsTable()
        print()

    def UiComponents(self):
        tableGeometry = 95
        self.groupNumber = 4
        self.teamsPerGroup = 4
        self.numberOfGames = factorial(self.teamsPerGroup - 1)

        allGroupStages = catchGroupStage(self.groupNumber)
        teamInfo, _, _ = catchTeamInfo(self.groupNumber)

        for _ in range(self.groupNumber):
            tableGeometry = self.groupOverview(tableGeometry, teamInfo)
        tableGeometry = 50

        for _ in range(self.groupNumber):
            tableGeometry = self.createGroupTable(tableGeometry, self.numberOfGames, allGroupStages)

        tableGeometry = 500
        for _ in range((int(self.groupNumber)) // int(2)):
            tableGeometry = self.createQuaterFinalsTable(tableGeometry, self.numberOfGames)

        self.resultUserInput()



# create pyqt5 app
App = QApplication(sys.argv)
# create the instance of our Window
window = Window()
# start the app
sys.exit(App.exec())
