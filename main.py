import secrets
import sqlite3 as sql
import string
import sys
import traceback
import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QListWidgetItem
from PyQt5.uic import loadUi
from email_sender import send_email


class StartWindow(QDialog):
    def __init__(self):
        super(StartWindow, self).__init__()
        loadUi("Start_window.ui", self)
        self.start_but.clicked.connect(self.open_rem_user)

    def open_rem_user(self):
        try:
            with sql.connect("SiBook_db.db") as self.connection:
                self.cursor = self.connection.cursor()
                self.cursor.execute(f"""SELECT book_id FROM users WHERE check_box = 1 """)
                try:
                    rem_per = self.cursor.fetchall()

                    try:
                        if rem_per:
                            try:
                                self.cursor.execute(
                                    f"""SELECT name, surname FROM users WHERE book_id = '{rem_per[0][0]}' """
                                )
                                result = self.cursor.fetchall()[0]
                                name, surname = result[0], result[1]
                                self.book_open(name, surname, rem_per[0][0])
                            except:
                                print(traceback.format_exc())
                        else:
                            try:
                                self.open_log_in()
                            except:
                                print(traceback.format_exc())
                    except:
                        print(traceback.format_exc())
                except:
                    print(traceback.format_exc())
        except:
            print(traceback.format_exc())

    def book_open(self, name, surname, bookid):
        screen4 = PhoneBook(name, surname, bookid)
        widget.addWidget(screen4)
        widget.setFixedWidth(1106)
        widget.setFixedHeight(814)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def open_log_in(self):
        screen1 = Authorization()
        widget.addWidget(screen1)
        widget.setFixedWidth(480)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Authorization(QDialog):
    def __init__(self):
        super(Authorization, self).__init__()
        loadUi("Enter_window.ui", self)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.log_in_but.clicked.connect(self.log_in_func)
        self.sign_up_but.clicked.connect(self.sign_up_func)
        self.exit_but.clicked.connect(self.close_app_func)
        self.remember_box.stateChanged.connect(self.ch_flag)
        self.flag = 0
        self.forget_but.clicked.connect(self.recover_pass)
        self.show_box.stateChanged.connect(self.show_pass)

    def show_pass(self):
        if self.show_box.isChecked():
            self.password_edit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

    def recover_pass(self):
        screen9 = RecoverPassword()
        widget.addWidget(screen9)
        widget.setFixedWidth(625)
        widget.setFixedHeight(420)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def ch_flag(self):
        if self.remember_box.isChecked():
            self.flag = 1
        else:
            self.flag = 0

    def log_in_func(self):
        try:
            login = self.login_edit.text()
            password = self.password_edit.text()
            flag = self.flag
            db = DataBase()
            db.check_user(login, password, flag)
        except Exception:
            print(traceback.format_exc())

    def sign_up_func(self):
        screen2 = Registration()
        widget.addWidget(screen2)
        widget.setFixedWidth(731)
        widget.setFixedHeight(685)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def close_app_func(self):
        sys.exit(app.exec())


