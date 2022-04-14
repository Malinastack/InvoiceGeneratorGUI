import datetime
from fpdf import FPDF
from tkinter import *
import gui

from tkinter import ttk

# from appJar import gui
# datę wystawienia,
# kolejny numer faktury zgodny z przyjętą numeracją,
# imiona i nazwiska lub nazwę sprzedawcy i nabywcy towaru/usługi oraz ich adresy,
# numer NIP podatnika (sprzedawcy),
# numer NIP, za pomocą którego nabywca jest zidentyfikowany na potrzeby podatku lub podatku od wartości dodanej,
# datę dokonania lub zakończenia dostawy towarów lub wykonania usługi lub datę otrzymania zapłaty, o ile jest określona, i różni się od daty wystawienia faktury,
# nazwę towaru lub usługi,
# jednostkę miary oraz ilość sprzedanych towarów lub usług,
# cenę jednostkową netto towaru lub usługi,
# kwoty wszelkich rabatów, obniżek i opustów,
# wartość sprzedaży netto,
# stawkę VAT oraz wartość podatku,
# sumę sprzedaży netto, z podziałem na wartości objęte poszczególnymi stawkami podatku oraz sprzedaż zwolnioną od podatku,
# kwoty podatku VAT z podziałem na poszczególne stawki,
# kwotę należności ogółem.


class Generator:
    def generator_1(self):
        i = 0
        x = datetime.datetime.now()
        while True:
            yield f"FV/{i}/{x.year}/{x.month}"
            i += 1


class Invoice:
    pdf = FPDF()
    list_of_products = []
    invoice_listbox = 0

    def save_to_pdf(self):
        self.pdf.add_page()
        self.pdf.add_font("DejaVu", "", "DejaVuSansCondensed.ttf", uni=True)
        self.pdf.set_font("DejaVu", "", 14)
        f = self.__str__()
        self.pdf.write(10, txt=f)
        self.pdf.output("Test.pdf")

    def generate_item_list(self, product):
        return f"""
               Nazwa towaru/usługi: {product['name']} 
               Ilość: {product['quantity']} 
               Cena jednostkowa: {product['cost']}zł 
               Wysokość podatku: {product['rate']}% 
               Netto: {product['netto']}zł 
               Brutto: {product['brutto']}zł"""

    def __init__(self):
        self.gen = Generator.generator_1(self)
        self.invoice_number = next(self.gen)
        self.seller = StringVar()
        self.buyer = StringVar()
        self.seller_nip = StringVar()
        self.buyer_nip = StringVar()
        self.list_of_products = Product.list_of_products

    def __str__(self):
        msg = f"""Numer faktury: {self.invoice_number}
               Imię i nazwisko sprzedawcy: {self.seller.get()}
               Imię i nazwisko nabywcy: {self.buyer.get()}
               NIP sprzedawcy: {self.seller_nip.get()}
               NIP nabywcy: {self.buyer_nip.get()}
               """
        msg2 = "\n".join(
            [self.generate_item_list(product) for product in self.list_of_products]
        )
        return msg + msg2


class Product:
    product = {}
    list_of_products = []

    def __init__(self):
        self.products()

    def products(self):
        self.product = {
            "name": self.product["name"],
            "quantity": self.product["quantity"],
            "cost": self.product["cost"],
            "rate": self.product["rate"],
            "netto": 0,
            "brutto": 0,
        }
        self.product["netto"] = float(self.product["quantity"]) * float(
            self.product["cost"]
        )
        self.product["brutto"] = float(self.product["netto"]) + float(
            self.product["netto"]
        ) * (float(self.product["rate"]) / 100)
        self.list_of_products.append(self.product)

    # def add_product(self, listbox):
    #     listbox.insert("end", self.list_of_products[-1]["name"])
