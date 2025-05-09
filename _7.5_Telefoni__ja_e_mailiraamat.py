import json
import smtplib, ssl
from email.message import EmailMessage
from tkinter import *
from tkinter import simpledialog, messagebox


try:
    with open("kontaktid.json", "r") as f:
        kontaktid = json.load(f)
except:
    kontaktid = []

def salvesta():
    with open("kontaktid.json", "w") as f:
        json.dump(kontaktid, f)

def uuenda():
    kast.delete(0, END)
    for k in kontaktid:
        kast.insert(END, f"{k['nimi']} | {k['telefon']} | {k['email']}")

def lisa():
    nimi = simpledialog.askstring("Lisa kontakt", "Sisesta nimi:")
    tel = simpledialog.askstring("Tel", "Sisesta telefon:")
    email = simpledialog.askstring("Email", "Sisesta email:")
    if nimi and tel and email:
        kontaktid.append({"nimi": nimi, "telefon": tel, "email": email})
        salvesta()
        uuenda()

def kustuta():
    nimi = simpledialog.askstring("Kustuta", "Sisesta nimi:")
    kontaktid[:] = [k for k in kontaktid if k['nimi'].lower() != nimi.lower()]
    salvesta()
    uuenda()

def muuda():
    nimi = simpledialog.askstring("Muuda", "Kontakti nimi:")
    for k in kontaktid:
        if k["nimi"].lower() == nimi.lower():
            k["nimi"] = simpledialog.askstring("Uus nimi", "", initialvalue=k["nimi"])
            k["telefon"] = simpledialog.askstring("Uus tel", "", initialvalue=k["telefon"])
            k["email"] = simpledialog.askstring("Uus email", "", initialvalue=k["email"])
            salvesta()
            uuenda()
            return
    messagebox.showerror("Viga", "Kontakti ei leitud.")

def sorteeri():
    väli = simpledialog.askstring("Sorteeri", "nimi / telefon / email:")
    if väli in ["nimi", "telefon", "email"]:
        kontaktid.sort(key=lambda k: k[väli])
        salvesta()
        uuenda()
    else:
        messagebox.showerror("Viga", "Vale valik!")

def saada():
    valik = kast.curselection()
    if not valik:
        messagebox.showerror("Viga", "Vali kontakt.")
        return

    kontakt = kontaktid[valik[0]]
    to = kontakt["email"]
    text = simpledialog.askstring("Sõnum", "Sisesta sõnum:")
    pw = simpledialog.askstring("Parool", "Gmaili parool:", show='*')
    from_email = "karolinao20081@gmail.com"

    msg = EmailMessage()
    msg.set_content(text)
    msg["Subject"] = "Tereee"
    msg["From"] = from_email
    msg["To"] = to

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls(context=ssl.create_default_context())
            s.login(from_email, pw)
            s.send_message(msg)
        messagebox.showinfo("OK", "Kiri saadetud!")
    except Exception as e:
        messagebox.showerror("Viga", str(e))

aken = Tk()
aken.title("Telefoniraamat")
aken.geometry("300x500")
aken.configure(bg="beige")

label = Label(aken, text="Phone", font=("Arial", 18), bg="beige", fg="black")
label.pack(pady=10)

kast = Listbox(aken, width=30, height=8, font=("Arial", 12), bg="white", selectmode=SINGLE)
kast.pack(pady=10)

frame_buttons = Frame(aken, bg="beige")
frame_buttons.pack(pady=20)

Button(frame_buttons, text="Lisa kontakt", width=15, height=2, font=("Arial", 12), bg="lightgray", command=lisa).pack(side=LEFT, padx=5, pady=5)
Button(frame_buttons, text="Kustuta kontakt", width=15, height=2, font=("Arial", 12), bg="lightgray", command=kustuta).pack(side=LEFT, padx=5, pady=5)
Button(frame_buttons, text="Muuda kontakt", width=15, height=2, font=("Arial", 12), bg="lightgray", command=muuda).pack(side=LEFT, padx=5, pady=5)

Button(aken, text="Sorteeri kontaktid", width=15, height=2, font=("Arial", 12), bg="lightgray", command=sorteeri).pack(pady=5)
Button(aken, text="Saada kiri", width=15, height=2, font=("Arial", 12), bg="lightgray", command=saada).pack(pady=5)


uuenda()

aken.mainloop()


