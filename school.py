import sys
from PyQt5.QtWidgets import QMessageBox,QApplication, QMainWindow , QTableWidgetItem
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
        self.tabWidget.tabBar().setVisible(False)
        self.menuBar().setVisible(False)
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
        self.menu31.triggered.connect(self.addattendanceinterface)
        self.saveattendance.clicked.connect(self.saveattendance1)
        self.getattendance.clicked.connect(self.getattendance1)
        self.rn5.currentIndexChanged.connect(self.load_date)
        self.editattendance.clicked.connect(self.editattendance1)
        self.deleteattendance.clicked.connect(self.deleteattendance1)
        self.menu41.triggered.connect(self.feesinterface)
        self.savefees.clicked.connect(self.savefees1)
        self.receipt2.currentIndexChanged.connect(self.changeregistration)
        self.getfees.clicked.connect(self.getfees1)
        self.deletefees.clicked.connect(self.deletefees1)
        self.editfees.clicked.connect(self.edit_fees1)
        self.menu51.triggered.connect(self.show_students)
        self.menu52.triggered.connect(self.show_marks)
        self.menu53.triggered.connect(self.show_attendance_details)
        self.menu54.triggered.connect(self.show_fees)
        self.menu61.triggered.connect(QApplication.quit)



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
                   QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
           
           except:
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
        
    def addattendanceinterface(self):
        self.tabWidget.setCurrentIndex(5)
        self.load_registration_numbers(self.rn4)
        self.load_registration_numbers(self.rn5)
        
    def saveattendance1(self):
        
        db,cr = connection()
        
        if not db or not cr:
            print("Error connecting to database")
            return
        
        registration = int(self.rn4.currentText())
        date = self.date1.text()
        morning = self.morn1.text()
        evening = self.even1.text()
        
        cr.execute("select * from attendance where registration_number=? and attendance_date=?",(registration,date))
        result=cr.fetchall()
        
        if result:
            
            QMessageBox.information(self,"School Management system","the attendance details for this day is already written , please try another trimestre or try to modify it")
        
        else:
            
            qry = "insert into attendance(registration_number,attendance_date,morning,evening) values(?,?,?,?)"
            value = (registration,date,morning,evening)
            cr.execute(qry,value)
            db.commit()
            QMessageBox.information(self,"School Management system","attendance details added successfully")
            close_connection(db)
        self.rn4.setCurrentIndex(0)
        self.morn1.clear()
        self.date1.clear()
        self.even1.clear()

    def getattendance1(self):
        db,cr = connection()
        
        if not db or not cr:
            print("Error connecting to database")
            return
        
        registration = int(self.rn5.currentText())
        date = self.date2.currentText()
        
        cr.execute("select morning,evening from attendance where registration_number=? and attendance_date=?",(registration,date))
        result=cr.fetchone()
        
        if result:
            
            self.morn2.setText(str(result[0]))
            self.even2.setText(str(result[1]))
        
        else:    
            QMessageBox.information(self,"School Management system","this date  does not exist in this database , please try another date or try another student")
    
    def load_date(self):
       registration = int(self.rn5.currentText())
       db, cr = connection()
       
       if db and cr:
           cr.execute("SELECT attendance_date FROM attendance where registration_number=?",(registration,))
           results = cr.fetchall()
           #on continue ici
           self.date2.clear()  # vide le combo avant de remplir
           
           if results :
              for r in results:
                 self.date2.addItem(r[0])
                 
           else:
              
              QMessageBox.information(self,"School Management system","An error occurred. There is no date in the database please add new ones")

       close_connection(db)
    def editattendance1(self):
        db,cr=connection()
        
        if not db or not cr:
            print("Error connecting to database")
            return
        
        registration = int(self.rn5.currentText())
        date = self.date2.currentText()
        morning = self.morn2.text()
        evening = self.even2.text()
        
        qry = "update attendance set morning=?,evening=? where registration_number=? and attendance_date=?"
        value = (morning,evening,registration,date)
        
        try:
            cr.execute(qry,value)
            db.commit()
            QMessageBox.information(self,"School Management system","attendance details modified successfully")
        
        except:
            
            QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
        
        close_connection(db)
        
        self.rn5.setCurrentIndex(0)
        self.morn2.clear()
        self.date2.setCurrentIndex(0)
        self.even2.clear()
        
    def deleteattendance1(self):
        db, cr = connection()
        
        if db and cr:
           
           registration=int(self.rn5.currentText())
           date = self.date2.currentText()
           
           try:
               qry="DELETE from attendance where registration_number=? and attendance_date=?" 
               cr.execute(qry,(registration,date))
               db.commit()
               QMessageBox.information(self,"School Management system","attendance details deleted successfully")

           except:
               QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
        
        close_connection(db)
        self.rn5.setCurrentIndex(0)
        self.morn2.clear()
        self.date2.clear()
        load_date(self)
        self.even2.clear()
        
    def feesinterface(self):
        self.tabWidget.setCurrentIndex(6)
        self.load_registration_numbers(self.rn6)
        self.receipt_number()
        self.load_receipt()
        self.rn7.setDisabled(True)
        
    def receipt_number(self):
        db,cr=connection()
        
        if db and cr:
            cr.execute("select * from fees")
            result=cr.fetchall()
            
            if result:
                self.receipt1.setText(str(len(result)+1))
            
            else:
                self.receipt1.setText(str(1))
            
            self.receipt1.setReadOnly(True)
        else :
            print("error")
            
        close_connection(db)
        
    def savefees1(self):
        db,cr = connection()
        
        if not db or not cr:
            print("Error connecting to database")
            return
        
        receipt = int(self.receipt1.text())
        registration = int(self.rn6.currentText())
        reason = self.reason1.text()
        amount = self.amount1.text()
        date = self.payementdate1.text()
        
        qry = "insert into fees(registration_number,receipt_number,reason,amount,fees_date) values(?,?,?,?,?)"
        value = (registration,receipt,reason,amount,date)
        cr.execute(qry,value)
        db.commit()
        QMessageBox.information(self,"School Management system","fees details added successfully")
        
        close_connection(db)
        
        self.rn6.setCurrentIndex(0)
        self.receipt1.setText(str(receipt+1))
        self.reason1.clear()
        self.amount1.clear()
        self.payementdate1.clear()
        self.load_receipt()
        
    def load_receipt(self):
        db, cr = connection()
        
        if db and cr:
            cr.execute("SELECT receipt_number FROM fees ")
            results = cr.fetchall()
            #on continue ici
            self.receipt2.clear()  # vide le combo avant de remplir
            
            if results :
               
               for r in results:
                  self.receipt2.addItem(r[0])
                 
            else:
               QMessageBox.information(self,"School Management system","An error occurred. There is no fees in the database please add new ones")
            
        close_connection(db)
        
    def changeregistration(self):
        db, cr = connection()
        
        receipt = self.receipt2.currentText()
        
        if db and cr:
            
            if not receipt:
               self.rn7.clear()
               close_connection(db)
               return
            
            receipt = int(receipt)
            
            cr.execute("SELECT registration_number from fees where receipt_number=? ",(receipt,))
            results = cr.fetchone()
            
            if results :
               self.rn7.setText(results[0])
                 
            else:
               
               QMessageBox.information(self,"School Management system","An error occurred. There is no registration number for this receipt in the database please add new ones")

        close_connection(db)
        
    def getfees1(self):
        db,cr = connection()
        
        if not db or not cr:
            print("Error connecting to database")
            return
        
        registration = int(self.rn7.text())
        receipt = int(self.receipt2.currentText())
        
        cr.execute("select reason,amount,fees_date from fees where registration_number=? and receipt_number=?",(registration,receipt))
        result=cr.fetchone()
        
        if result:
            self.reason2.setText(str(result[0]))
            self.amount2.setText(str(result[1]))
            self.payementdate2.setText(str(result[2]))
            
        else:
            QMessageBox.information(self,"School Management system","this receipt number  does not exist in this database , please try another date or try another student")
            
    def deletefees1(self):
        db, cr = connection()
        
        if db and cr:
           receipt = int(self.receipt2.currentText())
           
           try:
               
               qry="DELETE from fees where receipt_number=?"
               cr.execute(qry,(receipt,))
               db.commit()
               QMessageBox.information(self,"School Management system","fees details deleted successfully")
               
           except:
               QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
        close_connection(db)
        
        self.reason2.clear()
        self.amount2.clear()
        self.payementdate2.clear()
        self.rn7.clear()
        self.load_receipt()
        self.changeregistration()
        
    def editfees1(self):
        db,cr=connection()
        
        if not db or not cr:
            print("Error connecting to database")
            return
        
        receipt = int(self.receipt2.currentText())
        reason = self.reason2.text()
        amount = self.amount2.text()
        date = self.payementdate2.text()
        qry = "update fees set reason=?,amount=?,fees_date=? where receipt_number=?"
        value = (reason,amount,date,receipt)
        
        try:
            cr.execute(qry,value)
            db.commit()
            QMessageBox.information(self,"School Management system","fees details modified successfully")
        except:
            QMessageBox.information(self,"School Management system","An error occurred. Please check the entered information and try again.")
        
        close_connection(db)
        
        self.reason2.clear()
        self.amount2.clear()
        self.payementdate2.clear()
        self.rn7.clear()
        self.load_receipt()
        self.changeregistration()
    
    def load_students(self):
        db, cr = connection()
        cr.execute(""" SELECT registration_number,full_name,gender,date_of_birth,address,phone,email,standard FROM student""")
        students = cr.fetchall()

        self.tableWidget.setRowCount(len(students))

        for row, student in enumerate(students):
            for col, value in enumerate(student):
                self.tableWidget.setItem(row,col,QTableWidgetItem(str(value)))

        close_connection(db)
        
    def show_students(self):
        self.tabWidget.setCurrentIndex(7)
        self.load_students()
        
    def load_marks(self):
        db, cr = connection()
        cr.execute(""" SELECT registration_number,trimestre,(language+english+maths+science+social)/5,language,english,maths,science,social FROM mark""")
        result = cr.fetchall()
        self.tableWidget2.setRowCount(len(result))
        for row, marks in enumerate(result):
            for col, value in enumerate(marks):
                self.tableWidget2.setItem(row , col , QTableWidgetItem("          "+str(value)+"  "))

        close_connection(db)
        
    def show_marks(self):
        self.tabWidget.setCurrentIndex(8)
        self.load_marks()
        
    def load_attendance_details(self):
        db, cr = connection()
        cr.execute(""" SELECT registration_number,attendance_date,morning,evening FROM attendance""")
        result = cr.fetchall()
        self.tableWidget3.setRowCount(len(result))
        for row, attendance in enumerate(result):
            for col, value in enumerate(attendance):
                self.tableWidget3.setItem(row,col,QTableWidgetItem("          "+str(value)+"  "))

        close_connection(db)
    def load_fees(self):
        db, cr = connection()
        cr.execute(""" SELECT registration_number,receipt_number,reason,amount,fees_date FROM fees""")
        result = cr.fetchall()
        self.tableWidget4.setRowCount(len(result))
        for row, fees in enumerate(result):
            for col, value in enumerate(fees):
                self.tableWidget4.setItem(row,col,QTableWidgetItem("          "+str(value)+"  "))

        close_connection(db)
        
    def show_attendance_details(self):
        self.tabWidget.setCurrentIndex(9)
        self.load_attendance_details()
        
    def show_fees(self):
        self.tabWidget.setCurrentIndex(10)
        self.load_fees()

def main():
    app = QApplication(sys.argv)
    window = School()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

