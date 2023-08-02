from math import factorial
import flet as ft
from updateGame import Databank

class RankTable:
    def createRank():
        table = ft.DataTable(
            #table design
            width=420,
            border=ft.border.all(2, "black"),
            border_radius=10,
            horizontal_lines=ft.border.BorderSide(1, "red"),
            heading_row_color=ft.colors.BLACK,
            bgcolor=ft.colors.BLACK87,
            

            #fill table
            columns=[
                ft.DataColumn(ft.Text("Team")),
                ft.DataColumn(ft.Text("Cups")),
                ft.DataColumn(ft.Text("Points")),
                ft.DataColumn(ft.Text("Rank")),
            ],
            rows=[]
        )
        return table
    
    def updateRankRuntime(myTable, groupName, teamsperGroup, nmbOfGroups):
        db = Databank()
        teamInfo, _, _ = db.catchGroupStage(nmbOfGroups, "teamInfo")

        for teamName in range(teamsperGroup):                                                #[0] = TeamName
            myTable.rows[teamName].cells[1].content.value = teamInfo[groupName][teamName][1] # cups
            myTable.rows[teamName].cells[2].content.value = teamInfo[groupName][teamName][2] # points
            myTable.rows[teamName].cells[3].content.value = teamInfo[groupName][teamName][3] # rank
        
        
    def updateRank(myTable, groupName, teamName, nmbOfGroups):
        db = Databank()
        teamInfo, _, _ = db.catchGroupStage(nmbOfGroups, "teamInfo")

        myTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(teamInfo[groupName][teamName][0])), # TeamName
                    ft.DataCell(ft.Text(teamInfo[groupName][teamName][1])), # cups
                    ft.DataCell(ft.Text(teamInfo[groupName][teamName][2])), # points
                    ft.DataCell(ft.Text(teamInfo[groupName][teamName][3])), # rank
                ]
            )
        )
    
class GroupstageTable:
    def groupTableMain(nmbOfGroups, teamsPerGroup, koTable, page):
        gamesPerGroup = factorial(teamsPerGroup - 1)
        dynamicRankTable = {}
        dynamicGroupstageTable = {}

        for num in range(nmbOfGroups):
            dynamicRankTable[num] = RankTable.createRank()
            dynamicGroupstageTable[num] = GroupstageTable._createResult()
            for groupName in range(teamsPerGroup):
                RankTable.updateRank(dynamicRankTable[num],num, groupName, nmbOfGroups)
            for groupName in range(gamesPerGroup):
                GroupstageTable._updateResult(dynamicGroupstageTable[num],num, groupName, page, dynamicRankTable[num], nmbOfGroups, koTable, "groupStage")

        return dynamicRankTable, dynamicGroupstageTable

    def _createResult():
            table = ft.DataTable(
                #table design
                width=420,
                border=ft.border.all(2, "black"),
                border_radius=10,
                horizontal_lines=ft.border.BorderSide(1, "red"),
                heading_row_color=ft.colors.BLACK,
                bgcolor=ft.colors.BLACK87,
                #fill table
                columns=[
                    ft.DataColumn(ft.Text("TeamA")),
                    ft.DataColumn(ft.Text("TeamB")),
                    ft.DataColumn(ft.Text("Cups")),
                    ft.DataColumn(ft.Text("Cups")),
                ],
                rows=[]
            )
            return table

    def _updateResult(myTable, groupName, teamName, page, rankTable, nmbOfGroups, koTable, xFinal):
        db = Databank()
        groupGames = db.catchGroupStage(nmbOfGroups, "groupStage")
        myTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][0])), # TeamA
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][1])), # TeamB
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][2])), # cupsA
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][3])), # cupsB
                ],
                on_select_changed=lambda e: (DlgWindow.generateDLGWindow(e, groupName, page, rankTable, nmbOfGroups, koTable, xFinal))
            )
        )

