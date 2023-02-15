from tkinter import *
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
import time
import sqlite3



def trans():
	trans = Tk()
	trans.geometry("1400x1150")
	trans.title("Heelz.com.ng Transaction Details")
	trans.configure(background = "#e0ffff")
	
	frame = LabelFrame(trans, width = 50, height = 30, bd = 4, padx = 25)
	frame.grid(row = 1, column = 0, columnspan = 6, padx = 20, pady=10,sticky = W)


	#-----------------FUNCTIONS-----------------------#

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
		query = "SELECT * FROM trans"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def validation():
		return len(order_entry.get())!=0, len(name_entry.get())!=0, len(add_entry.get())!=0, len(email_entry.get())!=0, len(nso_entry.get())!=0,  len(nst_entry.get())!=0, len(nsr_entry.get())!=0, len(amo_entry.get())!=0, len(stat_entry.get())!=0, len(pay_entry.get())!=0, len(date_entry.get())!=0

	def add_record():
		if validation():
			query = "INSERT INTO trans VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?)"
			parameters = (order_entry.get(),name_entry.get(),add_entry.get(),phone_entry.get(),email_entry.get(),nso_entry.get(),nst_entry.get(),nsr_entry.get(),amo_entry.get(),stat_text.get(),pay_text.get(),date_entry.get())

			run_query(query,parameters)
			display["text"] = "Record {} has been added".format(name_entry.get())

			order_entry.delete(0,END)
			name_entry.delete(0,END)
			add_entry.delete(0,END)
			phone_entry.delete(0,END)
			email_entry.delete(0,END)
			nso_entry.delete(0,END)
			nst_entry.delete(0,END)
			nsr_entry.delete(0,END)
			amo_entry.delete(0,END)
			stat_entry.delete(0,END)
			pay_entry.delete(0,END)
			date_entry.delete(0,END)


		else:
			display["text"] = "Please fill all entries"

		view_record()

	def delete_record():
		try:
			tree.item(tree.selection())["values"][1]
		except IndexError as e:
			display["text"] = "Please select a record to delete"
		query = "DELETE FROM trans WHERE ID = ?"
		number = tree.item(tree.selection())["text"]
		run_query(query,(number,))
		display["text"] = "Record {} has been deleted".format(number)
		view_record()


	def edit_box():
		try:
			tree.item(tree.selection())["values"][0]
		except IndexError as e:
			display["text"]= "Please select a record to edit"

		order_text = tree.item(tree.selection())["values"][0]
		name_text = tree.item(tree.selection())["values"][1]
		add_text = tree.item(tree.selection())["values"][2]
		phone_text = tree.item(tree.selection())["values"][3]
		email_text = tree.item(tree.selection())["values"][4]
		nso_text = tree.item(tree.selection())["values"][5]
		nst_text = tree.item(tree.selection())["values"][6]
		nsr_text = tree.item(tree.selection())["values"][7]
		amo_text = tree.item(tree.selection())["values"][8]
		stat_text = tree.item(tree.selection())["values"][9]
		pay_text = tree.item(tree.selection())["values"][10]
		date_text = tree.item(tree.selection())["values"][11]


		new_edit = Tk()
		new_edit.title("Edit Record")

		Label(new_edit,text = "Old(Order Number)").grid(row = 0, column = 0, padx = 10  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = order_text),state = "readonly").grid(row=0, column = 1, padx = 10  )
		Label(new_edit,text = "New(Order number").grid(row = 1, column = 0, padx = 10  )
		new_order = Entry(new_edit,bd = 3, width = 30)
		new_order.grid(row = 1, column =1, padx = 10,   )

		Label(new_edit,text = "Old(Customer Name)").grid(row = 2, column = 0, padx = 10, pady = 10)
		Entry(new_edit, textvariable = StringVar(new_edit,value = name_text),state = "readonly").grid(row=2, column = 1, padx = 10, pady = 10)
		Label(new_edit,text = "New(Customer Name").grid(row = 3, column = 0, padx = 10  )
		new_name = Entry(new_edit,bd = 3, width = 30)
		new_name.grid(row = 3, column =1, padx = 10  )

		Label(new_edit,text = "Old(Customer Address)").grid(row = 4, column = 0, padx = 10  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = add_text),state = "readonly").grid(row=4, column = 1, padx = 10  )
		Label(new_edit,text = "New(Customer Address").grid(row = 5, column = 0, padx = 10  )
		new_add = Entry(new_edit,bd = 3, width = 30)
		new_add.grid(row = 5, column =1, padx = 10  )


		Label(new_edit,text = "Old(Phone Number)").grid(row = 6, column = 0, padx = 10  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = phone_text),state = "readonly").grid(row=6, column = 1, padx = 10  )
		Label(new_edit,text = "New(Phone Number").grid(row = 7, column = 0, padx = 10  )
		new_phone = Entry(new_edit,bd = 3, width = 30)
		new_phone.grid(row = 7, column =1, padx = 10  )

		Label(new_edit,text = "Old(Email Address)").grid(row = 8, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = email_text),state = "readonly").grid(row=8, column = 1, padx = 10  )
		Label(new_edit,text = "New(Email Address").grid(row = 9, column = 0, padx = 10  )
		new_email = Entry(new_edit,bd = 3, width = 30)
		new_email.grid(row = 9, column =1, padx = 10  )

		Label(new_edit,text = "Old(Shoes Ordered)").grid(row = 10, column = 0, padx = 10  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = nso_text),state = "readonly").grid(row=10, column = 1, padx = 10,  )
		Label(new_edit,text = "New(Shoes Ordered").grid(row = 11, column = 0, padx = 10,   )
		new_nso = Spinbox(new_edit,from_=0, to = 100, bd = 3, width = 30)
		new_nso.grid(row = 11, column =1, padx = 10,   )

		Label(new_edit,text = "Old(Shoes Taken)").grid(row = 12, column = 0, padx = 10,  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = nst_text),state = "readonly").grid(row=12, column = 1, padx = 10,   )
		Label(new_edit,text = "New(Shoes Taken").grid(row = 13, column = 0, padx = 10,   )
		new_nst = Spinbox(new_edit,from_=0, to = 100,bd = 3, width = 30)
		new_nst.grid(row = 13, column =1, padx = 10,  )

		Label(new_edit,text = "Old(Shoes Rejected)").grid(row = 14, column = 0, padx = 10,  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = nsr_text),state = "readonly").grid(row=14, column = 1, padx = 10,   )
		Label(new_edit,text = "New(Shoes Rejected").grid(row = 15, column = 0, padx = 10,  )
		new_nsr = Spinbox(new_edit,from_=0, to = 100,bd = 3, width = 30)
		new_nsr.grid(row = 15, column =1, padx = 10,  )

		Label(new_edit,text = "Old(Amount Paid)").grid(row = 16, column = 0, padx = 10  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = amo_text),state = "readonly").grid(row=16, column = 1, padx = 10,  )
		Label(new_edit,text = "New(Amount Paid").grid(row = 17, column = 0, padx = 10,  )
		new_amount = Entry(new_edit,bd = 3, width = 30)
		new_amount.grid(row = 17, column =1, padx = 10,  )

		Label(new_edit,text = "Old(Status of Delivery)").grid(row = 18, column = 0, padx = 10,  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = stat_text),state = "readonly").grid(row=18, column = 1, padx = 10,   )
		Label(new_edit,text = "New(Status of Delivery").grid(row = 19, column = 0, padx = 10  )
		new_status = ttk.Combobox(new_edit,textvariable = stat_text, width = 30)
		new_status.configure(values = ("Fully Delivered","Partially Delivered","Rejected","Cancelled","In Transit",))
		new_status.grid(row = 19, column =1, padx = 10,   )

		Label(new_edit,text = "Old(Payment Method)").grid(row = 20, column = 0, padx = 10,   )
		Entry(new_edit, textvariable = StringVar(new_edit,value = pay_text),state = "readonly").grid(row=20, column = 1, padx = 10  )
		Label(new_edit,text = "New(Payment Method").grid(row = 21, column = 0, padx = 10,   )
		new_pay = ttk.Combobox(new_edit,textvariable = pay_text, width = 30)
		new_pay.configure(values = ("Cash","POS","Paystack","Bank Transfer","Courier","Store Credit"))		
		new_pay.grid(row = 21, column =1, padx = 10,  )

		Label(new_edit,text = "Old(Date)").grid(row = 22, column = 0, padx = 10  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = date_text),state = "readonly").grid(row=22, column = 1, padx = 10  )
		Label(new_edit,text = "New(Date").grid(row = 23, column = 0, padx = 10  )
		new_date = DateEntry(new_edit,width = 30)
		new_date.grid(row = 23, column =1, padx = 10)

		Button(new_edit, text = "Save Changes", cursor = "hand2", command = lambda:edit_record(new_order.get(),order_text,new_name.get(),name_text,new_add.get(),add_text,new_phone.get(),phone_text,new_email.get(),email_text,new_nso.get(),nso_text,new_nst.get(),nst_text,new_nsr.get(),nsr_text,new_amount.get(),amo_text,new_status.get(),stat_text,new_pay.get(),pay_text,new_date.get(),date_text)).grid(row = 24, column = 1)

		new_edit.mainloop()


		#sqlite3.OperationalError: near "WHERE": syntax error
		#Please ensure there are no commas before the WHERE clause
	def edit_record(new_order,order_text,new_name,name_text,new_add,add_text,new_phone,phone_text,new_email,email_text,new_nso,nso_text,new_nst,nst_text,new_nsr,nsr_text,new_amount,amo_text,new_status,stat_text,new_pay,pay_text,new_date,date_text):
		query = "UPDATE trans SET orderr = ?,  name = ?,  address = ?,  phone = ?,  email = ?,  nso = ?,  nst = ?,  nsr = ?,  amo = ?,  status = ?,  pay = ?,  datee = ? WHERE orderr = ? AND name = ? AND address = ? AND phone = ? AND email = ? AND  nso = ? AND  nst = ? AND nsr = ? AND amo = ? AND status = ? AND pay = ? AND datee = ?"
		parameters = (new_order,new_name,new_add,new_phone,new_email,new_nso,new_nst,new_nsr,new_amount,new_status,new_pay,new_date,order_text,name_text,add_text,phone_text,email_text,nso_text,nst_text,nsr_text,amo_text,stat_text,pay_text,date_text)
		run_query(query,parameters)
		display["text"] = "Record {} has been updated to {}".format(new_name,name_text)			
		view_record()

	def helpp():
		messagebox.showinfo("Help!!!","This is Dean Winchester, and I need your help")

					#LABELS 1

	top_label = Label(trans, text = "Transaction Details", font = "Garamond 30 bold italic underline", fg = "#4b3300", bg = "#e0ffff")
	top_label.grid(row = 0, column = 0)

	order_label = Label(frame, text = "Order Number", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	order_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)

	name_label = Label(frame, text = "Customer Name", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	name_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 10)

	add_label = Label(frame, text = "Customer Address", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	add_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 10)

	phone_label = Label(frame, text = "Customer Phone number", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	phone_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 10)

	email_label = Label(frame, text = "Customer Email address", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	email_label.grid(row = 5, column = 0, sticky = W, padx = 10, pady = 10)

	nso_label = Label(frame, text = "Number of Shoes Ordered", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	nso_label.grid(row = 6, column = 0, sticky = W, padx = 10, pady = 10)


				#ENTRY1

	order_text = StringVar()
	order_entry = Entry(frame, textvariable = order_text, width = 55, bd = 3)
	order_entry.grid(row = 1, column = 1, sticky = W)

	name_text = StringVar()
	name_entry = Entry(frame, textvariable = name_text, width = 55, bd = 3)
	name_entry.grid(row = 2, column = 1, sticky = W)

	add_text = StringVar()
	add_entry = Entry(frame, textvariable = add_text, width = 55, bd = 3)
	add_entry.grid(row = 3, column = 1, sticky = W)

	phone_text = StringVar()
	phone_entry = Entry(frame, textvariable = phone_text, width = 55, bd = 3)
	phone_entry.grid(row = 4, column = 1, sticky = W)

	email_text = StringVar()
	email_entry = Entry(frame, textvariable = email_text, width = 55, bd = 3)
	email_entry.grid(row = 5, column = 1, sticky = W)

	nso_text = StringVar()
	nso_entry = Spinbox(frame, textvariable = nso_text, cursor = "hand2", from_=0, to = 10000,width = 15, bd = 3)
	nso_entry.grid(row = 6, column = 1, sticky = W)


					#LABELS 2

	nst_label = Label(frame, text = "Number of Shoes Taken", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	nst_label.grid(row = 1, column = 2, sticky = W, padx = 121, pady = 10)

	nsr_label = Label(frame, text = "Number of Shoes Rejected", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	nsr_label.grid(row = 2, column = 2, sticky = W, padx = 121, pady = 10)

	stat_label = Label(frame, text = "Status of Delivery ", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	stat_label.grid(row = 4, column = 2, sticky = W, padx = 121, pady = 10)

	amo_label = Label(frame, text = "Amount Paid", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	amo_label.grid(row = 3, column = 2, sticky = W, padx = 121, pady = 10)

	pay_label = Label(frame, text = "Payment Method", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	pay_label.grid(row = 5, column = 2, sticky = W, padx = 121, pady = 10)

	date_label = Label(frame, text = "Date", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	date_label.grid(row = 6, column = 2, sticky = W, padx = 121, pady = 10)


				#ENTRY2

	nst_text = StringVar()
	nst_entry = Spinbox(frame, textvariable = nst_text, cursor = "hand2", from_=0, to = 10000,width = 15, bd = 3)
	nst_entry.grid(row = 1, column = 3, sticky = W)

	nsr_text = StringVar()
	nsr_entry = Spinbox(frame, textvariable = nsr_text,cursor = "hand2", from_=0, to = 10000,width = 15, bd = 3)
	nsr_entry.grid(row = 2, column = 3, sticky = W)

	amo_text = StringVar()
	amo_entry = Entry(frame, textvariable = amo_text, width = 15, bd = 3)
	amo_entry.grid(row = 3, column = 3, sticky = W)

	stat_text = StringVar()
	stat_entry = ttk.Combobox(frame, cursor = "hand2", textvariable = stat_text)
	stat_entry.config(values = ("Fully Delivered", "Partially Delivered","Rejected","Cancelled", "Rescheduled","In Transit"))
	stat_entry.grid(row = 4, column = 3, sticky = W)

	pay_text = StringVar()
	pay_entry = ttk.Combobox(frame, cursor = "hand2", textvariable = pay_text)
	pay_entry.config(values = ("Cash", "POS","Paystack","Bank Transfer", "Courier","Store Credit"))
	pay_entry.grid(row = 5, column = 3, sticky = W)

	date_text = StringVar()
	date_entry = DateEntry(frame, cursor = "hand2", textvariable = date_text, width = 15, bd = 3)
	date_entry.grid(row = 6, column = 3, sticky = W)

				#BUTTONS

	add_but = Button(frame, text = "Add Transaction",  cursor = "hand2", bd = 2, fg = "#ff00ad", bg = "#e0ffff", font = "Garamond 15 bold italic",command = add_record)
	add_but.grid(row = 7, column = 1, padx = 50, pady = (10,15))

	display = Label(frame, text = "",font = "Garamond 15 bold italic", fg = "blue")
	display.grid(row = 7, column = 2, padx = 15)

	#-----------------------TREEVIEW-------------------------------------#

	tree = ttk.Treeview(trans,height = 150, columns = ["","","","","","","","","","","","",])
	tree.grid(row=9, column = 0, columnspan = 2, padx = 25)

	style = ttk.Style()
	style.configure("Treeview.Heading", font = "Garamond 9 bold italic")

	tree.heading("#0",text = "ID")
	tree.column("#0", width = 50)

	tree.heading("#1",text = "Order Number")
	tree.column("#1", width = 100)

	tree.heading("#2",text = "Customer Name")
	tree.column("#2", width = 120)

	tree.heading("#3",text = "Address")
	tree.column("#3", width = 140)

	tree.heading("#4",text = "Phone Number")
	tree.column("#4", width = 110)

	tree.heading("#5",text = "Email address")
	tree.column("#5", width = 100)

	tree.heading("#6",text = "Shoes Ordered")
	tree.column("#6", width = 100)

	tree.heading("#7",text = "Shoes Taken")
	tree.column("#7", width = 100)

	tree.heading("#8",text = "Shoes Rejected")
	tree.column("#8", width = 100)

	tree.heading("#9",text = "Amount Paid")
	tree.column("#9", width = 100)

	tree.heading("#10",text = "Status of Delivery")
	tree.column("#10", width = 100)

	tree.heading("#11",text = "Payment Method")
	tree.column("#11", width = 100)

	tree.heading("#12",text = "Delivery Date")
	tree.column("#12", width = 100)
	view_record()
	#-------------------MENUS AND SUB MENUS--------------------------#

	main_menu = Menu()
	submenu = Menu()

	main_menu.add_cascade(label = "File" )
	main_menu.add_cascade(label = "Add",command = add_record)
	main_menu.add_cascade(label = "Edit", command = edit_box)
	main_menu.add_cascade(label = "Delete", command = delete_record)
	main_menu.add_cascade(label = "Help",command = helpp)
	main_menu.add_cascade(label = "Exit",command = trans.destroy)

	submenu.add_command(label = "Add Record", command = add_record)
	submenu.add_command(label = "Edit Record",command = edit_box)
	submenu.add_command(label = "Delete Record", command = delete_record)
	submenu.add_separator()
	submenu.add_command(label = "Help",command = helpp)
	submenu.add_command(label = "Exit", command = trans.destroy)

	trans.configure(menu = main_menu)


	def tick():
		d = datetime.datetime.now()
		mytime = time.strftime("%I : %M : %S%p")
		mydate = "{:%B - %d - %Y}".format(d)
		lblInfo.config(text = mytime + "\t" + mydate)
		lblInfo.after(200,tick)
	lblInfo = Label(trans, font = "Garamond 15 bold italic", fg = "blue", bg = "#e0ffff")
	lblInfo.grid(row = 0, column = 1)
	tick()

	trans.mainloop()
trans()