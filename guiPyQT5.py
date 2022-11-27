#import python lib
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from math import factorial

#import own functions
from updateGame import inputGameResults, catchGroupStage


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        # setting title
        self.setWindowTitle("Bierpong Tunier")
        # setting geometry
        self.setGeometry(0, 0, 1600, 800)
        # calling method
        self.UiComponents()
        # showing all the widgets
        self.show()


    def createGroupTable(self, tableGeometry, numberOfGames, allGroupStages):
        # creating table
        col1 = QListWidget(self)
        col2 = QListWidget(self)
        col3 = QListWidget(self)
        col4 = QListWidget(self)
        col1.setGeometry(tableGeometry, 50, 150, numberOfGames * 22)
        tableGeometry += 150
        col2.setGeometry(tableGeometry, 50, 150, numberOfGames * 22)
        tableGeometry += 150
        col3.setGeometry(tableGeometry, 50, 50, numberOfGames * 22)
        tableGeometry += 50
        col4.setGeometry(tableGeometry, 50, 50, numberOfGames * 22)
        tableGeometry += 100

        # set headers
        team1 = QListWidgetItem("Team 1")
        team2 = QListWidgetItem("Team 2")
        cupsTeam1 = QListWidgetItem("Cups")
        cupsTeam2 = QListWidgetItem("Cups")

        # fill columns 
        col1.addItem(team1)
        for i in range(numberOfGames):
            col1.addItem(allGroupStages[0][i][0])

        col2.addItem(team2)
        for i in range(numberOfGames):
            col2.addItem(allGroupStages[0][i][1])

        col3.addItem(cupsTeam1)
        for i in range(numberOfGames):
            col3.addItem(str(allGroupStages[0][i][2]))

        col4.addItem(cupsTeam2)
        for i in range(numberOfGames):
            col4.addItem(str(allGroupStages[0][i][3]))

        allGroupStages.pop(0)

        return tableGeometry

    def resultUserInput(self):

        #TODO dont use a table for small textes

        # info Text for the User
        col0 = QListWidget(self)
        col1 = QListWidget(self)
        col2 = QListWidget(self)
        col3 = QListWidget(self)
        col4 = QListWidget(self)
        col0.setGeometry(0, 478, 150, 22)
        col1.setGeometry(50, 478, 150, 22)
        col2.setGeometry(200, 478, 150, 22)
        col3.setGeometry(350, 478, 50, 22)
        col4.setGeometry(400, 478, 50, 22)
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
        self.button = QPushButton('Show text', self)

        self.group.setGeometry(0, 500, 150, 22)
        self.team1Name.setGeometry(50, 500, 150, 22)
        self.team2Name.setGeometry(200, 500, 150, 22)
        self.team1Result.setGeometry(350, 500, 50, 22)
        self.team2Result.setGeometry(400, 500, 50, 22)
        self.button.setGeometry(450, 500, 80, 22)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()


    # method for components
    def UiComponents(self):
        tableGeometry = 50
        groupNumber = 4
        teamsPerGroup = 4
        numberOfGames = factorial(teamsPerGroup - 1)

        allGroupStages = catchGroupStage(groupNumber)

        for i in range(groupNumber):
            tableGeometry = self.createGroupTable(tableGeometry, numberOfGames, allGroupStages)

        self.resultUserInput()

    def updateGameInTable(self, groupValue, team1NameValue, team2NameValue, team1ResultValue, team2ResultValue):

        print()

    def on_click(self):
        
        groupValue = self.group.text()
        team1NameValue = self.team1Name.text()
        team2NameValue = self.team2Name.text()
        team1ResultValue = self.team1Result.text()
        team2ResultValue = self.team2Result.text()

        inputGameResults(groupValue, team1NameValue, team2NameValue, team1ResultValue, team2ResultValue)
        # self.updateGameInTable(groupValue, team1NameValue, team2NameValue, team1ResultValue, team2ResultValue)
        allGroupStages = catchGroupStage(4)
        self.createGroupTableTest(50, 6, allGroupStages)

        QMessageBox.question(self, 'Message - pythonspot.com', team1NameValue + " vs " + team2NameValue + " " + team1ResultValue + " : " + team2ResultValue, QMessageBox.Ok, QMessageBox.Ok)
        self.group.setText("")
        self.team1Name.setText("")
        self.team2Name.setText("")
        self.team1Result.setText("")
        self.team2Result.setText("")

        
        # self.createGroupTable()


    #testetsetstes schauen ob sich das window live verändern kann
    def createGroupTableTest(self, tableGeometry, numberOfGames, allGroupStages):
        # creating table
        col1 = QListWidget(self)
        col2 = QListWidget(self)
        col3 = QListWidget(self)
        col4 = QListWidget(self)
        col1.setGeometry(tableGeometry, 200, 150, numberOfGames * 22)
        tableGeometry += 150
        col2.setGeometry(tableGeometry, 200, 150, numberOfGames * 22)
        tableGeometry += 150
        col3.setGeometry(tableGeometry, 200, 50, numberOfGames * 22)
        tableGeometry += 50
        col4.setGeometry(tableGeometry, 200, 50, numberOfGames * 22)
        tableGeometry += 100

        # set headers
        team1 = QListWidgetItem("Team 1")
        team2 = QListWidgetItem("Team 2")
        cupsTeam1 = QListWidgetItem("Cups")
        cupsTeam2 = QListWidgetItem("Cups")

        # fill columns 
        col1.addItem(team1)
        for i in range(numberOfGames):
            col1.addItem(allGroupStages[0][i][0])

        col2.addItem(team2)
        for i in range(numberOfGames):
            col2.addItem(allGroupStages[0][i][1])

        col3.addItem(cupsTeam1)
        for i in range(numberOfGames):
            col3.addItem(str(allGroupStages[0][i][2]))

        col4.addItem(cupsTeam2)
        for i in range(numberOfGames):
            col4.addItem(str(allGroupStages[0][i][3]))

        allGroupStages.pop(0)

        return tableGeometry



# create pyqt5 app
App = QApplication(sys.argv)
# create the instance of our Window
window = Window()
# start the app
sys.exit(App.exec())
