import sys
from PyQt5.QtWidgets import QMessageBox,QApplication, QMainWindow
from PyQt5.uic import loadUi
import sqlite3
class School(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("school.ui", self)
        
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menuBar().setVisible(False)
        self.login.clicked.connect(self.login1)
        self.menu11.triggered.connect(self.addnewstudent)
    def addnewstudent(self):
        self.tabWidget.setCurrentIndex(2)
        self.connection()
    def login1(self):
        user=self.user.text()
        pwd=self.pwd.text()
        if (user=="admin" and pwd=="admin"):
            self.tabWidget.setCurrentIndex(1)
            self.menuBar().setVisible(True)
        else:
            QMessageBox.critical(self,"School Management system","incorrect username or password")
    def connection(self):
        try:
            db=sqlite3.connect("school.db")
            cr=db.cursor()
            cr.execute("select * from student")
            result=cr.fetchall()
            if result:
                self.rn.setText(str(len(result)+1))
            else:
                self.rn.setText(str(1))
        except:
            print("error")
 
def main():
    app = QApplication(sys.argv)
    window = School()
    window.show()
    sys.exit(app.exec_())
	

if __name__ == "__main__":
    main()
