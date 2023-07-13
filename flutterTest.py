import flet as ft
import sqlite3 as sql

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
        def createTable():
            myTable = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Team")),
                    ft.DataColumn(ft.Text("Cups")),
                    ft.DataColumn(ft.Text("Points")),
                    ft.DataColumn(ft.Text("Rank")),
                ],
                rows=[]
            )
            return myTable
    
        def addNewData(myTable):
            cur, conn = Database.openDB()

            allGroupNames = ["groupA", "groupB", "groupC", "groupD", "groupE", "groupF", "groupG", "groupH"]
            
            for i in range(8):
                cur.execute("SELECT * FROM " + allGroupNames[i])
                x = cur.fetchall()
                
                print(x[0][0])

                myTable.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(x[0][0])),
                            ft.DataCell(ft.Text(x[0][1])),
                            ft.DataCell(ft.Text(x[0][2])),
                            ft.DataCell(ft.Text(x[0][3])),
                        ]
                    )
                )

            Database.closeDB(conn)

    
class Button:
        def addButton():
            addButton = ft.ElevatedButton(
                "Add new",
                bgcolor="blue",
                color="white",
            )
            return addButton
             


def mainPage(page: ft.Page):
    startTable = Table.createTable()
    Table.addNewData(startTable)

    page.add(
        ft.Column([
            ft.Text("My CRUD sample", size=30, weight="bold"),
            ft.Row([Button.addButton()]),
            startTable
        ]),
    )


if __name__ =="__main__":
    ft.app(target=mainPage)
    mainPage()

