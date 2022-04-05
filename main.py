import sys
import sqlite3
import numpy as np

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import QEvent, QPoint, pyqtSignal, Qt, QDir, QSize
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QGraphicsDropShadowEffect, QSizeGrip, \
    QTableWidgetItem, QAbstractScrollArea, QFileDialog, QLabel, QApplication, QStackedWidget
from Tools import user, product, search, history, Ultilities
from Tools.create_print_file import print_bill, print_bill_shift_working, print_transfer_bill, print_wholesales_bill
from datetime import datetime
from PIL import Image, ImageDraw
# from ui_Login import *

now_id = None
type_window = True
icons_maximize = './icons/square-white.svg'


def dot(number):
    result = ""
    number = int(number)
    while number > 0:
        t = number % 1000
        number = number - int(t)
        number = int(number / 1000)
        if number > 0:
            for i in range(len(str(t)), 3):
                t = "0" + str(t)
        if result == "":
            result = str(t)
        else:
            result = str(t) + "." + result

    return result


def goto_menu():
    widget.addWidget(MenuScreen())
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_sell():
    widget.addWidget(SellScreen())
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_shift_work():
    widget.addWidget(ShiftSummaryScreen())
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_view_history():
    widget.addWidget(ViewHistoryScreen())
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_warehouse():
    widget.addWidget(ViewStockScreen())
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_sign_up():
    widget.addWidget(SignUpScreen())
    widget.setCurrentIndex(widget.currentIndex() + 1)


