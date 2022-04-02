import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Tools import user, product, search, history, Ultilities
import numpy as np
from Tools.create_print_file import print_bill
from datetime import datetime
from PIL import Image, ImageDraw
import sqlite3

now_id = None
type_window = True


def dot(number):
    first = True
    result = ""
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
    w_screen = MenuScreen()
    widget.addWidget(w_screen)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_sell():
    w_screen = SellScreen()
    widget.addWidget(w_screen)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_shift_work():
    w_screen = ShiftSummaryScreen()
    widget.addWidget(w_screen)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_view_history():
    w_screen = ViewHistoryScreen()
    widget.addWidget(w_screen)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_warehouse():
    w_screen = ViewStockScreen()
    widget.addWidget(w_screen)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_sign_up():
    w_screen = SignUpScreen()
    widget.addWidget(w_screen)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_import_export():
    w_screen = ImportExportScreen()
    widget.addWidget(w_screen)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def _logout():
    global now_id
    now_id = None
    w_screen = LoginScreen()
    widget.addWidget(w_screen)
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


def btn_min_clicked():
    widget.showMinimized()


class LoginScreen(QMainWindow):

    def __init__(self):
        super(LoginScreen, self).__init__(None)
        self.movement = None
        self.end = None
        self.pressing = None
        self.start = None
        loadUi("./GUI/login.ui", self)

        self.password.setEchoMode(QLineEdit.Password)

        self.login.clicked.connect(self._login)
        self.showPassword.clicked.connect(self._show_password)
        self.login.installEventFilter(self)
        self.close_btn.clicked.connect(self.show_popup_turn_off)

        self.yes_btn.clicked.connect(btn_close_clicked)
        self.no_btn.clicked.connect(self.hide_popup_turn_off)

        self.yes_btn.installEventFilter(self)
        self.no_btn.installEventFilter(self)
        self.close_btn.installEventFilter(self)
        self.username.installEventFilter(self)
        self.password.installEventFilter(self)

        w = self.widget_close.width()
        h = self.widget_close.height()
        self.widget_close.setGeometry(0, 0, w, h)

        # self.setTabOrder(self.username, self.password)

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


class MenuScreen(QMainWindow):
    # default icon of maximize button
    icons_maximize = './icons/square-white.svg'

    def __init__(self):
        # setup
        data = user.find_id(now_id)
        super(MenuScreen, self).__init__()

        # title
        loadUi("./GUI/Menu_.ui", self)
        self.setMinimumSize(1080, 300)
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.state_title = "Wellcome - Have a great day at work!"
        self.minimize_btn.clicked.connect(btn_min_clicked)
        self.maximize_btn.clicked.connect(btn_max_clicked)
        self.close_btn.clicked.connect(btn_close_clicked)

        # change to screen utilities
        self.log_out.clicked.connect(_logout)
        self.sell_button.clicked.connect(goto_sell)
        self.signup.clicked.connect(goto_sign_up)
        self.import_export_btn.clicked.connect(goto_import_export)
        self.view_stock_btn.clicked.connect(goto_warehouse)
        self.shift_summary_btn.clicked.connect(goto_shift_work)
        self.view_history_btn.clicked.connect(goto_view_history)

        # animation hover
        self.close_btn.installEventFilter(self)
        self.log_out.installEventFilter(self)
        self.minimize_btn.installEventFilter(self)
        self.maximize_btn.installEventFilter(self)

        # setup for move window
        self.start = QPoint(0, 0)
        self.pressing = False

        # change size window
        QSizeGrip(self.size_grip)

    def eventFilter(self, widget, event):
        self.update_time()
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

        if type_window:
            self.status_title.setStyleSheet("font: 10pt")
        else:
            self.status_title.setStyleSheet("font: 12pt")
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

    def update_time(self):
        time_now = datetime.now()
        self.status_title.setText(self.state_title + "  [" + str(time_now.date())
                                  + " - " + str(time_now.time())[0:8] + "]")


