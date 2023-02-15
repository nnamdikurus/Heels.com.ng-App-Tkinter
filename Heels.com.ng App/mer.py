from tkinter import *
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
import time
import sqlite3



def expenses():
	exp = Tk()
	exp.title("Expenses")
	exp.geometry("1350x850")
	exp.configure(background = "#c3f705")



	#--------------------------FUNCTIONS-------------------------------#

	def run_query(query,parameters=()):
		conn = sqlite3.connect("Heels.com.ng.db")
		cur = conn.cursor()
		query_result = cur.execute(query,parameters)
		conn.commit()
		return query_result

	def view_record():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM mer"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])


	def validation():
		return len(name_entry.get())!=0,len(phone_entry.get())!=0,len(email_entry.get())!=0,len(code_entry.get())!=0,len(acc_entry.get())!=0,len(stat_entry.get())!=0,len(date_entry.get())!=0 

	def add_record():
		if validation():
			query = "INSERT INTO mer VALUES(NULL,?,?,?,?,?,?,?)"
			parameters = (name_entry.get(),phone_entry.get(),email_entry.get(),code_entry.get(),acc_entry.get(),stat_entry.get(),date_entry.get())
			run_query(query,parameters)
			display["text"] = "Record {} has been added".format(name_entry.get())

			name_entry.delete(0,END)
			phone_entry.delete(0,END)
			email_entry.delete(0,END)
			code_entry.delete(0,END)
			acc_entry.delete(0,END)
			stat_entry.delete(0,END)
			date_entry.delete(0,END)

		else:
			display["text"] = "Please fill all entries"
		view_record()


	def delete_record():
		try:
			tree.item(tree.selection())["values"][1]
		except IndexError as e:
			display["text"] = "Please select a record to delete"
		query = "DELETE FROM mer WHERE ID=?"
		number = tree.item(tree.selection())["text"]
		run_query(query,(number,))
		display["text"] = "Record {} has been deleted".format(number)
		view_record()


	def edit_box():
		try:
			tree.item(tree.selection())["values"][0]
		except IndexError as e:
			display["text"] = "Please select a record to edit"
		name_text = tree.item(tree.selection())["values"][0]
		phone_text = tree.item(tree.selection())["values"][1]
		email_text = tree.item(tree.selection())["values"][2]
		code_text = tree.item(tree.selection())["values"][3]
		acc_text = tree.item(tree.selection())["values"][4]
		stat_text = tree.item(tree.selection())["values"][5]
		date_text = tree.item(tree.selection())["values"][6]

		new_edit = Toplevel()
		new_edit.title("Edit Record")

		Label(new_edit, text = "Old(Merchant Name)").grid(row = 0, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = name_text), state = "readonly").grid(row = 0, column = 1)
		Label(new_edit, text = "New(Merchant Name)").grid(row = 1, column = 0)
		new_name = Entry(new_edit, width = 30, bd = 3)
		new_name.grid(row = 1, column = 1)

		Label(new_edit, text = "Old(Merchant Phone Number)").grid(row = 2, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = phone_text), state = "readonly").grid(row = 2, column = 1)
		Label(new_edit, text = "New(Merchant Phone Number)").grid(row = 3, column = 0)
		new_phone = Entry(new_edit, width = 30, bd = 3)
		new_phone.grid(row = 3, column = 1)

		Label(new_edit, text = "Old(Merchant Email)").grid(row = 4, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = email_text), state = "readonly").grid(row = 4, column = 1)
		Label(new_edit, text = "New(Merchant Email)").grid(row = 5, column = 0)
		new_email = Entry(new_edit, width = 30, bd = 3)
		new_email.grid(row = 5, column = 1)

		Label(new_edit, text = "Old(Merchant Code)").grid(row = 6, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = code_text), state = "readonly").grid(row = 6, column = 1)
		Label(new_edit, text = "New(Merchant Code)").grid(row = 7, column = 0)
		new_code = Entry(new_edit, width = 30, bd = 3)
		new_code.grid(row = 7, column = 1)

		Label(new_edit, text = "Old(Merchant Account Details)").grid(row = 8, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = acc_text), state = "readonly").grid(row = 8, column = 1)
		Label(new_edit, text = "New(Merchant Account Details)").grid(row = 9, column = 0)
		new_acc = Entry(new_edit, width = 30, bd = 3)
		new_acc.grid(row = 9, column = 1)

		Label(new_edit, text = "Old(Merchant Status)").grid(row = 10, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = stat_text), state = "readonly").grid(row = 10, column = 1)
		Label(new_edit, text = "New(Merchant Status)").grid(row = 11, column = 0)
		new_status = ttk.Combobox(new_edit, textvariable = stat_text, width = 30)
		new_status.configure(values= ("Active","Dormant"))
		new_status.grid(row = 11, column = 1)

		Label(new_edit, text = "Old(Date Enrolled)").grid(row = 12, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = date_text), state = "readonly").grid(row = 12, column = 1)
		Label(new_edit, text = "New(Date Enrolled)").grid(row = 13, column = 0)
		new_date = DateEntry(new_edit, width = 30, bd = 3)
		new_date.grid(row = 13, column = 1)

		Button(new_edit, text = "Save Changes", cursor = "hand2", command = lambda:edit_record(new_name.get(),name_text,new_phone.get(),phone_text,new_email.get(),email_text,new_code.get(),code_text,new_acc.get(),acc_text,new_status.get(),stat_text,new_date.get(),date_text)).grid(row = 14, column = 1)


		new_edit.mainloop()

	def edit_record(new_name,name_text,new_phone,phone_text,new_email,email_text,new_code,code_text,new_acc,acc_text,new_status,stat_text,new_date,date_text):
			query = "UPDATE mer SET name = ?,  phone = ?,  email = ?,  code = ?,  acc = ?,  status = ?,  datee = ? WHERE  name = ? AND  phone = ? AND email = ? AND code = ? AND acc = ? AND status = ? AND datee = ?"
			parameters = (new_name,new_phone,new_email,new_code,new_acc,new_status,new_date,name_text,phone_text,email_text,code_text,acc_text,stat_text,date_text)
			run_query(query,parameters)
			display["text"] = "Record {} has been changed to {}".format(name_text,new_name)
			view_record()


	def helpp():
		messagebox.showinfo("Hey!!!","Look at my Junk")



	#--------------------------IMAGES-------------------------------#


	img = ImageTk.PhotoImage(Image.open("C:\\Icons\\mer.png"))
	img_label = Label(mer, image = img, width = 370, height = 340)
	img_label.grid(row = 1, column = 1, sticky = N)

	#--------------------------FRAMES-------------------------------#

	frame = LabelFrame(mer, width = 50, bd = 3, bg = "#f7f6a8", padx = 10)
	frame.grid(row = 1, column = 0, padx = 20, pady = 10, sticky = W)

	#--------------------------LABELS-------------------------------#

	topic_label = Label(mer,text = "Merchant Catalogue", font = "Georgia 30 bold underline", bg = "#c3f705")
	topic_label.grid(row = 0, column = 0, padx = 1, pady = 10)

	name_label = Label(frame,text = "Merchant Name", font = "Georgia 11 bold", bg = "#f7f6a8")
	name_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 5)

	phone_label = Label(frame,text = "Merchant Phone Number", font = "Georgia 11 bold", bg = "#f7f6a8")
	phone_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 5)

	email_label = Label(frame,text = "Merchant Email Address", font = "Georgia 11 bold", bg = "#f7f6a8")
	email_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 5)

	code_label = Label(frame,text = "Merchant Code", font = "Georgia 11 bold", bg = "#f7f6a8")
	code_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 5)

	account_label = Label(frame,text = "Merchant Bank Accout Details", font = "Georgia 11 bold", bg = "#f7f6a8")
	account_label.grid(row = 5, column = 0, sticky = W, padx = 10, pady = 5)

	stat_label = Label(frame,text = "Status of Enrollment", font = "Georgia 11 bold", bg = "#f7f6a8")
	stat_label.grid(row = 6, column = 0, sticky = W, padx = 10, pady = 5)

	date_label = Label(frame,text = "Date Enrolled", font = "Georgia 11 bold", bg = "#f7f6a8")
	date_label.grid(row = 7, column = 0, sticky = W, padx = 10, pady = 5)

	#--------------------------ENTRIES-------------------------------#

	name_text = StringVar()
	name_entry = Entry(frame, textvariable = name_text, width = 40, bd = 3)
	name_entry.grid(row = 1, column = 1, sticky = W)

	phone_text = StringVar()
	phone_entry = Entry(frame, textvariable = phone_text, width = 40, bd = 3)
	phone_entry.grid(row = 2, column = 1, sticky = W)

	email_text = StringVar()
	email_entry = Entry(frame, textvariable = email_text, width = 40, bd = 3)
	email_entry.grid(row = 3, column = 1, sticky = W)

	code_text = StringVar()
	code_entry = Entry(frame, textvariable = code_text, width = 40, bd = 3)
	code_entry.grid(row = 4, column = 1, sticky = W)

	acc_text = StringVar()
	acc_entry = Entry(frame, textvariable = acc_text, width = 40, bd = 3)
	acc_entry.grid(row = 5, column = 1, sticky = W)

	stat_text = StringVar()
	stat_entry = ttk.Combobox(frame,textvariable = stat_text)
	stat_entry.configure(values = ("Active", "Dormant"))
	stat_entry.grid(row = 6, column = 1, sticky = W)

	date_text = StringVar()
	date_entry = DateEntry(frame, textvariable = date_text)
	date_entry.grid(row = 7, column = 1, sticky = W)


	#--------------------------BUTTONS-------------------------------#

	add_butt = Button(frame, text = "Add Merchant",  cursor = "hand2", font = "Georgia 11 bold", bg = "#f7f6a8", command = add_record)
	add_butt.grid(row = 8, column = 0, pady = 20)

	display = Label(frame, text = "",font = "Garamond 15 bold italic", fg = "blue", bg = "#f7f6a8")
	display.grid(row = 9, column = 1, padx = 15)


	#--------------------------TREEVIEW-------------------------------#

	tree = ttk.Treeview(mer, height = 15, columns = ["","","","","","",""])
	tree.grid(row = 10, column = 0, columnspan = 3, padx = 20)

	tree.heading("#0",text = "ID")
	tree.column("#0",width = 80)

	tree.heading("#1",text = "Merchant Name")
	tree.column("#1",width = 200)

	tree.heading("#2",text = "Phone Number")
	tree.column("#2",width = 200)

	tree.heading("#3",text = "Email Address")
	tree.column("#3",width = 200)

	tree.heading("#4",text = "Code")
	tree.column("#4",width = 50)

	tree.heading("#5",text = "Account Details")
	tree.column("#5",width = 300)

	tree.heading("#6",text = "Status")
	tree.column("#6",width = 100)

	tree.heading("#7",text = "Date")
	tree.column("#7",width = 100)

	style = ttk.Style()
	style.configure("Treeview.Heading",font = "Georgia 11 bold italic")

	#--------------------------SCROLLBAR-------------------------------#

	sb = Scrollbar(mer,command = tree.yview)
	sb.grid(row = 10, column = 3, sticky = NS, ipady = 3)

	#--------------------------MENUS AND SUBMENU-------------------------------#

	main_menu = Menu()
	submenu = Menu()

	main_menu.add_cascade(label = "File", menu = submenu)
	main_menu.add_cascade(label = "Add", command = add_record)
	main_menu.add_cascade(label = "Edit",command = edit_box)
	main_menu.add_cascade(label = "Delete", command = delete_record)	
	main_menu.add_cascade(label = "Help",command = helpp)
	main_menu.add_cascade(label = "Exit",command = mer.destroy)

	submenu.add_command(label = "Add Record", command = add_record)
	submenu.add_command(label = "Edit Record",command = edit_box)
	submenu.add_command(label = "Delete Record", command = delete_record)
	submenu.add_separator()
	submenu.add_command(label = "Help",command = helpp)
	submenu.add_command(label = "Exit",command = mer.destroy)

	mer.configure(menu = main_menu)

	#--------------------------TIME AND DATE-------------------------------#

	def tick():
		d = datetime.datetime.now()
		mydate = "{:%B - %d - %Y}".format(d)
		mytime = time.strftime("%I : %M : %S%p")
		lblInfo.config(text = mytime +"\t" + mydate)
		lblInfo.after(200,tick)
	lblInfo = Label(mer, font = "Georgia 11 bold italic", fg = "red", bg = "#c3f705")
	lblInfo.grid(row = 0, column = 1)
	tick()







	view_record()


	mer.mainloop()
	








merchant()