class SemiFinal:
    def updateSemiRuntime(semiFinalTable):
        db = Databank()
        _, groupWinnerFirst, groupWinnerSecond = db.catchGroupStage(2, "teamInfo")
        semiFinalData = db.catchQF("semi_finals")

        rank1VSrank2 = 1
        for idx in range(2):
            semiFinalTable.rows[idx].cells[0].content.value = groupWinnerFirst[0][0]
            semiFinalTable.rows[idx].cells[1].content.value = groupWinnerSecond[rank1VSrank2][0]
            semiFinalTable.rows[idx].cells[2].content.value = 0 
            semiFinalTable.rows[idx].cells[3].content.value = 0

            db.updateKOtabelDB(groupWinnerFirst[0][0], groupWinnerSecond[rank1VSrank2][0], "0", "0", "semi_finals", idx)

            groupWinnerFirst.pop(0)
            if (rank1VSrank2 == 1 or len(groupWinnerSecond) < 2) and len(groupWinnerSecond) > 1:
                groupWinnerSecond.pop(1)
                rank1VSrank2 = 0
            elif rank1VSrank2 == 0:
                groupWinnerSecond.pop(0)
                rank1VSrank2 = 1

    def updateSemi(semiFinalTable, nmbOfGroups, koTable, xFinal, page):
        db = Databank()
        _, groupWinnerFirst, groupWinnerSecond = db.catchGroupStage(2, "teamInfo")
        semiFinalData = db.catchQF("semi_finals")
        if len(semiFinalData) > 0: # if there is already data in the semi Final Table
            for idx in range(len(semiFinalData)):
                semiFinalTable.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(semiFinalData[idx][0])),
                            ft.DataCell(ft.Text(semiFinalData[idx][1])),
                            ft.DataCell(ft.Text(semiFinalData[idx][2])),
                            ft.DataCell(ft.Text(semiFinalData[idx][3])),
                        ],
                        #fill in the right database
                        on_select_changed=lambda e: (DlgWindow.generateDLGWindow(e, _, page, _, nmbOfGroups, koTable, xFinal))
                    )
                )
        else: # if there is not data in the semi final table
            nmbOfGroups = 2
            xFinal = "semi_finals"
            rank1VSrank2 = 1
            for _ in range(len(groupWinnerFirst)):
                semiFinalTable.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(groupWinnerFirst[0][0])),
                            ft.DataCell(ft.Text(groupWinnerSecond[rank1VSrank2][0])),
                            ft.DataCell(ft.Text("0")),
                            ft.DataCell(ft.Text("0")),
                        ],
                        #fill in the right database
                        on_select_changed=lambda e: (DlgWindow.generateDLGWindow(e, _, page, _, nmbOfGroups, koTable, xFinal))
                    )
                )
                db.addSF(groupWinnerFirst[0][0], groupWinnerSecond[rank1VSrank2][0], 0, 0, xFinal),
                groupWinnerFirst.pop(0)
                if (rank1VSrank2 == 1 or len(groupWinnerSecond) < 2) and len(groupWinnerSecond) > 1:
                    groupWinnerSecond.pop(1)
                    rank1VSrank2 = 0
                elif rank1VSrank2 == 0:
                    groupWinnerSecond.pop(0)
                    rank1VSrank2 = 1

class Final:
    def updateFinal(finalTable, semiFinalTable, nmbOfGroups, koTable, xFinal, page):
        db = Databank()
        winners = db.catchWinner("semi_finals")
        #filter the winner form the semi Finals
        finalTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("winners[0][0]")),
                    ft.DataCell(ft.Text("winners[0][1]")),
                    ft.DataCell(ft.Text("0")),
                    ft.DataCell(ft.Text("0")),
                ],
                on_select_changed=lambda e: (DlgWindow.generateDLGWindow(e, _, page, _, nmbOfGroups, koTable, xFinal))
            )
        )
        # addFinals(winners[0][0], winners[0][1], 0, 0, xFinal)

class KOstage:
    def createKOtable():
        return GroupstageTable._createResult()
    
    def individualTable(nmbOfGroups, page):
        koTable = {}
        if (nmbOfGroups == 2):
            xFinal = "semi_finals"
            semiFinalTable = KOstage.createKOtable()
            finalTable = KOstage.createKOtable()

            koTable[0] = semiFinalTable
            koTable[10] = finalTable

            SemiFinal.updateSemi(semiFinalTable, nmbOfGroups, koTable, xFinal, page)
            Final.updateFinal(finalTable, semiFinalTable, nmbOfGroups, koTable, "finals", page)

            print()

        return koTable


