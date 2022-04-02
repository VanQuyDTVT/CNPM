import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Tools import user, product, search, history, Ultilities
import numpy as np
from Tools.create_print_file import print_bill

now_id = None
type_window = True


def dot(number):
    first = True
    while number > 0:
        e = 1000
        t = number % e
        if t == 0:
            t = '000'
        if first:
            result = str(t)
        else:
            result = str(t) + "." + result

        number = number - int(t)
        number = int(number / e)
        first = False

    return result


def goto_menu():
    menu = MenuScreen()
    widget.addWidget(menu)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_sell():
    sell = SellScreen()
    widget.addWidget(sell)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_view_stock():
    view_stock = ViewStockScreen()
    widget.addWidget(view_stock)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_import_export():
    import_export = ImportExportScreen()
    widget.addWidget(import_export)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_shift_sumary():
    shift_sumary = ShiftSummaryScreen()
    widget.addWidget(shift_sumary)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_signup():
    signup = SignUpScreen()
    widget.addWidget(signup)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_view_history():
    view_history = ViewHistoryScreen()
    widget.addWidget(view_history)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def _logout():
    global now_id
    now_id = None
    logout = LoginScreen()
    widget.addWidget(logout)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def btn_close_clicked():
    widget.close()


def btn_max_clicked():
    global type_window

    if type_window:
        widget.showMinimized()
        widget.showMaximized()
        type_window = False

    else:
        type_window = True
        widget.setGeometry(int((size.width() - size_app[0]) / 2), int((size.height() - size_app[1]) / 2),
                           size_app[0], size_app[1])


def btn_min_clicked(self):
    widget.showMinimized()


class LoginScreen(QMainWindow):

    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("./GUI/login.ui", self)
        self.login.clicked.connect(self._login)
        self.username.installEventFilter(self)
        self.password.installEventFilter(self)
        self.showPassword.clicked.connect(self._show_password)
        self.login.installEventFilter(self)
        self.border.installEventFilter(self)
        self.close_btn.clicked.connect(self.show_popup_turn_off)

        self.yes_btn.clicked.connect(btn_close_clicked)
        self.no_btn.clicked.connect(self.hide_popup_turn_off)

        self.yes_btn.installEventFilter(self)
        self.no_btn.installEventFilter(self)
        self.close_btn.installEventFilter(self)

        w = self.widget_close.width()
        h = self.widget_close.height()
        self.widget_close.setGeometry(0, 0, w, h)

        self.setTabOrder(self.username, self.password)

        self.icon_emotion.setPixmap(QPixmap('./Image/sad.png'))

        self.widget_close.setHidden(True)

    def show_popup_turn_off(self):
        self.widget_close.setHidden(False)

        effect = QGraphicsDropShadowEffect()
        effect.setOffset(0, 0)
        effect.setColor(QColor(255, 255, 255))
        effect.setBlurRadius(20)

        self.border.setStyleSheet("background-color: #555")
        self.login.setStyleSheet("color: #555")

        self.border_2.setGraphicsEffect(effect)

    def hide_popup_turn_off(self):
        self.widget_close.setHidden(True)
        self.border.setStyleSheet("background-color: #fff")
        self.login.setStyleSheet("color: #fff")

    def on_hovered(self):
        self.login.setStyleSheet("""
            background-color: #000;
            """)

    def hover_out(self):
        self.login.setStyleSheet("""
            background-color: #333;
            """)

    def _show_password(self):
        if self.showPassword.isChecked():
            self.password.setEchoMode(QLineEdit.Password)
        else:
            self.password.setEchoMode(QLineEdit.Normal)

    def eventFilter(self, widget, event):
        if widget == self.login and event.type() == QtCore.QEvent.HoverEnter:
            self.on_hovered()
        elif widget == self.login and event.type() == QtCore.QEvent.HoverLeave:
            self.hover_out()

        elif widget == self.yes_btn and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/check-red.svg"))
            self.icon_emotion.setPixmap(QPixmap('./Image/sad.png'))
            self.label_3.setText("Goodbye")
        elif widget == self.yes_btn and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/check-black.svg"))
            self.icon_emotion.setPixmap(QPixmap('./Image/happy.png'))
            self.label_3.setText("Close")

        elif widget == self.no_btn and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/x-dark_blue.svg"))
            self.icon_emotion.setPixmap(QPixmap('./Image/happy.png'))
            self.label_3.setText("Welcome")
        elif widget == self.no_btn and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/x-black.svg"))
            self.icon_emotion.setPixmap(QPixmap('./Image/sad.png'))
            self.label_3.setText("Close")

        elif widget == self.close_btn and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/power-red.svg"))
        elif widget == self.close_btn and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/power-black.svg"))

        if self.username.text() != "":
            self.label.setText("")
            self.user.setText("Username")
        else:
            self.label.setText("Type Username")
            self.user.setText("")

        if self.password.text() != "":
            self.label_2.setText("")
            self.passw.setText("Password")
        else:
            self.label_2.setText("Type Password")
            self.passw.setText("")
        return False

    def _login(self):
        input_username = self.username.text()
        input_password = self.password.text()
        state = user.login(input_username, input_password)
        global now_id
        if state[0] == 'false':
            now_id = None
            self.status.setText("Username or password is wrong !!!")

        else:
            now_id = state[1]
            goto_menu()


