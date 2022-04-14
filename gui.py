from tkinter import *


def create_window():
    add_invoice = Tk()
    add_invoice.title("Dodawanie faktury")
    add_invoice.geometry("400x400")
    Label(add_invoice, text="Imię i nazwisko sprzedawcy").pack()
    entry = Entry(add_invoice, width=40)
    entry.pack()
    Label(add_invoice, text="Imię i nazwisko nabywcy").pack()
    entry2 = Entry(add_invoice, width=40)
    entry2.pack()
    Label(add_invoice, text="NIP sprzedawcy").pack()
    entry3 = Entry(add_invoice, width=40)
    entry3.pack()
    Label(add_invoice, text="NIP nabywcy").pack()
    entry4 = Entry(add_invoice, width=40)
    entry4.pack()
    button = Button(add_invoice, text="Zatwierdź", command=submit)
    button.pack()
    window.destroy()


window = Tk()
window.title('Generator faktur')
window.geometry("300x200")
window.configure(bg='#3089B6')
button = Button(window, text="Dodaj fakturę", command=create_window, width=20, bg='#67767E')
button.pack(padx=10, pady=10)
button2 = Button(window, text="Edytuj fakturę", command=create_window, width=20, bg='#67767E')
button2.pack(padx=10, pady=10)
button3 = Button(window, text="Drukuj fakturę", command=create_window, width=20, bg='#67767E')
button3.pack(padx=10, pady=10)
button4 = Button(window, text="Lista faktur", command=create_window, width=20, bg='#67767E')
button4.pack(padx=10, pady=10)


window.mainloop()