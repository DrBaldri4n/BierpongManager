from math import factorial
import flet as ft
import sqlite3 as sql
from updateGame import catchGroupStage, inputGameResults, deleteInputDB
# lets try this with flutter!!

class Database:
        def openDB():
            conn = sql.connect('beerpong.db')
            cur = conn.cursor()
            return cur, conn
    
        def closeDB(conn):
            conn.commit()
            conn.close()

class Table:
        def createRank():
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Team")),
                    ft.DataColumn(ft.Text("Cups")),
                    ft.DataColumn(ft.Text("Points")),
                    ft.DataColumn(ft.Text("Rank")),
                ],
                rows=[]
            )
            return table
        
        def createResult():
             table = ft.DataTable(
                  columns=[
                    ft.DataColumn(ft.Text("TeamA")),
                    ft.DataColumn(ft.Text("TeamB")),
                    ft.DataColumn(ft.Text("Cups")),
                    ft.DataColumn(ft.Text("Cups")),
                  ],
                  rows=[]
             )
             return table
    
        def updateRankRuntime(myTable, groupName, teamName):
            x = myTable
            # Update ranktable in runtime
            
            
        def updateRank(myTable, groupName, teamName):
            teamInfo, _, _ = catchGroupStage(8, "teamInfo")

            myTable.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(teamInfo[groupName][teamName][0])),
                        ft.DataCell(ft.Text(teamInfo[groupName][teamName][1])),
                        ft.DataCell(ft.Text(teamInfo[groupName][teamName][2])),
                        ft.DataCell(ft.Text(teamInfo[groupName][teamName][3])),
                    ]
                )
                
            )
        
        def updateResult(myTable, groupName, teamName, page):
            groupGames = catchGroupStage(8, "groupStage")

            myTable.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(groupGames[groupName][teamName][0])),
                        ft.DataCell(ft.Text(groupGames[groupName][teamName][1])),
                        ft.DataCell(ft.Text(groupGames[groupName][teamName][2])),
                        ft.DataCell(ft.Text(groupGames[groupName][teamName][3])),
                    ],

                    on_select_changed=lambda e: (Button.generateDropDown(e, groupName, 2, myTable, page), Button.generateDropDown(e, groupName,3, myTable, page))
                )
            )

    
class Button:
        def updateButton(e, teamsperGroup, teamname, myTable, page):
            e.control.cells[0].content.value = 
            for num in range(teamsperGroup):
                 Table.updateRank(myTable, 0, num)
                 page.update()
            page.update()

        def editDatabase(e, groupName, myTable):
            allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
            
            # cupsCurr = teamInfo[]

            teamX = e.control.cells[0].content.value
            teamY = e.control.cells[1].content.value
            cupsX = str(e.control.cells[2].content.value)
            cupsY = str(e.control.cells[3].content.value)

            #TODO Über DB prüfen ob erg schon vorhanden
            # wenn ja delete und neu einfügen
            # wenn nein komplett neu einfügen

            if (cupsX == "0" or cupsY == "0"):
                pass
            else:
                inputGameResults(allGroupNames[groupName], teamX, teamY, cupsX, cupsY)

            

            print(teamX, " vs ",teamY, " = ", cupsX, ":", cupsY)


        def generateDropDown(e, groupName, cell, myTable, page):
            def editAndSave(_):
                e.control.cells[cell].content.value = cups.value

                Button.editDatabase(e, groupName, myTable)

                page.remove(cups)
                page.update()

            cups = ft.Dropdown(
                on_change=editAndSave,
                options=[
                    ft.dropdown.Option(0),
                    ft.dropdown.Option(1),
                    ft.dropdown.Option(2),
                    ft.dropdown.Option(3),
                    ft.dropdown.Option(4),
                    ft.dropdown.Option(5),
                    ft.dropdown.Option(6),
                    ft.dropdown.Option(7),
                    ft.dropdown.Option(8),
                    ft.dropdown.Option(9),
                    ft.dropdown.Option(10),
                ],
                width=200,
            )
            page.add(cups)
            



def mainPage(page):
    page.scroll = "always"

    groups = 4 #TODO user setting
    teamsPerGroup = 4
    gamesPerGroup = factorial(teamsPerGroup - 1)

    table1 = Table.createRank()
    for num in range(teamsPerGroup):
        Table.updateRank(table1,0, num)

    updateButton1 = ft.ElevatedButton("update",
        bgcolor="blue",
        color="white",
        on_click=lambda e:Button.updateButton(teamsPerGroup, 0, table1, page)
        )

    table2 = Table.createRank()
    for num in range(teamsPerGroup):
        Table.updateRank(table2, 1,  num)

    updateButton2 = ft.ElevatedButton("update",
        bgcolor="blue",
        color="white",
        on_click=lambda e:Button.updateButton(teamsPerGroup, 0, table2, page)
        )


    table10 = Table.createResult()
    for num in range(gamesPerGroup):
         Table.updateResult(table10,0, num, page)
    table11 = Table.createResult()
    for num in range(gamesPerGroup):
         Table.updateResult(table11,1, num, page)


    page.add(
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            value=f"BEERPONG",
            size=60,
            weight=ft.FontWeight.W_100,
        ),
        ft.Column([
            ft.Row([table1, table2]),
            ft.Row([updateButton1, updateButton2]),
            ft.Row([table10, table11]),
        ]),
    )

if __name__ == "__main__":
    ft.app(target=mainPage)
    page = ft.Page
    mainPage(page)
    