class SellScreen(QMainWindow):
    icons_maximize = './icons/square-white.svg'

    # sell
    c_search_box = pyqtSignal()
    bill = list()
    discount = 0
    tax = 0
    text_search_temp = ".none--"

    def __init__(self):
        data = user.find_id(now_id)
        super(SellScreen, self).__init__()
        loadUi("./GUI/Sell_.ui", self)

        # setting for move and resize window
        self.start = QPoint(0, 0)
        self.pressing = False
        QSizeGrip(self.size_grip)

        # title app
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.status_title.setText("Sell")
        self.minimize_btn.clicked.connect(btn_min_clicked)
        self.maximize_btn.clicked.connect(btn_max_clicked)
        self.close_btn.clicked.connect(btn_close_clicked)
        self.return_home.clicked.connect(goto_menu)
        self.log_out.clicked.connect(_logout)

        # tab selected style
        self.sell_button.setStyleSheet("background-color: #2b2c60;")

        # animation hover for buttons
        self.close_btn.installEventFilter(self)
        self.log_out.installEventFilter(self)
        self.minimize_btn.installEventFilter(self)
        self.maximize_btn.installEventFilter(self)
        self.return_home.installEventFilter(self)
        self.search_box.installEventFilter(self)
        self.left_menu_btn.installEventFilter(self)
        self.close_search_btn.installEventFilter(self)

        # change to screen utilities
        self.log_out.clicked.connect(_logout)
        self.sell_button.clicked.connect(goto_sell)
        self.signup.clicked.connect(goto_sign_up)
        self.import_export_btn.clicked.connect(goto_import_export)
        self.view_stock_btn.clicked.connect(goto_warehouse)
        self.shift_summary_btn.clicked.connect(goto_shift_work)
        self.view_history_btn.clicked.connect(goto_view_history)

        # setting for sell-screen
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 70)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 25)
        self.load_data()
        self.tableWidget.itemChanged.connect(self.__editing)
        self.tableWidget.doubleClicked.connect(self.__remove_item_in_bill)
        self.printbill.clicked.connect(self.__order_out)

        # search in sell-screen
        self.table_search.setColumnWidth(0, 150)
        self.table_search.setColumnWidth(1, 300)
        self.table_search.doubleClicked.connect(self.__choose_product)
        self.search_btn.clicked.connect(self.__search)
        self.widget_search.setHidden(True)
        self.close_search_btn.clicked.connect(self.__close_search)

        # left-menu
        self.left_menu_btn.clicked.connect(self.__open_left_menu)
        self.close_left_menu.clicked.connect(self.__close_left_menu)
        self.left_menu_btn.setHidden(True)

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
        # hover title
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

        elif widget == self.left_menu_btn and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/menu-dark_blue.svg"))
        elif widget == self.left_menu_btn and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/menu-white.svg"))

        elif widget == self.close_search_btn and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/x-circle-red.svg"))
        elif widget == self.close_search_btn and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/x-circle-white.svg"))

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

        # search
        if self.text_search_temp == ".none--":
            self.text_search_temp = self.search_box.text()

        text_search = self.search_box.text()
        if len(text_search) != 0:
            self.label_search.setText("")
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
                    self.table_search.setCellWidget(a, 0,
                                                    insert_image_search(self, pid=int(result[a, 0]), type="products"))
                    self.table_search.setItem(a, 1, QTableWidgetItem(result[a, 1]))
                    # self.table_search.item(a, 1).setTextAlignment(Qt.AlignHCenter)
                    self.table_search.setRowHeight(a, 80)
                # self.table_search.item(0, 1).setBackground(QtGui.QColor(0, 255, 0))

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
    icons_maximize = './icons/square-white.svg'

    def __init__(self):
        # print("view stock")
        data = user.find_id(now_id)
        super(ViewStockScreen, self).__init__()
        loadUi("./GUI/ViewStock_v.ui", self)

        self.load_data()

        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 100)

        # title app
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.status_title.setText("Warehouse")
        self.minimize_btn.clicked.connect(btn_min_clicked)
        self.maximize_btn.clicked.connect(btn_max_clicked)
        self.close_btn.clicked.connect(btn_close_clicked)
        self.return_home.clicked.connect(goto_menu)
        self.log_out.clicked.connect(_logout)

        # tab selected style
        self.view_stock_btn.setStyleSheet("background-color: #2b2c60;")

        # setting for move and resize window
        self.start = QPoint(0, 0)
        self.pressing = False
        QSizeGrip(self.size_grip)

        # animation hover for buttons
        self.close_btn.installEventFilter(self)
        self.log_out.installEventFilter(self)
        self.minimize_btn.installEventFilter(self)
        self.maximize_btn.installEventFilter(self)
        self.return_home.installEventFilter(self)

        # change to screen utilities
        self.log_out.clicked.connect(_logout)
        self.sell_button.clicked.connect(goto_sell)
        self.signup.clicked.connect(goto_sign_up)
        self.import_export_btn.clicked.connect(goto_import_export)
        self.view_stock_btn.clicked.connect(goto_warehouse)
        self.shift_summary_btn.clicked.connect(goto_shift_work)
        self.view_history_btn.clicked.connect(goto_view_history)

        # left-menu
        self.left_menu_btn.clicked.connect(self.__open_left_menu)
        self.close_left_menu.clicked.connect(self.__close_left_menu)
        self.left_menu_btn.setHidden(True)

    def load_data(self):
        data = search.search("-view-stock")
        row = len(data)
        self.tableWidget.setRowCount(row)
        r = 0
        for item in data:
            self.tableWidget.setCellWidget(r, 0, insert_image_search(self, pid=int(item[0]), type="products"))
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

    def __open_left_menu(self):
        self.left_menu.setHidden(False)
        self.left_menu_btn.setHidden(True)

    def __close_left_menu(self):
        self.left_menu.setHidden(True)
        self.left_menu_btn.setHidden(False)

    def eventFilter(self, widget, event):
        # hover title
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


