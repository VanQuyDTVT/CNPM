from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from datetime import datetime
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.color.color import HexColor, X11Color

from borb.pdf.pdf import PDF
from PIL import Image as PILImage
import os


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


def _logo():
    height = 250
    img = PILImage.open('./Image/logo.png')  # .convert('L') # convert to gray
    width = int(height * img.size[0] / img.size[1])
    img = img.resize((width, height))

    table = Table(number_of_rows=1, number_of_columns=1, horizontal_alignment=Alignment.CENTERED)
    table.add(
        Image(
            img,
            height=Decimal(100),
            width=Decimal(100),
            horizontal_alignment=Alignment.CENTERED,
        ))
    # table.add(Paragraph("PQY STORE", font_size=30))
    table.no_borders()
    return table


def _build_():
    # height = 200
    img = PILImage.open('./Image/line.png')  # .convert('L') # convert to gray
    # width = int(height * img.size[0] / img.size[1])
    # img = img.resize((width, height))

    table = Table(number_of_rows=1, number_of_columns=1, horizontal_alignment=Alignment.CENTERED)
    table.add(
        Image(
            img,
            height=Decimal(20),
            width=Decimal(330),
            horizontal_alignment=Alignment.CENTERED,
        ))
    # table.add(Paragraph("PQY STORE", font_size=30))
    table.no_borders()
    return table


def _build_information(title, font_size=40):
    table_001 = Table(number_of_rows=1, number_of_columns=1)
    table_001.add(Paragraph(title, font_size=font_size, font="Helvetica-Bold", horizontal_alignment=Alignment.CENTERED, ))
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


def _thank_you_():
    table_001 = Table(number_of_rows=3, number_of_columns=1)
    table_001.add(Paragraph("Thank you!!! ", font_size=10, font="Helvetica-Bold", horizontal_alignment=Alignment.CENTERED, ))
    table_001.add(Paragraph("PassWifi: NgocYencute ^_^", font_size=10, font="Helvetica-Bold", horizontal_alignment=Alignment.CENTERED, ))
    table_001.add(Paragraph("Address: TrongtimYenne ~.~", font_size=10, font="Helvetica-Bold",
                            horizontal_alignment=Alignment.CENTERED, ))
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


def _note(note):
    table_001 = Table(number_of_rows=3, number_of_columns=1)
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph("Note: " + note, font_size=10, font="Helvetica-Bold",
                            horizontal_alignment=Alignment.CENTERED, ))
    table_001.add(Paragraph(" "))
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


def _line_():
    table_001 = Table(number_of_rows=1, number_of_columns=1)
    table_001.add(Paragraph("------------------------------------", horizontal_alignment=Alignment.CENTERED, ))
    table_001.no_borders()
    return table_001


def _build_invoice_information(id_bill=0, data=None):
    table_001 = Table(number_of_rows=2, number_of_columns=3)
    table_001.add(Paragraph(" "))
    if id_bill == 0:
        table_001.add(Paragraph(" ", horizontal_alignment=Alignment.CENTERED))
    else:
        table_001.add(Paragraph("ID bill: " + str(id_bill), horizontal_alignment=Alignment.CENTERED))
    table_001.add(Paragraph(" "))
    if data is None:
        now = datetime.now()
        time = str(now.time())[0:8]
        table_001.add(Paragraph("Time: " + time, horizontal_alignment=Alignment.RIGHT))
        table_001.add(Paragraph(" "))
        table_001.add(Paragraph("Date: %d/%d/%d" % (now.day, now.month, now.year)))
    else:
        table_001.add(Paragraph("Start: " + data[0][2] + " - " + data[0][1][0:8], horizontal_alignment=Alignment.RIGHT))
        table_001.add(Paragraph(" "))
        table_001.add(Paragraph("End: " + data[-1][2] + " - " + data[-1][1][0:8]))

    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


