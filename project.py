################# Imports ####################

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import sqlite3
from db import connect
from get_result import get_result

class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        uic.loadUi('main.ui', self)
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self.handle_buttons()

    ################# Handle the buttons ####################

    def handle_buttons(self):
        self.pushButton_12.clicked.connect(self.browse)
        self.pushButton_6.clicked.connect(self.show_new_test_tab)
        self.pushButton_2.clicked.connect(self.show_show_past_result_tab)
        self.pushButton_8.clicked.connect(self.show_delete_past_result_tab)
        self.pushButton_10.clicked.connect(self.exit)
        self.pushButton_11.clicked.connect(self.new_test)
        self.pushButton_20.clicked.connect(self.show_past_result)
        self.pushButton_21.clicked.connect(self.delete_past_result)

    ################# Open the Tabs ####################

    def show_new_test_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def show_show_past_result_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def show_delete_past_result_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def show_displaying_result_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def exit(self):
        self.close()

    ################# Operations ####################

    def browse(self):
        fname=QFileDialog.getOpenFileName(self, 'Get Path', 'Documents', 'Images (*.jpeg *.jpg *.png)')
        self.lineEdit_10.setText(fname[0])

    def new_test(self):
        name = str(self.lineEdit.text())
        national_id = str(self.lineEdit_7.text()).replace("-", "")
        national_id = national_id.replace(" ", "")
        ray_path = str(self.lineEdit_10.text())
        try:
            warning = QMessageBox.warning(self, 'New Test', "Are you sure to make the test",
                                          QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes:
                if len(national_id) == 14 and len(name) >= 2 and len(ray_path) >= 4:
                    state = get_result(ray_path, "model.h5")
                    if not state:
                        patient_state = "Positive"
                    else:
                        patient_state = "Negative"
                    self.connection = sqlite3.connect('patients.db')
                    self.cursor = self.connection.cursor()
                    self.cursor.execute('''INSERT INTO patients (
                                                                patient_name,
                                                                patient_national_id,
                                                                patient_ray_path,
                                                                patient_state
                                                                )
                                                            VALUES (? , ? , ?, ?)''', (name, national_id, ray_path,
                                                                                       patient_state))

                    self.connection.commit()
                    self.connection.close()
                    self.connection.close()
                    self.lineEdit.setText("")
                    self.lineEdit_7.setText("")
                    self.lineEdit_10.setText("")

                    #Displaying the result#

                    self.connection = sqlite3.connect('patients.db')
                    self.cursor = self.connection.cursor()
                    query = f'''SELECT * FROM patients WHERE
                                                        patient_national_id = {national_id}
                                        '''
                    data = self.cursor.execute(query).fetchall()
                    self.show_displaying_result_tab()
                    self.lineEdit_2.setText(data[0][1])
                    self.lineEdit_8.setText(str(data[0][2]))
                    self.lineEdit_13.setText(data[0][4])
                else:
                    m = QMessageBox(self)
                    m.setWindowTitle("Error")
                    m.setText("please Enter a valid data")
                    m.exec_()

        except:
            m = QMessageBox(self)
            m.setWindowTitle("Error")
            m.setText("Error, please try again in other time")
            m.exec_()

    def show_past_result(self):
        national_id = str(self.lineEdit_11.text()).replace("-", "")
        national_id = national_id.replace(" ", "")
        try:
            self.connection = sqlite3.connect('patients.db')
            self.cursor = self.connection.cursor()
            query = f'''SELECT * FROM patients WHERE
                                    patient_national_id = {national_id}
                    '''
            data = self.cursor.execute(query).fetchall()
            self.connection.close()
            if len(data) == 0:
                m = QMessageBox(self)
                m.setWindowTitle("Error")
                m.setText("Not found, please check the national id")
                m.exec_()
            else:
                self.show_displaying_result_tab()
                self.lineEdit_2.setText(data[0][1])
                self.lineEdit_8.setText(str(data[0][2]))
                self.lineEdit_13.setText(data[0][4])
                self.lineEdit_11.setText("")
        except:
            m = QMessageBox(self)
            m.setWindowTitle("Error")
            m.setText("Error, please check national id or try again later")
            m.exec_()

    def delete_past_result(self):
        national_id = str(self.lineEdit_12.text()).replace("-", "")
        national_id = national_id.replace(" ", "")
        try:
            self.connection = sqlite3.connect('patients.db')
            self.cursor = self.connection.cursor()
            query = f'''SELECT * FROM patients WHERE
                                            patient_national_id = {national_id}
                            '''
            data = self.cursor.execute(query).fetchall()
            self.connection.close()
            if len(data) == 0:
                m = QMessageBox(self)
                m.setWindowTitle("Error")
                m.setText("Not found, please check the national id")
                m.exec_()
            else:
                warning = QMessageBox.warning(self, 'Deleting a result', "Are you sure to delete the result",
                                              QMessageBox.Yes | QMessageBox.No)
                if warning == QMessageBox.Yes:
                    self.connection = sqlite3.connect('patients.db')
                    self.cursor = self.connection.cursor()
                    query = f"DELETE FROM patients WHERE patient_national_id = {national_id}"
                    self.cursor.execute(query)
                    self.connection.commit()
                    self.connection.close()
                    m = QMessageBox(self)
                    m.setWindowTitle("Deleted")
                    m.setText("The result has been deleted.")
                    m.exec_()
                    self.lineEdit_12.setText("")
        except:
            m = QMessageBox(self)
            m.setWindowTitle("Error")
            m.setText("Error, please check national id or try again later")
            m.exec_()


################# Main Function ####################


def main():

    try:
        f = open('patients.db', 'r')
        f.close()
    except:
        connect()

    app = QApplication(sys.argv)
    window = MainApp()
    window.setWindowTitle("Corona checker")
    window.setFixedSize(800, 470)
    window.move(230, 150)
    window.show()
    app.exec_()


if __name__ != '__main__':
    pass
else:
    main()
