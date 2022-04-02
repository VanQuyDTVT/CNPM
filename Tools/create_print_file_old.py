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
import random
from borb.pdf.pdf import PDF
from PIL import Image as PILImage
import os


def dot(number):
    number = int(number)
    first = True
    if number == 0:
        result = "0"
    else:
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


def _logo():
    height = 60
    img = PILImage.open('./Image/logo.pqy')  # .convert('L') # convert to gray
    width = int(height * img.size[0] / img.size[1])
    img = img.resize((width, height))

    table = Table(number_of_rows=1, number_of_columns=1, horizontal_alignment=Alignment.CENTERED)
    table.add(
        Image(
            img,
            height=Decimal(50),
            width=Decimal(180),
            horizontal_alignment=Alignment.CENTERED,
        ))
    # table.add(Paragraph("PQY STORE", font_size=30))
    table.no_borders()
    return table


def _build_invoice_information():
    table_001 = Table(number_of_rows=5, number_of_columns=3)

    table_001.add(Paragraph("Date: ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    now = datetime.now()
    table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))
    table_001.add(Paragraph("[Street Address]"))

    table_001.add(Paragraph("[City, State, ZIP Code]"))
    table_001.add(Paragraph("Invoice #", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d" % random.randint(1000, 10000)))

    table_001.add(Paragraph("[Phone]"))
    table_001.add(Paragraph("Due Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))

    table_001.add(Paragraph("[Email Address]"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.add(Paragraph("[Company Website]"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


def _build_billing_and_shipping_information():
    table_001 = Table(number_of_rows=6, number_of_columns=2)
    table_001.add(
        Paragraph(
            "BILL TO",
            background_color=HexColor("263238"),
            font_color=X11Color("White"),
        )
    )
    table_001.add(
        Paragraph(
            "SHIP TO",
            background_color=HexColor("263238"),
            font_color=X11Color("White"),
        )
    )
    table_001.add(Paragraph("[Recipient Name]"))        # BILLING
    table_001.add(Paragraph("[Recipient Name]"))        # SHIPPING
    table_001.add(Paragraph("[Company Name]"))          # BILLING
    table_001.add(Paragraph("[Company Name]"))          # SHIPPING
    table_001.add(Paragraph("[Street Address]"))        # BILLING
    table_001.add(Paragraph("[Street Address]"))        # SHIPPING
    table_001.add(Paragraph("[City, State, ZIP Code]")) # BILLING
    table_001.add(Paragraph("[City, State, ZIP Code]")) # SHIPPING
    table_001.add(Paragraph("[Phone]"))                 # BILLING
    table_001.add(Paragraph("[Phone]"))                 # SHIPPING
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


def _build_itemized_description_table(data, tax, discount):
    row = len(data) + 7
    table_001 = Table(number_of_rows=row, number_of_columns=4,
                      column_widths=[Decimal(0.5), Decimal(0.1), Decimal(0.2), Decimal(0.2)])

    table_001.add(TableCell(Paragraph("Name", font_color=X11Color("White")), background_color=HexColor("000000")))
    table_001.add(TableCell(Paragraph("Amount", font_color=X11Color("White"), horizontal_alignment=Alignment.CENTERED),
                            background_color=HexColor("000000")))
    table_001.add(TableCell(Paragraph("Price", font_color=X11Color("White"), horizontal_alignment=Alignment.RIGHT),
                            background_color=HexColor("000000")))
    table_001.add(TableCell(Paragraph("Changes", font_color=X11Color("White"), horizontal_alignment=Alignment.RIGHT),
                            background_color=HexColor("000000")))

    odd_color = HexColor("BBBBBB")
    even_color = HexColor("FFFFFF")
    row_number = 1
    total = 0
    for item in data:
        c = even_color if row_number % 2 == 0 else odd_color
        table_001.add(TableCell(Paragraph(item[1]), background_color=c))
        table_001.add(TableCell(Paragraph(dot(item[5]), horizontal_alignment=Alignment.CENTERED), background_color=c))
        table_001.add(TableCell(Paragraph(dot(item[3]), horizontal_alignment=Alignment.RIGHT), background_color=c))
        table_001.add(TableCell(Paragraph(dot(int(item[5]) * int(item[3])), horizontal_alignment=Alignment.RIGHT), background_color=c))
        total += int(item[5]) * int(item[3])
        row_number += 1

    # Optionally add some empty rows to have a fixed number of rows for styling purposes
    for row_numberr in range(row_number, row_number+2):
        c = even_color if row_numberr % 2 == 0 else odd_color
        for _ in range(0, 4):
            table_001.add(TableCell(Paragraph(" "), background_color=c))

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


def print_bill(data, tax=0, discount=0):
    pdf = Document()
    page = Page()
    pdf.append_page(page)

    page_layout = SingleColumnLayout(page)
    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)

    page_layout.add(_logo())
    page_layout.add(_build_invoice_information())
    # page_layout.add(Paragraph(" "))
    page_layout.add(_build_billing_and_shipping_information())
    page_layout.add(_build_itemized_description_table(data, tax, discount))

    with open("output.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)

    os.system("output.pdf")
    os.remove("output.pdf")



