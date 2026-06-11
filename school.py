import sys
from PyQt5.QtWidgets import QMessageBox,QApplication, QMainWindow
from PyQt5.uic import loadUi
import sqlite3
#sql
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
#qt
class School(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("school.ui", self)        
        # login page
        self.tabWidget.setCurrentIndex(0)
        #self.tabWidget.tabBar().setVisible(False)
        #☺self.menuBar().setVisible(False)
        self.login.clicked.connect(self.login1)
        # add new student page
        self.menu11.triggered.connect(self.addnewstudentinterface)
        self.save.clicked.connect(self.addnewstudent)
        # modify/delete student page 
        self.menu12.triggered.connect(self.modifystudentinterface)
        self.rn1.currentIndexChanged.connect(self.load_student_data)
        self.edit1.clicked.connect(self.editstudent)
        self.delete1.clicked.connect(self.delete)
        # adding mark page
        self.menu21.triggered.connect(self.addmarksinterface)
        self.savemark.clicked.connect(self.savemark1)
        self.getmark.clicked.connect(self.getmark1)
        self.editmark.clicked.connect(self.editmark1)
        self.deletemark.clicked.connect(self.deletemark1)


    def login1(self):
        # getting the user and pwd 
        user = self.user.text()
        pwd = self.pwd.text()
        
        if (user == "admin" and pwd == "admin"):
            self.tabWidget.setCurrentIndex(1) # change the page
            self.menuBar().setVisible(True)
        else:
            QMessageBox.critical(self,"School Management system","incorrect username or password")
    
    def addnewstudentinterface(self):
        self.tabWidget.setCurrentIndex(2)
        self.registration_number_new_student()
    
    def registration_number_new_student(self):
        db,cr=connection()
        if db and cr:
            cr.execute("select * from student")
            result=cr.fetchall()
            if result:
                self.rn.setText(str(len(result)+1))
            else:
                self.rn.setText(str(1))
            self.rn.setReadOnly(True)
        else :
            print("error")
        close_connection(db)
    def addnewstudent(self):
        db,cr = connection()
        if not db or not cr:
            print("Error connecting to database")
            return
        registration = self.rn.text()
        name = self.fn.text()
        date = self.dt.text()
        address = self.ad.toPlainText()
        phone_number = self.nb.text()
        email = self.em.text()
        standard = self.st.currentText()
        if self.m.isChecked():
            gender = "male"
        elif self.f.isChecked():
            gender = "female"
        # (registration,name,gender,address,date,phone_number,standard,email)
        qry = "insert into student(registration_number,full_name,gender,date_of_birth,address,phone,email,standard) values(?,?,?,?,?,?,?,?)"
        value = (registration,name,gender,date,address,phone_number,email,standard)
        cr.execute(qry,value)
        db.commit()
        QMessageBox.information(self,"School Management system","student added successfully")
        close_connection(db)
        self.clear_form()
        self.registration_number_new_student()
        
    def clear_form(self):
        self.fn.clear()
        self.nb.clear()
        self.em.clear()
        self.ad.clear()
        self.dt.clear()
        self.st.setCurrentIndex(0)
    
    def modifystudentinterface(self):
        self.tabWidget.setCurrentIndex(3)
        self.load_registration_numbers(self.rn1)
        self.load_student_data()
        
    def load_registration_numbers(self,combo):
       db, cr = connection()
       if db and cr:
           cr.execute("SELECT registration_number FROM student")
           results = cr.fetchall()
           #on continue ici
           combo.clear()  # vide le combo avant de remplir
           if results :
              for r in results:
                 combo.addItem(r[0])
                 
           else:
              QMessageBox.information(self,"School Management system","An error occurred. There is no student in the database please add new ones")
              self.addnewstudentinterface()

       close_connection(db)
    
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
       #enlever un eleve
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
        self.load_registration_numbers(self.rn1)
    
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
        qry="update student set "+ ch +" where registration_number=?"
        try:
            cr.execute(qry,value)
            db.commit()
            QMessageBox.information(self,"School Management system","student modified successfully")
        except:
            QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
        close_connection(db)
        self.clear_form()
    
    def addmarksinterface(self):
        self.tabWidget.setCurrentIndex(4)
        self.load_registration_numbers(self.rn2)
        self.load_registration_numbers(self.rn3)
    
    def savemark1(self):
        db,cr = connection()
        if not db or not cr:
            print("Error connecting to database")
            return
        registration = int(self.rn2.currentText())
        trimestre = int(self.tr1.text())
        language = int(self.lang1.text())
        english = int(self.eng1.text())
        maths = int(self.math1.text())
        science = int(self.sc1.text())
        social = int(self.soc1.text())
        cr.execute("select * from mark where registration_number=? and trimestre=?",(registration,trimestre))
        result=cr.fetchall()
        if result:
            QMessageBox.information(self,"School Management system","this trimestre is already written , please try another trimestre or try to modify it")
        else:
            qry = "insert into mark(registration_number,trimestre,language,english,maths,science,social) values(?,?,?,?,?,?,?)"
            value = (registration,trimestre,language,english,maths,science,social)
            cr.execute(qry,value)
            db.commit()
            QMessageBox.information(self,"School Management system","marks added successfully")
            close_connection(db)
        self.rn2.setCurrentIndex(0)
        self.tr1.clear()
        self.lang1.clear()
        self.eng1.clear()
        self.math1.clear()
        self.sc1.clear()
        self.soc1.clear()
    
    def getmark1(self):
        db,cr = connection()
        if not db or not cr:
            print("Error connecting to database")
            return
        registration = int(self.rn3.currentText())
        trimestre = int(self.tr2.currentText())
        cr.execute("select language,english,maths,science,social from mark where registration_number=? and trimestre=?",(registration,trimestre))
        result=cr.fetchone()
        if result:
            self.lang2.setText(str(result[0]))
            self.eng2.setText(str(result[1]))
            self.math2.setText(str(result[2]))
            self.sc2.setText(str(result[3]))
            self.soc2.setText(str(result[4]))
        else:
            QMessageBox.information(self,"School Management system","this trimestre does not exist in this database , please try another trimestre or try another student")
    
    def editmark1(self):
        db,cr=connection()
        if not db or not cr:
            print("Error connecting to database")
            return
        registration = int(self.rn3.currentText())
        trimestre = int(self.tr2.currentText())
        language = int(self.lang2.text())
        english = int(self.eng2.text())
        maths = int(self.math2.text())
        science = int(self.sc2.text())
        social = int(self.soc2.text())
        qry = "update mark set language=?,english=?,maths=?,science=?,social=?  where registration_number=? and trimestre=?"
        value = (language,english,maths,science,social,registration,trimestre)
        try:
            cr.execute(qry,value)
            db.commit()
            QMessageBox.information(self,"School Management system","marks modified successfully")
        except:
            QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
        close_connection(db)
        self.clearmarks()
    
    def deletemark1(self):
        db, cr = connection()
        if db and cr:
           registration=int(self.rn3.currentText())
           trimestre=int(self.tr2.currentText())
           try:
               qry="DELETE from mark where registration_number=? and trimestre=?" 
               cr.execute(qry,(registration,trimestre))
               db.commit()
               QMessageBox.information(self,"School Management system","marks deleted successfully")

           except:
               QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
        close_connection(db)
        self.clearmarks()

    def clearmarks(self):
        self.lang2.clear()
        self.eng2.clear()
        self.math2.clear()
        self.sc2.clear()
        self.soc2.clear()
        self.rn3.setCurrentIndex(0)
        self.tr2.setCurrentIndex(0)
def main():
    app = QApplication(sys.argv)
    window = School()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