class Registration(QDialog):
    def __init__(self):
        super(Registration, self).__init__()
        loadUi("Registration_window.ui", self)
        self.confirm_but.clicked.connect(self.create_account_func)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.rep_pass_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.exit_rec_but.clicked.connect(self.back_func)

    def create_account_func(self):
        db = DataBase()
        name, surname, password = self.name_edit.text(), self.surname_edit.text(), self.password_edit.text()
        email, datebirth = self.mail_edit.text(), self.datebirth_edit.text()
        check = 0
        if password == self.rep_pass_edit.text():
            try:
                db.add_user(name, surname, email, password, datebirth, check)
            except:
                print(traceback.format_exc())

    def back_func(self):
        screen1 = Authorization()
        widget.addWidget(screen1)
        widget.setFixedWidth(480)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DataBase:
    def __init__(self):
        with sql.connect("SiBook_db.db") as self.connection:
            self.cursor = self.connection.cursor()

            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users (
                 name TEXT,
                 surname TEXT,
                 book_id INTEGER,
                 email VARCHAR(255),
                 password VARCHAR(255),
                 date_birth TEXT,
                 check_box  INTEGER
                 )"""
            )

    def add_user(self, name, surname, email, password, datebirth, check):
        bookid = "".join([secrets.choice(string.ascii_letters) for _ in range(10)])
        with sql.connect("SiBook_db.db") as self.connection:
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"""SELECT email FROM users WHERE email = '{email}'""")
            if not self.cursor.fetchall():
                try:
                    if name == "" and surname == "":
                        raise Exception
                    else:
                        self.cursor.execute(
                            f"""INSERT INTO users VALUES ('{name}', '{surname}', '{bookid}', '{email}', '{password}',
                            '{datebirth}', '{check}')"""
                        )
                        self.cursor.execute(
                            f"""SELECT name, surname, book_id, email, password FROM users WHERE email = '{email}' 
                            AND password = '{password}'"""
                        )
                        result = self.cursor.fetchall()[0]
                        name, surname, bookid, email, password = result[0], result[1], result[2], result[3], result[4]
                        self.check_user(email, password, flag=0)
                        self.open_book(name, surname, bookid)
                except:
                    print(traceback.format_exc())
            else:
                self.exist_user()

    def delete_account(self, account, number):
        try:
            with sql.connect("SiBook_db.db") as self.connection:
                self.cursor = self.connection.cursor()
                self.cursor.execute(f"""DELETE FROM '{account}' WHERE phone_number = '{number}'  """)
        except:
            print(traceback.format_exc())

    def change_contact(self, account, first_num, number, name, surname, address, datebirth):

        try:
            print("Начинаем")
            with sql.connect("SiBook_db.db") as self.connection:
                self.cursor = self.connection.cursor()
                try:
                    self.cursor.execute(
                        f"""UPDATE '{account}' 
                        SET name = '{name}', surname = '{surname}', phone_number = '{number}', address = '{address}', date_birth = '{datebirth}' 
                        WHERE phone_number = '{first_num}'  """)
                    self.connection.commit()
                    print(first_num, number)
                except:
                    print(traceback.format_exc())

        except:
            print(traceback.format_exc())

    def open_book(self, name, surname, bookid):
        screen4 = PhoneBook(name, surname, bookid)
        widget.addWidget(screen4)
        widget.setFixedWidth(1106)
        widget.setFixedHeight(814)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def exist_user(self):
        screen3 = ExUser()
        widget.addWidget(screen3)
        widget.setFixedWidth(731)
        widget.setFixedHeight(685)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def check_user(self, email, password, flag):
        with sql.connect("SiBook_db.db") as self.connection:
            self.cursor = self.connection.cursor()
            try:
                self.cursor.execute(f"""SELECT name, surname, book_id, email FROM users WHERE email = '{email}' 
                AND password = '{password}'""")
                result = self.cursor.fetchall()[0]
                name, surname, bookid = result[0], result[1], result[2]
                print(result[2])
                if flag == 1:
                    try:
                        self.cursor.execute(f"""UPDATE users SET check_box = 0 WHERE check_box = 1 """)
                        self.cursor.execute(f"""UPDATE users SET check_box = 1 WHERE book_id = '{bookid}'""")
                    except:
                        print(traceback.format_exc())
                self.create_users_contacts(bookid)
                self.open_book(name, surname, bookid)
            except:
                print(traceback.format_exc())
                self.no_user()

    def no_user(self):
        screen10 = NoUser_log()
        widget.addWidget(screen10)
        widget.setFixedWidth(640)
        widget.setFixedHeight(480)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def create_users_contacts(self, ac_id):
        print("Работаем!")
        with sql.connect("SiBook_db.db") as self.connection:
            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute(
                    f"""CREATE TABLE IF NOT EXISTS '{ac_id}' (
                         name TEXT,
                         surname TEXT,
                         phone_number TEXT,
                         address VARCHAR(255),
                         date_birth TEXT
                         )"""
                )
            except:
                print(traceback.format_exc())
                self.exist_contact()

    def add_new_contact(self, ac_id, name_con, surname_con, number, address, date_birth):
        self.create_users_contacts(ac_id)
        with sql.connect("SiBook_db.db") as self.connection:
            try:
                self.cursor = self.connection.cursor()
                print(ac_id)
                self.cursor.execute(
                    f"""INSERT INTO '{ac_id}' VALUES ('{name_con}', '{surname_con}', '{number}', '{address}',
                                                    '{date_birth}')""")
            except:
                print(traceback.format_exc())
                self.exist_contact()

    def exist_contact(self):
        screen3 = ExUser()
        widget.addWidget(screen3)
        widget.setFixedWidth(640)
        widget.setFixedHeight(480)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def clear_check_flag(self):
        with sql.connect("SiBook_db.db") as self.connection:
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"""UPDATE users SET check_box = 0 WHERE check_box = 1""")


class ExContact(QDialog):
    def __init__(self):
        super(ExContact, self).__init__()
        loadUi("Exist_contact.ui", self)
        self.exit_but.clicked.connect(self.exit_win)

    def exit_win(self):
        screen2 = Authorization()
        widget.addWidget(screen2)
        widget.setFixedWidth(640)
        widget.setFixedHeight(480)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ExUser(QDialog):
    def __init__(self):
        super(ExUser, self).__init__()
        loadUi("Exist_user.ui", self)
        self.exit_but.clicked.connect(self.exit_win)

    def exit_win(self):
        screen2 = Registration()
        widget.addWidget(screen2)
        widget.setFixedWidth(731)
        widget.setFixedHeight(685)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class PhoneBook(QDialog):
    def __init__(self, name, surname, bookid):
        super(PhoneBook, self).__init__()
        loadUi("Main_book.ui", self)
        self.table_list = [self.table_ab, self.table_vg, self.table_de, self.table_jy, self.table_kl, self.table_mn,
                           self.table_op, self.table_rs, self.table_tu, self.table_fh, self.table_csh, self.table_uh,
                           self.table_xyz, self.table_az]
        self.set_column_width()
        self.account_id = bookid
        self.set_account(name, surname)
        self.name = name
        self.surname = surname
        self.add_contact_but.clicked.connect(self.add_contact)
        self.exit_but.clicked.connect(self.come_back)
        self.account_label.clicked.connect(self.open_user_cabinet)
        self.refresh_but.clicked.connect(self.fil_table)
        self.delete_contact_but.clicked.connect(self.del_cont)
        self.change_contact_but.clicked.connect(self.change_contact)

    def del_cont(self):
        number = self.get_data()
        for table in self.table_list:
            row = table.currentRow()
            print(row)
            if row > -1:
                table.removeRow(row)
                table.selectionModel().clearCurrentIndex()
                db = DataBase()
                db.delete_account(self.account_id, number)

    def change_contact(self):
        screen9 = Change_user(self.account_id, self.name, self.surname)
        widget.addWidget(screen9)
        widget.setFixedWidth(731)
        widget.setFixedHeight(685)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def fil_table(self):
        try:
            for table in self.table_list:
                if table == self.table_ab:
                    self.load_data("А", "Б", table)
                elif table == self.table_vg:
                    self.load_data("В", "Г", table)
                elif table == self.table_de:
                    self.load_data("Д", "Е", table)
                    self.load_data("Ё", "ё", table)
                elif table == self.table_jy:
                    self.load_data("Ж", "З", table)
                    self.load_data("И", "Й", table)
                elif table == self.table_kl:
                    self.load_data("К", "Л", table)
                elif table == self.table_mn:
                    self.load_data("М", "Н", table)
                if table == self.table_op:
                    self.load_data("О", "П", table)
                elif table == self.table_rs:
                    self.load_data("Р", "С", table)
                elif table == self.table_tu:
                    self.load_data("Т", "У", table)
                elif table == self.table_fh:
                    self.load_data("Ф", "Х", table)
                elif table == self.table_csh:
                    self.load_data("Ц", "Ч", table)
                    self.load_data("Ш", "Щ", table)
                elif table == self.table_uh:
                    self.load_data("Ъ", "Ы", table)
                    self.load_data("Ь", "Э", table)
                elif table == self.table_xyz:
                    self.load_data("Ю", "Я", table)
                elif table == self.table_az:
                    self.load_data("", "", table)
        except Exception:
            print(traceback.format_exc())

    def load_data(self, letter1, letter2, table):
        if table is not self.table_list[-1]:
            with sql.connect("SiBook_db.db") as self.connection:
                try:
                    table.setRowCount(50)
                    table_row = 0
                    self.cursor = self.connection.cursor()
                    try:
                        for row in self.cursor.execute(
                                f""" SELECT * FROM '{self.account_id}' 
                                WHERE surname LIKE '{letter1}%' 
                                OR surname LIKE '{letter2}%' 
                                ORDER BY surname"""
                        ):
                            table.setItem(table_row, 0, QtWidgets.QTableWidgetItem(row[0]))
                            table.setItem(table_row, 1, QtWidgets.QTableWidgetItem(row[2]))
                            table.setItem(table_row, 2, QtWidgets.QTableWidgetItem(row[4]))
                            table_row += 1
                    except Exception:
                        print(traceback.format_exc())
                except Exception:
                    print(traceback.format_exc())
        else:
            with sql.connect("SiBook_db.db") as self.connection:
                try:
                    table.setRowCount(50)
                    table_row = 0
                    self.cursor = self.connection.cursor()
                    try:
                        for row in self.cursor.execute(
                                f""" SELECT * FROM '{self.account_id}'
                                WHERE surname LIKE 'A%'
                                OR surname LIKE 'B%'
                                OR surname LIKE 'C%'
                                OR surname LIKE 'D%'
                                OR surname LIKE 'E%'
                                OR surname LIKE 'F%'
                                OR surname LIKE 'G%'
                                OR surname LIKE 'H%'
                                OR surname LIKE 'I%'
                                OR surname LIKE 'J%'
                                OR surname LIKE 'K%'
                                OR surname LIKE 'L%'
                                OR surname LIKE 'M%'
                                OR surname LIKE 'N%'
                                OR surname LIKE 'O%'
                                OR surname LIKE 'P%'
                                OR surname LIKE 'Q%'
                                OR surname LIKE 'R%'
                                OR surname LIKE 'S%'
                                OR surname LIKE 'T%'
                                OR surname LIKE 'U%'
                                OR surname LIKE 'V%'
                                OR surname LIKE 'W%'
                                OR surname LIKE 'X%'
                                OR surname LIKE 'Y%'
                                OR surname LIKE 'Z%'
                                ORDER BY surname"""):
                            table.setItem(table_row, 0, QtWidgets.QTableWidgetItem(row[0]))
                            table.setItem(table_row, 1, QtWidgets.QTableWidgetItem(row[2]))
                            table.setItem(table_row, 2, QtWidgets.QTableWidgetItem(row[4]))
                            table_row += 1
                    except Exception:
                        print(traceback.format_exc())
                except Exception:
                    print(traceback.format_exc())

    def come_back(self):
        screen7 = Authorization()
        widget.addWidget(screen7)
        widget.setFixedWidth(480)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def set_account(self, first_name, second_name):
        self.account_label.setText(first_name + " " + second_name)

    def add_contact(self):
        screen5 = AddContact(self.account_id)
        widget.addWidget(screen5)
        widget.setFixedWidth(731)
        widget.setFixedHeight(685)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def set_column_width(self):
        for table in self.table_list:
            table.setColumnWidth(0, 235)
            table.setColumnWidth(1, 219)
            table.setColumnWidth(2, 273)

    def open_user_cabinet(self):
        screen8 = UserCabinet(self.name, self.account_id)
        widget.addWidget(screen8)
        widget.setFixedWidth(910)
        widget.setFixedHeight(623)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class UserCabinet(QDialog):
    def __init__(self, name, user_id):
        super(UserCabinet, self).__init__()
        loadUi("User_cabinet.ui", self)
        self.user_id = user_id
        self.name = name
        self.surname = self.get_data()[2]
        self.email, self.datebirth = self.get_data()[0], datetime.datetime.strptime(self.get_data()[1],
                                                                                    '%d.%m.%Y').date()
        self.name_label.setText(f"{self.name} {self.surname}")
        self.email_label.setText(f"{self.email}")
        self.datebirth_label.setText(f"{self.datebirth}")
        self.exit_but.clicked.connect(self.back)
        self.exit_to_login_but.clicked.connect(self.back_to_login)
        self.birthdays()

    def back_to_login(self):
        screen7 = Authorization()
        widget.addWidget(screen7)
        widget.setFixedWidth(480)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def birthdays(self):
        current_month = self.calendarWidget.monthShown()
        with sql.connect("SiBook_db.db") as connection:
            try:
                self.cursor = connection.cursor()
                result = self.cursor.execute(
                    f"""SELECT name, date_birth, surname 
                    FROM '{self.user_id}' """
                ).fetchall()
                for index in range(len(result)):
                    if f"0{current_month}" == result[index][1][3:5] or f"{current_month}" == result[index][1][3:5]:
                        item = QListWidgetItem(f"{result[index][0]} {result[index][2]} - {result[index][1]}")
                        self.listWidget.addItem(item)

            except :
                print(traceback.format_exc())

    def get_data(self):
        with sql.connect("SiBook_db.db") as connection:
            try:
                self.cursor = connection.cursor()
                self.cursor.execute(
                    f"""SELECT email, date_birth, surname FROM users WHERE book_id = '{self.user_id}' """)
                result = self.cursor.fetchall()[0]
                datetime_obj = datetime.datetime.strptime(result[1], '%d.%m.%Y').date()
                return result
            except :
                print(traceback.format_exc())

    def back(self):
        screen4 = PhoneBook(self.name, self.surname, self.user_id)
        widget.addWidget(screen4)
        widget.setFixedWidth(1106)
        widget.setFixedHeight(814)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AddContact(QDialog):
    def __init__(self, id_user):
        super(AddContact, self).__init__()
        loadUi("Add_contact.ui", self)
        self.confirm_but.clicked.connect(self.new_contact)
        self.exit_add_but.clicked.connect(self.cancel_add)
        self.user_id = id_user

    def cancel_add(self):
        with sql.connect("SiBook_db.db") as self.connection:
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"""SELECT name, surname FROM users WHERE book_id = '{self.user_id}' """)
            result = self.cursor.fetchall()[0]
            name, surname = result[0], result[1]
            self.back_to_book(name, surname, self.user_id)

    def back_to_book(self, name, surname, bookid):
        screen4 = PhoneBook(name, surname, bookid)
        widget.addWidget(screen4)
        widget.setFixedWidth(1106)
        widget.setFixedHeight(814)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def new_contact(self):
        name = self.name_edit.text()
        surname = self.surname_edit.text()
        number = self.number_edit.text()
        address = self.addres_edit.text()
        date_birth = self.datebirth_edit.text()
        db = DataBase()
        db.add_new_contact(self.user_id, name, surname, number, address, date_birth)
        self.cancel_add()


class RecoverPassword(QDialog):
    def __init__(self):
        super(RecoverPassword, self).__init__()
        loadUi("Recovery_password_window.ui", self)
        self.get_code_but.clicked.connect(self.send_code)
        self.exit_but.clicked.connect(self.back)
        self.email = self.email_edit.text()

    def back(self):
        screen_1 = Authorization()
        widget.addWidget(screen_1)
        widget.setFixedWidth(502)
        widget.setFixedHeight(671)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def get_id(self):
        try:
            with sql.connect("SiBook_db.db") as self.connection:
                self.cursor = self.connection.cursor()
                self.cursor.execute(f"""SELECT password FROM users WHERE email = '{self.email_edit.text()}' """)
                result = self.cursor.fetchone()
                if result is None:
                    self.no_user()
                    print("Такого пользователя не существует!")
                else:
                    return result[0]
        except Exception as exc:
            print(traceback.format_exc())

    def send_code(self):
        mail = self.get_id()
        print(mail)
        send_email(rec=self.email_edit.text(), email=mail)

    def no_user(self):
        screen10 = NoUser()
        widget.addWidget(screen10)
        widget.setFixedWidth(640)
        widget.setFixedHeight(480)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class NoUser(QDialog):
    def __init__(self):
        super(NoUser, self).__init__()
        loadUi("No_user.ui", self)
        self.exit_but.clicked.connect(self.back)

    def back(self):
        screen9 = RecoverPassword()
        widget.addWidget(screen9)
        widget.setFixedWidth(625)
        widget.setFixedHeight(420)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class NoUser_log(QDialog):
    def __init__(self):
        super(NoUser_log, self).__init__()
        loadUi("No_user.ui", self)
        self.exit_but.clicked.connect(self.back)

    def back(self):
        screen9 = Authorization()
        widget.addWidget(screen9)
        widget.setFixedWidth(480)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Change_user(QDialog):
    def __init__(self, account, name, surname):
        super(Change_user, self).__init__()
        loadUi("Change_contact.ui", self)
        self.account_id = account
        self.name = name
        self.surname = surname
        self.confirm_but.clicked.connect(self.change_data)
        self.exit_add_but.clicked.connect(self.exit)

    def exit(self):
        screen4 = PhoneBook(self.name, self.surname, self.account_id)
        widget.addWidget(screen4)
        widget.setFixedWidth(1106)
        widget.setFixedHeight(814)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def change_data(self):
        try:
            db = DataBase()
            db.change_contact(
                self.account_id, self.first_num_edit.text(), self.number_edit.text(), self.name_edit.text(),
                self.surname_edit.text(), self.addres_edit.text(), self.datebirth_edit.text())
        except:
            print(traceback.format_exc())
        self.exit()


if __name__ == "__main__":
    db = DataBase()
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    screen1 = StartWindow()
    widget.addWidget(screen1)
    widget.setFixedWidth(907)
    widget.setFixedHeight(629)
    widget.setWindowTitle("SiBook")
    widget.show()
    sys.exit(app.exec())
