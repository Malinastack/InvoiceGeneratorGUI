import datetime
from fpdf import FPDF
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
    invoice_number = ""
    seller = ""
    buyer = ""
    seller_nip = ""
    buyer_nip = ""
    payment_brutto = 0
    payment_netto = 0
    tax = 0
    z = "TAK"
    quantity_of_products = 0
    product = {}
    list_of_products = []


    def products(self):
        print("Dodawanie produktu/usługi")
        self.product = {"name": input("Podaj nazwę produktu/usługi: "),
                        "quantity": input("Podaj ilość: "),
                        "cost": input("Podaj cene jednostkową: "),
                        "rate": input("Podaj wysokość podatku: "),
                        "netto": 0,
                        "brutto": 0}
        self.product['netto'] = float(self.product['quantity'])*float(self.product['cost'])
        self.product['brutto'] = float(self.product['netto'])+float(self.product['netto'])*(float(self.product['rate'])/100)
        self.payment_brutto += self.product['brutto']
        self.payment_netto += self.product['netto']
        self.tax = (float(self.payment_brutto))-(float(self.payment_netto))
        self.list_of_products.append(self.product)

    def __init__(self):
        self.gen = Generator.generator_1(self)
        self.invoice_number = next(self.gen)
        self.seller = input("Podaj imię i nazwisko sprzedawcy: ")
        self.buyer = input("Podaj imię i nazwisko nabywcy: ")
        self.seller_nip = input("Podaj nip sprzedawcy: ")
        self.buyer_nip = input("Podaj nip nabywcy: ")

        while self.z == "TAK":
            self.products()
            self.z = input("Czy chcesz dodać kolejny produkt? Wpisz TAK jeśli chcesz kontynuować: ")


    def generate_item_list(self, item):
        return f"""Nazwa towaru/usługi: {item['name']} \
               Ilość: {item['quantity']} \
               Cena jednostkowa: {item['cost']}zł \
               Wysokość podatku: {item['rate']}% \
               Netto: {item['netto']}zł \
               Brutto: {item['brutto']}zł"""

    def save_to_pdf(self):
        self.pdf.add_page()
        self.pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.pdf.set_font('DejaVu', '', 14)
        f = self.__str__()
        self.pdf.write(10, txt=f)
        self.pdf.output("Test.pdf")

    def __str__(self):
        msg =  f"""Numer faktury: {self.invoice_number}
               Imię i nazwisko sprzedawcy: {self.seller}
               Imię i nazwisko nabywcy: {self.buyer}
               NIP sprzedawcy: {self.seller_nip}
               NIP nabywcy: {self.buyer_nip}
               Lista towarów:
               {[self.generate_item_list(item) for item in self.list_of_products]}
               Całkowita wartość brutto: {round(self.payment_brutto, 2)}zł  
               Całkowita wartość netto: {round(self.payment_netto, 2)}zł  
               Wartość podatku: {round(self.tax, 2)}zł\n"""
        return msg






faktura1 = Invoice()
print(faktura1)
faktura1.save_to_pdf()



# lista2 = [{"cena": 1235, "ilość": 2000}]
# element = {"cena": 123,
#            "ilość": 10}
# element2 = {"cena": 133,
#            "ilość": 15}
# lista = ['a', 'b', 'c']
# lista2.append(element)
# lista2.append(element2)
# # for product in lista:
# #     print(f"{product['cena']}"
# #           f"{product['ilość']}")
#
# print([f"{item['cena']}" for item in lista2])