class MenuScreen(QMainWindow):
    def __init__(self):
        data = user.find_id(now_id)
        super(MenuScreen, self).__init__()

        loadUi("./GUI/menu.ui", self)
        self.setMinimumSize(1080, 300)
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))

        self.status_title.setText("")

        self.minimize_btn.clicked.connect(btn_min_clicked)
        self.maximize_btn.clicked.connect(btn_max_clicked)
        self.close_btn.clicked.connect(btn_close_clicked)

        self.log_out.clicked.connect(_logout)
        self.signup.clicked.connect(goto_signup)
        self.sell_button.clicked.connect(goto_sell)
        self.view_stock_btn.clicked.connect(goto_view_stock)
        self.shift_summary_btn.clicked.connect(goto_shift_sumary)
        self.view_history_btn.clicked.connect(goto_view_history)
        self.import_export_btn.clicked.connect(goto_import_export)

        self.signup.installEventFilter(self)
        self.sell_button.installEventFilter(self)
        self.view_stock_btn.installEventFilter(self)
        self.shift_summary_btn.installEventFilter(self)
        self.view_history_btn.installEventFilter(self)
        self.import_export_btn.installEventFilter(self)

        self.close_btn.installEventFilter(self)
        self.log_out.installEventFilter(self)
        self.minimize_btn.installEventFilter(self)
        self.maximize_btn.installEventFilter(self)

        self.start = QPoint(0, 0)
        self.pressing = False

        QSizeGrip(self.size_grip)

    icons_maximize = './icons/square-white.svg'

    def eventFilter(self, widget, event):
        if widget == self.minimize_btn and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/minus-dark_blue.svg"))
        elif widget == self.minimize_btn and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/minus-white.svg"))

        elif widget == self.maximize_btn and event.type() == QtCore.QEvent.HoverEnter:
            if type_window:
                self.icons_maximize = "./icons/square-dark_blue.svg"
            else:
                self.icons_maximize = "./icons/minimize-dark_blue.svg"
        elif widget == self.maximize_btn and event.type() == QtCore.QEvent.HoverLeave:
            if type_window:
                self.icons_maximize = "./icons/square-white.svg"
            else:
                self.icons_maximize = "./icons/minimize-white.svg"

        elif widget == self.log_out and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/log-out-red.svg"))
        elif widget == self.log_out and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/log-out-white.svg"))

        elif widget == self.close_btn and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/x-red.svg"))
        elif widget == self.close_btn and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/x-white.svg"))
        else:
            self.maximize_btn.setIcon(QIcon(self.icons_maximize))

            if event.type() == QtCore.QEvent.HoverEnter:
                widget.setStyleSheet("""
                                background-color: #070725;
                                """)
            if event.type() == QtCore.QEvent.HoverLeave:
                widget.setStyleSheet("""
                                background-color: #14142c;
                                """)

        return False

    def resizeEvent(self, QResizeEvent):
        super(MenuScreen, self).resizeEvent(QResizeEvent)

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            widget.setGeometry(self.mapToGlobal(self.movement).x(),
                               self.mapToGlobal(self.movement).y(),
                               widget.width(),
                               widget.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


class SignUpScreen(QMainWindow):
    c_fullname = pyqtSignal()
    c_birthday = pyqtSignal()
    c_phone = pyqtSignal()
    c_username = pyqtSignal()
    c_password = pyqtSignal()
    c_identification = pyqtSignal()

    def __init__(self):
        data = user.find_id(now_id)
        super(SignUpScreen, self).__init__()
        loadUi("./GUI/Signup.ui", self)

        self.fullname.installEventFilter(self)
        self.birthday.installEventFilter(self)
        self.phone.installEventFilter(self)
        self.username.installEventFilter(self)
        self.password.installEventFilter(self)
        self.identification.installEventFilter(self)

        self.c_fullname.connect(self.type_fullname)
        self.c_birthday.connect(self.type_birthday)
        self.c_phone.connect(self.type_phone)
        self.c_username.connect(self.type_username)
        self.c_password.connect(self.type_password)
        self.c_identification.connect(self.type_identification)

        self.btn_create.clicked.connect(self._signup)
        self.returnHome.clicked.connect(goto_menu)

    def _signup(self):
        fullname = self.fullname.text()
        birthday = self.birthday.text()
        phone = self.phone.text()
        position = self.position.currentText()
        position = position.strip(' ')
        username = self.username.text()
        password = self.password.text()
        identification = self.identification.text()
        invalid = 0
        if fullname == '' or fullname == 'Full name' or fullname == 'Enter the name!':
            self.fullname.setText("Enter the name!")
            self.fullname.setStyleSheet(self.style_text_error)
        else:
            invalid += 1
        if birthday == '' or birthday == 'Birthday' or birthday == 'dd/mm/yyyy':
            self.birthday.setText("dd/mm/yyyy")
            self.birthday.setStyleSheet(self.style_text_error)
        else:
            date = birthday.split('/')
            if len(date) != 3:
                self.birthday.setText("dd/mm/yyyy")
                self.birthday.setStyleSheet(self.style_text_error)
            else:
                temp = 3
                if int(date[0]) > 31:
                    temp -= 1
                if int(date[1]) > 12:
                    temp -= 1
                if int(date[2]) < 1800 or int(date[2]) > 2022:
                    temp -= 1
            if temp == 3:
                invalid += 1
            else:
                self.birthday.setStyleSheet(self.style_text_error)

        if invalid == 2:
            user.add_member(fullname, username, password, birthday, position, phone, identification)
            self.status.setText("Sign up for <b>" + fullname + "</b> successful!")
            self.status.setStyleSheet("""
                color: rgb(50,255,50);
            """)
        else:
            self.status.setText("Invalid information provided!")
            self.status.setStyleSheet("""
                            color: rgb(255,50,50);
                        """)

    style_text_input = """
                font: 87 "Arial Black";
                background-color: rgb(1, 67, 97);
                border-style:solid;
                border-radius: 5px;
                gridline-color: rgb(255, 0, 0);
                border-bottom-color: rgb(255, 0, 0);
                alternate-background-color: rgba(255, 255, 255, 0); 
                color: rgb(255, 255, 255);
                border-color: rgba(255, 255, 255, 0);
                gridline-color: rgba(255, 255, 255, 0);
            """

    style_text_error = """
                    font: 87 "Arial Black";
                    background-color: rgb(1, 67, 97);
                    border-style:solid;
                    border-radius: 5px;
                    gridline-color: rgb(255, 0, 0);
                    border-bottom-color: rgb(255, 0, 0);
                    alternate-background-color: rgba(255, 255, 255, 0); 
                    color: rgb(255, 30, 30);
                    border-color: rgba(255, 255, 255, 0);
                    gridline-color: rgba(255, 255, 255, 0);
                """

    def type_fullname(self):
        self.fullname.clear()
        self.fullname.setStyleSheet(self.style_text_input)

    def type_birthday(self):
        self.birthday.clear()
        self.birthday.setStyleSheet(self.style_text_input)

    def type_phone(self):
        self.phone.clear()
        self.phone.setStyleSheet(self.style_text_input)

    def type_username(self):
        self.username.clear()
        self.username.setStyleSheet(self.style_text_input)

    def type_password(self):
        self.password.clear()
        self.password.setStyleSheet(self.style_text_input)

    def type_identification(self):
        self.identification.clear()
        self.identification.setStyleSheet(self.style_text_input)

    temp = 0

    def eventFilter(self, widget, event):
        birth = self.birthday.text()
        if birth == '' or birth == 'Birthday' or birth == 'dd/mm/yyyy':
            # do nothing
            None
        elif birth[-1] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/'}:
            birth = birth[0:len(birth) - 1]
            self.birthday.setText(birth)

        if self.temp < len(birth):
            if len(birth) == 2 or len(birth) == 5:
                self.birthday.setText(birth + '/')
            elif len(birth) > 10:
                self.birthday.setText(birth[0:10])

        if len(birth) != self.temp:
            self.temp = len(birth)

        if widget == self.fullname:
            if event.type() == QEvent.FocusOut:
                pass
            elif event.type() == QEvent.FocusIn:
                self.c_fullname.emit()  # When the focus falls again, edit Enter the box, send clicked Signal out
            else:
                pass
        if widget == self.birthday:
            if event.type() == QEvent.FocusOut:
                pass
            elif event.type() == QEvent.FocusIn:
                self.c_birthday.emit()  # When the focus falls again, edit Enter the box, send clicked Signal out
            else:
                pass
        if widget == self.phone:
            if event.type() == QEvent.FocusOut:
                pass
            elif event.type() == QEvent.FocusIn:
                self.c_phone.emit()  # When the focus falls again, edit Enter the box, send clicked Signal out
            else:
                pass
        if widget == self.username:
            if event.type() == QEvent.FocusOut:
                pass
            elif event.type() == QEvent.FocusIn:
                self.c_username.emit()  # When the focus falls again, edit Enter the box, send clicked Signal out
            else:
                pass
        if widget == self.password:
            if event.type() == QEvent.FocusOut:
                pass
            elif event.type() == QEvent.FocusIn:
                self.c_password.emit()  # When the focus falls again, edit Enter the box, send clicked Signal out
            else:
                pass
        if widget == self.identification:
            if event.type() == QEvent.FocusOut:
                pass
            elif event.type() == QEvent.FocusIn:
                self.c_identification.emit()  # When the focus falls again, edit Enter the box, send clicked Signal out
            else:
                pass
        return False


class SellScreen(QMainWindow):
    c_search_box = pyqtSignal()
    bill = list()
    discount = 0
    tax = 0
    text_search_temp = ".none--"
    icons_maximize = './icons/square-white.svg'

    def __init__(self):
        data = user.find_id(now_id)
        super(SellScreen, self).__init__()
        loadUi("./GUI/Sell.ui", self)

        # title app
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.status_title.setText("Sell")
        self.minimize_btn.clicked.connect(btn_min_clicked)
        self.maximize_btn.clicked.connect(btn_max_clicked)
        self.close_btn.clicked.connect(btn_close_clicked)
        self.return_home.clicked.connect(goto_menu)

        self.search_box.installEventFilter(self)
        self.load_data()

        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 70)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 25)
        self.tableWidget.itemChanged.connect(self.__editing)
        self.tableWidget.doubleClicked.connect(self.__remove_item_in_bill)

        self.close_btn.installEventFilter(self)
        self.log_out.installEventFilter(self)
        self.minimize_btn.installEventFilter(self)
        self.maximize_btn.installEventFilter(self)
        self.return_home.installEventFilter(self)

        self.shift_summary_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.view_stock_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.view_history_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        self.start = QPoint(0, 0)
        self.pressing = False

        QSizeGrip(self.size_grip)

        # self.table_search.setHidden(True)

        self.table_search.setColumnWidth(0, 150)
        self.table_search.setColumnWidth(1, 300)
        self.table_search.doubleClicked.connect(self.__choose_product)
        self.printbill.clicked.connect(self.__order_out)

        self.search_btn.clicked.connect(self.__search)
        self.close_search_btn.clicked.connect(self.__close_search)
        self.left_menu_btn.clicked.connect(self.__open_left_menu)
        self.close_left_menu.clicked.connect(self.__close_left_menu)

        self.left_menu.setHidden(True)
        self.widget_search.setHidden(True)

    def __order_out(self):
        id_bill = Ultilities.get_id_bill()
        print_bill(self.bill, id_bill)
        for item in range(0, len(self.bill)):
            id = self.bill[0][0]
            name = self.bill[0][1]
            amount = self.bill[0][2]
            price = self.bill[0][3]
            sold = self.bill[0][5]

            history.add_history(id_bill, name, sold, price, self.discount, self.tax, now_id)
            product.sell(id, int(amount), int(sold))
            self.bill.pop(0)
        self.load_data()

    def __remove_item_in_bill(self):
        for item in self.tableWidget.selectedItems():
            if item.column() == 4:
                self.bill.pop(item.row())
                self.load_data()

    def __editing(self, item):
        row = item.row()
        col = item.column()
        text = item.text()

        if text == "":
            self.load_data()
        elif col == 1:
            check = True
            for i in range(0, len(text)):
                if text[i] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    check = False
            if check:
                if int(item.text()) >= 1:
                    if str(self.bill[row][5]) == str(item.text()):
                        None
                    else:
                        self.bill[row][5] = item.text()
                        self.load_data()
                else:
                    self.load_data()
            else:
                self.load_data()

    def __choose_product(self):
        for item in self.table_search.selectedItems():
            result = search.search(item.text())
            row = len(self.bill)
            if row != 0:
                valid = False
                for item in self.bill:
                    if result[0][0] == item[0]:
                        item[5] = str(int(item[5]) + 1)
                        valid = True
                if not valid:
                    result = np.append(result, [[1]]).reshape(1, 6)
                    self.bill += result.tolist()
            else:
                result = np.append(result, [[1]]).reshape(1, 6)
                self.bill += result.tolist()

            self.load_data()

    def __search(self):
        self.widget_search.setHidden(False)
        self.search_btn.setHidden(True)
        self.search_box.setFocus()

    def __close_search(self):
        self.widget_search.setHidden(True)
        self.search_btn.setHidden(False)

    def __open_left_menu(self):
        self.left_menu.setHidden(False)
        self.left_menu_btn.setHidden(True)

    def __close_left_menu(self):
        self.left_menu.setHidden(True)
        self.left_menu_btn.setHidden(False)

    def load_data(self):
        row = len(self.bill)
        self.tableWidget.setRowCount(row)
        r = 0
        for item in self.bill:
            self.tableWidget.setItem(r, 0, QTableWidgetItem(item[1]))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(item[5]))

            self.tableWidget.setItem(r, 2, QTableWidgetItem(dot(int(item[3]))))
            self.tableWidget.setItem(r, 3, QTableWidgetItem(dot(int(item[3]) * int(item[5]))))
            self.tableWidget.setItem(r, 4, QTableWidgetItem("x"))

            self.tableWidget.item(r, 0).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 2).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 3).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 4).setFlags(self.tableWidget.item(r, 4).flags() & ~Qt.ItemIsEditable)

            self.tableWidget.item(r, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 2).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setStyleSheet("QLineEdit { background-color: rgb(200, 200, 200) }")
            self.tableWidget.item(r, 4).setBackground(QtGui.QColor(255, 0, 0))
            self.tableWidget.item(r, 4).setForeground(QtGui.QColor(255, 255, 255))

            self.tableWidget.item(r, 0).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 2).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 3).setForeground(QtGui.QColor(0, 0, 0))

            r += 1

    def eventFilter(self, widget, event):

        if widget == self.minimize_btn and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/minus-dark_blue.svg"))
        elif widget == self.minimize_btn and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/minus-white.svg"))

        elif widget == self.maximize_btn and event.type() == QtCore.QEvent.HoverEnter:
            if type_window:
                self.icons_maximize = "./icons/square-dark_blue.svg"
            else:
                self.icons_maximize = "./icons/minimize-dark_blue.svg"
        elif widget == self.maximize_btn and event.type() == QtCore.QEvent.HoverLeave:
            if type_window:
                self.icons_maximize = "./icons/square-white.svg"
            else:
                self.icons_maximize = "./icons/minimize-white.svg"

        elif widget == self.log_out and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/log-out-red.svg"))
        elif widget == self.log_out and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/log-out-white.svg"))

        elif widget == self.close_btn and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/x-red.svg"))
        elif widget == self.close_btn and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/x-white.svg"))

        elif widget == self.return_home and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/home-dark_blue.svg"))
        elif widget == self.return_home and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/home-white.svg"))

        else:
            self.maximize_btn.setIcon(QIcon(self.icons_maximize))

        if self.text_search_temp == ".none--":
            self.text_search_temp = self.search_box.text()
        else:
            None

        text_search = self.search_box.text()
        if len(text_search) != 0:
            self.label_search.setText("")
            # text_search = "-all"
        else:
            self.label_search.setText("Search")
        if text_search != self.text_search_temp:
            self.text_search_temp = text_search
            result = search.search(text_search)

            if len(result) == 0:
                self.search_box.setStyleSheet("color: #f00;")
            else:
                self.search_box.setStyleSheet("color: #fff;")
                row, col = result.shape
                self.table_search.setRowCount(row)
                for a in range(0, row):
                    self.table_search.setCellWidget(a, 0, insert_image_search(self, pid=int(result[a, 0])))
                    self.table_search.setItem(a, 1, QTableWidgetItem(result[a, 1]))
                    # self.table_search.item(a, 1).setTextAlignment(Qt.AlignHCenter)
                    self.table_search.setRowHeight(a, 80)
                # self.table_search.item(0, 1).setBackground(QtGui.QColor(0, 255, 0))
        else:
            None

        if widget == self.search_box:
            if event.type() == QEvent.FocusOut:
                pass
            elif event.type() == QEvent.FocusIn:
                self.search_box.setText("")
            else:
                pass

        return False

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            widget.setGeometry(self.mapToGlobal(self.movement).x(),
                               self.mapToGlobal(self.movement).y(),
                               widget.width(),
                               widget.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


class ViewStockScreen(QMainWindow):

    def __init__(self):
        # print("view stock")
        data = user.find_id(now_id)
        super(ViewStockScreen, self).__init__()
        loadUi("./GUI/view_stock.ui", self)
        self.name_user.setText(str(data[1]))

        self.returnHome.clicked.connect(self.goto_menu)

        self.load_data()

        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 100)

    def load_data(self):
        data = search.search("-view-stock")
        row = len(data)
        self.tableWidget.setRowCount(row)
        r = 0
        for item in data:
            self.tableWidget.setCellWidget(r, 0, insert_image_search(self, pid=int(item[0])))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(item[1]))
            self.tableWidget.setItem(r, 2, QTableWidgetItem(dot(int(item[2]))))
            self.tableWidget.setItem(r, 3, QTableWidgetItem(dot(int(item[3]))))
            self.tableWidget.setItem(r, 4, QTableWidgetItem(dot(int(item[4]))))
            self.tableWidget.setItem(r, 5, QTableWidgetItem("--/--/----"))

            self.tableWidget.item(r, 1).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 2).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 3).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 4).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 5).setFlags(Qt.ItemIsEditable)

            self.tableWidget.item(r, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 4).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 5).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.tableWidget.item(r, 1).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 2).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 3).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 4).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 5).setForeground(QtGui.QColor(0, 0, 0))

            self.tableWidget.setRowHeight(r, 80)

            if int(item[2]) < 10:
                for j in range(1, self.tableWidget.columnCount()):
                    self.tableWidget.item(r, j).setBackground(QtGui.QColor(255, 100, 100))
            elif int(item[2]) < 30:
                for j in range(1, self.tableWidget.columnCount()):
                    self.tableWidget.item(r, j).setBackground(QtGui.QColor(255, 200, 150))
            elif int(item[2]) < 50:
                for j in range(1, self.tableWidget.columnCount()):
                    self.tableWidget.item(r, j).setBackground(QtGui.QColor(255, 255, 150))
            # self.tableWidget.item(r, 0).setForeground(QtGui.QColor(0, 0, 0))

            r += 1

    def goto_menu(self):
        menu = MenuScreen()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ShiftSummaryScreen(QMainWindow):
    def __init__(self):
        print(now_id)
        data = user.find_id(now_id)
        super(ShiftSummaryScreen, self).__init__()
        loadUi("./GUI/ShiftSummary.ui", self)
        self.name_user.setText(str(data[1]))
        self.returnHome.clicked.connect(self.goto_menu)
        self.total_shift_custom.clicked.connect(self.__total_shift_custom)
        self.show_time.clicked.connect(self.__show_time)
        self.total_shift.clicked.connect(self.__total_shift)
        self.total_shift_day.clicked.connect(self.__total_shift_day)
        self.total_shift_month.clicked.connect(self.__total_shift_month)
        self.frame_custom.setHidden(True)
        self.time_from.setHidden(True)
        self.time_to.setHidden(True)

    def __total_shift_month(self):
        self.frame_custom.setHidden(True)
        data = search.history("-shift-working-month")
        if str(data[0][2][5]) == '0':
            month = str(data[0][2][6:7])
        else:
            month = str(data[0][2][5:7])
        self.title_table.setText("Total Sale of Month " + month)
        self.load_data(data=data)

    def __total_shift_day(self):
        self.frame_custom.setHidden(True)
        data = search.history("-shift-working-day")
        empty = np.array([])
        if str(data) == str(empty):
            self.title_table.setText("Still no orders today")
        else:
            if str(data[0][2][9]) == '0':
                day = str(data[0][2][11:12])
            else:
                day = str(data[0][2][10:12])
            self.title_table.setText("Total Sale of Day " + day)
        self.load_data(data=data)

    def __total_shift(self):
        self.frame_custom.setHidden(True)
        data = search.history("-shift-working")
        self.title_table.setText("Total Sale of " + str(user.find_id(now_id)[1]))
        self.load_data(data=data)

    def load_data(self, data):

        # self.tableWidget.setColumnWidth(0, 150)
        # self.tableWidget.setColumnWidth(1, 200)
        # self.tableWidget.setColumnWidth(2, 80)
        # self.tableWidget.setColumnWidth(3, 100)
        # self.tableWidget.setColumnWidth(4, 100)

        row = len(data)
        self.tableWidget.setRowCount(row)
        sum_price = 0
        if row > 0:
            r = 0
            for item in data:
                sum_price += int(item[5]) * int(item[6])
                self.tableWidget.setItem(r, 0, QTableWidgetItem(item[2] + " " + item[1][0:8]))
                self.tableWidget.setItem(r, 1, QTableWidgetItem(item[3]))
                self.tableWidget.setItem(r, 2, QTableWidgetItem(str(user.find_id(int(item[9]))[1])))
                self.tableWidget.setItem(r, 3, QTableWidgetItem(item[4]))
                self.tableWidget.setItem(r, 4, QTableWidgetItem(item[5]))
                self.tableWidget.setItem(r, 5, QTableWidgetItem(item[6]))
                self.tableWidget.setItem(r, 6, QTableWidgetItem(item[7]))
                self.tableWidget.setItem(r, 7, QTableWidgetItem(item[8]))

                """
    
                self.tableWidget.item(r, 1).setFlags(Qt.ItemIsEditable)
                self.tableWidget.item(r, 2).setFlags(Qt.ItemIsEditable)
                self.tableWidget.item(r, 3).setFlags(Qt.ItemIsEditable)
                self.tableWidget.item(r, 4).setFlags(Qt.ItemIsEditable)
    
                self.tableWidget.item(r, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.item(r, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.item(r, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.tableWidget.item(r, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    
                self.tableWidget.item(r, 1).setForeground(QtGui.QColor(0, 0, 0))
                self.tableWidget.item(r, 2).setForeground(QtGui.QColor(0, 0, 0))
                self.tableWidget.item(r, 3).setForeground(QtGui.QColor(0, 0, 0))
                self.tableWidget.item(r, 4).setForeground(QtGui.QColor(0, 0, 0))
    
                self.tableWidget.setRowHeight(r, 80)
    
                if int(item[2]) < 10:
                    for j in range(1, self.tableWidget.columnCount()):
                        self.tableWidget.item(r, j).setBackground(QtGui.QColor(255, 100, 100))
                elif int(item[2]) < 30:
                    for j in range(1, self.tableWidget.columnCount()):
                        self.tableWidget.item(r, j).setBackground(QtGui.QColor(255, 200, 150))
                elif int(item[2]) < 50:
                    for j in range(1, self.tableWidget.columnCount()):
                        self.tableWidget.item(r, j).setBackground(QtGui.QColor(255, 255, 150))
                # self.tableWidget.item(r, 0).setForeground(QtGui.QColor(0, 0, 0))
    
                """

                r += 1
            # print(sum_price)
            self.sum_price.setText(dot(sum_price))
        else:
            self.sum_price.setText(str(sum_price))

    def __show_time(self):
        # print(self.show_time.text())
        if self.show_time.text() == "Only Date":
            self.time_from.setHidden(True)
            self.time_to.setHidden(True)
            self.show_time.setText("Time && Day")
        else:
            self.time_from.setHidden(False)
            self.time_to.setHidden(False)
            self.show_time.setText("Only Date")

    def __total_shift_custom(self):
        self.frame_custom.setHidden(False)

    def goto_menu(self):
        menu = MenuScreen()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ImportExportScreen(QMainWindow):
    # Import_Export
    c_search_box = pyqtSignal()

    style_text_input = """
                        font: 87 "Arial Black";
                        background-color: rgb(1, 67, 97);
                        border-style:solid;
                        border-radius: 5px;
                        gridline-color: rgb(255, 0, 0);
                        border-bottom-color: rgb(255, 0, 0);
                        alternate-background-color: rgba(255, 255, 255, 0); 
                        color: rgb(255, 255, 255);
                        border-color: rgba(255, 255, 255, 0);
                        gridline-color: rgba(255, 255, 255, 0);
                    """

    bill = list()
    discount = 0
    tax = 0
    text_search_temp = ".none--"

    def __init__(self):
        # print("view stock")
        data = user.find_id(now_id)
        super(ImportExportScreen, self).__init__()
        loadUi("./GUI/Import_Export.ui", self)
        self.name_user.setText(str(data[1]))

        self.returnHome.clicked.connect(self.goto_menu)
        self.export_btn.clicked.connect(self.export_products)
        self.import_btn.clicked.connect(self.import_products)

        self.search_box.installEventFilter(self)
        self.load_data()

        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 70)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 25)
        self.tableWidget.itemChanged.connect(self.__editing)
        self.tableWidget.doubleClicked.connect(self.__remove_item_in_bill)

        self.c_search_box.connect(self.type_search_box)
        self.table_search.setHidden(True)

        self.table_search.setColumnWidth(0, 150)
        self.table_search.setColumnWidth(1, 300)
        self.table_search.doubleClicked.connect(self.__search_clicked)

    def import_products(self):
        print("import")

    def export_products(self):
        print("export")

    def __remove_item_in_bill(self):
        for item in self.tableWidget.selectedItems():
            if item.column() == 4:
                self.bill.pop(item.row())
                self.load_data()

    def __editing(self, item):
        row = item.row()
        col = item.column()
        text = item.text()

        if text == "":
            self.load_data()
        elif col == 1:
            check = True
            for i in range(0, len(text)):
                if text[i] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    check = False
            if check:
                if int(item.text()) >= 1:
                    if str(self.bill[row][5]) == str(item.text()):
                        None
                    else:
                        self.bill[row][5] = item.text()
                        # print("changed")
                        self.load_data()
                else:
                    self.load_data()
            else:
                self.load_data()

    def type_search_box(self):
        self.search_box.clear()
        self.search_box.setStyleSheet(self.style_text_input)

    def __search_clicked(self):
        for item in self.table_search.selectedItems():
            result = search.search(item.text())
            row = len(self.bill)
            if row != 0:
                valid = False
                for item in self.bill:
                    if result[0][0] == item[0]:
                        item[5] = str(int(item[5]) + 1)
                        valid = True
                if not valid:
                    result = np.append(result, [[1]]).reshape(1, 6)
                    self.bill += result.tolist()
            else:
                result = np.append(result, [[1]]).reshape(1, 6)
                self.bill += result.tolist()
            self.load_data()
        self.table_search.setHidden(True)
        self.search_box.setText("Search")

    def load_data(self):
        row = len(self.bill)
        self.tableWidget.setRowCount(row)
        r = 0
        for item in self.bill:
            self.tableWidget.setItem(r, 0, QTableWidgetItem(item[1]))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(item[5]))

            self.tableWidget.setItem(r, 2, QTableWidgetItem(dot(int(item[4]))))
            self.tableWidget.setItem(r, 3, QTableWidgetItem(dot(int(item[4]) * int(item[5]))))
            self.tableWidget.setItem(r, 4, QTableWidgetItem("x"))

            self.tableWidget.item(r, 0).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 2).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 3).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 4).setFlags(self.tableWidget.item(r, 4).flags() & ~Qt.ItemIsEditable)

            self.tableWidget.item(r, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 2).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setStyleSheet("QLineEdit { background-color: rgb(200, 200, 200) }")
            self.tableWidget.item(r, 4).setBackground(QtGui.QColor(255, 0, 0))
            self.tableWidget.item(r, 4).setForeground(QtGui.QColor(255, 255, 255))

            self.tableWidget.item(r, 0).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 2).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 3).setForeground(QtGui.QColor(0, 0, 0))

            r += 1

    def eventFilter(self, widget, event):
        if self.text_search_temp == ".none--":
            self.text_search_temp = self.search_box.text()
        else:
            None

        text_search = self.search_box.text()
        if text_search != self.text_search_temp:
            self.text_search_temp = text_search
            if text_search == 'Search' or text_search == '':
                result = ""
                self.table_search.setHidden(True)

            else:
                result = search.search(text_search)

            if len(result) == 0:
                None
            else:
                self.table_search.setHidden(False)
                row, col = result.shape
                self.table_search.setRowCount(row)
                for a in range(0, row):
                    self.table_search.setCellWidget(a, 0, insert_image_search(self, pid=int(result[a, 0])))
                    self.table_search.setItem(a, 1, QTableWidgetItem(result[a, 1]))
                    # self.table_search.item(a, 1).setTextAlignment(Qt.AlignHCenter)
                    self.table_search.setRowHeight(a, 80)
                # self.table_search.item(0, 1).setBackground(QtGui.QColor(0, 255, 0))
        else:
            None

        if widget == self.search_box:
            # print('as')
            if event.type() == QEvent.FocusOut:
                # self.search_box.setText("search")
                pass
            elif event.type() == QEvent.FocusIn:
                self.c_search_box.emit()  # When the focus falls again, edit Enter the box, send clicked Signal out
            else:
                pass

        return False

    def goto_menu(self):
        menu = MenuScreen()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ViewHistoryScreen(QMainWindow):
    icons_maximize = './icons/square-white.svg'

    def __init__(self):
        data = user.find_id(now_id)
        super(ViewHistoryScreen, self).__init__()
        loadUi("./GUI/ViewHistory_v.ui", self)
        self.name_user.setText(str(data[1]))

        self.returnHome.clicked.connect(self.goto_menu)

        self.load_data()

        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)

    def load_data(self):
        data = search.history("-view-history")
        # print(data)
        row = len(data)
        self.tableWidget.setRowCount(row)
        r = 0
        sum_price = 0

        for item in data:
            sum_price += int(item[5]) * int(item[6])
            self.tableWidget.setItem(r, 0, QTableWidgetItem(item[2] + " " + item[1][0:8]))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(item[3]))
            self.tableWidget.setItem(r, 2, QTableWidgetItem(str(user.find_id(int(item[9]))[1])))
            self.tableWidget.setItem(r, 3, QTableWidgetItem(item[4]))
            self.tableWidget.setItem(r, 4, QTableWidgetItem(item[5]))
            self.tableWidget.setItem(r, 5, QTableWidgetItem(item[6]))
            self.tableWidget.setItem(r, 6, QTableWidgetItem(item[7]))
            self.tableWidget.setItem(r, 7, QTableWidgetItem(item[8]))

            """

            self.tableWidget.item(r, 1).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 2).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 3).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 4).setFlags(Qt.ItemIsEditable)

            self.tableWidget.item(r, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            self.tableWidget.item(r, 1).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 2).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 3).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 4).setForeground(QtGui.QColor(0, 0, 0))

            self.tableWidget.setRowHeight(r, 80)

            if int(item[2]) < 10:
                for j in range(1, self.tableWidget.columnCount()):
                    self.tableWidget.item(r, j).setBackground(QtGui.QColor(255, 100, 100))
            elif int(item[2]) < 30:
                for j in range(1, self.tableWidget.columnCount()):
                    self.tableWidget.item(r, j).setBackground(QtGui.QColor(255, 200, 150))
            elif int(item[2]) < 50:
                for j in range(1, self.tableWidget.columnCount()):
                    self.tableWidget.item(r, j).setBackground(QtGui.QColor(255, 255, 150))
            # self.tableWidget.item(r, 0).setForeground(QtGui.QColor(0, 0, 0))
            
            """

            r += 1
        # print(sum_price)
        self.sum_price.setText(dot(sum_price))

    def goto_menu(self):
        menu = MenuScreen()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class insert_image_search(QtWidgets.QLabel):
    def __init__(self, parent, pid):
        super(insert_image_search, self).__init__(None)
        pic = QtGui.QPixmap("./Image/products/" + str(pid) + ".jpg")
        # pic = pic.scaled(20, 100, QtCore.Qt.KeepAspectRatio)
        pic = pic.scaled(150, 80)
        self.setPixmap(pic)


# main
app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
size_app = [1080, 720]
login = LoginScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login)
widget.setGeometry(int((size.width() - size_app[0]) / 2), int((size.height() - size_app[1]) / 2),
                   size_app[0], size_app[1])
# widget.setWindowTitle("PQY Store")
# widget.setWindowIcon(QIcon('./Image/0a890a8477d7b889e1c6.jpg'))
widget.setWindowFlags(Qt.FramelessWindowHint)
widget.show()

try:
    sys.exit(app.exec_())

except:
    print("Exiting...")