def goto_import_export():
    widget.addWidget(ImportExportScreen())
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
        super(LoginScreen, self).__init__()
        self.movement = None
        self.end = None
        self.pressing = None
        self.start = None
        loadUi("./GUI/Login.ui", self)
        # Ui_mainWindow.setupUi(self)

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

    def eventFilter(self, widget_name, event):
        if widget_name == self.login and event.type() == QEvent.HoverEnter:
            self.on_hovered()
        elif widget_name == self.login and event.type() == QEvent.HoverLeave:
            self.hover_out()

        elif widget_name == self.yes_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/check-red.svg"))
            self.icon_emotion.setPixmap(QPixmap('./Image/sad.png'))
            self.label_3.setText("Goodbye")
        elif widget_name == self.yes_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/check-black.svg"))
            self.icon_emotion.setPixmap(QPixmap('./Image/happy.png'))
            self.label_3.setText("Close")

        elif widget_name == self.no_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-dark_blue.svg"))
            self.icon_emotion.setPixmap(QPixmap('./Image/happy.png'))
            self.label_3.setText("Welcome")
        elif widget_name == self.no_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-black.svg"))
            self.icon_emotion.setPixmap(QPixmap('./Image/sad.png'))
            self.label_3.setText("Close")

        elif widget_name == self.close_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/power-red.svg"))
        elif widget_name == self.close_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/power-black.svg"))

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

    def __init__(self):
        # setup
        self.movement = None
        self.end = None
        data = user.find_id(now_id)
        super(MenuScreen, self).__init__()

        # title
        loadUi("./GUI/Menu.ui", self)
        self.setMinimumSize(1080, 300)
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.state_title = "Wellcome - Have a great day at work!"
        self.minimize_btn.clicked.connect(btn_min_clicked)
        self.maximize_btn.clicked.connect(btn_max_clicked)
        self.close_btn.clicked.connect(btn_close_clicked)

        # change to screen utilities
        if data[5] == "Manager":
            self.log_out.clicked.connect(_logout)
            self.sell_button.clicked.connect(goto_sell)
            self.signup.clicked.connect(goto_sign_up)
            self.import_export_btn.clicked.connect(goto_import_export)
            self.view_stock_btn.clicked.connect(goto_warehouse)
            self.shift_summary_btn.clicked.connect(goto_shift_work)
            self.view_history_btn.clicked.connect(goto_view_history)
        elif data[5] == "Seller":
            self.log_out.clicked.connect(_logout)
            self.sell_button.clicked.connect(goto_sell)
            self.signup.setHidden(True)
            self.import_export_btn.clicked.connect(goto_import_export)
            self.view_stock_btn.clicked.connect(goto_warehouse)
            self.shift_summary_btn.clicked.connect(goto_shift_work)
            self.view_history_btn.setHidden(True)

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

    def eventFilter(self, widget_name, event):
        global icons_maximize

        self.update_time()
        if widget_name == self.minimize_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/minus-dark_blue.svg"))
        elif widget_name == self.minimize_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/minus-white.svg"))

        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverEnter:
            if type_window:
                icons_maximize = "./icons/square-dark_blue.svg"
            else:
                icons_maximize = "./icons/minimize-dark_blue.svg"
        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverLeave:
            if type_window:
                icons_maximize = "./icons/square-white.svg"
            else:
                icons_maximize = "./icons/minimize-white.svg"

        elif widget_name == self.log_out and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/log-out-red.svg"))
        elif widget_name == self.log_out and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/log-out-white.svg"))

        elif widget_name == self.close_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-red.svg"))
        elif widget_name == self.close_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-white.svg"))
        else:
            self.maximize_btn.setIcon(QIcon(icons_maximize))

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
    c_search_box = pyqtSignal()
    bill = list()
    discount = 0
    tax = 0
    text_search_temp = ".none--"

    def __init__(self):
        self.movement = None
        self.end = None
        data = user.find_id(now_id)
        super(SellScreen, self).__init__()
        loadUi("./GUI/Sell.ui", self)

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
        # self.log_out.clicked.connect(_logout)
        # self.sell_button.clicked.connect(goto_sell)
        # self.signup.clicked.connect(goto_sign_up)
        # self.import_export_btn.clicked.connect(goto_import_export)
        # self.view_stock_btn.clicked.connect(goto_warehouse)
        # self.shift_summary_btn.clicked.connect(goto_shift_work)
        # self.view_history_btn.clicked.connect(goto_view_history)
        if data[5] == "Manager":
            self.log_out.clicked.connect(_logout)
            self.sell_button.clicked.connect(goto_sell)
            self.signup.clicked.connect(goto_sign_up)
            self.import_export_btn.clicked.connect(goto_import_export)
            self.view_stock_btn.clicked.connect(goto_warehouse)
            self.shift_summary_btn.clicked.connect(goto_shift_work)
            self.view_history_btn.clicked.connect(goto_view_history)
        elif data[5] == "Seller":
            self.log_out.clicked.connect(_logout)
            self.sell_button.clicked.connect(goto_sell)
            self.signup.setHidden(True)
            self.import_export_btn.clicked.connect(goto_import_export)
            self.view_stock_btn.clicked.connect(goto_warehouse)
            self.shift_summary_btn.clicked.connect(goto_shift_work)
            self.view_history_btn.setHidden(True)

        # setting for sell-screen
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
        if len(self.bill) > 0:
            id_bill = Ultilities.get_id_bill()
            print_bill(self.bill, id_bill)
            for item in range(0, len(self.bill)):
                index = self.bill[0][0]
                name = self.bill[0][1]
                amount = self.bill[0][2]
                price = self.bill[0][3]
                sold = self.bill[0][5]

                history.add_history(id_bill, name, sold, price, self.discount, self.tax, now_id)
                product.sell(index, int(amount), int(sold))
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
                    if str(self.bill[row][5]) != str(item.text()):
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
                for element in self.bill:
                    if result[0][0] == element[0]:
                        element[5] = str(int(element[5]) + 1)
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
        sum_total = 0
        row = len(self.bill)
        self.tableWidget.setRowCount(row)
        r = 0
        for item in self.bill:
            sum_total += int(item[3]) * int(item[5])
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
            self.tableWidget.item(r, 4).setBackground(QColor(255, 0, 0))
            self.tableWidget.item(r, 4).setForeground(QColor(255, 255, 255))

            self.tableWidget.item(r, 0).setForeground(QColor(0, 0, 0))
            self.tableWidget.item(r, 2).setForeground(QColor(0, 0, 0))
            self.tableWidget.item(r, 3).setForeground(QColor(0, 0, 0))

            r += 1

        if sum_total == 0:
            self.label_total.setText("0")
        else:
            self.label_total.setText(dot(sum_total))

    def eventFilter(self, widget_name, event):
        global icons_maximize

        size_window = self.tableWidget.size().width()
        self.tableWidget.setColumnWidth(0, int(size_window*0.37))
        self.tableWidget.setColumnWidth(1, int(size_window*0.1))
        self.tableWidget.setColumnWidth(2, int(size_window*0.2))
        self.tableWidget.setColumnWidth(3, int(size_window*0.2))
        self.tableWidget.setColumnWidth(4, int(size_window*0.1))

        if type_window:
            self.tableWidget.setStyleSheet("font: 12pt;")
        else:
            self.tableWidget.setStyleSheet("font: 14pt;")

        # hover title
        if widget_name == self.minimize_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/minus-dark_blue.svg"))
        elif widget_name == self.minimize_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/minus-white.svg"))

        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverEnter:
            if type_window:
                icons_maximize = "./icons/square-dark_blue.svg"
            else:
                icons_maximize = "./icons/minimize-dark_blue.svg"
        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverLeave:
            if type_window:
                icons_maximize = "./icons/square-white.svg"
            else:
                icons_maximize = "./icons/minimize-white.svg"

        elif widget_name == self.log_out and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/log-out-red.svg"))
        elif widget_name == self.log_out and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/log-out-white.svg"))

        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/menu-dark_blue.svg"))
        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/menu-white.svg"))

        elif widget_name == self.close_search_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-circle-red.svg"))
        elif widget_name == self.close_search_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-circle-white.svg"))

        elif widget_name == self.close_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-red.svg"))
        elif widget_name == self.close_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-white.svg"))

        elif widget_name == self.return_home and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/home-dark_blue.svg"))
        elif widget_name == self.return_home and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/home-white.svg"))

        else:
            self.maximize_btn.setIcon(QIcon(icons_maximize))

        # search
        if self.text_search_temp == ".none--":
            self.text_search_temp = self.search_box.text()

        text_search = self.search_box.text()
        if len(text_search) != 0:
            self.label_search.setText("")
        else:
            self.label_search.setText("Search")
            text_search = "-all"

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
                    self.table_search.setCellWidget(
                        a, 0, insert_image_search(self, pid=int(result[a, 0]), type_img="products"))
                    self.table_search.setItem(a, 1, QTableWidgetItem(result[a, 1]))
                    # self.table_search.item(a, 1).setTextAlignment(Qt.AlignHCenter)
                    self.table_search.setRowHeight(a, 80)
                # self.table_search.item(0, 1).setBackground(QColor(0, 255, 0))

        if widget_name == self.search_box:
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
    data_stock = search.search("-view-stock")
    data_update = data_stock.copy()
    will_change = False

    def __init__(self):
        self.movement = None
        self.end = None
        data = user.find_id(now_id)
        super(ViewStockScreen, self).__init__()
        loadUi("./GUI/View_Stock.ui", self)

        self.load_data()

        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 100)

        self.confirm_btn.clicked.connect(self.__confirm_edit)
        self.cancel_btn.clicked.connect(self.__cancel_edit)

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
        self.left_menu_btn.installEventFilter(self)

        # change to screen utilities
        if data[5] == "Manager":
            self.log_out.clicked.connect(_logout)
            self.sell_button.clicked.connect(goto_sell)
            self.signup.clicked.connect(goto_sign_up)
            self.import_export_btn.clicked.connect(goto_import_export)
            self.view_stock_btn.clicked.connect(goto_warehouse)
            self.shift_summary_btn.clicked.connect(goto_shift_work)
            self.view_history_btn.clicked.connect(goto_view_history)
        elif data[5] == "Seller":
            self.log_out.clicked.connect(_logout)
            self.sell_button.clicked.connect(goto_sell)
            self.signup.setHidden(True)
            self.import_export_btn.clicked.connect(goto_import_export)
            self.view_stock_btn.clicked.connect(goto_warehouse)
            self.shift_summary_btn.clicked.connect(goto_shift_work)
            self.view_history_btn.setHidden(True)

        # left-menu
        self.left_menu_btn.clicked.connect(self.__open_left_menu)
        self.close_left_menu.clicked.connect(self.__close_left_menu)
        self.left_menu_btn.setHidden(True)

        self.tableWidget.itemChanged.connect(self.log_change)
        self.data_stock = search.search("-view-stock")
        self.data_update = self.data_stock.copy()
        self.will_change = True
        self.load_data(data=self.data_update)
        self.will_change = False

        if user.find_id(now_id)[5] != "Manager":
            self.confirm_btn.setHidden(True)
            self.cancel_btn.setHidden(True)

    def log_change(self, item):
        if not self.will_change:
            if str(self.data_update[item.row()][item.column()]) != str(item.text()):
                if item.column() in {2, 3, 4}:
                    check = True
                    for c in range(0, len(item.text())):
                        if item.text()[c] not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                            check = False
                            break
                    if check:
                        # self.tableWidget.item(item.row(), item.column()).setForeground(QColor(255, 0, 0))
                        self.data_update[item.row()][item.column()] = item.text()
            self.will_change = True
            self.load_data(data=self.data_update)
            self.will_change = False

    def __cancel_edit(self):
        self.will_change = True
        self.load_data()
        self.will_change = False
        self.data_update = self.data_stock.copy()

    def __confirm_edit(self):
        for item in self.data_update:
            type_change = ["id", "name", "amount", "retail_price", "cost_price"]
            for i in range(1, len(item)):
                product.change_information_product(item[0], type_change[i], item[i])

        self.data_stock = search.search("-view-stock")
        self.data_update = self.data_stock.copy()
        self.will_change = True
        self.load_data()
        self.will_change = False

    def load_data(self, data=None):
        if data is None:
            data = self.data_stock
        row = len(data)
        self.status_table.setText("Number of product: "+str(row))
        self.tableWidget.setRowCount(row)
        r = 0
        for item in data:
            self.tableWidget.setCellWidget(r, 0, insert_image_search(self, pid=int(item[0]), type_img="products"))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(item[1]))
            self.tableWidget.setItem(r, 2, QTableWidgetItem(dot(int(item[2]))))
            self.tableWidget.setItem(r, 3, QTableWidgetItem(dot(int(item[3]))))
            self.tableWidget.setItem(r, 4, QTableWidgetItem(dot(int(item[4]))))
            self.tableWidget.setItem(r, 5, QTableWidgetItem("--/--/----"))

            if user.find_id(now_id)[5] != "Manager":
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

            self.tableWidget.setRowHeight(r, 80)

            if int(item[2]) < 10:
                for j in range(1, self.tableWidget.columnCount()):
                    self.tableWidget.item(r, j).setBackground(QColor(255, 100, 100))
            elif int(item[2]) < 30:
                for j in range(1, self.tableWidget.columnCount()):
                    self.tableWidget.item(r, j).setBackground(QColor(255, 200, 150))
            elif int(item[2]) < 50:
                for j in range(1, self.tableWidget.columnCount()):
                    self.tableWidget.item(r, j).setBackground(QColor(255, 255, 150))
            # self.tableWidget.item(r, 0).setForeground(QColor(0, 0, 0))

            for i in range(1, 5):
                if item[i] == self.data_stock[r][i]:
                    self.tableWidget.item(r, i).setForeground(QColor(0, 0, 0))
                else:
                    self.tableWidget.item(r, i).setForeground(QColor(255, 255, 255))
                    self.tableWidget.item(r, i).setBackground(QColor(10, 10, 10))

            self.tableWidget.item(r, 5).setForeground(QColor(0, 0, 0))
            r += 1

    def __open_left_menu(self):
        self.left_menu.setHidden(False)
        self.left_menu_btn.setHidden(True)

    def __close_left_menu(self):
        self.left_menu.setHidden(True)
        self.left_menu_btn.setHidden(False)

    def eventFilter(self, widget_name, event):
        global icons_maximize

        if type_window:
            self.tableWidget.setStyleSheet("font: 12pt Comfortaa;")
        else:
            self.tableWidget.setStyleSheet("font: 16pt Comfortaa;")

        size_window = self.tableWidget.size().width()
        # self.tableWidget.setColumnWidth(0, int(size_window * 0.2))
        self.tableWidget.setColumnWidth(1, int(size_window * 0.2))
        self.tableWidget.setColumnWidth(2, int(size_window * 0.2))
        self.tableWidget.setColumnWidth(3, int(size_window * 0.15))
        self.tableWidget.setColumnWidth(4, int(size_window * 0.15))
        self.tableWidget.setColumnWidth(5, int(size_window * 0))

        # hover title
        if widget_name == self.minimize_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/minus-dark_blue.svg"))
        elif widget_name == self.minimize_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/minus-white.svg"))

        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverEnter:
            if type_window:
                icons_maximize = "./icons/square-dark_blue.svg"
            else:
                icons_maximize = "./icons/minimize-dark_blue.svg"
        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverLeave:
            if type_window:
                icons_maximize = "./icons/square-white.svg"
            else:
                icons_maximize = "./icons/minimize-white.svg"

        elif widget_name == self.log_out and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/log-out-red.svg"))
        elif widget_name == self.log_out and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/log-out-white.svg"))

        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/menu-dark_blue.svg"))
        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/menu-white.svg"))

        elif widget_name == self.close_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-red.svg"))
        elif widget_name == self.close_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-white.svg"))

        elif widget_name == self.return_home and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/home-dark_blue.svg"))
        elif widget_name == self.return_home and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/home-white.svg"))

        else:
            self.maximize_btn.setIcon(QIcon(icons_maximize))

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
    
    select = None
    data_shift_working = []
    data_shift_short = []
    mode_view = 0

    def __init__(self):
        self.movement = None
        self.end = None
        data = user.find_id(now_id)
        super(ShiftSummaryScreen, self).__init__()
        loadUi("./GUI/Shift_Summary.ui", self)

        self.print_btn.clicked.connect(self.__print_bill)
        self.total_shift.clicked.connect(self.__total_shift)
        self.total_shift_day.clicked.connect(self.__total_shift_day)
        self.total_shift_month.clicked.connect(self.__total_shift_month)
        self.total_shift_custom.clicked.connect(self.__total_shift_custom)
        self.render_btn.clicked.connect(self.__render_total_custom)
        self.show_time.clicked.connect(self.__show_time)
        self.custom_setting.setHidden(True)

        if data[5] != "Manager":
            self.total_shift_day.setHidden(True)
            self.total_shift_month.setHidden(True)
            self.total_shift_custom.setHidden(True)

        self.horizontalSpacer_9.setHidden(True)
        self.horizontalSpacer_10.setHidden(True)
        self.horizontalSpacer_11.setHidden(True)
        self.time_from.setHidden(True)
        self.time_to.setHidden(True)

        time_now = datetime.now()
        self.dateEdit.setDate(datetime.now().date())
        self.dateEdit_2.setDate(datetime.now().date())

        # mode view
        if self.mode_view == 0:
            self.normal_view_btn.setStyleSheet("background-color: #2b2c60")
        elif self.mode_view == 1:
            self.bill_view_btn.setStyleSheet("background-color: #2b2c60")
        elif self.mode_view == 2:
            self.product_view_btn.setStyleSheet("background-color: #2b2c60")

        self.normal_view_btn.clicked.connect(self.__normal_view)
        self.bill_view_btn.clicked.connect(self.__bill_view)
        self.product_view_btn.clicked.connect(self.__product_view)

        # title app
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.status_title.setText("Shift Working")
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
        self.left_menu_btn.installEventFilter(self)

        # change to screen utilities
        if data[5] == "Manager":
            self.log_out.clicked.connect(_logout)
            self.sell_button.clicked.connect(goto_sell)
            self.signup.clicked.connect(goto_sign_up)
            self.import_export_btn.clicked.connect(goto_import_export)
            self.view_stock_btn.clicked.connect(goto_warehouse)
            self.shift_summary_btn.clicked.connect(goto_shift_work)
            self.view_history_btn.clicked.connect(goto_view_history)
        elif data[5] == "Seller":
            self.log_out.clicked.connect(_logout)
            self.sell_button.clicked.connect(goto_sell)
            self.signup.setHidden(True)
            self.import_export_btn.clicked.connect(goto_import_export)
            self.view_stock_btn.clicked.connect(goto_warehouse)
            self.shift_summary_btn.clicked.connect(goto_shift_work)
            self.view_history_btn.setHidden(True)

        # left-menu
        self.left_menu_btn.clicked.connect(self.__open_left_menu)
        self.close_left_menu.clicked.connect(self.__close_left_menu)
        self.left_menu_btn.setHidden(True)

    def __normal_view(self):
        self.mode_view = 0
        self.__change_mode_view()

    def __bill_view(self):
        self.mode_view = 1
        self.__change_mode_view()

    def __product_view(self):
        self.mode_view = 2
        self.__change_mode_view()

    def __change_mode_view(self):
        self.normal_view_btn.setStyleSheet("")
        self.bill_view_btn.setStyleSheet("")
        self.product_view_btn.setStyleSheet("")
        if self.mode_view == 0:
            self.normal_view_btn.setStyleSheet("background-color: #2b2c60")

        elif self.mode_view == 1:
            self.bill_view_btn.setStyleSheet("background-color: #2b2c60")

        elif self.mode_view == 2:
            self.product_view_btn.setStyleSheet("background-color: #2b2c60")

        self.load_data(self.data_shift_working)

    def __print_bill(self):
        if self.data_shift_short is []:
            print_bill_shift_working(self.data_shift_working, title="SHIFT WORKING")
        else:
            print_bill_shift_working(self.data_shift_short, title="SHIFT WORKING")

        for item in range(0, len(self.data_shift_working)):
            index = self.data_shift_working[item][0]
            history.shift_case(index)
            # self.data_shift_working.pop(0)
        self.data_shift_working = []
        self.load_data(self.data_shift_working)

    def __open_left_menu(self):
        self.left_menu.setHidden(False)
        self.left_menu_btn.setHidden(True)

    def __close_left_menu(self):
        self.left_menu.setHidden(True)
        self.left_menu_btn.setHidden(False)

    def __total_shift_month(self):
        self.select = 3
        self.custom_setting.setHidden(True)
        self.horizontalSpacer_9.setHidden(True)
        self.horizontalSpacer_10.setHidden(True)
        self.horizontalSpacer_11.setHidden(True)

        self.data_shift_working = search.history("-shift-working-month")
        empty = np.array([])
        if str(self.data_shift_working) == str(empty):
            self.title_table.setText("Still no orders this month")
        else:
            if str(self.data_shift_working[0][2][5]) == '0':
                month_string = str(self.data_shift_working[0][2][6:7])
            else:
                month_string = str(self.data_shift_working[0][2][5:7])
            self.title_table.setText("Total Sale of Month " + month_string)
        self.load_data(data=self.data_shift_working)

    def __total_shift_day(self):
        self.select = 2
        self.custom_setting.setHidden(True)
        self.horizontalSpacer_9.setHidden(True)
        self.horizontalSpacer_10.setHidden(True)
        self.horizontalSpacer_11.setHidden(True)
        self.data_shift_working = search.history("-shift-working-day")
        empty = np.array([])
        if str(self.data_shift_working) == str(empty):
            self.title_table.setText("Still no orders today")
        else:
            if str(self.data_shift_working[0][2][9]) == '0':
                day = str(self.data_shift_working[0][2][11:12])
            else:
                day = str(self.data_shift_working[0][2][10:12])
            self.title_table.setText("Total Sale of Day " + day)
        self.load_data(data=self.data_shift_working)

    def __total_shift(self):
        self.custom_setting.setHidden(True)
        self.horizontalSpacer_9.setHidden(True)
        self.horizontalSpacer_10.setHidden(True)
        self.horizontalSpacer_11.setHidden(True)
        self.data_shift_working = search.history("-shift-working")

        self.title_table.setText("Total Shift Revenue of " + str(user.find_id(now_id)[1]))
        self.load_data(data=self.data_shift_working)
        self.select = 1

    def load_data(self, data):
        data_display = []
        size_table = []
        height = self.tableWidget.size().height()

        if self.mode_view == 0:
            data_display = data
            size_table = [0.15, 0.12, 0.1, 0.12, 0.1, 0.1, 0.1, 0.08, 0.08]

        elif self.mode_view == 1:
            size_table = [0.2, 0.2, 0.15, 0, 0, 0, 0.15, 0.13, 0.13]
            for item in data.copy():
                if len(data_display) == 0:
                    data_display.append(item)
                    data_display[-1][6] = str(int(data_display[-1][6]) * int(data_display[-1][5]))
                else:
                    exist = False
                    for item_new in data_display:
                        if item[3] == item_new[3]:
                            item_new[6] = str(int(item_new[6]) + int(item[6])*int(item[5]))
                            item_new[5] = "1"
                            exist = True
                            break
                    if not exist:
                        data_display.append(item)
                        data_display[-1][6] = str(int(data_display[-1][6]) * int(data_display[-1][5]))

        elif self.mode_view == 2:
            size_table = [0, 0, 0, 0.2, 0.1, 0.2, 0.2, 0.1, 0.1]
            for item in data.copy():
                if len(data_display) == 0:
                    data_display.append(item)
                else:
                    exist = False
                    for item_new in data_display:
                        if item[4] == item_new[4]:
                            item_new[5] = str(int(item_new[5]) + int(item[5]))
                            exist = True
                            break
                    if not exist:
                        data_display.append(item)

            self.data_shift_short = data_display

        size_window = self.tableWidget.size().width()

        for i in range(0, 9):
            self.tableWidget.setColumnWidth(i, int(size_window * size_table[i]))

        row = len(data_display)
        self.tableWidget.setRowCount(row)
        sum_price = 0
        if row > 0:
            r = 0
            for item in data_display:
                if item[3] not in {"Import", "Export"}:

                    sum_price += int(item[5]) * int(item[6])
                    self.tableWidget.setItem(r, 0, QTableWidgetItem(item[2] + " " + item[1][0:8]))
                    self.tableWidget.setItem(r, 1, QTableWidgetItem(item[3]))
                    self.tableWidget.setItem(r, 2, QTableWidgetItem(str(user.find_id(int(item[9]))[1])))
                    self.tableWidget.setItem(r, 3, QTableWidgetItem(item[4]))
                    self.tableWidget.setItem(r, 4, QTableWidgetItem(item[5]))
                    self.tableWidget.setItem(r, 5, QTableWidgetItem(dot(item[6])))
                    self.tableWidget.setItem(r, 6, QTableWidgetItem(dot(int(item[5])*int(item[6]))))
                    self.tableWidget.setItem(r, 7, QTableWidgetItem(item[7]))
                    self.tableWidget.setItem(r, 8, QTableWidgetItem(item[8]))

                    self.tableWidget.item(r, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.item(r, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.item(r, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.item(r, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.item(r, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.item(r, 5).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.tableWidget.item(r, 6).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.tableWidget.item(r, 7).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.tableWidget.item(r, 8).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                    if not r % 2:
                        for j in range(0, self.tableWidget.columnCount()):
                            self.tableWidget.item(r, j).setBackground(QColor(222, 222, 255))

                    r += 1
            self.sum_price.setText("Total Revenue: " + dot(sum_price))
        else:
            self.sum_price.setText("Total Revenue: " + str(sum_price))

    def __show_time(self):
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
        self.horizontalSpacer_9.setHidden(False)
        self.horizontalSpacer_10.setHidden(False)
        self.horizontalSpacer_11.setHidden(False)

    def __render_total_custom(self):
        date_start = self.dateEdit.date()
        date_end = self.dateEdit_2.date()
        if self.show_time.text() == " Only Date":
            time_start = self.time_from.time()
            time_end = self.time_to.time()
            self.data_shift_working = history.bill_in_time_custom(
                date_start.year(), date_start.month(), date_start.day(),
                date_end.year(), date_end.month(), date_end.day(),
                time_start.toString("h"), time_start.toString("mm"),
                time_end.toString("h"), time_end.toString("mm"))
            self.title_table.setText(
                "Total Shift Revenue of " +
                str(date_start.toString("yyyy/MM/dd")) +
                " " + str(time_start.toString("HH:mm")) + " - " +
                str(date_end.toString("yyyy/MM/dd")) + " " + str(time_end.toString("HH:mm")))
        else:
            self.data_shift_working = history.bill_in_time_custom(
                date_start.year(), date_start.month(), date_start.day(),
                date_end.year(), date_end.month(), date_end.day())
            self.title_table.setText("Total Shift Revenue of " +
                                     str(date_start.toString("yyyy/MM/dd")) + " - " +
                                     str(date_end.toString("yyyy/MM/dd")))

        self.load_data(data=self.data_shift_working)

    def eventFilter(self, widget_name, event):
        global icons_maximize

        size_window = self.tableWidget.size().width()

        if self.mode_view == 0:
            self.tableWidget.setColumnWidth(0, int(size_window * 0.17))
            self.tableWidget.setColumnWidth(1, int(size_window * 0.1))
            self.tableWidget.setColumnWidth(2, int(size_window * 0.1))
            self.tableWidget.setColumnWidth(3, int(size_window * 0.15))
            self.tableWidget.setColumnWidth(4, int(size_window * 0.07))
            self.tableWidget.setColumnWidth(5, int(size_window * 0.1))
            self.tableWidget.setColumnWidth(6, int(size_window * 0.1))
            self.tableWidget.setColumnWidth(7, int(size_window * 0.1))
            self.tableWidget.setColumnWidth(8, int(size_window * 0.07))
        elif self.mode_view == 1:
            self.tableWidget.setColumnWidth(0, int(size_window * 0.2))
            self.tableWidget.setColumnWidth(1, int(size_window * 0.15))
            self.tableWidget.setColumnWidth(2, int(size_window * 0.15))
            self.tableWidget.setColumnWidth(3, int(size_window * 0))
            self.tableWidget.setColumnWidth(4, int(size_window * 0))
            self.tableWidget.setColumnWidth(5, int(size_window * 0))
            self.tableWidget.setColumnWidth(6, int(size_window * 0.15))
            self.tableWidget.setColumnWidth(7, int(size_window * 0.15))
            self.tableWidget.setColumnWidth(8, int(size_window * 0.15))
        elif self.mode_view == 2:
            self.tableWidget.setColumnWidth(0, int(size_window * 0))
            self.tableWidget.setColumnWidth(1, int(size_window * 0))
            self.tableWidget.setColumnWidth(2, int(size_window * 0))
            self.tableWidget.setColumnWidth(3, int(size_window * 0.2))
            self.tableWidget.setColumnWidth(4, int(size_window * 0.1))
            self.tableWidget.setColumnWidth(5, int(size_window * 0.15))
            self.tableWidget.setColumnWidth(6, int(size_window * 0.2))
            self.tableWidget.setColumnWidth(7, int(size_window * 0.1))
            self.tableWidget.setColumnWidth(8, int(size_window * 0.1))

        if type_window:
            self.tableWidget.setStyleSheet("font: 12pt Comfortaa;")
        else:
            self.tableWidget.setStyleSheet("font: 16pt Comfortaa;")

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
        if widget_name == self.minimize_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/minus-dark_blue.svg"))
        elif widget_name == self.minimize_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/minus-white.svg"))

        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverEnter:
            if type_window:
                icons_maximize = "./icons/square-dark_blue.svg"
            else:
                icons_maximize = "./icons/minimize-dark_blue.svg"
        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverLeave:
            if type_window:
                icons_maximize = "./icons/square-white.svg"
            else:
                icons_maximize = "./icons/minimize-white.svg"

        elif widget_name == self.log_out and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/log-out-red.svg"))
        elif widget_name == self.log_out and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/log-out-white.svg"))

        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/menu-dark_blue.svg"))
        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/menu-white.svg"))

        elif widget_name == self.close_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-red.svg"))
        elif widget_name == self.close_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-white.svg"))

        elif widget_name == self.return_home and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/home-dark_blue.svg"))
        elif widget_name == self.return_home and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/home-white.svg"))

        else:
            self.maximize_btn.setIcon(QIcon(icons_maximize))

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
    
    import_selected = True
    transfer_selected = True
    time_to_display_import_success = 0

    def __init__(self):
        self.movement = None
        self.end = None
        self.time_s = None
        data = user.find_id(now_id)
        super(ImportExportScreen, self).__init__()
        loadUi("./GUI/Import_Export.ui", self)

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
        self.status_title.setText("Import / Export Products")
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
        self.left_menu_btn.installEventFilter(self)

        # change to screen utilities
        if data[5] == "Manager":
            self.log_out.clicked.connect(_logout)
            self.sell_button.clicked.connect(goto_sell)
            self.signup.clicked.connect(goto_sign_up)
            self.import_export_btn.clicked.connect(goto_import_export)
            self.view_stock_btn.clicked.connect(goto_warehouse)
            self.shift_summary_btn.clicked.connect(goto_shift_work)
            self.view_history_btn.clicked.connect(goto_view_history)
        elif data[5] == "Seller":
            self.log_out.clicked.connect(_logout)
            self.sell_button.clicked.connect(goto_sell)
            self.signup.setHidden(True)
            self.import_export_btn.clicked.connect(goto_import_export)
            self.view_stock_btn.clicked.connect(goto_warehouse)
            self.shift_summary_btn.clicked.connect(goto_shift_work)
            self.view_history_btn.setHidden(True)

        # left-menu
        self.left_menu_btn.clicked.connect(self.__open_left_menu)
        self.close_left_menu.clicked.connect(self.__close_left_menu)
        self.left_menu_btn.setHidden(True)

    def __confirm(self):
        note_str = self.lineEdit_note.text()
        if not self.import_selected:
            if self.transfer_selected:
                print_transfer_bill(self.bill, note=note_str)
            else:
                print_wholesales_bill(self.bill, note=note_str)

        for item in self.bill:
            if self.import_selected:
                product.import_product(item[0], item[2], item[5])
                history.add_history("Import", item[1], item[5], item[3], discount=0, tax=0,
                                    seller=now_id, out_case=True, note=note_str)
            else:
                product.export_product(item[0], item[2], item[5])
                history.add_history("Export", item[1], item[5], item[4], discount=0, tax=0,
                                    seller=now_id, out_case=True, note=note_str)

        self.lineEdit_note.setText("")
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
                for element in self.bill:
                    if result[0][0] == element[0]:
                        element[5] = str(int(element[5]) + 1)
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
                    if str(self.bill[row][5]) != str(item.text()):
                        self.bill[row][5] = item.text()
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
            self.tableWidget.setCellWidget(r, 0, insert_image_search(self, pid=int(item[0]), type_img="products"))
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
            self.tableWidget.item(r, 5).setBackground(QColor(255, 0, 0))
            self.tableWidget.item(r, 5).setForeground(QColor(255, 255, 255))

            self.tableWidget.item(r, 1).setForeground(QColor(0, 0, 0))
            self.tableWidget.item(r, 3).setForeground(QColor(0, 0, 0))
            self.tableWidget.item(r, 4).setForeground(QColor(0, 0, 0))

            r += 1

    def eventFilter(self, widget_name, event):
        global icons_maximize
        if self.time_to_display_import_success == 0:
            self.time_s = datetime.now().hour * 3600 + datetime.now().minute * 60 + datetime.now().second
        else:
            time_now = datetime.now().hour * 3600 + datetime.now().minute * 60 + datetime.now().second
            if (time_now - self.time_s) >= self.time_to_display_import_success:
                self.time_to_display_import_success = 0
                self.confirm_import_btn.setStyleSheet("")

        if self.text_search_temp == ".none--":
            self.text_search_temp = self.search_box.text()

        text_search = self.search_box.text()
        if len(text_search) != 0:
            self.label_search.setText("")
        else:
            self.label_search.setText("Search")
            text_search = "-all"

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
                    self.table_search.setCellWidget(
                        a, 0, insert_image_search(self, pid=int(result[a, 0]), type_img="products"))
                    self.table_search.setItem(a, 1, QTableWidgetItem(result[a, 1]))
                    self.table_search.setRowHeight(a, 80)

        # hover title
        if widget_name == self.minimize_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/minus-dark_blue.svg"))
        elif widget_name == self.minimize_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/minus-white.svg"))

        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverEnter:
            if type_window:
                icons_maximize = "./icons/square-dark_blue.svg"
            else:
                icons_maximize = "./icons/minimize-dark_blue.svg"
        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverLeave:
            if type_window:
                icons_maximize = "./icons/square-white.svg"
            else:
                icons_maximize = "./icons/minimize-white.svg"

        elif widget_name == self.log_out and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/log-out-red.svg"))
        elif widget_name == self.log_out and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/log-out-white.svg"))

        elif widget_name == self.close_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-red.svg"))
        elif widget_name == self.close_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-white.svg"))

        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/menu-dark_blue.svg"))
        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/menu-white.svg"))

        elif widget_name == self.return_home and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/home-dark_blue.svg"))
        elif widget_name == self.return_home and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/home-white.svg"))

        elif widget_name == self.close_search_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-circle-red.svg"))
        elif widget_name == self.close_search_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-circle-white.svg"))

        elif widget_name == self.close_create_product and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-circle-red.svg"))
        elif widget_name == self.close_create_product and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-circle-black.svg"))

        else:
            self.maximize_btn.setIcon(QIcon(icons_maximize))

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

    def __init__(self):
        self.movement = None
        self.end = None
        data = user.find_id(now_id)
        super(ViewHistoryScreen, self).__init__()
        loadUi("./GUI/View_History.ui", self)

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
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.resizeColumnsToContents()

        # title app
        self.name_user.setText(str(data[1]) + " [" + str(data[5]) + "]  ")
        url = './Image/user/' + str(now_id) + '.png'
        self.name_user.setIcon(QIcon(url))
        self.status_title.setText("History")
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
        self.left_menu_btn.installEventFilter(self)

        # tab selected style
        self.view_history_btn.setStyleSheet("background-color: #2b2c60;")

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
        row = len(data)
        self.tableWidget.setRowCount(row)
        r = 0
        sum_price = 0

        for item in data:
            if item[3] not in {"Import", "Export"}:
                sum_price += int(item[5]) * int(item[6])

            self.tableWidget.setItem(r, 0, QTableWidgetItem(item[2] + " " + item[1][0:8]))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(str(item[3])))
            self.tableWidget.setItem(r, 2, QTableWidgetItem(str(user.find_id(int(item[9]))[1])))
            self.tableWidget.setItem(r, 3, QTableWidgetItem(str(item[4])))
            self.tableWidget.setItem(r, 4, QTableWidgetItem(dot(item[5])))
            self.tableWidget.setItem(r, 5, QTableWidgetItem(dot(item[6])))
            self.tableWidget.setItem(r, 6, QTableWidgetItem(dot(item[7])))
            self.tableWidget.setItem(r, 7, QTableWidgetItem(dot(item[8])))
            self.tableWidget.setItem(r, 8, QTableWidgetItem(str(item[12])))

            self.tableWidget.item(r, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(r, 5).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 6).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.item(r, 7).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            r += 1
        self.sum_price.setText("Sum Revenue:  " + dot(sum_price) + "  VND")

    def __open_left_menu(self):
        self.left_menu.setHidden(False)
        self.left_menu_btn.setHidden(True)

    def __close_left_menu(self):
        self.left_menu.setHidden(True)
        self.left_menu_btn.setHidden(False)

    def eventFilter(self, widget_name, event):
        global icons_maximize

        if type_window:
            self.tableWidget.setStyleSheet("font: 12pt Comfortaa;")
        else:
            self.tableWidget.setStyleSheet("font: 16pt Comfortaa;")

        size_window = self.tableWidget.size().width()
        self.tableWidget.setColumnWidth(0, int(size_window * 0.16))
        self.tableWidget.setColumnWidth(1, int(size_window * 0.1))
        self.tableWidget.setColumnWidth(2, int(size_window * 0.1))
        self.tableWidget.setColumnWidth(3, int(size_window * 0.14))
        self.tableWidget.setColumnWidth(4, int(size_window * 0.07))
        self.tableWidget.setColumnWidth(5, int(size_window * 0.1))
        self.tableWidget.setColumnWidth(6, int(size_window * 0.07))
        self.tableWidget.setColumnWidth(7, int(size_window * 0.07))

        # hover title
        if widget_name == self.minimize_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/minus-dark_blue.svg"))
        elif widget_name == self.minimize_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/minus-white.svg"))

        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverEnter:
            if type_window:
                icons_maximize = "./icons/square-dark_blue.svg"
            else:
                icons_maximize = "./icons/minimize-dark_blue.svg"
        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverLeave:
            if type_window:
                icons_maximize = "./icons/square-white.svg"
            else:
                icons_maximize = "./icons/minimize-white.svg"

        elif widget_name == self.log_out and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/log-out-red.svg"))
        elif widget_name == self.log_out and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/log-out-white.svg"))

        elif widget_name == self.close_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-red.svg"))
        elif widget_name == self.close_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-white.svg"))

        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/menu-dark_blue.svg"))
        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/menu-white.svg"))

        elif widget_name == self.return_home and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/home-dark_blue.svg"))
        elif widget_name == self.return_home and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/home-white.svg"))

        else:
            self.maximize_btn.setIcon(QIcon(icons_maximize))

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
    
    temp = 0
    image_uploaded = False

    def __init__(self):
        self.movement = None
        self.end = None
        data = user.find_id(now_id)
        super(SignUpScreen, self).__init__()
        loadUi("./GUI/Sign_Up.ui", self)

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
        self.left_menu_btn.installEventFilter(self)

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

    def eventFilter(self, widget_name, event):
        global icons_maximize
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
        if widget_name == self.minimize_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/minus-dark_blue.svg"))
        elif widget_name == self.minimize_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/minus-white.svg"))

        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverEnter:
            if type_window:
                icons_maximize = "./icons/square-dark_blue.svg"
            else:
                icons_maximize = "./icons/minimize-dark_blue.svg"
        elif widget_name == self.maximize_btn and event.type() == QEvent.HoverLeave:
            if type_window:
                icons_maximize = "./icons/square-white.svg"
            else:
                icons_maximize = "./icons/minimize-white.svg"

        elif widget_name == self.log_out and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/log-out-red.svg"))
        elif widget_name == self.log_out and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/log-out-white.svg"))

        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/menu-dark_blue.svg"))
        elif widget_name == self.left_menu_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/menu-white.svg"))

        elif widget_name == self.close_btn and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/x-red.svg"))
        elif widget_name == self.close_btn and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/x-white.svg"))

        elif widget_name == self.return_home and event.type() == QEvent.HoverEnter:
            widget_name.setIcon(QIcon("./icons/home-dark_blue.svg"))
        elif widget_name == self.return_home and event.type() == QEvent.HoverLeave:
            widget_name.setIcon(QIcon("./icons/home-white.svg"))

        else:
            self.maximize_btn.setIcon(QIcon(icons_maximize))

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


class insert_image_search(QLabel):
    def __init__(self, parent, pid, type_img):
        super(insert_image_search, self).__init__(None)
        self.parent = parent
        pic = QPixmap("./Image/" + type_img + "/" + str(pid) + ".png")
        # pic = pic.scaled(20, 100, Qt.KeepAspectRatio)
        if type_img == "products":
            pic = pic.scaled(150, 80)
        elif type_img == "user":
            pic = pic.scaled(80, 80)
        self.setPixmap(pic)


def pre_process_img(url_img, url_save="van_quy.png"):
    # img to png circle
    img = Image.open(url_img)
    height, width = img.size
    if height != width:
        redun = abs(int((height - width) / 2))
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
    im.save(url_save)


# main
app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
size_app = [1080, 720]
login = LoginScreen()
widget = QStackedWidget()
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
