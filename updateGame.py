import sqlite3

def incCups(group, teamX, cupsX, teamY, cupsY):
    cur.execute("UPDATE " + group + " SET cups = cups + (?) WHERE team_name = (?)", (cupsX, teamX))
    cur.execute("UPDATE " + group + " SET cups = cups + (?) WHERE team_name = (?)", (cupsY, teamY))

def incPoints(group, teamX, cupsX, teamY, cupsY):
    if cupsX > cupsY:
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (3, teamX))
    elif cupsX < cupsY:
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (3, teamY))
    else:
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (1, teamX))
        cur.execute("UPDATE " + group + " SET points = points + (?) WHERE team_name = (?)", (1, teamY))

def printGroups(allGroupNames, groupNumbers):
    for i in range(groupNumbers):
        cur.execute("SELECT * FROM " + allGroupNames[i])
        print(allGroupNames[i], cur.fetchall())

def createGroupStage(allGroupNames, groupNumbers):
    for indexGroup in range(groupNumbers):
        cur.execute("SELECT team_name FROM " + allGroupNames[indexGroup])
        groupX = cur.fetchall()
        cur.execute("SELECT count() FROM " + allGroupNames[indexGroup])
        groupSize = cur.fetchall()
        groupSize = groupSize[0][0]

        cupsX = 0
        cupsY = 0
        print(allGroupNames[indexGroup])
        for j in range(groupSize - 1):
            for i in range(j + 1, groupSize):
                print(groupX[j][0], " vs ", groupX[i][0])
            #     cupsX = input("erziehlte Cups für " + groupX[j][0] + ": ")
            #     cupsY = input("erziehlte Cups für " + groupX[i][0] + ": ")
            #     incCups(allGroupNames[indexGroup], groupX[j][0], cupsX, groupX[i][0], cupsY)
            #     incPoints(allGroupNames[indexGroup], groupX[j][0], cupsX, groupX[i][0], cupsY)
            #     nextGroup = input("nächste Gruppe?(0 = nein | 1 = ja): ")
            #     if int(nextGroup) == 1:
            #         break
            # if int(nextGroup) == 1:
            #         break
        
        print()
        

def main(allGroupNames, groupNumbers):
    createGroupStage(allGroupNames, groupNumbers)
    # while True:
    #     printGroups(allGroupNames, groupNumbers)
    #     changeCups = input("Cup anzahl ändern?(0 = nein | 1 = ja): ")
    #     if changeCups == "1":
    #         incCups()
    #     changePoints = input("Punktezahl ändern?(0 = nein | 1 = ja): ")
    #     if changePoints == "1":
    #         incPoints()
    #     gameEnd = input("programm beenden?(0 = nein | 1 = ja): ")
    #     if gameEnd == "1":
    #         break

    printGroups(allGroupNames, groupNumbers)

if __name__ == "__main__":
    conn = sqlite3.connect('beerpong.db')
    cur = conn.cursor()
    
    allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
    groupNumbers = 4
    main(allGroupNames, groupNumbers)
    
    conn.commit()
    conn.close()