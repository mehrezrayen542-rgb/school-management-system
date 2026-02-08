import sys
from PyQt5.QtWidgets import QMessageBox,QApplication, QMainWindow
from PyQt5.uic import loadUi
import sqlite3
def connection():
    try:
        global db
        db=sqlite3.connect("school.db")
        cr=db.cursor()
        return db, cr
    except sqlite3.Error as er:
        print("Error connecting to SQLite:", er)
        return None, None
    except:
        print("error")
def close_connection(db):
    if db :
       db.close()
class School(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("school.ui", self)
        
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menuBar().setVisible(False)
        self.login.clicked.connect(self.login1)
        self.menu11.triggered.connect(self.addnewstudentinterface)
        self.save.clicked.connect(self.addnewstudent)
    def addnewstudent(self):
        db,cr=connection()
        if not db or not cr:
            print("Error connecting to database")
            return
        registration=self.rn.text()
        name=self.fn.text()
        date=self.dt.text()
        address=self.ad.toPlainText()
        phone_number=self.nb.text()
        email=self.em.text()
        standard=self.st.currentText()
        if self.m.isChecked():
            gender="male"
        elif self.f.isChecked():
            gender="female"
        (registration,name,gender,address,date,phone_number,standard,email)
        qry="insert into student(registration_number,full_name,gender,date_of_birth,address,phone,email,standard) values(?,?,?,?,?,?,?,?)"
        value=(registration,name,gender,date,address,phone_number,email,standard)
        cr.execute(qry,value)
        db.commit()
        
        close_connection(db)
    def addnewstudentinterface(self):
        self.tabWidget.setCurrentIndex(2)
        self.registration_number_new_student()
    def login1(self):
        user=self.user.text()
        pwd=self.pwd.text()
        if (user=="admin" and pwd=="admin"):
            self.tabWidget.setCurrentIndex(1)
            self.menuBar().setVisible(True)
        else:
            QMessageBox.critical(self,"School Management system","incorrect username or password")
    def registration_number_new_student(self):
        db,cr=connection()
        if db and cr:
            cr.execute("select * from student")
            result=cr.fetchall()
            if result:
                self.rn.setText(str(len(result)+1))
            else:
                self.rn.setText(str(1))
        else :
            print("error")
        close_connection(db)
 
def main():
    app = QApplication(sys.argv)
    window = School()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