class ShiftSummaryScreen(QMainWindow):
    icons_maximize = './icons/square-white.svg'
    select = None

    def __init__(self):
        data = user.find_id(now_id)
        super(ShiftSummaryScreen, self).__init__()
        loadUi("./GUI/ShiftSummary_.ui", self)

        self.total_shift.clicked.connect(self.__total_shift)
        self.total_shift_day.clicked.connect(self.__total_shift_day)
        self.total_shift_month.clicked.connect(self.__total_shift_month)
        self.total_shift_custom.clicked.connect(self.__total_shift_custom)
        self.show_time.clicked.connect(self.__show_time)
        self.custom_setting.setHidden(True)
        self.time_from.setHidden(True)
        self.time_to.setHidden(True)

        # title app
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.status_title.setText("Status")
        self.minimize_btn.clicked.connect(btn_min_clicked)
        self.maximize_btn.clicked.connect(btn_max_clicked)
        self.close_btn.clicked.connect(btn_close_clicked)
        self.return_home.clicked.connect(goto_menu)
        self.log_out.clicked.connect(_logout)

        # tab selected style
        self.shift_summary_btn.setStyleSheet("background-color: #2b2c60;")

        # setting for move and resize window
        self.start = QPoint(0, 0)
        self.pressing = False
        QSizeGrip(self.size_grip)

        # animation hover for buttons
        self.close_btn.installEventFilter(self)
        self.log_out.installEventFilter(self)
        self.minimize_btn.installEventFilter(self)
        self.maximize_btn.installEventFilter(self)
        self.return_home.installEventFilter(self)

        # change to screen utilities
        self.log_out.clicked.connect(_logout)
        self.sell_button.clicked.connect(goto_sell)
        self.signup.clicked.connect(goto_sign_up)
        self.import_export_btn.clicked.connect(goto_import_export)
        self.view_stock_btn.clicked.connect(goto_warehouse)
        self.shift_summary_btn.clicked.connect(goto_shift_work)
        self.view_history_btn.clicked.connect(goto_view_history)

        # left-menu
        self.left_menu_btn.clicked.connect(self.__open_left_menu)
        self.close_left_menu.clicked.connect(self.__close_left_menu)
        self.left_menu_btn.setHidden(True)

    def __open_left_menu(self):
        self.left_menu.setHidden(False)
        self.left_menu_btn.setHidden(True)

    def __close_left_menu(self):
        self.left_menu.setHidden(True)
        self.left_menu_btn.setHidden(False)

    def __total_shift_month(self):
        self.select = 3
        self.custom_setting.setHidden(True)
        data = search.history("-shift-working-month")
        empty = np.array([])
        if str(data) == str(empty):
            self.title_table.setText("Still no orders this month")
        else:
            if str(data[0][2][5]) == '0':
                month = str(data[0][2][6:7])
            else:
                month = str(data[0][2][5:7])
                self.title_table.setText("Total Sale of Month " + month)
        self.load_data(data=data)

    def __total_shift_day(self):
        self.select = 2
        self.custom_setting.setHidden(True)
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
        self.custom_setting.setHidden(True)
        data = search.history("-shift-working")
        # # print(data)
        # data_short = [[]]
        # for item in data:
        #     if len(data_short) == 0:
        #         data_short[0] = item
        #     else:
        #         for i in data_short:
        #             if item[4] == i[4]:
        #                 i[5] += 1
        #                 break
        # print(data_short)

        self.title_table.setText("Total Shift Revenue of " + str(user.find_id(now_id)[1]))
        self.load_data(data=data)
        self.select = 1

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
            self.sum_price.setText("Total Evenue: " + dot(sum_price))
        else:
            self.sum_price.setText("Total Evenue: " + str(sum_price))

        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.resizeColumnsToContents()

    def __show_time(self):
        # print(self.show_time.text())
        if self.show_time.text() == " Only Date":
            self.time_from.setHidden(True)
            self.time_to.setHidden(True)
            self.show_time.setText(" Time && Day")
        else:
            self.time_from.setHidden(False)
            self.time_to.setHidden(False)
            self.show_time.setText(" Only Date")

    def __total_shift_custom(self):
        self.select = 4
        self.custom_setting.setHidden(False)

    def eventFilter(self, widget, event):
        # animation selected
        if self.select is not None:
            if self.select == 1:
                self.total_shift.setStyleSheet("""background-color: #2b2c60;border-color: #fff;
                                               border-bottom-color: transparent;""")
                self.total_shift_day.setStyleSheet("")
                self.total_shift_month.setStyleSheet("")
                self.total_shift_custom.setStyleSheet("")
            if self.select == 2:
                self.total_shift.setStyleSheet("")
                self.total_shift_day.setStyleSheet("""background-color: 2b2c60;border-color: #fff;
                                                               border-bottom-color: transparent;""")
                self.total_shift_month.setStyleSheet("")
                self.total_shift_custom.setStyleSheet("")
            if self.select == 3:
                self.total_shift.setStyleSheet("")
                self.total_shift_day.setStyleSheet("")
                self.total_shift_month.setStyleSheet("""background-color: 2b2c60;border-color: #fff;
                                                               border-bottom-color: transparent;""")
                self.total_shift_custom.setStyleSheet("")
            if self.select == 4:
                self.total_shift.setStyleSheet("")
                self.total_shift_day.setStyleSheet("")
                self.total_shift_month.setStyleSheet("")
                self.total_shift_custom.setStyleSheet("""background-color: 2b2c60;border-color: #fff;
                                                               border-bottom-color: transparent;""")

        # hover title
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