def _build_itemized_description_table(data, tax, discount, code=0):
    row = len(data) + 6
    table_001 = Table(number_of_rows=row, number_of_columns=4,
                      column_widths=[Decimal(0.5), Decimal(0.1), Decimal(0.2), Decimal(0.2)])

    table_001.add(TableCell(Paragraph("Name", font_color=X11Color("White")), background_color=HexColor("000000")))
    table_001.add(TableCell(Paragraph("Amount", font_color=X11Color("White"), horizontal_alignment=Alignment.CENTERED),
                            background_color=HexColor("000000")))
    table_001.add(TableCell(Paragraph("Price", font_color=X11Color("White"), horizontal_alignment=Alignment.RIGHT),
                            background_color=HexColor("000000")))
    table_001.add(TableCell(Paragraph("Changes", font_color=X11Color("White"), horizontal_alignment=Alignment.RIGHT),
                            background_color=HexColor("000000")))

    odd_color = HexColor("AAAAAA")
    even_color = HexColor("DDDDDD")
    other_color = HexColor("FFFFFF")
    row_number = 1
    total = 0
    if code == 0:
        # print bill sell
        for item in data:
            c = even_color if (row_number % 2 == 0) else odd_color
            table_001.add(TableCell(Paragraph(item[1]), background_color=c))
            table_001.add(
                TableCell(Paragraph(dot(item[5]), horizontal_alignment=Alignment.CENTERED), background_color=c))
            table_001.add(TableCell(Paragraph(dot(item[3]), horizontal_alignment=Alignment.RIGHT), background_color=c))
            table_001.add(TableCell(Paragraph(dot(int(item[5]) * int(item[3])), horizontal_alignment=Alignment.RIGHT),
                                    background_color=c))
            total += int(item[5]) * int(item[3])
            row_number += 1
    elif code == 1:
        # print_bill_shift_working
        for item in data:
            c = even_color if row_number % 2 == 0 else odd_color
            table_001.add(TableCell(Paragraph(item[4]), background_color=c))
            table_001.add(
                TableCell(Paragraph(dot(item[5]), horizontal_alignment=Alignment.CENTERED), background_color=c))
            table_001.add(TableCell(Paragraph(dot(item[6]), horizontal_alignment=Alignment.RIGHT), background_color=c))
            table_001.add(TableCell(Paragraph(dot(int(item[5]) * int(item[6])), horizontal_alignment=Alignment.RIGHT),
                                    background_color=c))
            total += int(item[5]) * int(item[6])
            row_number += 1
    elif code == 2:
        # print bill shift warehouse

        row = len(data) + 1
        table_001 = Table(number_of_rows=row, number_of_columns=2,
                          column_widths=[Decimal(0.6), Decimal(0.3)])

        table_001.add(TableCell(Paragraph("Name", font_color=X11Color("White")), background_color=HexColor("000000")))
        table_001.add(
            TableCell(Paragraph("Amount", font_color=X11Color("White"), horizontal_alignment=Alignment.CENTERED),
                      background_color=HexColor("000000")))

        for item in data:
            c = even_color if row_number % 2 == 0 else odd_color
            table_001.add(TableCell(Paragraph(item[1]), background_color=c))
            table_001.add(
                TableCell(Paragraph(dot(item[5]), horizontal_alignment=Alignment.CENTERED), background_color=c))
            row_number += 1

        table_001.no_borders()
        return table_001
    elif code == 3:
        # wholesales bill
        for item in data:
            c = even_color if (row_number % 2 == 0) else odd_color
            table_001.add(TableCell(Paragraph(item[1]), background_color=c))
            table_001.add(
                TableCell(Paragraph(dot(item[5]), horizontal_alignment=Alignment.CENTERED), background_color=c))
            table_001.add(TableCell(Paragraph(dot(item[4]), horizontal_alignment=Alignment.RIGHT), background_color=c))
            table_001.add(TableCell(Paragraph(dot(int(item[5]) * int(item[4])), horizontal_alignment=Alignment.RIGHT),
                                    background_color=c))
            total += int(item[5]) * int(item[4])
            row_number += 1

    # Optionally add some empty rows to have a fixed number of rows for styling purposes
    for row_number in range(row_number, row_number+1):
        for _ in range(0, 4):
            table_001.add(TableCell(Paragraph(" "), background_color=other_color))

    table_001.add(
        TableCell(Paragraph("Subtotal", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT, ), col_span=3, ))
    table_001.add(TableCell(Paragraph(dot(total) + " VND", horizontal_alignment=Alignment.RIGHT)))
    table_001.add(
        TableCell(Paragraph("Discounts", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT, ), col_span=3, ))
    discounts = int(total * discount)
    table_001.add(TableCell(Paragraph(dot(discounts) + " VND", horizontal_alignment=Alignment.RIGHT)))
    table_001.add(
        TableCell(Paragraph("Taxes", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3, ))
    taxes = int(total * tax)
    table_001.add(TableCell(Paragraph(dot(taxes) + " VND", horizontal_alignment=Alignment.RIGHT)))
    table_001.add(
        TableCell(Paragraph("Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT), col_span=3, ))
    table_001.add(TableCell(Paragraph(dot(total - discount + taxes) + " VND", horizontal_alignment=Alignment.RIGHT)))
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


def print_bill(data, id_bill, tax=0, discount=0):
    pdf = Document()
    page = Page()
    pdf.append_page(page)
    page_layout = SingleColumnLayout(page)
    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)
    page_layout.add(_logo())
    page_layout.add(_build_information("PAY BILL"))
    page_layout.add(_build_invoice_information(id_bill))
    page_layout.add(_build_())
    page_layout.add(_build_itemized_description_table(data, tax, discount))
    page_layout.add(Paragraph(" "))
    page_layout.add(_line_())
    page_layout.add(_thank_you_())

    with open(".output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)

    os.startfile(".output.pdf")
    # os.remove("output.pdf")


def print_bill_shift_working(data, tax=0, discount=0, title="SHIFT WORKING"):
    pdf = Document()
    page = Page()
    pdf.append_page(page)
    page_layout = SingleColumnLayout(page)
    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)
    page_layout.add(_logo())
    page_layout.add(_build_information(title))
    page_layout.add(_build_invoice_information(data=data))
    page_layout.add(_build_())
    page_layout.add(_build_itemized_description_table(data, tax, discount, code=1))

    with open(".output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)

    os.startfile(".output.pdf")
    # os.remove("output.pdf")


def print_transfer_bill(data, note):
    pdf = Document()
    page = Page()
    pdf.append_page(page)
    page_layout = SingleColumnLayout(page)
    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)
    page_layout.add(_logo())
    page_layout.add(_build_information("WAREHOUSE TRANSFER BILL", 22))
    page_layout.add(_build_invoice_information())
    if note != "":
        page_layout.add(_note(note))
    page_layout.add(_build_())
    page_layout.add(_build_itemized_description_table(data, tax=0, discount=0, code=2))
    page_layout.add(_line_())

    with open(".output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)
    os.startfile(".output.pdf")
    # os.remove("output.pdf")


def print_wholesales_bill(data, note):
    pdf = Document()
    page = Page()
    pdf.append_page(page)
    page_layout = SingleColumnLayout(page)
    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)
    page_layout.add(_logo())
    page_layout.add(_build_information("WHOLESALES BILL"))
    page_layout.add(_build_invoice_information())
    if note != "":
        page_layout.add(_note(note))
    page_layout.add(_build_())
    page_layout.add(_build_itemized_description_table(data, tax=0, discount=0, code=3))
    page_layout.add(_line_())

    with open(".output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)
    os.startfile(".output.pdf")
    # os.remove("output.pdf")