class DlgWindow:
    def editDatabase(e, groupName, rankTable, koTable, nmbOfGroups, xFinal):
        db = Databank()
        allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]

        teamX = e.control.cells[0].content.value
        teamY = e.control.cells[1].content.value
        cupsX = str(e.control.cells[2].content.value)
        cupsY = str(e.control.cells[3].content.value)
        # get the SF table 
        teamsperGroup = 4
        if xFinal == "eight_finals":
            db.addEight(teamX, teamY, cupsX, cupsY, xFinal)
        if xFinal == "semi_finals":
            db.updateGameResult(teamX, teamY, cupsX, cupsY, xFinal)
            x = db.catchQF("semi_finals")
        else:
            db.inputGameResults(allGroupNames[groupName], teamX, teamY, cupsX, cupsY)
            RankTable.updateRankRuntime(rankTable, groupName, teamsperGroup, nmbOfGroups)
            if (len(koTable) > 0): #if != null
                SemiFinal.updateSemiRuntime(koTable[0]) #semi Final Table

        print(teamX, " vs ",teamY, " = ", cupsX, ":", cupsY)

    def generateDLGWindow(e, groupName, page, rankTable, nmbOfGroups, koTable, xFinal):
        teamA = e.control.cells[0].content.value
        teamB = e.control.cells[1].content.value
        dlgWindow = ft.AlertDialog(
            title=ft.Text("input result"),
            actions=[
                ft.Column([
                    ft.Row([
                        ft.Text(teamA, width=100, text_align=ft.TextAlign.CENTER),
                        ft.Text(teamB, width=100, text_align=ft.TextAlign.CENTER),
                    ]),
                    ft.Row([
                        ft.Dropdown(
                            on_change=lambda v: editTable(v, 2, nmbOfGroups, koTable, xFinal), # cell for Cups TeamA #2
                            options=[
                                ft.dropdown.Option(0), ft.dropdown.Option(1), ft.dropdown.Option(2),
                                ft.dropdown.Option(3), ft.dropdown.Option(4), ft.dropdown.Option(5),
                                ft.dropdown.Option(6), ft.dropdown.Option(7), ft.dropdown.Option(8),
                                ft.dropdown.Option(9), ft.dropdown.Option(10),
                            ],
                            width=100,
                        ),
                        ft.Dropdown(
                            on_change=lambda v: editTable(v, 3, nmbOfGroups, koTable, xFinal), # cell for Cups TeamA #3
                            options=[
                                ft.dropdown.Option(0), ft.dropdown.Option(1), ft.dropdown.Option(2),
                                ft.dropdown.Option(3), ft.dropdown.Option(4), ft.dropdown.Option(5),
                                ft.dropdown.Option(6), ft.dropdown.Option(7), ft.dropdown.Option(8),
                                ft.dropdown.Option(9), ft.dropdown.Option(10),
                            ],
                            width=100,
                        )
                    ]),
                ]),
            ],
        )
        # open the dialog window
        page.dialog = dlgWindow
        dlgWindow.open = True
        page.update()

        def editTable(v, cell, nmbOfGroups, koTable, xFinal):
            e.control.cells[cell].content.value = v.data
            if cell == 3:
                DlgWindow.editDatabase(e, groupName, rankTable, koTable, nmbOfGroups, xFinal)
                dlgWindow.open = False
            page.update()

class GUItable:
    ''' TODO
    - how many KO tables do I need?
    - fill all KO tables
    - update all KO tables with every result change in the group stage
    - update the right database table with the result input AND update*
    - *update all KO tables with every result change in the KO stage
    '''
    def guiTables(dynamicRankTable, dynamicGroupstageTable, koTable):
        sortRankTableGUI = {}
        sortGroupStageTableGUI = {}
        sortKOtableGUI = {}
        if len(dynamicRankTable) == 2:
            sortRankTableGUI[0] = ft.DataTable(width=420)
            sortGroupStageTableGUI[0] = ft.DataTable(width=420)
            sortKOtableGUI[0] = ft.DataTable(width=210)
            sortKOtableGUI[1] = ft.DataTable(width=420)
            sortKOtableGUI[2] = koTable[0]
            for num in range(2):
                sortRankTableGUI[num + 1] = dynamicRankTable[num]
                sortGroupStageTableGUI[num + 1] = dynamicGroupstageTable[num]

        elif len(dynamicRankTable) == 4:
            i = 0
            widthe = 210
            for num in range(4):
                if num % 2 == 0:
                    sortKOtableGUI[num] = ft.DataTable(width=widthe)
                    widthe *= 2
                else:
                    sortKOtableGUI[num] = koTable[i] 
                    i += 1

            for num in range(len(dynamicRankTable)):
                sortRankTableGUI[num] = dynamicRankTable[num]
                sortGroupStageTableGUI[num] = dynamicGroupstageTable[num]

        elif len(dynamicRankTable) == 6:
            sortKOtableGUI[0] = ft.DataTable(width=210)
            for num in range(0, 4):
                sortRankTableGUI[num] = dynamicRankTable[num]
                sortGroupStageTableGUI[num] = dynamicGroupstageTable[num]
                sortKOtableGUI[num + 1] = koTable[num]
            sortRankTableGUI[4] = ft.DataTable(width=420)
            sortGroupStageTableGUI[4] = ft.DataTable(width=420)
            for num in range(5, 7):
                sortRankTableGUI[num] = dynamicRankTable[num - 1]
                sortGroupStageTableGUI[num] = dynamicGroupstageTable[num - 1]
                sortKOtableGUI[num] = ft.DataTable()
        else:
            sortRankTableGUI = dynamicRankTable
            sortGroupStageTableGUI = dynamicGroupstageTable
            sortKOtableGUI[0] = ft.DataTable(width=210)
            sortKOtableGUI[1] = koTable[0]
            sortKOtableGUI[2] = ft.DataTable(width=420)
            sortKOtableGUI[3] = koTable[1]
            sortKOtableGUI[4] = ft.DataTable(width=210)
            sortKOtableGUI[5] = koTable[2]
            sortKOtableGUI[6] = ft.DataTable(width=420)
            sortKOtableGUI[7] = koTable[3]

        for num in range(8 - len(dynamicRankTable)):
            sortRankTableGUI[len(sortRankTableGUI)] = ft.DataTable(width=420)
            sortGroupStageTableGUI[len(sortGroupStageTableGUI)] = ft.DataTable(width=420)
            sortKOtableGUI[len(sortKOtableGUI)] = ft.DataTable(width=420)
        #Final Table
        sortKOtableGUI[12] = ft.DataTable(width=420)
        sortKOtableGUI[13] = ft.DataTable(width=210)
        sortKOtableGUI[14] = koTable[10]

        return sortRankTableGUI, sortGroupStageTableGUI, sortKOtableGUI

