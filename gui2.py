import tkinter as tk
import datetime


class Generator:
    def generator_1(self):
        i = 0
        x = datetime.datetime.now()
        while True:
            yield f"FV/{i}/{x.year}/{x.month}"
            i += 1

#a


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame()
        container.grid(row=0, column=0, sticky="nsew")

        self.listing = {}

        for p in (WelcomePage, InvoiceForm):
            page_name = p.__name__
            frame = p(parent=container, controller=self)
            frame.grid(row=0, column=0, sticky="nesw", pady=20, padx=20)
            self.listing[page_name] = frame

        self.up_frame("WelcomePage")

    def up_frame(self, page_name):
        page = self.listing[page_name]
        page.tkraise()


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Generator faktur \n")
        label.pack()
        button2 = tk.Button(
            self,
            text="To Invoice form",
            command=lambda: controller.up_frame("InvoiceForm"),
        )
        button2.pack()


def generate_item_list(product):
    return f"""
       Nazwa towaru/usługi: {product['name']} 
       Ilość: {product['quantity']} 
       Cena jednostkowa: {product['cost']}zł 
       Wysokość podatku: {product['rate']}% 
       Netto: {product['netto']}zł 
       Brutto: {product['brutto']}zł"""


class InvoiceForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Imię i nazwisko sprzedawcy")
        label.grid(row=0, column=0)
        label2 = tk.Label(self, text="Imię i nazwisko nabywcy")
        label2.grid(row=2, column=0)
        label3 = tk.Label(self, text="NIP sprzedawcy")
        label3.grid(row=4, column=0)
        label4 = tk.Label(self, text="NIP nabywcy")
        label4.grid(row=6, column=0)

        self.seller_name_entry = tk.Entry(self, width=40)
        self.seller_name_entry.grid(row=1, column=0)

        self.buyer_name_entry = tk.Entry(self, width=40)
        self.buyer_name_entry.grid(row=3, column=0)

        self.seller_nip_entry = tk.Entry(self, width=40)
        self.seller_nip_entry.grid(row=5, column=0)

        self.buyer_nip_entry = tk.Entry(self, width=40)
        self.buyer_nip_entry.grid(row=7, column=0)

        button = tk.Button(
            self, text="Submit", command=lambda: self.submit(), width=20, bg="#67767E"
        )
        button.grid(row=8, column=0, pady=10)

        self.listbox = tk.Listbox(self, bg="#f7ffde", width=40, font=("Arial", 10))
        self.listbox.grid(row=9, column=0)

        button = tk.Button(
            self,
            text="Add product",
            command=lambda: self.invoice_product_window(),
            width=20,
            bg="#67767E",
        )
        button.grid(row=8, column=0, pady=10)
        button = tk.Button(
            self, text="Submit", command=lambda: self.submit(), width=20, bg="#67767E"
        )
        button.grid(row=10, column=0, pady=10)

        self.gen = Generator.generator_1(self)
        self.invoice_number = next(self.gen)
        self.seller_name = None
        self.buyer_name = None
        self.seller_nip = None
        self.buyer_nip = None
        self.list_of_products = []
        self.product = None

    def invoice_product_window(self):
        product_window = tk.Toplevel()
        product_window.title("Dodaj produkt")
        label = tk.Label(product_window, text="Nazwa produktu/usługi")
        label.grid(row=0, column=0)

        self.product_name_entry = tk.Entry(product_window, width=40)
        self.product_name_entry.grid(row=1, column=0)

        label1 = tk.Label(product_window, text="Ilość")
        label1.grid(row=2, column=0)

        self.product_quantity_entry = tk.Entry(product_window, width=40)
        self.product_quantity_entry.grid(row=3, column=0)

        label2 = tk.Label(product_window, text="Cena jednostkowa")
        label2.grid(row=4, column=0)

        self.product_cost_entry = tk.Entry(product_window, width=40)
        self.product_cost_entry.grid(row=5, column=0)

        label3 = tk.Label(product_window, text="Wysokość podatku")
        label3.grid(row=6, column=0)
        self.product_rate_entry = tk.Entry(product_window, width=40)
        self.product_rate_entry.grid(row=7, column=0)

        button = tk.Button(
            product_window,
            text="Submit",
            command=lambda: [self.add_product(), self.add_to_listbox(self.listbox)],
            width=20,
            bg="#67767E",
        )
        button.grid(row=8, column=0, pady=10)

        product_window.mainloop()

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
        self.product["brutto"] = float(self.product["netto"]) + float(
            self.product["netto"]
        ) * (float(self.product["rate"]) / 100)
        self.list_of_products.append(self.product)

    def add_to_listbox(self, listbox):
        listbox.insert("end", self.list_of_products[-1]["name"])

    def submit(self):
        self.seller_name = self.seller_name_entry.get()
        self.buyer_name = self.buyer_name_entry.get()
        self.seller_nip = self.seller_nip_entry.get()
        self.buyer_nip = self.buyer_nip_entry.get()
        print(self.__str__())

    def __str__(self):
        msg = f"""Numer faktury: {self.invoice_number}
        Imię i nazwisko sprzedawcy: {self.seller_name}
        Imię i nazwisko nabywcy: {self.buyer_name}
        NIP sprzedawcy: {self.seller_nip}
        NIP nabywcy: {self.buyer_nip}"""
        msg2 = "\n".join(
            [generate_item_list(product) for product in self.list_of_products]
        )
        return msg + msg2


app = MainFrame()
app.mainloop()
