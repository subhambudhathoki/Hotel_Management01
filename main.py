from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title('Hotel Management Software for storing basic guest info')
photo = PhotoImage(file = "C:\hotel.PNG")
root.iconphoto(False, photo)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 1200
height = 600
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(0, 0)



def Database():
    global conn, cursor
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, firstname TEXT, lastname TEXT, gender TEXT, address TEXT, username TEXT, password TEXT)")


def Create():
    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or ADDRESS.get() == "" or USERNAME.get() == "" or PASSWORD.get() == "":
        txt_result.config(text="Please complete the required field!", fg="red")
    else:
        Database()
        cursor.execute(
            "INSERT INTO `member` (firstname, lastname, gender, address, username, password) VALUES(?, ?, ?, ?, ?, ?)",
            (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(ADDRESS.get()), str(USERNAME.get()),
             str(PASSWORD.get())))
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        conn.commit()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        ADDRESS.set("")
        USERNAME.set("")
        PASSWORD.set("")
        cursor.close()
        conn.close()
        txt_result.config(text="Welcome To Hotel Paradise", fg="green")


def Read():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    cursor.close()
    conn.close()
    txt_result.config(text="Successfully read the data from database", fg="green")


def Update():
    Database()
    if GENDER.get() == "":
        txt_result.config(text="Please select a gender", fg="red")
    else:
        tree.delete(*tree.get_children())
        cursor.execute(
            "UPDATE `member` SET `firstname` = ?, `lastname` = ?, `gender` =?,  `address` = ?,  `username` = ?, `password` = ? WHERE `mem_id` = ?",
            (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(ADDRESS.get()), str(USERNAME.get()),
             str(PASSWORD.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        ADDRESS.set("")
        USERNAME.set("")
        PASSWORD.set("")
        btn_create.config(state=NORMAL)
        btn_read.config(state=NORMAL)
        btn_update.config(state=DISABLED)
        btn_delete.config(state=NORMAL)
        txt_result.config(text="Successfully updated the data", fg="green")


def OnSelected(event):
    global mem_id;
    curItem = tree.focus()
    contents = (tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    ADDRESS.set("")
    USERNAME.set("")
    PASSWORD.set("")
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    ADDRESS.set(selecteditem[4])
    USERNAME.set(selecteditem[5])
    PASSWORD.set(selecteditem[6])
    btn_create.config(state=DISABLED)
    btn_read.config(state=DISABLED)
    btn_update.config(state=NORMAL)
    btn_delete.config(state=DISABLED)


def Delete():
    if not tree.selection():
        txt_result.config(text="Please select an item first", fg="red")
    else:
        result = tkMessageBox.askquestion('Hotel Management Software',
                                          'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
            txt_result.config(text="Thank You For Visiting Us", fg="blue")


def Exit():
    result = tkMessageBox.askquestion('Hotel Management software', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()


FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
ADDRESS = StringVar()
USERNAME = StringVar()
PASSWORD = StringVar()

#LAYOYT
Top = Frame(root, width=900, height=50, bd=8, relief="raise" , bg="black")
Top.pack(side=TOP)
Left = Frame(root, width=300, height=500, bd=8, relief="raise")
Left.pack(side=LEFT)
Right = Frame(root, width=600, height=500, bd=8, relief="raise",bg="black")
Right.pack(side=RIGHT)
Forms = Frame(Left, width=300, height=450)
Forms.pack(side=TOP)
Buttons = Frame(Left, width=300, height=75, bd=8, relief="raise")
Buttons.pack(side=BOTTOM)
RadioGroup = Frame(Forms)
Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 16)).pack(side=LEFT)
Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 16)).pack(side=LEFT)



#=================LABEL================
txt_title = Label(Top, width=900, font=('arial', 26), text="ⓌⒺⓁⒸⓄⓂⒺ ⓉⓄ ⒽⓄⓉⒺⓁ ⓅⒶⓇⒶⒹⒾⓈⒺ",bg="green", fg="cyan")
txt_title.pack()
txt_firstname = Label(Forms, text="Ｆｕｌｌ Ｎａｍｅ:", font=('arial', 18), bd=15)
txt_firstname.grid(row=0, sticky="e")
txt_lastname = Label(Forms, text="Ｒｏｏｍ ｎｏ:", font=('arial', 18), bd=15)
txt_lastname.grid(row=1, sticky="e")
txt_gender = Label(Forms, text="Ｇｅｎｄｅｒ:", font=('arial', 18), bd=15)
txt_gender.grid(row=5, sticky="e")
txt_address = Label(Forms, text="Ａｄｄｒｅｓｓ:", font=('arial', 18), bd=15)
txt_address.grid(row=3, sticky="e")
txt_username = Label(Forms, text="Ｓｔａｙｉｎｇ Ｄａｙｓ:", font=('arial', 18), bd=15)
txt_username.grid(row=4, sticky="e")
txt_password = Label(Forms, text="Ｃｏｎｔａｃｔ Ｎｏ:", font=('arial', 18), bd=15)
txt_password.grid(row=2, sticky="e")
txt_result = Label(Buttons)
txt_result.pack(side=TOP)
txt_password = Label(Forms, text="Checkout time:12:00 PM ", font=('arial', 11), bd=15,fg="green")
txt_password.grid(row=6, sticky="e")


#============ENTRY==============================
firstname = Entry(Forms, textvariable=FIRSTNAME, width=30 , bg="green" , fg='white')
firstname.grid(row=0, column=1)
lastname = Entry(Forms, textvariable=LASTNAME, width=30,fg='white', bg="green")
lastname.grid(row=1, column=1)
RadioGroup.grid(row=5, column=1)
address = Entry(Forms, textvariable=ADDRESS, width=30,fg='white', bg="green")
address.grid(row=3, column=1)
username = Entry(Forms, textvariable=USERNAME, width=30,fg='white', bg="green")
username.grid(row=4, column=1)
password = Entry(Forms, textvariable=PASSWORD, width=30,fg='white', bg="green")
password.grid(row=2, column=1)


#============BUTTON========================================
btn_create = Button(Buttons, width=20, text="Check In",fg='green', command=Create , pady=20)
btn_create.pack(side=LEFT)
btn_read = Button(Buttons, width=10, text="Guest Detail", command=Read,pady=20)
btn_read.pack(side=LEFT)
btn_update = Button(Buttons, width=10, text="Update info", command=Update, state=DISABLED,pady=20)
btn_update.pack(side=LEFT)
btn_delete = Button(Buttons, width=10, text="Check Out",fg='red', command=Delete,pady=20)
btn_delete.pack(side=LEFT)
btn_exit = Button(Buttons, width=10, text="Exit", command=Exit,pady=20)
btn_exit.pack(side=LEFT)


scrollbary = Scrollbar(Right, orient=VERTICAL)
scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
tree = ttk.Treeview(Right, columns=("MemberID", "Name", "Room No", "Gender", "Address", "No Of Days", "Contact No"),
                    selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Name', text="Name", anchor=W)
tree.heading('Room No', text="Room No", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Address', text="Address", anchor=W)
tree.heading('No Of Days', text="No Of Days", anchor=W)
tree.heading('Contact No', text="Contact No", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=80)
tree.column('#5', stretch=NO, minwidth=0, width=150)
tree.column('#6', stretch=NO, minwidth=0, width=120)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)


if __name__ == '__main__':
    root.mainloop()
