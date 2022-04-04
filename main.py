import datetime
from fpdf import FPDF
from tkinter import *
import tkinter as tk
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
from tkinter import ttk

LARGEFONT = ("Verdana", 35)


class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Invoice, Product):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)
        button1 = ttk.Button(self, text="Invoice",
                             command=lambda: controller.show_frame(Invoice))
        button1.grid(row=1, column=1, padx=10, pady=10)


class Generator:
    def generator_1(self):
        i = 0
        x = datetime.datetime.now()
        while True:
            yield f"FV/{i}/{x.year}/{x.month}"
            i += 1


class Invoice(tk.Frame):
    pdf = FPDF()
    invoice_number = ""
    seller = ""
    buyer = ""
    seller_nip = ""
    buyer_nip = ""

    def save_to_pdf(self):
        self.pdf.add_page()
        self.pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.pdf.set_font('DejaVu', '', 14)
        f = self.__str__()
        self.pdf.write(10, txt=f)
        self.pdf.output("Test.pdf")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        content = ttk.Frame(self,  borderwidth=5)
        content.grid(column=0, row=0)
        self.gen = Generator.generator_1(self)
        self.invoice_number = next(self.gen)
        self.seller = StringVar()
        self.buyer = StringVar()
        self.seller_nip = StringVar()
        self.buyer_nip = StringVar()
        label = ttk.Label(content, text='Imię i nazwisko sprzedawcy:')
        label.grid(column=0, row=1)
        label2 = ttk.Label(content, text='Imię i nazwisko nabywcy:')
        label2.grid(column=0, row=3)
        label3 = ttk.Label(content, text='NIP sprzedawcy:')
        label3.grid(column=0, row=5)
        label4 = ttk.Label(content, text='NIP nabywcy:')
        label4.grid(column=0, row=7)
        label8 = ttk.Label(content, text='Aby dodać produkt/usługę wciśnij przycisk --->')
        label8.grid(column=0, row=10)
        seller_entry = tk.Entry(content, width=50, textvariable=self.seller)
        seller_entry.grid(column=0, row=2)
        buyer_entry = tk.Entry(content, width=50, textvariable=self.buyer)
        buyer_entry.grid(column=0, row=4)
        seller_nip_entry = tk.Entry(content, width=50, textvariable=self.seller_nip)
        seller_nip_entry.grid(column=0, row=6)
        buyer_nip_entry = tk.Entry(content, width=50, textvariable=self.buyer_nip)
        buyer_nip_entry.grid(column=0, row=8)
        button1 = ttk.Button(content, text="Product",
                             command=lambda: controller.show_frame(Product))
        button1.grid(row=9, column=1)
        button2 = ttk.Button(content, text="Save to PDF", command=self.save_to_pdf)
        button2.grid(column=1, row=2)


    def __str__(self):
        msg =  f"""Numer faktury: {self.invoice_number}
               Imię i nazwisko sprzedawcy: {self.seller.get()}
               Imię i nazwisko nabywcy: {self.buyer.get()}
               NIP sprzedawcy: {self.seller_nip.get()}
               NIP nabywcy: {self.buyer_nip.get()}"""
        return msg


class Product(tk.Frame):
    pdf = FPDF()
    product = {}
    list_of_products = []
    my_listbox = 0
    payment_brutto = 0
    payment_netto = 0
    tax = 0

    def products(self):
        self.product = {"name": self.product['name'].get(),
                        "quantity": self.product['quantity'].get(),
                        "cost": self.product['cost'].get(),
                        "rate": self.product['rate'].get(),
                        "netto": 0,
                        "brutto": 0,
                        }
        self.product['netto'] = float(self.product['quantity'])*float(self.product['cost'])
        self.product['brutto'] = float(self.product['netto'])+float(self.product['netto'])*(float(self.product['rate'])/100)
        self.payment_brutto += self.product['brutto']
        self.payment_netto += self.product['netto']
        self.tax = (float(self.payment_brutto))-(float(self.payment_netto))
        self.list_of_products.append(self.product)
        window = tk.Toplevel()

        label = tk.Label(window, text="Poprawnie dodano produkt/usługe!")
        label.pack(fill='x', padx=50, pady=5)

        button_close = tk.Button(window, text="Close", command=window.destroy)
        button_close.pack(fill='x')

    def generate_item_list(self, item):
        return f"""Nazwa towaru/usługi: {item['name']} \
               Ilość: {item['quantity']} \
               Cena jednostkowa: {item['cost']}zł \
               Wysokość podatku: {item['rate']}% \
               Netto: {item['netto']}zł \
               Brutto: {item['brutto']}zł"""

    def add_product(self, listbox):
        listbox.insert('end', self.list_of_products[-1]['name'])

    def save_to_pdf(self):
        Invoice.pdf.add_page()
        Invoice.pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        Invoice.pdf.set_font('DejaVu', '', 14)
        f = self.__str__()
        Invoice.pdf.write(10, txt=f)
        Invoice.pdf.output("Test.pdf")

    def product_window(self):
        self.product = {"name": StringVar(),
                        "quantity": StringVar(),
                        "cost": StringVar(),
                        "rate": StringVar(),
                        "netto": 0,
                        "brutto": 0}
        self.payment_brutto = 0
        self.payment_netto = 0
        self.tax = 0
        window = tk.Toplevel()

        label5 = ttk.Label(window, text='Nazwa produktu/usługi:')
        label5.grid(column=0, row=12)
        label6 = ttk.Label(window, text='Ilość:')
        label6.grid(column=0, row=14)
        label7 = ttk.Label(window, text='Cena jednostkowa:')
        label7.grid(column=0, row=16)
        label8 = ttk.Label(window, text='Wysokość podatku:')
        label8.grid(column=0, row=18)
        product_name = tk.Entry(window, width=50, textvariable=self.product['name'])
        product_name.grid(column=0, row=13)
        quantity = tk.Entry(window, width=50, textvariable=self.product['quantity'])
        quantity.grid(column=0, row=15)
        product_cost = tk.Entry(window, width=50, textvariable=self.product['cost'])
        product_cost.grid(column=0, row=17)
        product_rate = tk.Entry(window, width=50, textvariable=self.product['rate'])
        product_rate.grid(column=0, row=19)
        button1 = ttk.Button(window, text="Zapisz", command=lambda: [self.products(), self.add_product(self.my_listbox), window.destroy()])
        button1.grid(column=0, row=20)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        content = ttk.Frame(self,  borderwidth=5)
        content.grid(column=0, row=0)
        self.my_listbox = Listbox(content)
        self.my_listbox.grid(column=1, row=0)
        button1 = ttk.Button(content, text="Dodaj", command=self.product_window)
        button1.grid(column=1, row=20)
        button2 = ttk.Button(content, text="Wróc", command=lambda: [controller.show_frame(Invoice)])
        button2.grid(column=2, row=20)
        button3 = ttk.Button(content, text="Save to PDF", command=lambda: [self.save_to_pdf()])
        button3.grid(column=3, row=20)

    def __str__(self):
        msg = f"""
                {[self.generate_item_list(item) for item in self.list_of_products]}
                Całkowita wartość brutto: {round(self.payment_brutto, 2)}zł
                Całkowita wartość netto: {round(self.payment_netto, 2)}zł
                Wartość podatku: {round(self.tax, 2)}zł\n"""
        return msg


app = TkinterApp()
app.mainloop()
