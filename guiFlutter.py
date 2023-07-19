from math import factorial
import flet as ft
from updateGame import catchGroupStage, inputGameResults, deleteInputDB
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
    
    def updateRankRuntime(myTable, groupName, teamsperGroup):
        teamInfo, _, _ = catchGroupStage(8, "teamInfo")

        for teamName in range(teamsperGroup):                                                #[0] = TeamName
            myTable.rows[teamName].cells[1].content.value = teamInfo[groupName][teamName][1] # cups
            myTable.rows[teamName].cells[2].content.value = teamInfo[groupName][teamName][2] # points
            myTable.rows[teamName].cells[3].content.value = teamInfo[groupName][teamName][3] # rank
        
        
    def updateRank(myTable, groupName, teamName):
        teamInfo, _, _ = catchGroupStage(8, "teamInfo")

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
    def createResult():
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

    def updateResult(myTable, groupName, teamName, page, rankTable):
        groupGames = catchGroupStage(8, "groupStage")
        myTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][0])), # TeamA
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][1])), # TeamB
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][2])), # cupsA
                    ft.DataCell(ft.Text(groupGames[groupName][teamName][3])), # cupsB
                ],
                on_select_changed=lambda e: (InteractiveButton.generateDLGWindow(e, groupName, page, rankTable))
            )
        )

class InteractiveButton:
    def editDatabase(e, groupName, rankTable):
        allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]

        teamX = e.control.cells[0].content.value
        teamY = e.control.cells[1].content.value
        cupsX = str(e.control.cells[2].content.value)
        cupsY = str(e.control.cells[3].content.value)

        teamsperGroup = 4
        inputGameResults(allGroupNames[groupName], teamX, teamY, cupsX, cupsY)
        RankTable.updateRankRuntime(rankTable, groupName, teamsperGroup)
        print(teamX, " vs ",teamY, " = ", cupsX, ":", cupsY)

    def generateDLGWindow(e, groupName, page, rankTable):
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
                            on_change=lambda v: editAndSave(v, cell=2), # cell for Cups TeamA #2
                            options=[
                                ft.dropdown.Option(0), ft.dropdown.Option(1), ft.dropdown.Option(2),
                                ft.dropdown.Option(3), ft.dropdown.Option(4), ft.dropdown.Option(5),
                                ft.dropdown.Option(6), ft.dropdown.Option(7), ft.dropdown.Option(8),
                                ft.dropdown.Option(9), ft.dropdown.Option(10),
                            ],
                            width=100,
                        ),
                        ft.Dropdown(
                            on_change=lambda v: editAndSave(v, cell=3), # cell for Cups TeamA #3
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

        def editAndSave(v, cell):
            e.control.cells[cell].content.value = v.data
            if cell == 3:
                InteractiveButton.editDatabase(e, groupName, rankTable)
                dlgWindow.open = False
            page.update()

def mainPage(page):
    
    groups = 8 #TODO user setting
    teamsPerGroup = 4
    gamesPerGroup = factorial(teamsPerGroup - 1)

    dynamicRankTable = {}
    dynamicGroupstageTable = {}
    for num in range(groups):
        dynamicRankTable[num] = RankTable.createRank()
        dynamicGroupstageTable[num] = GroupstageTable.createResult()
        for groupName in range(teamsPerGroup):
            RankTable.updateRank(dynamicRankTable[num],num, groupName)
        for groupName in range(gamesPerGroup):
            GroupstageTable.updateResult(dynamicGroupstageTable[num],num, groupName, page, dynamicRankTable[num])

    if groups < 8:
        for num in range(8 - len(dynamicRankTable)):
            dynamicRankTable[len(dynamicRankTable)] = ft.DataTable(width=420)
            dynamicGroupstageTable[len(dynamicGroupstageTable)] = ft.DataTable(width=420)

    text = ft.Text(
            text_align=ft.TextAlign.RIGHT,
            value=f"BEERPONG",
            size=60,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLACK,
            width=1025,
        )
    
    allTables = ft.Column(
            [
            ft.Row([
                text
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
                ft.Text(
                    #CREDITS
                    value="~by Baldri4n",
                    text_align=ft.TextAlign.RIGHT,
                    color=ft.colors.BLACK,
                    width=1700,
                )
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
    