class ImportExportScreen(QMainWindow):
    # Import_Export

    bill = list()
    text_search_temp = ".none--"
    icons_maximize = './icons/square-white.svg'
    import_selected = True
    transfer_selected = True
    time_to_display_import_success = 0

    def __init__(self):
        data = user.find_id(now_id)
        super(ImportExportScreen, self).__init__()
        loadUi("./GUI/Import_Export_v.ui", self)

        self.upload_btn.setIcon(QIcon("./icons/upload-black.svg"))
        self.import_btn.clicked.connect(self.import_products)
        self.export_btn.clicked.connect(self.export_products)
        self.create_product.clicked.connect(self.popup_create_product)
        self.close_create_product.clicked.connect(self.close_popup_create_product)
        self.upload_btn.clicked.connect(self._upload_image)

        self.close_search_btn.installEventFilter(self)
        self.close_create_product.installEventFilter(self)

        self.widget_4.setHidden(True)
        self.widget_create_product.setHidden(True)

        # setting for table-screen
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(2, 70)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 25)
        self.tableWidget.itemChanged.connect(self.__editing)
        self.tableWidget.doubleClicked.connect(self.__remove_item_in_bill)
        self.confirm_import_btn.clicked.connect(self.__confirm)
        self.load_data()
        self.import_products()
        self.transfer_export()
        self.transfer.clicked.connect(self.transfer_export)
        self.wholesaler.clicked.connect(self.wholesaler_export)
        self.btn_create.clicked.connect(self.create_new_product)

        # search in search
        self.table_search.setColumnWidth(0, 150)
        self.table_search.setColumnWidth(1, 300)
        self.table_search.doubleClicked.connect(self.__choose_product)
        self.search_btn.clicked.connect(self.__search)
        self.widget_search.setHidden(True)
        self.close_search_btn.clicked.connect(self.__close_search)

        # title app
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.status_title.setText("Status")
        self.minimize_btn.clicked.connect(btn_min_clicked)
        self.maximize_btn.clicked.connect(btn_max_clicked)
        self.close_btn.clicked.connect(btn_close_clicked)
        self.return_home.clicked.connect(goto_menu)
        self.log_out.clicked.connect(_logout)

        # tab selected style
        self.import_export_btn.setStyleSheet("background-color: #2b2c60;")

        # setting for move and resize window
        self.start = QPoint(0, 0)
        self.pressing = False
        QSizeGrip(self.size_grip)

        # animation hover for buttons
        self.close_btn.installEventFilter(self)
        self.log_out.installEventFilter(self)
        self.minimize_btn.installEventFilter(self)
        self.maximize_btn.installEventFilter(self)
        self.return_home.installEventFilter(self)

        # change to screen utilities
        self.log_out.clicked.connect(_logout)
        self.sell_button.clicked.connect(goto_sell)
        self.signup.clicked.connect(goto_sign_up)
        self.import_export_btn.clicked.connect(goto_import_export)
        self.view_stock_btn.clicked.connect(goto_warehouse)
        self.shift_summary_btn.clicked.connect(goto_shift_work)
        self.view_history_btn.clicked.connect(goto_view_history)

        # left-menu
        self.left_menu_btn.clicked.connect(self.__open_left_menu)
        self.close_left_menu.clicked.connect(self.__close_left_menu)
        self.left_menu_btn.setHidden(True)

    def __confirm(self):
        if not self.import_selected:
            code = "transfer" if self.transfer_selected else "wholesaler"
            id_bill = Ultilities.get_id_bill()
            print_bill(self.bill, id_bill, code_bill=code)
        for item in self.bill:
            if self.import_selected:
                product.import_product(item[0], item[2], item[5])
            else:
                product.export_product(item[0], item[2], item[5])

        self.confirm_import_btn.setStyleSheet("background-color: #0f0")
        while len(self.bill) > 0:
            self.bill.pop(0)
        self.load_data()
        self.time_to_display_import_success = 3

    def create_new_product(self):
        name_product = self.name_product.text()
        retail_price = self.retail_price.text()
        cost_price = self.cost_price.text()

        error = 0

        if name_product == "":
            error += 1
            self.name_product_s.setStyleSheet("color: #f00")
        if cost_price == "":
            error += 1
            self.cost_price_s.setStyleSheet("color: #f00")
        if retail_price == "":
            error += 1
            self.retail_price_s.setStyleSheet("color: #f00")
        if error > 0:
            self.status.setText("Have error in input!!")
            self.status.setStyleSheet("color: #f00")
        else:
            product.add_product(name_product, retail_price, cost_price)
            self.status.setText(str(name_product + " add successful"))
            self.status.setStyleSheet("color: #0f0")
            self.name_product.setText("")
            self.cost_price.setText("")
            self.retail_price.setText("")
            self.upload_btn.setIcon(QIcon("./icons/upload-black.svg"))

    def popup_create_product(self):
        self.widget_search.setHidden(True)
        self.widget_create_product.setHidden(False)
        self.create_product.setHidden(True)
        self.search_btn.setHidden(False)
        self.name_product.setFocus()

    def close_popup_create_product(self):
        self.widget_create_product.setHidden(True)
        self.create_product.setHidden(False)

    def import_products(self):
        self.confirm_import_btn.setText("Import to Warehouse")
        self.import_selected = True
        self.widget_4.setHidden(True)
        self.create_product.setHidden(False)
        self.import_btn.setStyleSheet("""background-color: 2b2c60;
                                      border-color: #fff; border-bottom-color: transparent;""")
        self.export_btn.setStyleSheet("")
        for i in range(3, 5):
            self.tableWidget.setColumnWidth(i, 0)

    def export_products(self):
        self.confirm_import_btn.setText("Export Products")
        self.import_selected = False
        self.widget_create_product.setHidden(True)
        self.widget_4.setHidden(False)
        self.create_product.setHidden(True)
        self.export_btn.setStyleSheet("""background-color: 2b2c60;
                                      border-color: #fff; border-bottom-color: transparent;""")
        self.import_btn.setStyleSheet("")
        if self.transfer_selected:
            for i in range(3, 5):
                self.tableWidget.setColumnWidth(i, 0)
        else:
            for i in range(3, 5):
                self.tableWidget.setColumnWidth(i, 100)

    def transfer_export(self):
        self.transfer_selected = True
        self.transfer.setStyleSheet("""background-color: 2b2c60;
                                              border-color: #fff; border-bottom-color: transparent;""")
        self.wholesaler.setStyleSheet("")
        for i in range(3, 5):
            self.tableWidget.setColumnWidth(i, 0)

    def wholesaler_export(self):
        self.transfer_selected = False
        self.wholesaler.setStyleSheet("""background-color: 2b2c60;
                                              border-color: #fff; border-bottom-color: transparent;""")
        self.transfer.setStyleSheet("")
        for i in range(3, 5):
            self.tableWidget.setColumnWidth(i, 100)

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
        self.widget_create_product.setHidden(True)
        self.widget_search.setHidden(False)
        self.search_btn.setHidden(True)
        self.search_box.setFocus()
        if self.import_selected:
            self.create_product.setHidden(False)

    def __close_search(self):
        self.widget_search.setHidden(True)
        self.search_btn.setHidden(False)

    def __remove_item_in_bill(self):
        for item in self.tableWidget.selectedItems():
            if item.column() == 5:
                self.bill.pop(item.row())
                self.load_data()

    def __editing(self, item):
        row = item.row()
        col = item.column()
        text = item.text()

        if text == "":
            self.load_data()
        elif col == 2:
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

    def load_data(self):
        row = len(self.bill)
        self.tableWidget.setRowCount(row)

        r = 0
        for item in self.bill:
            self.tableWidget.setCellWidget(r, 0, insert_image_search(self, pid=int(item[0]), type="products"))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(item[1]))
            self.tableWidget.setItem(r, 2, QTableWidgetItem(item[5]))
            self.tableWidget.setItem(r, 3, QTableWidgetItem(dot(int(item[4]))))
            self.tableWidget.setItem(r, 4, QTableWidgetItem(dot(int(item[4]) * int(item[5]))))
            self.tableWidget.setItem(r, 5, QTableWidgetItem("x"))
            self.tableWidget.setRowHeight(r, 80)

            # self.tableWidget.item(r, 0).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 1).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 3).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 4).setFlags(Qt.ItemIsEditable)
            self.tableWidget.item(r, 5).setFlags(self.tableWidget.item(r, 5).flags() & ~Qt.ItemIsEditable)

            self.tableWidget.item(r, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 4).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 5).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # self.tableWidget.setStyleSheet("QLineEdit { background-color: rgb(200, 200, 200) }")
            self.tableWidget.item(r, 5).setBackground(QtGui.QColor(255, 0, 0))
            self.tableWidget.item(r, 5).setForeground(QtGui.QColor(255, 255, 255))

            self.tableWidget.item(r, 1).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 3).setForeground(QtGui.QColor(0, 0, 0))
            self.tableWidget.item(r, 4).setForeground(QtGui.QColor(0, 0, 0))

            r += 1

    def eventFilter(self, widget, event):
        if self.time_to_display_import_success == 0:
            self.time_ghim = datetime.now().hour * 3600 + datetime.now().minute * 60 + datetime.now().second
        else:
            time_now = datetime.now().hour * 3600 + datetime.now().minute * 60 + datetime.now().second
            if (time_now - self.time_ghim) >= self.time_to_display_import_success:
                self.time_to_display_import_success = 0
                self.confirm_import_btn.setStyleSheet("")

        if self.text_search_temp == ".none--":
            self.text_search_temp = self.search_box.text()

        text_search = self.search_box.text()
        if len(text_search) != 0:
            self.label_search.setText("")
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
                    self.table_search.setCellWidget(a, 0,
                                                    insert_image_search(self, pid=int(result[a, 0]), type="products"))
                    self.table_search.setItem(a, 1, QTableWidgetItem(result[a, 1]))
                    self.table_search.setRowHeight(a, 80)

        # hover title
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

        elif widget == self.close_search_btn and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/x-circle-red.svg"))
        elif widget == self.close_search_btn and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/x-circle-white.svg"))

        elif widget == self.close_create_product and event.type() == QtCore.QEvent.HoverEnter:
            widget.setIcon(QIcon("./icons/x-circle-red.svg"))
        elif widget == self.close_create_product and event.type() == QtCore.QEvent.HoverLeave:
            widget.setIcon(QIcon("./icons/x-circle-black.svg"))

        else:
            self.maximize_btn.setIcon(QIcon(self.icons_maximize))

        text = "" if self.name_product.text() != "" else "Enter name product"
        self.name_product_s.setText(text)

        text = "" if self.cost_price.text() != "" else "Enter cost price"
        self.cost_price_s.setText(text)

        text = "" if self.retail_price.text() != "" else "Enter retail price"
        self.retail_price_s.setText(text)

        text = self.cost_price.text()
        if text != "" and text[-1] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            text = text[0: len(text)-1]
            self.cost_price.setText(text)

        text = self.retail_price.text()
        if text != "" and text[-1] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            text = text[0: len(text) - 1]
            self.retail_price.setText(text)

        return False

    def _upload_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Image to Upload',
                                                      QDir.currentPath(), 'Images (*.png *.jpg *.jfif)')
            if not filename:
                return
        conn = sqlite3.connect('data.db')
        new_id = int(Ultilities.get_last_id(conn, "Products")) + 1
        conn.close()
        url = "./Image/products/" + str(new_id) + ".png"
        img = Image.open(filename)
        im = img.resize((150, 80))
        im.save(url)
        self.upload_btn.setIcon(QIcon(url))
        self.upload_btn.setIconSize(QSize(150, 80))
        self.image_uploaded = True

    def __open_left_menu(self):
        self.left_menu.setHidden(False)
        self.left_menu_btn.setHidden(True)

    def __close_left_menu(self):
        self.left_menu.setHidden(True)
        self.left_menu_btn.setHidden(False)

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