def mainPage(page):
    
    nmbOfGroups = 2 #TODO user setting
    teamsPerGroup = 4
    koTable = {}
    
    # Creating ko Table
    koTable = KOstage.individualTable(nmbOfGroups, page)

    # Creating Group Tables
    dynamicRankTable, dynamicGroupstageTable = GroupstageTable.groupTableMain(nmbOfGroups, teamsPerGroup, koTable,  page)
    sortRankTableGUI, sortGroupStageTableGUI, sortKOtableGUI = GUItable.guiTables(dynamicRankTable, dynamicGroupstageTable, koTable)

    # put it in the GUI
    header = ft.Text(
            text_align=ft.TextAlign.RIGHT,
            value=f"BEERPONG",
            size=60,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLACK,
            width=1025,
        )
    credits = ft.Text(
                    value="~by Baldri4n",
                    text_align=ft.TextAlign.RIGHT,
                    color=ft.colors.BLACK,
                    width=1700,
                )

    allTables = ft.Column(
            [
            ft.Row([
                header
            ]),
            ft.Row([
                sortRankTableGUI[0], sortRankTableGUI[1], sortRankTableGUI[2], sortRankTableGUI[3],
                    ]),
            ft.Row([
                sortRankTableGUI[4], sortRankTableGUI[5], sortRankTableGUI[6], sortRankTableGUI[7],
                    ]),
            ft.Row([
                sortGroupStageTableGUI[0], sortGroupStageTableGUI[1], sortGroupStageTableGUI[2], sortGroupStageTableGUI[3],
            ]),
            ft.Row([
                sortGroupStageTableGUI[4], sortGroupStageTableGUI[5], sortGroupStageTableGUI[6], sortGroupStageTableGUI[7],
            ]),
            ft.Row([
                sortKOtableGUI[0], sortKOtableGUI[1], sortKOtableGUI[2], sortKOtableGUI[3],   #eight Final
            ]),
            ft.Row([
                sortKOtableGUI[4], sortKOtableGUI[5], sortKOtableGUI[6], sortKOtableGUI[7],    #eightFinal
            ]),
            ft.Row([
                # sortKOtableGUI[8], sortKOtableGUI[9], sortKOtableGUI[10], sortKOtableGUI[11],    # freeTables for puffer
            ]),
            ft.Row([
                sortKOtableGUI[12], sortKOtableGUI[13], sortKOtableGUI[14],  #Final
            ]),
            ft.Row([
                credits
            ])
            ]
        )

    page.scroll = "ALWAYS"
    page.theme_mode = ft.ThemeMode.DARK
    page.add(
        ft.Container(
            image_src="beerpong.png",
            image_fit=ft.ImageFit.COVER,
            content=allTables,
        )  
    )
    
if __name__ == "__main__":
    ft.app(target=mainPage)
    page = ft.Page
    mainPage(page)
    
    #TODO add finals
