from tkinter import Label, Entry, Button, Tk, Listbox, LEFT, END
import datetime
from fpdf import FPDF


class Generator:
    def generator_1(self):
        i = 0
        x = datetime.datetime.now()
        while True:
            yield f"FV/{i}/{x.year}/{x.month}"
            i += 1


class App:
    list_of_products = []
    product = {}
    pdf = FPDF()

    def submit(self):
        self.seller = self.seller_entry.get()
        self.buyer = self.buyer_entry.get()
        self.seller_nip = self.seller_nip_entry.get()
        self.buyer_nip = self.buyer_nip_entry.get()

    def save_to_pdf(self):
        self.pdf.add_page()
        self.pdf.add_font("DejaVu", "", "DejaVuSansCondensed.ttf", uni=True)
        self.pdf.set_font("DejaVu", "", 14)
        f = self.__str__()
        self.pdf.write(10, txt=f)
        self.pdf.output("Test.pdf")

    def clear(self):
        self.product_name_entry.delete(0, END)
        self.product_quantity_entry.delete(0, END)
        self.product_cost_entry.delete(0, END)
        self.product_rate_entry.delete(0, END)

    def generate_item_list(self, product):
        return f"""
        Nazwa towaru/usługi: {product['name']} 
        Ilość: {product['quantity']} 
        Cena jednostkowa: {product['cost']}zł 
        Wysokość podatku: {product['rate']}% 
        Netto: {product['netto']}zł 
        Brutto: {product['brutto']}zł"""

    def add_product(self):
        self.product = {
            "name": self.product_name_entry.get(),
            "quantity": self.product_quantity_entry.get(),
            "cost": self.product_cost_entry.get(),
            "rate": self.product_rate_entry.get(),
            "netto": 0,
            "brutto": 0,
        }
        self.product["netto"] = float(self.product["quantity"]) * float(
            self.product["cost"]
        )
        self.product["brutto"] = float(self.product["netto"]) + \
            float(self.product["netto"]) * (float(self.product["rate"]) / 100)
        self.list_of_products.append(self.product)

    def add_to_listbox(self, listbox):
        listbox.insert("end", self.list_of_products[-1]["name"])

    def add_invoice_product(self):
        add_product = Tk()
        add_product.title("Dodawanie produktu/usługi")
        add_product.geometry("400x400")
        Label(add_product, text="Nazwa produktu/usługi").pack()
        self.product_name_entry = Entry(add_product, width=40)
        self.product_name_entry.pack()
        Label(add_product, text="Ilość").pack()
        self.product_quantity_entry = Entry(add_product, width=40)
        self.product_quantity_entry.pack()
        Label(add_product, text="Cena jednostkowa").pack()
        self.product_cost_entry = Entry(add_product, width=40)
        self.product_cost_entry.pack()
        Label(add_product, text="Wysokość podatku").pack()
        self.product_rate_entry = Entry(add_product, width=40)
        self.product_rate_entry.pack()
        button = Button(
            add_product,
            text="Zatwierdź",
            command=lambda: [self.add_product(), self.add_to_listbox(self.listbox), self.clear()]
        )
        button.pack(side=LEFT)

    def add_invoice(self):
        add_invoice = Tk()
        add_invoice.title("Dodawanie faktury")
        add_invoice.geometry("400x400")
        Label(add_invoice, text="Imię i nazwisko sprzedawcy").pack()
        self.seller_entry = Entry(add_invoice, width=40)
        self.seller_entry.pack()
        Label(add_invoice, text="Imię i nazwisko nabywcy").pack()
        self.buyer_entry = Entry(add_invoice, width=40)
        self.buyer_entry.pack()
        Label(add_invoice, text="NIP sprzedawcy").pack()
        self.seller_nip_entry = Entry(add_invoice, width=40)
        self.seller_nip_entry.pack()
        Label(add_invoice, text="NIP nabywcy").pack()
        self.buyer_nip_entry = Entry(add_invoice, width=40)
        self.buyer_nip_entry.pack()
        Label(add_invoice, text="Lista produktów/usług:").pack()
        self.listbox = Listbox(add_invoice, bg="#f7ffde", width=40, font=('Arial', 10))
        self.listbox.pack(padx=5, pady=10)
        button = Button(
            add_invoice, text="Dodaj produkt", command=self.add_invoice_product
        )
        button.pack(side=LEFT)
        button2 = Button(
            add_invoice,
            text="Zatwierdź",
            command=lambda: [self.submit(), print(self.__str__())],
        )
        button2.pack(side=LEFT)
        button2 = Button(
            add_invoice,
            text="Zapisz jako PDF",
            command=lambda: [self.save_to_pdf()],
        )
        button2.pack(side=LEFT)
        self.window.destroy()

    def __init__(self):
        self.window = Tk()
        self.gen = Generator.generator_1(self)
        self.invoice_number = next(self.gen)
        self.seller_entry = None
        self.buyer_entry = None
        self.seller_nip_entry = None
        self.buyer_nip_entry = None
        self.product_name_entry = None
        self.product_quantity_entry = None
        self.product_cost_entry = None
        self.product_rate_entry = None
        self.seller = None
        self.buyer = None
        self.buyer_nip = None
        self.seller_nip = None
        self.listbox = None
        self.window.title("Generator faktur")
        self.window.geometry("300x200")
        self.window.configure(bg="#3089B6")
        button = Button(
            self.window,
            text="Dodaj fakturę",
            command=self.add_invoice,
            width=20,
            bg="#67767E",
        )
        button.pack(padx=10, pady=10)
        button2 = Button(
            self.window,
            text="Edytuj fakturę",
            command=self.add_invoice,
            width=20,
            bg="#67767E",
        )
        button2.pack(padx=10, pady=10)
        button3 = Button(
            self.window,
            text="Drukuj fakturę",
            command=self.add_invoice,
            width=20,
            bg="#67767E",
        )
        button3.pack(padx=10, pady=10)
        button4 = Button(
            self.window,
            text="Lista faktur",
            command=self.add_invoice,
            width=20,
            bg="#67767E",
        )
        button4.pack(padx=10, pady=10)
        self.window.mainloop()

    def __str__(self):
        msg = f"""Numer faktury: {self.invoice_number}
        Imię i nazwisko sprzedawcy: {self.seller}
        Imię i nazwisko nabywcy: {self.buyer}
        NIP sprzedawcy: {self.seller_nip}
        NIP nabywcy: {self.buyer_nip}"""
        msg2 = "\n".join(
            [self.generate_item_list(product) for product in self.list_of_products]
        )
        return msg + msg2



cos = App()
