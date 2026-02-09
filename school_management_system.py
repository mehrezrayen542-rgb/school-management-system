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
        self.menu12.triggered.connect(self.modifystudentinterface)
        self.edit1.clicked.connect(self.editstudent)
        self.rn1.currentIndexChanged.connect(self.load_student_data)
        self.delete1.clicked.connect(self.delete)
    def delete(self):
        db, cr = connection()
        if db and cr:
           registration=int(self.rn1.currentText())
           
           try:
               qry="DELETE from student where registration_number=?"
               cr.execute(qry,(registration,))
               db.commit()
               try:
                   qry="UPDATE student SET registration_number = registration_number-1 WHERE registration_number > ?"
                   cr.execute(qry, (registration,))
                   db.commit()
                   QMessageBox.information(self,"School Management system","student deleted successfully")
               except:
                   print("erreur ici 1")
                   QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
           except:
               print("erreur ici 2")
               QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
        close_connection(db)
        self.load_registration_numbers()

   
    def load_student_data(self):
       registration = self.rn1.currentText()
       db, cr = connection()
       if db and cr:
           cr.execute("SELECT full_name, gender, date_of_birth, address, phone, email, standard FROM student WHERE registration_number=?", (registration,))
           result = cr.fetchone()
           if result:
               self.fn1.setText(result[0])
               gender = result[1]
               if gender == "male":
                   self.m1.setChecked(True)
               elif gender == "female":
                   self.f1.setChecked(True)
               self.dt1.setText(result[2])
               self.ad1.setPlainText(result[3])
               self.nb1.setText(result[4])
               self.em1.setText(result[5])
               index = self.st1.findText(result[6])
               if index > 0:
                   self.st1.setCurrentIndex(index)
       close_connection(db)

    def load_registration_numbers(self):
       db, cr = connection()
       if db and cr:
           cr.execute("SELECT registration_number FROM student")
           results = cr.fetchall()
           #on continue ici
           self.rn1.clear()  # vide le combo avant de remplir
           for r in results:
              self.rn1.addItem(r[0])
       close_connection(db)

    def clear_form(self):
        self.fn.clear()
        self.nb.clear()
        self.em.clear()
        self.ad.clear()
        self.dt.clear()
        self.st.setCurrentIndex(0)
    def editstudent(self):
        db,cr=connection()
        if not db or not cr:
            print("Error connecting to database")
            return
        ch=""
        value=[]
        registration=self.rn1.currentText()
        #(registration_number,full_name,gender,date_of_birth,address,phone,email,standard)
        if self.fn1.text():
            ch+="full_name=?, "
            value.append(self.fn1.text())
        if self.m1.isChecked() or self.f1.isChecked():
                ch+="gender=?, "
                if self.m1.isChecked():
                    value.append("male")
                elif self.f1.isChecked():
                    value.append("female")
        if self.dt1.text():
            ch+="date_of_birth=?, "
            value.append(self.dt1.text())
        if self.ad1.toPlainText():
            ch+="address=?, "
            value.append(self.ad1.toPlainText())
        if self.nb1.text():
            ch+="phone=?, "
            value.append(self.nb1.text())
        if self.em1.text():
            ch+="email=?, "
            value.append(self.em1.text())
        if self.st1.currentText()!="select standard":
            ch+="standard=? "
            value.append(self.st1.currentText())
        value.append(registration)
        qry="update student set "+ch+" where registration_number=?"
        try:
            cr.execute(qry,value)
            db.commit()
            QMessageBox.information(self,"School Management system","student modified successfully")
        except:
            QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
        close_connection(db)
        self.clear_form()
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
        #(registration,name,gender,address,date,phone_number,standard,email)
        qry="insert into student(registration_number,full_name,gender,date_of_birth,address,phone,email,standard) values(?,?,?,?,?,?,?,?)"
        value=(registration,name,gender,date,address,phone_number,email,standard)
        cr.execute(qry,value)
        db.commit()
        QMessageBox.information(self,"School Management system","student added successfully")
        close_connection(db)
        self.clear_form()
    def addnewstudentinterface(self):
        self.tabWidget.setCurrentIndex(2)
        self.registration_number_new_student()
    def modifystudentinterface(self):
        self.tabWidget.setCurrentIndex(3)
        self.load_registration_numbers()
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