class ViewHistoryScreen(QMainWindow):
    icons_maximize = './icons/square-white.svg'

    def __init__(self):
        data = user.find_id(now_id)
        super(ViewHistoryScreen, self).__init__()
        loadUi("./GUI/ViewHistory_v.ui", self)

        self.load_data()

        # self.tableWidget.setColumnWidth(0, 150)
        # self.tableWidget.setColumnWidth(1, 200)
        # self.tableWidget.setColumnWidth(2, 80)
        # self.tableWidget.setColumnWidth(3, 100)
        # self.tableWidget.setColumnWidth(4, 100)

        # self.tableWidget.setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget.setStyleSheet("""
        #                                 QTableWidget::item {
        #                                     color:#fff;
        #                                     border: 0px;
        #                                     padding: 5px;
        #                                     font: 30pt Comfortaa;
        #                                     }
        #                                 """)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.resizeColumnsToContents()


        # title app
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.status_title.setText("Status")
        self.minimize_btn.clicked.connect(btn_min_clicked)
        self.maximize_btn.clicked.connect(btn_max_clicked)
        self.close_btn.clicked.connect(btn_close_clicked)
        self.return_home.clicked.connect(goto_menu)
        self.log_out.clicked.connect(_logout)

        # setting for move and resize window
        self.start = QPoint(0, 0)
        self.pressing = False
        QSizeGrip(self.size_grip)

        # animation hover for buttons
        self.close_btn.installEventFilter(self)
        self.log_out.installEventFilter(self)
        self.minimize_btn.installEventFilter(self)
        self.maximize_btn.installEventFilter(self)
        self.return_home.installEventFilter(self)

        # change to screen utilities
        self.log_out.clicked.connect(_logout)
        self.sell_button.clicked.connect(goto_sell)
        self.signup.clicked.connect(goto_sign_up)
        self.import_export_btn.clicked.connect(goto_import_export)
        self.view_stock_btn.clicked.connect(goto_warehouse)
        self.shift_summary_btn.clicked.connect(goto_shift_work)
        self.view_history_btn.clicked.connect(goto_view_history)

        # left-menu
        self.left_menu_btn.clicked.connect(self.__open_left_menu)
        self.close_left_menu.clicked.connect(self.__close_left_menu)
        self.left_menu_btn.setHidden(True)

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
            self.tableWidget.setItem(r, 1, QTableWidgetItem(str(item[3])))
            self.tableWidget.setItem(r, 2, QTableWidgetItem(str(user.find_id(int(item[9]))[1])))
            self.tableWidget.setItem(r, 3, QTableWidgetItem(str(item[4])))
            self.tableWidget.setItem(r, 4, QTableWidgetItem(str(item[5])))
            self.tableWidget.setItem(r, 5, QTableWidgetItem(str(item[6])))
            self.tableWidget.setItem(r, 6, QTableWidgetItem(str(item[7])))
            self.tableWidget.setItem(r, 7, QTableWidgetItem(str(item[8])))

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

            """

            r += 1
        self.sum_price.setText(dot(sum_price))

    def __open_left_menu(self):
        self.left_menu.setHidden(False)
        self.left_menu_btn.setHidden(True)

    def __close_left_menu(self):
        self.left_menu.setHidden(True)
        self.left_menu_btn.setHidden(False)

    def eventFilter(self, widget, event):
        # hover title
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


class SignUpScreen(QMainWindow):
    icons_maximize = './icons/square-white.svg'
    temp = 0
    image_uploaded = False

    def __init__(self):
        data = user.find_id(now_id)
        super(SignUpScreen, self).__init__()
        loadUi("./GUI/SignUp_v.ui", self)

        self.upload_btn.setIcon(QIcon("./icons/upload-white.svg"))

        self.fullname.installEventFilter(self)
        self.birthday.installEventFilter(self)
        self.phone.installEventFilter(self)
        self.position.installEventFilter(self)
        self.username.installEventFilter(self)
        self.password.installEventFilter(self)
        self.identification.installEventFilter(self)

        self.btn_create.clicked.connect(self._signup)
        self.upload_btn.clicked.connect(self._upload_image)

        # title app
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.status_title.setText("Status")
        self.minimize_btn.clicked.connect(btn_min_clicked)
        self.maximize_btn.clicked.connect(btn_max_clicked)
        self.close_btn.clicked.connect(btn_close_clicked)
        self.return_home.clicked.connect(goto_menu)
        self.log_out.clicked.connect(_logout)

        # tab selected style
        self.signup.setStyleSheet("background-color: #2b2c60;")
        # setting for move and resize window
        self.start = QPoint(0, 0)
        self.pressing = False

        # animation hover for buttons
        self.close_btn.installEventFilter(self)
        self.log_out.installEventFilter(self)
        self.minimize_btn.installEventFilter(self)
        self.maximize_btn.installEventFilter(self)
        self.return_home.installEventFilter(self)

        # change to screen utilities
        self.log_out.clicked.connect(_logout)
        self.sell_button.clicked.connect(goto_sell)
        self.signup.clicked.connect(goto_sign_up)
        self.import_export_btn.clicked.connect(goto_import_export)
        self.view_stock_btn.clicked.connect(goto_warehouse)
        self.shift_summary_btn.clicked.connect(goto_shift_work)
        self.view_history_btn.clicked.connect(goto_view_history)

        # left-menu
        self.left_menu_btn.clicked.connect(self.__open_left_menu)
        self.close_left_menu.clicked.connect(self.__close_left_menu)
        self.left_menu_btn.setHidden(True)

    def _upload_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
        conn = sqlite3.connect('data.db')
        new_id = int(Ultilities.get_last_id(conn, "Member")) + 1
        conn.close()
        url = "./Image/user/"+str(new_id)+".png"
        pre_process_img(filename, url)

        self.upload_btn.setIcon(QIcon(url))
        self.upload_btn.setIconSize(QSize(280, 280))
        self.image_uploaded = True

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
        color_error = "color: #f00; "
        if fullname == '':
            # self.fullname_s.setText("Enter the name!")
            self.fullname_s.setStyleSheet(color_error)
        else:
            invalid += 1
        if birthday == '':
            self.birthday_s.setStyleSheet(color_error)
        else:
            date = birthday.split('/')
            temp = 3
            if len(date) != 3:
                self.birthday_s_2.setText("Birthday [dd/mm/yyyy]")
                self.birthday_s.setStyleSheet(color_error)
            else:
                if int(date[0]) > 31:
                    temp -= 1
                if int(date[1]) > 12:
                    temp -= 1
                if int(date[2]) < 1800 or int(date[2]) > 2022:
                    temp -= 1
            if temp == 3:
                invalid += 1
            else:
                self.birthday_s_2.setText("Birthday [dd/mm/yyyy]")
                self.birthday_s.setStyleSheet(color_error)
        if phone == "":
            self.phone_s.setStyleSheet(color_error)
        else:
            invalid += 1
        if position == "Position":
            self.position.setStyleSheet(color_error)
        else:
            invalid += 1
        if username == "":
            self.username_s.setStyleSheet(color_error)
        else:
            invalid += 1
        if password == "":
            self.password_s.setStyleSheet(color_error)
        else:
            invalid += 1
        if identification == "":
            self.identification_s.setStyleSheet(color_error)
        else:
            invalid += 1
        if self.image_uploaded:
            invalid += 1
        else:
            self.upload_btn.setIcon(QIcon("./icons/upload-red.svg"))
            self.upload_stt.setStyleSheet("color: #f00")

        if invalid == 8:
            user.add_member(fullname, username, password, birthday, position, phone, identification)
            self.status.setText("Sign up for <b>" + fullname + "</b> successful!")
            self.status.setStyleSheet("color: rgb(50,255,50);")
        else:
            self.status.setText("Invalid information provided!")
            self.status.setStyleSheet("color: #f55;")

    def eventFilter(self, widget, event):

        # filter input form keyboard
        input_v = self.phone.text()
        if input_v != "" and input_v[-1] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            input_v = input_v[0:len(input_v) - 1]
            self.phone.setText(input_v)
        input_v = self.identification.text()
        if input_v != "" and input_v[-1] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            input_v = input_v[0:len(input_v) - 1]
            self.identification.setText(input_v)
        birth = self.birthday.text()
        if birth != '' and birth[-1] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/'}:
            birth = birth[0:len(birth) - 1]
            self.birthday.setText(birth)

        if self.temp < len(birth):
            if len(birth) == 2 or len(birth) == 5:
                self.birthday.setText(birth + '/')
            elif len(birth) > 10:
                self.birthday.setText(birth[0:10])

        if len(birth) != self.temp:
            self.temp = len(birth)

        # hover title
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

        # animation when input
        text = "Enter Fullname" if (self.fullname.text() == "") else ""
        self.fullname_s.setText(text)
        text = "Enter Birthday" if (self.birthday.text() == "") else ""
        self.birthday_s.setText(text)
        text = "Enter Phone number" if (self.phone.text() == "") else ""
        self.phone_s.setText(text)
        text = "Enter Username" if (self.username.text() == "") else ""
        self.username_s.setText(text)
        text = "Enter Password" if (self.password.text() == "") else ""
        self.password_s.setText(text)
        text = "Enter Identification" if (self.identification.text() == "") else ""
        self.identification_s.setText(text)

        # if self.position.currentIndex() == 0:
        #     self.position.setStyleSheet("color: #555;")
        # else:
        #     self.position.setStyleSheet("color: #000;")

        return False

    def __open_left_menu(self):
        self.left_menu.setHidden(False)
        self.left_menu_btn.setHidden(True)

    def __close_left_menu(self):
        self.left_menu.setHidden(True)
        self.left_menu_btn.setHidden(False)

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


class insert_image_search(QtWidgets.QLabel):
    def __init__(self, parent, pid, type):
        super(insert_image_search, self).__init__(None)

        pic = QtGui.QPixmap("./Image/" + type + "/" + str(pid) + ".png")
        # pic = pic.scaled(20, 100, QtCore.Qt.KeepAspectRatio)
        if type == "products":
            pic = pic.scaled(150, 80)
        elif type == "user":
            pic = pic.scaled(80, 80)
        self.setPixmap(pic)


def pre_process_img(url_img, url_save="van_quy.png"):
    # img to png circle
    img = Image.open(url_img)
    height, width = img.size
    print(img.size)
    if height != width:
        redun = abs(int((height - width) / 2))
        print(redun)
        if height > width:
            img = img.crop((redun, 0, height - redun, width))
        else:
            img = img.crop((0, redun, height, width-redun))
        height, width = img.size

    lum_img = Image.new('L', (height, width), 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice(((0, 0), (height, width)), 0, 360,
                  fill=255, outline="white")
    img_arr = np.array(img)
    lum_img_arr = np.array(lum_img)
    final_img_arr = np.dstack((img_arr, lum_img_arr))
    im = Image.fromarray(final_img_arr)
    print(im.size)
    im.save(url_save)


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
widget.setWindowFlags(Qt.FramelessWindowHint)
widget.show()

try:
    sys.exit(app.exec_())

except Exception as bug:
    print(bug)
    print("Exiting...")
