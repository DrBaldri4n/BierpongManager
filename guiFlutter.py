from math import factorial
import flet as ft
from updateGame import catchGroupStage, inputGameResults, addEight
# lets try this with flutter!!

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
        teamInfo, _, _ = catchGroupStage(nmbOfGroups, "teamInfo")

        for teamName in range(teamsperGroup):                                                #[0] = TeamName
            myTable.rows[teamName].cells[1].content.value = teamInfo[groupName][teamName][1] # cups
            myTable.rows[teamName].cells[2].content.value = teamInfo[groupName][teamName][2] # points
            myTable.rows[teamName].cells[3].content.value = teamInfo[groupName][teamName][3] # rank
        
        
    def updateRank(myTable, groupName, teamName, nmbOfGroups):
        teamInfo, _, _ = catchGroupStage(nmbOfGroups, "teamInfo")

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
    def groupTableMain(nmbOfGroups, teamsPerGroup, page):
        gamesPerGroup = factorial(teamsPerGroup - 1)
        dynamicRankTable = {}
        dynamicGroupstageTable = {}

        for num in range(nmbOfGroups):
            dynamicRankTable[num] = RankTable.createRank()
            dynamicGroupstageTable[num] = GroupstageTable._createResult()
            for groupName in range(teamsPerGroup):
                RankTable.updateRank(dynamicRankTable[num],num, groupName, nmbOfGroups)
            for groupName in range(gamesPerGroup):
                GroupstageTable._updateResult(dynamicGroupstageTable[num],num, groupName, page, dynamicRankTable[num], nmbOfGroups, "groupStage")

        if nmbOfGroups < 8:
            for num in range(8 - len(dynamicRankTable)):
                dynamicRankTable[len(dynamicRankTable)] = ft.DataTable(width=420)
                dynamicGroupstageTable[len(dynamicGroupstageTable)] = ft.DataTable(width=420)

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

    def _updateResult(myTable, groupName, teamName, page, rankTable, nmbOfGroups, xFinal):
        groupGames = catchGroupStage(nmbOfGroups, "groupStage")
        myTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][0])), # TeamA
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][1])), # TeamB
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][2])), # cupsA
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][3])), # cupsB
                ],
                on_select_changed=lambda e: (DlgWindow.generateDLGWindow(e, groupName, page, rankTable, nmbOfGroups, xFinal))
            )
        )

class KOstage:
    def createKOtable():
        return GroupstageTable._createResult()
    
    def updateKOtable(table, nmbOfGroups, xFinal, page):
        _, groupWinnerFirst, groupWinnerSecond = catchGroupStage(2, "teamInfo")
        rank1VSrank2 = 1
        for _ in range(len(groupWinnerFirst)):
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(groupWinnerFirst[0][0])),
                        ft.DataCell(ft.Text(groupWinnerSecond[rank1VSrank2][0])),
                        ft.DataCell(ft.Text("0")),
                        ft.DataCell(ft.Text("0")),
                    ],
                    #fill in the right database
                    on_select_changed=lambda e: (DlgWindow.generateDLGWindow(e, _, page, _, nmbOfGroups, xFinal))
                )
            )
            addEight(groupWinnerFirst[0][0], groupWinnerSecond[rank1VSrank2][0], 0, 0, xFinal),

            groupWinnerFirst.pop(0)
            if (rank1VSrank2 == 1 or len(groupWinnerSecond) < 2) and len(groupWinnerSecond) > 1:
                groupWinnerSecond.pop(1)
                rank1VSrank2 = 0
            elif rank1VSrank2 == 0:
                groupWinnerSecond.pop(0)
                rank1VSrank2 = 1


class DlgWindow:
    def editDatabase(e, groupName, rankTable, nmbOfGroups, xFinal):
        allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]

        teamX = e.control.cells[0].content.value
        teamY = e.control.cells[1].content.value
        cupsX = str(e.control.cells[2].content.value)
        cupsY = str(e.control.cells[3].content.value)

        teamsperGroup = 4
        if xFinal == "eight_finals":
            addEight(teamX, teamY, cupsX, cupsY, xFinal)
        else:
            inputGameResults(allGroupNames[groupName], teamX, teamY, cupsX, cupsY)
            RankTable.updateRankRuntime(rankTable, groupName, teamsperGroup, nmbOfGroups)
        print(teamX, " vs ",teamY, " = ", cupsX, ":", cupsY)

    def generateDLGWindow(e, groupName, page, rankTable, nmbOfGroups, xFinal):
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
                            on_change=lambda v: editTable(v, 2, nmbOfGroups, xFinal), # cell for Cups TeamA #2
                            options=[
                                ft.dropdown.Option(0), ft.dropdown.Option(1), ft.dropdown.Option(2),
                                ft.dropdown.Option(3), ft.dropdown.Option(4), ft.dropdown.Option(5),
                                ft.dropdown.Option(6), ft.dropdown.Option(7), ft.dropdown.Option(8),
                                ft.dropdown.Option(9), ft.dropdown.Option(10),
                            ],
                            width=100,
                        ),
                        ft.Dropdown(
                            on_change=lambda v: editTable(v, 3, nmbOfGroups, xFinal), # cell for Cups TeamA #3
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

        def editTable(v, cell, nmbOfGroups, xFinal):
            e.control.cells[cell].content.value = v.data
            if cell == 3:
                DlgWindow.editDatabase(e, groupName, rankTable, nmbOfGroups, xFinal)
                dlgWindow.open = False
            page.update()

def mainPage(page):
    
    nmbOfGroups = 4 #TODO user setting
    teamsPerGroup = 4
    
    # Creating Group Tables
    dynamicRankTable, dynamicGroupstageTable = GroupstageTable.groupTableMain(nmbOfGroups, teamsPerGroup, page)
    
    # Creating ko Table
    koTable = {}
    for num in range(int(nmbOfGroups/2)):
        koTable[num] = KOstage.createKOtable()
        KOstage.updateKOtable(koTable[num], nmbOfGroups, "eight_finals", page)
    if int(nmbOfGroups/2) < 4:
        for num in range(4 - int(nmbOfGroups/2)):
            koTable[len(koTable)] = ft.DataTable(width=420)

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
                dynamicRankTable[2], dynamicRankTable[0], dynamicRankTable[1], dynamicRankTable[3],
                    ]),
            ft.Row([
                dynamicRankTable[6], dynamicRankTable[4], dynamicRankTable[5], dynamicRankTable[7],
                    ]),
            ft.Row([

                dynamicGroupstageTable[2], dynamicGroupstageTable[0], dynamicGroupstageTable[1], dynamicGroupstageTable[3],
            ]),
            ft.Row([
                dynamicGroupstageTable[6], dynamicGroupstageTable[4], dynamicGroupstageTable[5], dynamicGroupstageTable[7],
            ]),
            ft.Row([
                koTable[2], koTable[0], koTable[1], koTable[3],     
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
    

    #TODO keine 8 mehr übergeben sonder anzahl der gruppen
    #TODO Achtelfinale einfügen