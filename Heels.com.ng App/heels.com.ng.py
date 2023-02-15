from tkinter import *
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
import time
import sqlite3

#-------------------SALES REPORT DETAILS-------------------------


def sales_report():
	sr = Toplevel(root)
	sr.title("Merchant Sales Report")
	sr.geometry("1350x850")
	sr.configure(background = "#c93073")


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
		query = "SELECT * FROM sr"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])


	def validation():
		return len(month_entry.get())!=0,len(name_entry.get())!=0,len(nos_entry.get())!=0,len(amount_entry.get())!=0,len(amount1_entry.get())!=0,len(status_entry.get())!=0,len(date_entry.get())!=0

	def add_record():
		if validation():
			query = "INSERT INTO sr VALUES(NULL,?,?,?,?,?,?,?)"
			parameters = (month_entry.get(),name_entry.get(),nos_entry.get(),amount_entry.get(),amount1_entry.get(),status_entry.get(),date_entry.get())
			run_query(query,parameters)
			display["text"] = "Record {} has been added".format(month_entry.get())

			month_entry.delete(0,END)
			name_entry.delete(0,END)
			nos_entry.delete(0,END)
			amount_entry.delete(0,END)
			amount1_entry.delete(0,END)
			status_entry.delete(0,END)
			date_entry.delete(0,END)

		else:
			display["text"] = "Please fill all entries"
		view_record()


	def delete_record():
		try:
			tree.item(tree.selection())["values"][1]
		except IndexError as e:
			display["text"] = "Please select a record to delete"
		query = "DELETE FROM sr WHERE ID=?"
		number = tree.item(tree.selection())["text"]
		run_query(query,(number,))
		display["text"] = "Record {} has been deleted".format(number)
		view_record()


	def edit_box():
		try:
			tree.item(tree.selection())["values"][0]
		except IndexError as e:
			display["text"] = "Please select a record to edit"
		month_text = tree.item(tree.selection())["values"][0]
		name_text = tree.item(tree.selection())["values"][1]
		nos_text = tree.item(tree.selection())["values"][2]
		amount_text = tree.item(tree.selection())["values"][3]
		amount1_text = tree.item(tree.selection())["values"][4]
		status_text = tree.item(tree.selection())["values"][5]
		date_text = tree.item(tree.selection())["values"][6]

		new_edit = Toplevel()
		new_edit.title("Edit Record")

		Label(new_edit, text = "Old(Month)").grid(row = 0, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = month_text), state = "readonly").grid(row = 0, column = 1)
		Label(new_edit, text = "New(Month)").grid(row = 1, column = 0)
		new_month = ttk.Combobox(new_edit, textvariable = month_text, width = 30)
		new_month.configure(values = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))
		new_month.grid(row = 1, column = 1)

		Label(new_edit, text = "Old(Name of Merchant)").grid(row = 2, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = name_text), state = "readonly").grid(row = 2, column = 1)
		Label(new_edit, text = "New(Name of Merchant)").grid(row = 3, column = 0)
		new_name = Entry(new_edit, width = 30, bd = 3)
		new_name.grid(row = 3, column = 1)

		Label(new_edit, text = "Old(Number of Shoes Sold)").grid(row = 4, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = nos_text), state = "readonly").grid(row = 4, column = 1)
		Label(new_edit, text = "New(Number of Shoes Sold)").grid(row = 5, column = 0)
		new_nos = Entry(new_edit, width = 30)
		new_nos.grid(row = 5, column = 1)

		Label(new_edit, text = "Old(Amount to be paid)").grid(row = 6, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = amount_text), state = "readonly").grid(row = 6, column = 1)
		Label(new_edit, text = "New(Amount to be paid)").grid(row = 7, column = 0)
		new_amount = Spinbox(new_edit, textvariable = amount_text, from_ = 1, to = 100, width = 30)
		new_amount.grid(row = 7, column = 1)

		Label(new_edit, text = "Old(Amount Profited to Heels)").grid(row = 8, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = amount_text), state = "readonly").grid(row = 8, column = 1)
		Label(new_edit, text = "New(Amount Profited to Heels)").grid(row = 9, column = 0)
		new_amount1 = Spinbox(new_edit, textvariable = amount_text, from_ = 1, to = 100, width = 30)
		new_amount1.grid(row = 9, column = 1)

		Label(new_edit, text = "Old(Status of Payment)").grid(row = 10, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = status_text), state = "readonly").grid(row = 10, column = 1)
		Label(new_edit, text = "New(Status of Payment)").grid(row = 11, column = 0)
		new_status = ttk. Combobox(new_edit, textvariable = status_text, width = 30)
		new_status.configure(values= ("Paid","Yet to be paid"))
		new_status.grid(row = 11, column = 1)

		Label(new_edit, text = "Old(Date)").grid(row = 12, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = date_text), state = "readonly").grid(row = 12, column = 1)
		Label(new_edit, text = "New(Date)").grid(row = 13, column = 0)
		new_date = DateEntry(new_edit, textvariable = date_text, width = 30)
		new_date.grid(row = 13, column = 1)

		Button(new_edit, text = "Save Changes", cursor = "hand2", command = lambda:edit_record(new_month.get(),month_text,new_name.get(),name_text,new_nos.get(),nos_text,new_amount.get(),amount_text,new_amount1.get(),amount1_text,new_status.get(),status_text,new_date.get(),date_text)).grid(row = 14, column = 1)


		new_edit.mainloop()

	def edit_record(new_month,month_text,new_name,name_text,new_nos,nos_text,new_amount,amount_text,new_amount1,amount_text1,new_status,status_text,new_date,date_text):
			query = "UPDATE sr SET month = ?,  name = ?,  nos = ?,  amount = ?,  amount1 = ?, status = ?, datee = ? WHERE  month = ? AND  name = ? AND nos = ? AND amount = ? AND amount1 = ? AND status = ? AND datee = ?"
			parameters = (new_month,new_name,new_nos,new_amount,new_amount1,new_status,new_date,month_text,name_text,nos_text,amount_text,amount_text1,status_text,date_text)
			run_query(query,parameters)
			display["text"] = "Record {} has been changed to {}".format(month_text,new_month)


			view_record()


	def helpp():
		messagebox.showinfo("Hey!!!","Look at my Junk")


	#--------------------------IMAGES-------------------------------#

	img = ImageTk.PhotoImage(Image.open("C:\\Icons\\salesreport1.png"))
	img_label = Label(sr, image = img, width = 550, height = 335)
	img_label.grid(row = 1, column = 1, sticky=SW)

	#--------------------------FRAMES-------------------------------#

	frame = LabelFrame(sr, width = 50, bd = 3, bg = "#97e8e1", padx = 10)
	frame.grid(row = 1, column = 0, padx = 10, pady = 5)

	#--------------------------LABELS-------------------------------#

	topic_label = Label(sr,text = "Merchants Sales Report Summary", font = "Georgia 30 bold underline", bg = "#c93073")
	topic_label.grid(row = 0, column = 0, padx = 1, pady = 10, sticky=W)

	month_label = Label(frame,text = "Month", font = "Georgia 11 bold", bg = "#97e8e1")
	month_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 5)

	mn_label = Label(frame,text = "Merchant Name", font = "Georgia 11 bold", bg = "#97e8e1")
	mn_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 5)

	nos_label = Label(frame,text = "Number of Shoes sold", font = "Georgia 11 bold", bg = "#97e8e1")
	nos_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 5)

	amount_label = Label(frame,text = "Amount to Merchant", font = "Georgia 11 bold", bg = "#97e8e1")
	amount_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 5)

	amount1_label = Label(frame,text = "Amount Profited to Heels", font = "Georgia 11 bold", bg = "#97e8e1")
	amount1_label.grid(row = 5, column = 0, sticky = W, padx = 10, pady = 5)

	status_label = Label(frame,text = "Status of Payment", font = "Georgia 11 bold", bg = "#97e8e1")
	status_label.grid(row = 6, column = 0, sticky = W, padx = 10, pady = 5)

	date_label = Label(frame,text = "Date Reconciled", font = "Georgia 11 bold", bg = "#97e8e1")
	date_label.grid(row = 7, column = 0, sticky = W, padx = 10, pady = 5)


	#--------------------------ENTRIES-------------------------------#

	month_text = StringVar()
	month_entry = ttk.Combobox(frame,  cursor = "hand2", textvariable = month_text)
	month_entry.config(values = ("January","February","March","April","May","June","July","August","September","October","November","December",))
	month_entry.grid(row = 1, column = 1, sticky = W)

	name_text = StringVar()
	name_entry = Entry(frame, textvariable = name_text, width = 40, bd = 3)
	name_entry.grid(row = 2, column = 1, sticky = W)

	nos_text = StringVar()
	nos_entry = Spinbox(frame,cursor = "hand2", textvariable = nos_text, from_=1, to = 100, width = 40, bd = 3)
	nos_entry.grid(row = 3, column = 1, sticky = W)

	amount_text = StringVar()
	amount_entry = Entry(frame, textvariable = amount_text, width = 40,cursor = "hand2")
	amount_entry.grid(row = 4, column = 1, sticky = W)


	amount1_text = StringVar()
	amount1_entry = Entry(frame, textvariable = amount1_text, width = 40,cursor = "hand2")
	amount1_entry.grid(row = 5, column = 1, sticky = W)


	status_text = StringVar()
	status_entry = ttk.Combobox(frame,  cursor = "hand2", textvariable = status_text, width = 15)
	status_entry.config(values = ("Paid","Not Yet Paid"))
	status_entry.grid(row = 6, column = 1, sticky = W)


	date_text = StringVar()
	date_entry = DateEntry(frame,  cursor = "hand2", textvariable = date_text, width = 15, bd = 3)
	date_entry.grid(row = 7, column = 1, sticky = W)

				#BUTTONS

	#--------------------------BUTTONS-------------------------------#


	add_butt = Button(frame, text = "Add Record",  cursor = "hand2", font = "Georgia 11 bold", bg = "#97e8e1",command = add_record)
	add_butt.grid(row = 8, column = 1, pady = 10)

	display = Label(frame, text = "",font = "Garamond 15 bold italic", fg = "blue", bg = "#97e8e1")
	display.grid(row = 9, column = 1, padx = 15)



	#--------------------------TREEVIEW-------------------------------#

	tree = ttk.Treeview(sr, height = 15, columns = ["","","","","","",""])
	tree.grid(row = 9, column = 0, columnspan = 2, padx = 10, pady = 10)

	tree.heading("#0",text = "ID")
	tree.column("#0",width = 80)

	tree.heading("#1",text = "Month")
	tree.column("#1",width = 100)

	tree.heading("#2",text = "Merchant Name")
	tree.column("#2",width = 100)

	tree.heading("#3",text = "Number of Shoes Sold")
	tree.column("#3",width = 200)

	tree.heading("#4",text = "Amount to Merchant")
	tree.column("#4",width = 150)

	tree.heading("#5",text = "Amount to Heels")
	tree.column("#5",width = 150)

	tree.heading("#6",text = "Status")
	tree.column("#6",width = 150)

	tree.heading("#7",text = "Date")
	tree.column("#7",width = 150)

	style = ttk.Style()
	style.configure("Treeview.Heading",font = "Georgia 11 bold italic")

	#--------------------------SCROLLBAR-------------------------------#

	sb = Scrollbar(sr,command = tree.yview)
	sb.grid(row = 8, column = 2, rowspan = 4, sticky = NS, ipady = 2)

	#--------------------------MENUS AND SUBMENU-------------------------------#

	main_menu = Menu()
	submenu = Menu()

	main_menu.add_cascade(label = "File", menu = submenu)
	main_menu.add_cascade(label = "Add", command = add_record)
	main_menu.add_cascade(label = "Edit",command = edit_box)
	main_menu.add_cascade(label = "Delete", command = delete_record)	
	main_menu.add_cascade(label = "Help",command = helpp)
	main_menu.add_cascade(label = "Exit",command = sr.destroy)

	submenu.add_command(label = "Add Record", command = add_record)
	submenu.add_command(label = "Edit Record",command = edit_box)
	submenu.add_command(label = "Delete Record", command = delete_record)
	submenu.add_separator()
	submenu.add_command(label = "Help",command = helpp)
	submenu.add_command(label = "Exit",command = sr.destroy)

	sr.configure(menu = main_menu)

	#--------------------------TIME AND DATE-------------------------------#

	def tick():
		d = datetime.datetime.now()
		mydate = "{:%B - %d - %Y}".format(d)
		mytime = time.strftime("%I : %M : %S%p")
		lblInfo.config(text = mytime +"\t" + mydate)
		lblInfo.after(200,tick)
	lblInfo = Label(sr, font = "Georgia 11 bold italic", fg = "red", bg = "#c3f705")
	lblInfo.grid(row = 0, column = 1)
	tick()

	view_record()


	sr.mainloop()


#-------------------PROFIT AND LOSS DETAILS-------------------------




def profitloss():
	prof = Toplevel(root)
	prof.title("Profit/Loss")
	prof.geometry("1250x1150")
	prof.configure(background = "#c93073")
	

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
		query = "SELECT * FROM prof"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
	


	#-----------------VIEW MENU-----------------------------

	def view_recordprof():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof WHERE status = 'Profit'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
	
	def view_recordloss():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof WHERE status = 'Loss'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_recordeven():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof WHERE status = 'Even'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])


	#-----------------SORT MENU-----------------------------

	def view_record_datenew():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof ORDER BY datee"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_dateold():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof ORDER BY datee DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_revhigh():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof ORDER BY rev DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_revlow():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof ORDER BY rev"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_exphigh():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof ORDER BY exp DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_explow():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof ORDER BY exp"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_nethigh():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof ORDER BY net DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_netlow():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM prof ORDER BY net"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])



	def validation():
		return len(month_entry.get())!=0,len(rev_entry.get())!=0,len(exp_entry.get())!=0,len(net_entry.get())!=0,len(stat_text.get())!=0,len(date_entry.get())!=0

	def add_record():
		if validation():
			query = "INSERT INTO prof VALUES(NULL,?,?,?,?,?,?)"
			parameters = (month_entry.get(),rev_entry.get(),exp_entry.get(),net_entry.get(),stat_text.get(),date_entry.get())
			run_query(query,parameters)
			display["text"] = "Record {} has been added".format(month_entry.get())

			month_entry.delete(0,END)
			rev_entry.delete(0,END)
			exp_entry.delete(0,END)
			net_entry.delete(0,END)
			stat_radio.delete(0,END)
			date_entry.delete(0,END)

		else:
			display["text"] = "Please fill all entries"
		view_record()


	def delete_record():
		try:
			tree.item(tree.selection())["values"][1]
		except IndexError as e:
			display["text"] = "Please select a record to delete"
		query = "DELETE FROM prof WHERE ID=?"
		number = tree.item(tree.selection())["text"]
		run_query(query,(number,))
		display["text"] = "Record {} has been deleted".format(number)
		view_record()



	def edit_box():
		try:
			tree.item(tree.selection())["values"][0]
		except IndexError as e:
			display["text"] = "Please select a record to edit"
		month_text = tree.item(tree.selection())["values"][0]
		rev_text = tree.item(tree.selection())["values"][1]
		exp_text = tree.item(tree.selection())["values"][2]
		net_text = tree.item(tree.selection())["values"][3]
		stat_text = tree.item(tree.selection())["values"][4]
		date_text = tree.item(tree.selection())["values"][5]

		new_edit = Toplevel()
		new_edit.title("Edit Record")

		Label(new_edit, text = "Old(Month)").grid(row = 0, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = month_text), state = "readonly").grid(row = 0, column = 1)
		Label(new_edit, text = "New(Month)").grid(row = 1, column = 0)
		new_month = ttk.Combobox(new_edit, textvariable = month_text, width = 30)
		new_month.configure(values = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))
		new_month.grid(row = 1, column = 1)

		Label(new_edit, text = "Old(All Revenue)").grid(row = 2, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = rev_text), state = "readonly").grid(row = 2, column = 1)
		Label(new_edit, text = "New(All Revenue)").grid(row = 3, column = 0)
		new_rev = Entry(new_edit, width = 30, bd = 3)
		new_rev.grid(row = 3, column = 1)

		Label(new_edit, text = "Old(All Expense)").grid(row = 4, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = exp_text), state = "readonly").grid(row = 4, column = 1)
		Label(new_edit, text = "New(All Expense)").grid(row = 5, column = 0)
		new_exp = Entry(new_edit, width = 30)
		new_exp.grid(row = 5, column = 1)

		Label(new_edit, text = "Old(Net Amount)").grid(row = 6, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = net_text), state = "readonly").grid(row = 6, column = 1)
		Label(new_edit, text = "New(Net Amount)").grid(row = 7, column = 0)
		new_net = Entry(new_edit, textvariable = net_text, width = 30)
		new_net.grid(row = 7, column = 1)

		Label(new_edit, text = "Old(Status)").grid(row = 8, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = stat_text), state = "readonly").grid(row = 8, column = 1)
		Label(new_edit, text = "New(Status)").grid(row = 9, column = 0)
		stat_radio = ttk.Combobox(new_edit, textvariable = stat_text, width = 40)
		stat_radio.configure(value = ("Profit","Loss","Even",))
		stat_radio.grid(row = 9, column = 1, sticky = W)

		Label(new_edit, text = "Old(Date)").grid(row = 10, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = date_text), state = "readonly").grid(row = 10, column = 1)
		Label(new_edit, text = "New(Date)").grid(row = 11, column = 0)
		new_date = DateEntry(new_edit, textvariable = date_text, width = 30)
		new_date.grid(row = 11, column = 1)

		Button(new_edit, text = "Save Changes", cursor = "hand2", command = lambda:edit_record(new_month.get(),month_text,new_rev.get(),rev_text,new_exp.get(),exp_text,new_net.get(),net_text,stat_radio.get(),stat_text,new_date.get(),date_text)).grid(row = 12, column = 1)


		new_edit.mainloop()

	def edit_record(new_month,month_text,new_rev,rev_text,new_exp,exp_text,new_net,net_text,stat_radio,stat_text,new_date,date_text):
			query = "UPDATE prof SET month = ?,  rev = ?,  exp = ?,  net = ?, status = ?, datee = ? WHERE  month = ? AND  rev = ? AND exp = ? AND net = ? AND status = ? AND datee = ?"
			parameters = (new_month,new_rev,new_exp,new_net,stat_radio,new_date,month_text,rev_text,exp_text,net_text,stat_text,date_text)
			run_query(query,parameters)
			display["text"] = "Record {} has been changed to {}".format(month_text,new_month)


			view_record()


	def helpp():
		messagebox.showinfo("Hey!!!","Look at my Junk")


	#--------------------------IMAGES-------------------------------#

	img = ImageTk.PhotoImage(Image.open("C:\\Icons\\profitloss1.png"))
	img_label = Label(prof, image = img, width = 600, height = 350)
	img_label.grid(row = 1, column = 1)

	#--------------------------FRAMES-------------------------------#

	frame = LabelFrame(prof, width = 50, bd = 3, bg = "#97e8e1", padx = 20, pady = 20)
	frame.grid(row = 1, column = 0, padx = 30, pady = 5)

	#--------------------------LABELS-------------------------------#

	topic_label = Label(prof,text = "Profit/Loss Summary", font = "Georgia 30 bold underline", bg = "#c93073")
	topic_label.grid(row = 0, column = 0, padx = 1, pady = 10, sticky=W)

	month_label = Label(frame,text = "Month", font = "Georgia 11 bold", bg = "#97e8e1")
	month_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 5)

	rev_label = Label(frame,text = "All Revenue", font = "Georgia 11 bold", bg = "#97e8e1")
	rev_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 5)

	exp_label = Label(frame,text = "All Expenses", font = "Georgia 11 bold", bg = "#97e8e1")
	exp_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 5)

	net_label = Label(frame,text = "Net Amount", font = "Georgia 11 bold", bg = "#97e8e1")
	net_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 5)

	status_label = Label(frame,text = "Status", font = "Georgia 11 bold", bg = "#97e8e1")
	status_label.grid(row = 5, column = 0, sticky = W, padx = 10, pady = 5)

	date_label = Label(frame,text = "Date Reconciled", font = "Georgia 11 bold", bg = "#97e8e1")
	date_label.grid(row = 6, column = 0, sticky = W, padx = 10, pady = 5)

	#--------------------------ENTRIES-------------------------------#

	month_text = StringVar()
	month_entry = ttk.Combobox(frame, textvariable = month_text)
	month_entry.configure(values = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))
	month_entry.grid(row = 1, column = 1, sticky = W)

	rev_text = StringVar()
	rev_entry = Entry(frame, textvariable = rev_text, width = 40, bd = 3)
	rev_entry.grid(row = 2, column = 1, sticky = W)

	exp_text = StringVar()
	exp_entry = Entry(frame, textvariable = exp_text, width = 40, bd = 3)
	exp_entry.grid(row = 3, column = 1, sticky = W)

	net_text = StringVar()
	net_entry = Entry(frame, textvariable = net_text, width = 40, bd = 3)
	net_entry.grid(row = 4, column = 1, sticky = W)

	stat_text = StringVar()
	stat_radio = ttk.Combobox(frame, textvariable = stat_text, width = 37)
	stat_radio.configure(value = ("Profit","Loss","Even",))
	stat_radio.grid(row = 5, column = 1, sticky = W)

	date_text = StringVar()
	date_entry = DateEntry(frame, textvariable = date_text,  cursor = "hand2", width = 15, bd = 3)
	date_entry.grid(row = 6, column = 1, sticky = W)


	#--------------------------BUTTONS-------------------------------#


	add_butt = Button(frame, text = "Add Summary",  cursor = "hand2", font = "Georgia 11 bold", bg = "#97e8e1",command = add_record)
	add_butt.grid(row = 7, column = 0, pady = 20)

	display = Label(frame, text = "",font = "Garamond 15 bold italic", fg = "blue", bg = "#97e8e1")
	display.grid(row = 8, column = 1, padx = 15)



	#--------------------------TREEVIEW-------------------------------#

	tree = ttk.Treeview(prof, height = 15, columns = ["","","","","",""])
	tree.grid(row = 9, column = 0, columnspan = 3, padx = 30, pady = 20)

	tree.heading("#0",text = "ID")
	tree.column("#0",width = 80)

	tree.heading("#1",text = "Month")
	tree.column("#1",width = 200)

	tree.heading("#2",text = "All Revenue")
	tree.column("#2",width = 200)

	tree.heading("#3",text = "All Expenses")
	tree.column("#3",width = 200)

	tree.heading("#4",text = "Net Amount")
	tree.column("#4",width = 150)

	tree.heading("#5",text = "Status")
	tree.column("#5",width = 150)

	tree.heading("#6",text = "Date")
	tree.column("#6",width = 150)

	style = ttk.Style()
	style.configure("Treeview.Heading",font = "Georgia 11 bold italic")

	#--------------------------SCROLLBAR-------------------------------#

	sb = Scrollbar(prof,command = tree.yview)
	sb.grid(row = 8, column = 2, rowspan = 4, sticky = NS, ipady = 2)

	#--------------------------MENUS AND SUBMENU-------------------------------#

	main_menu = Menu()
	submenu = Menu()
	view_menu = Menu()
	sort_menu = Menu()
	date_menu = Menu()
	rev_menu = Menu()
	exp_menu = Menu()
	net_menu = Menu()

	main_menu.add_cascade(label = "File", menu = submenu)
	main_menu.add_cascade(label = "View", menu = view_menu)
	main_menu.add_cascade(label = "Sort", menu = sort_menu)
	main_menu.add_cascade(label = "Statistics")	
	main_menu.add_cascade(label = "Help",command = helpp)
	main_menu.add_cascade(label = "Exit",command = prof.destroy)

	submenu.add_command(label = "Add Record", command = add_record)
	submenu.add_command(label = "Edit Record",command = edit_box)
	submenu.add_command(label = "Delete Record", command = delete_record)
	submenu.add_separator()
	submenu.add_command(label = "Help",command = helpp)
	submenu.add_command(label = "Exit",command = prof.destroy)

	view_menu.add_command(label = "All Summary", command = view_record)
	view_menu.add_command(label = "All Profits", command = view_recordprof)
	view_menu.add_command(label = "All Loss", command = view_recordloss)
	view_menu.add_command(label = "All Even", command = view_recordeven)

	sort_menu.add_cascade(label = "By Date", menu = date_menu)
	date_menu.add_command(label = "Newest", command = view_record_datenew)
	date_menu.add_command(label = "Oldest", command = view_record_dateold)

	sort_menu.add_cascade(label = "By Revenue", menu = rev_menu)
	rev_menu.add_command(label = "Highest", command = view_record_revhigh)
	rev_menu.add_command(label = "Lowest", command = view_record_revlow)

	sort_menu.add_cascade(label = "By Expense", menu = exp_menu)
	exp_menu.add_command(label = "Highest", command = view_record_exphigh)
	exp_menu.add_command(label = "Lowest", command = view_record_explow)

	sort_menu.add_cascade(label = "By Net", menu = net_menu)
	net_menu.add_command(label = "Highest", command = view_record_nethigh)
	net_menu.add_command(label = "Lowest", command = view_record_netlow)

	prof.configure(menu = main_menu)

	#--------------------------TIME AND DATE-------------------------------#

	def tick():
		d = datetime.datetime.now()
		mydate = "{:%B - %d - %Y}".format(d)
		mytime = time.strftime("%I : %M : %S%p")
		lblInfo.config(text = mytime +"\t" + mydate)
		lblInfo.after(200,tick)
	lblInfo = Label(prof, font = "Georgia 11 bold italic", fg = "red", bg = "#c3f705")
	lblInfo.grid(row = 0, column = 1)
	tick()


	view_record()


	prof.mainloop()
	


#-------------------REVENUE DETAILS-------------------------




def revenue():
	rev = Toplevel(root)
	rev.title("Revenue")
	rev.geometry("1250x850")
	rev.configure(background = "#c3f705")


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
		query = "SELECT * FROM rev"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	#------------------VIEW MENU---------------------------#

	def view_record_pos():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM rev WHERE mode = 'POS'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_cash():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM rev WHERE mode = 'Cash'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_bt():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM rev WHERE mode = 'Bank Transfer'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_paystack():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM rev WHERE mode = 'Paystack'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_courier():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM rev WHERE mode = 'Courier'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_store():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM rev WHERE mode = 'Store Credit'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])




	#------------------SORT MENU---------------------------#

	def view_record_datenew():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM rev ORDER BY datee"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_dateold():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM rev ORDER BY datee DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_revhigh():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM rev ORDER BY amount DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])

	def view_record_revlow():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM rev ORDER BY datee"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])






	def validation():
		return len(order_entry.get())!=0,len(name_entry.get())!=0,len(amount_entry.get())!=0,len(mode_entry.get())!=0,len(date_entry.get())!=0

	def add_record():
		if validation():
			query = "INSERT INTO rev VALUES(NULL,?,?,?,?,?)"
			parameters = (order_entry.get(),name_entry.get(),amount_entry.get(),mode_entry.get(),date_entry.get())
			run_query(query,parameters)
			display["text"] = "Record {} has been added".format(order_entry.get())

			order_entry.delete(0,END)
			name_entry.delete(0,END)
			amount_entry.delete(0,END)
			mode_entry.delete(0,END)
			date_entry.delete(0,END)

		else:
			display["text"] = "Please fill all entries"
		view_record()


	def delete_record():
		try:
			tree.item(tree.selection())["values"][1]
		except IndexError as e:
			display["text"] = "Please select a record to delete"
		query = "DELETE FROM rev WHERE ID=?"
		number = tree.item(tree.selection())["text"]
		run_query(query,(number,))
		display["text"] = "Record {} has been deleted".format(number)
		view_record()


	def edit_box():
		try:
			tree.item(tree.selection())["values"][0]
		except IndexError as e:
			display["text"] = "Please select a record to edit"
		order_text = tree.item(tree.selection())["values"][0]
		name_text = tree.item(tree.selection())["values"][1]
		amount_text = tree.item(tree.selection())["values"][2]
		mode_text = tree.item(tree.selection())["values"][3]
		date_text = tree.item(tree.selection())["values"][4]

		new_edit = Toplevel()
		new_edit.title("Edit Record")

		Label(new_edit, text = "Old(Order Number)").grid(row = 0, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = order_text), state = "readonly").grid(row = 0, column = 1)
		Label(new_edit, text = "New(Order Number)").grid(row = 1, column = 0)
		new_order = Entry(new_edit, width = 30, bd = 3)
		new_order.grid(row = 1, column = 1)

		Label(new_edit, text = "Old(Name of Customer)").grid(row = 2, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = name_text), state = "readonly").grid(row = 2, column = 1)
		Label(new_edit, text = "New(Name of Customer)").grid(row = 3, column = 0)
		new_name = Entry(new_edit, width = 30, bd = 3)
		new_name.grid(row = 3, column = 1)

		Label(new_edit, text = "Old(Amount)").grid(row = 4, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = amount_text), state = "readonly").grid(row = 4, column = 1)
		Label(new_edit, text = "New(Amount)").grid(row = 5, column = 0)
		new_amount = Entry(new_edit, width = 30)
		new_amount.grid(row = 5, column = 1)

		Label(new_edit, text = "Old(Mode of Payment)").grid(row = 6, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = mode_text), state = "readonly").grid(row = 6, column = 1)
		Label(new_edit, text = "New(Mode of Payment)").grid(row = 7, column = 0)
		new_mode = ttk.Combobox(new_edit, textvariable = mode_text, width = 30)
		new_mode.configure(values = ("Cash","POS","Bank Transfer","Paystack","Courier","Store Credit"))
		new_mode.grid(row = 7, column = 1)

		Label(new_edit, text = "Old(Date)").grid(row = 8, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = date_text), state = "readonly").grid(row = 8, column = 1)
		Label(new_edit, text = "New(Date)").grid(row = 9, column = 0)
		new_date = DateEntry(new_edit, textvariable = date_text, width = 30, bd = 3)
		new_date.grid(row = 9, column = 1)

		Button(new_edit, text = "Save Changes", cursor = "hand2", command = lambda:edit_record(new_order.get(),order_text,new_name.get(),name_text,new_amount.get(),amount_text,new_mode.get(),mode_text,new_date.get(),date_text)).grid(row = 10, column = 1)


		new_edit.mainloop()

	def edit_record(new_order,order_text,new_name,name_text,new_amount,amount_text,new_mode,mode_text,new_date,date_text):
			query = "UPDATE rev SET orderr = ?,  name = ?,  amount = ?,  mode = ?,  datee = ? WHERE  orderr = ? AND  name = ? AND amount = ? AND mode = ? AND datee = ?"
			parameters = (new_order,new_name,new_amount,new_mode,new_date,order_text,name_text,amount_text,mode_text,date_text)
			run_query(query,parameters)
			display["text"] = "Record {} has been changed to {}".format(order_text,new_order)


			view_record()


	def helpp():
		messagebox.showinfo("Hey!!!","Look at my Junk")


	#--------------------------IMAGES-------------------------------#

	img = ImageTk.PhotoImage(Image.open("C:\\Icons\\profitloss1.png"))
	img_label = Label(rev, image = img, width = 600, height = 300)
	img_label.grid(row = 1, column = 1)

	#--------------------------FRAMES-------------------------------#

	frame = LabelFrame(rev, width = 50, bd = 3, bg = "#97e8e1", padx = 20, pady = 10)
	frame.grid(row = 1, column = 0, padx = 30, pady = 5)

	#--------------------------LABELS-------------------------------#

	topic_label = Label(rev,text = "Revenue Summary", font = "Georgia 30 bold underline", bg = "#c93073")
	topic_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky=W)

	order_label = Label(frame,text = "Order Number", font = "Georgia 11 bold", bg = "#97e8e1")
	order_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 5)

	cus_label = Label(frame,text = "Customer Name", font = "Georgia 11 bold", bg = "#97e8e1")
	cus_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 5)

	amo_label = Label(frame,text = "Amount", font = "Georgia 11 bold", bg = "#97e8e1")
	amo_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 5)

	mode_label = Label(frame,text = "Mode of Payment", font = "Georgia 11 bold", bg = "#97e8e1")
	mode_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 5)

	date_label = Label(frame,text = "Date Reconciled", font = "Georgia 11 bold", bg = "#97e8e1")
	date_label.grid(row = 5, column = 0, sticky = W, padx = 10, pady = 5)

	#--------------------------ENTRIES-------------------------------#

	order_text = StringVar()
	order_entry = Entry(frame, textvariable = order_text)
	order_entry.grid(row = 1, column = 1, sticky = W)

	name_text = StringVar()
	name_entry = Entry(frame, textvariable = name_text, width = 40, bd = 3)
	name_entry.grid(row = 2, column = 1, sticky = W)

	amount_text = StringVar()
	amount_entry = Entry(frame, textvariable = amount_text, width = 40, bd = 3)
	amount_entry.grid(row = 3, column = 1, sticky = W)

	mode_text = StringVar()
	mode_entry = ttk.Combobox(frame, textvariable = mode_text, width = 40,cursor = "hand2")
	mode_entry.config(values = ("Cash","POS","Courier","Paystack","Bank Transfer","Store Credit"))
	mode_entry.grid(row = 4, column = 1, sticky = W)


	date_text = StringVar()
	date_entry = DateEntry(frame,  cursor = "hand2", textvariable = date_text, width = 15, bd = 3)
	date_entry.grid(row = 5, column = 1, sticky = W)


	#--------------------------BUTTONS-------------------------------#


	add_butt = Button(frame, text = "Add Record",  cursor = "hand2", font = "Georgia 11 bold", bg = "#97e8e1",command = add_record)
	add_butt.grid(row = 6, column = 0, pady = 20)

	display = Label(frame, text = "",font = "Garamond 15 bold italic", fg = "blue", bg = "#97e8e1")
	display.grid(row = 7, column = 1, padx = 15)



	#--------------------------TREEVIEW-------------------------------#

	tree = ttk.Treeview(rev, height = 18, columns = ["","","","",""])
	tree.grid(row = 8, column = 0, columnspan = 3, padx = 20, pady = 20)

	tree.heading("#0",text = "ID")
	tree.column("#0",width = 80)

	tree.heading("#1",text = "Order Number")
	tree.column("#1",width = 200)

	tree.heading("#2",text = "Customer Name")
	tree.column("#2",width = 200)

	tree.heading("#3",text = "Amount")
	tree.column("#3",width = 100)

	tree.heading("#4",text = "Mode of Payment")
	tree.column("#4",width = 150)

	tree.heading("#5",text = "Date")
	tree.column("#5",width = 150)

	style = ttk.Style()
	style.configure("Treeview.Heading",font = "Georgia 11 bold italic")

	#--------------------------SCROLLBAR-------------------------------#

	sb = Scrollbar(rev,command = tree.yview)
	sb.grid(row = 8, column = 2, rowspan = 4, sticky = NS, ipady = 2)

	#--------------------------MENUS AND SUBMENU-------------------------------#

	main_menu = Menu()
	submenu = Menu()
	view_menu = Menu()
	sort_menu = Menu()
	date_menu = Menu()
	rev_menu = Menu()

	main_menu.add_cascade(label = "File", menu = submenu)
	main_menu.add_cascade(label = "View", menu = view_menu)
	main_menu.add_cascade(label = "Sort", menu = sort_menu)
	main_menu.add_cascade(label = "Statistics")	
	main_menu.add_cascade(label = "Help",command = helpp)
	main_menu.add_cascade(label = "Exit",command = rev.destroy)

	submenu.add_command(label = "Add Record", command = add_record)
	submenu.add_command(label = "Edit Record",command = edit_box)
	submenu.add_command(label = "Delete Record", command = delete_record)
	submenu.add_separator()
	submenu.add_command(label = "Help",command = helpp)
	submenu.add_command(label = "Exit",command = rev.destroy)

	view_menu.add_command(label = "All Transactions", command = view_record)
	view_menu.add_command(label = "All POS Transactions", command = view_record_pos)
	view_menu.add_command(label = "All Cash Transactions", command = view_record_cash)
	view_menu.add_command(label = "All Bank Transfer Transactions", command = view_record_bt)
	view_menu.add_command(label = "All Paystack Transactions", command = view_record_paystack)
	view_menu.add_command(label = "All Courier Transactions", command = view_record_courier)
	view_menu.add_command(label = "All Store Credit Transactions", command = view_record_store)

	sort_menu.add_cascade(label = "Date by", menu = date_menu)
	date_menu.add_command(label = "Newest", command = view_record_datenew)
	date_menu.add_command(label = "Oldest", command = view_record_dateold)

	sort_menu.add_cascade(label = "Revenue by", menu = rev_menu)
	rev_menu.add_command(label = "Highest", command = view_record_revhigh)
	rev_menu.add_command(label = "Lowest", command = view_record_revlow)








	rev.configure(menu = main_menu)

	#--------------------------TIME AND DATE-------------------------------#

	def tick():
		d = datetime.datetime.now()
		mydate = "{:%B - %d - %Y}".format(d)
		mytime = time.strftime("%I : %M : %S%p")
		lblInfo.config(text = mytime +"\t" + mydate)
		lblInfo.after(200,tick)
	lblInfo = Label(rev, font = "Georgia 11 bold italic", fg = "red", bg = "#c3f705")
	lblInfo.grid(row = 0, column = 1)
	tick()

	view_record()


	rev.mainloop()
	

#-------------------EXPENSES DETAILS-------------------------


def expenses():
	exp = Toplevel(root)
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
		query = "SELECT * FROM exp"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])


	def validation():
		return len(exp_entry.get())!=0,len(amo_entry.get())!=0,len(date_entry.get())!=0,len(debit_entry.get())!=0

	def add_record():
		if validation():
			query = "INSERT INTO exp VALUES(NULL,?,?,?,?)"
			parameters = (exp_entry.get(),amo_entry.get(),date_entry.get(),debit_entry.get())
			run_query(query,parameters)
			display["text"] = "Record {} has been added".format(exp_entry.get())

			exp_entry.delete(0,END)
			amo_entry.delete(0,END)
			date_entry.delete(0,END)
			debit_entry.delete(0,END)

		else:
			display["text"] = "Please fill all entries"
		view_record()


	def delete_record():
		try:
			tree.item(tree.selection())["values"][1]
		except IndexError as e:
			display["text"] = "Please select a record to delete"
		query = "DELETE FROM exp WHERE ID=?"
		number = tree.item(tree.selection())["text"]
		run_query(query,(number,))
		display["text"] = "Record {} has been deleted".format(number)
		view_record()


	def edit_box():
		try:
			tree.item(tree.selection())["values"][0]
		except IndexError as e:
			display["text"] = "Please select a record to edit"
		exp_text = tree.item(tree.selection())["values"][0]
		amo_text = tree.item(tree.selection())["values"][1]
		date_text = tree.item(tree.selection())["values"][2]
		debit_text = tree.item(tree.selection())["values"][3]

		new_edit = Toplevel()
		new_edit.title("Edit Record")

		Label(new_edit, text = "Old(Expense/Charge)").grid(row = 0, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = exp_text), state = "readonly").grid(row = 0, column = 1)
		Label(new_edit, text = "New(Expense/Charge)").grid(row = 1, column = 0)
		new_exp = Entry(new_edit, width = 30, bd = 3)
		new_exp.grid(row = 1, column = 1)

		Label(new_edit, text = "Old(Amount)").grid(row = 2, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = amo_text), state = "readonly").grid(row = 2, column = 1)
		Label(new_edit, text = "New(Amount)").grid(row = 3, column = 0)
		new_amo = Entry(new_edit, width = 30, bd = 3)
		new_amo.grid(row = 3, column = 1)

		Label(new_edit, text = "Old(Date Charged)").grid(row = 4, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = date_text), state = "readonly").grid(row = 4, column = 1)
		Label(new_edit, text = "New(Date Charged)").grid(row = 5, column = 0)
		new_date = DateEntry(new_edit, width = 30)
		new_date.grid(row = 5, column = 1)

		Label(new_edit, text = "Old(Debited from)").grid(row = 6, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = debit_text), state = "readonly").grid(row = 6, column = 1)
		Label(new_edit, text = "New(Debited from)").grid(row = 7, column = 0)
		new_debit = Entry(new_edit, width = 30, bd = 3)
		new_debit.grid(row = 7, column = 1)


		Button(new_edit, text = "Save Changes", cursor = "hand2", command = lambda:edit_record(new_exp.get(),exp_text,new_amo.get(),amo_text,new_date.get(),date_text,new_debit.get(),debit_text)).grid(row = 8, column = 1)


		new_edit.mainloop()

	def edit_record(new_exp,exp_text,new_amo,amo_text,new_date,date_text,new_debit,debit_text):
			query = "UPDATE exp SET expense = ?,  amount = ?,  datee = ?,  debit = ? WHERE  expense = ? AND  amount = ? AND datee = ? AND debit = ?"
			parameters = (new_exp,new_amo,new_date,new_debit,exp_text,amo_text,date_text,debit_text)
			run_query(query,parameters)
			display["text"] = "Record {} has been changed to {}".format(exp_text,new_exp)
			view_record()


	def helpp():
		messagebox.showinfo("Hey!!!","Look at my Junk")



	#--------------------------IMAGES-------------------------------#


	img = ImageTk.PhotoImage(Image.open("C:\\Icons\\expenses.png"))
	img_label = Label(exp, image = img, width = 400, height = 270)
	img_label.grid(row = 1, column = 1)

	#--------------------------FRAMES-------------------------------#

	frame = LabelFrame(exp, width = 50, bd = 3, bg = "#f7f6a8", padx = 20, pady = 20)
	frame.grid(row = 1, column = 0, padx = 30, pady = 10)

	#--------------------------LABELS-------------------------------#

	topic_label = Label(exp,text = "Detailed Expenses/Charges", font = "Georgia 30 bold underline", bg = "#c3f705")
	topic_label.grid(row = 0, column = 0, padx = 10, pady = 20, sticky=W)

	exp_label = Label(frame,text = "Expense/Charge", font = "Georgia 11 bold", bg = "#f7f6a8")
	exp_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 5)

	amo_label = Label(frame,text = "Amount", font = "Georgia 11 bold", bg = "#f7f6a8")
	amo_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 5)

	date_label = Label(frame,text = "Date Charged", font = "Georgia 11 bold", bg = "#f7f6a8")
	date_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 5)

	debit_label = Label(frame,text = "Debited from", font = "Georgia 11 bold", bg = "#f7f6a8")
	debit_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 5)

	#--------------------------ENTRIES-------------------------------#


	exp_text = StringVar()
	exp_entry = Entry(frame, textvariable = exp_text, width = 40, bd = 3)
	exp_entry.grid(row = 1, column = 1, sticky = W)

	amo_text = StringVar()
	amo_entry = Entry(frame, textvariable = amo_text, width = 40, bd = 3)
	amo_entry.grid(row = 2, column = 1, sticky = W)

	date_text = StringVar()
	date_entry = DateEntry(frame, textvariable = date_text, width = 20, bd = 3)
	date_entry.grid(row = 3, column = 1, sticky = W)

	debit_text = StringVar()
	debit_entry = Entry(frame, textvariable = debit_text, width = 40, bd = 3)
	debit_entry.grid(row = 4, column = 1, sticky = W)


	#--------------------------BUTTONS-------------------------------#

	add_butt = Button(frame, text = "Add Expense",  cursor = "hand2", font = "Georgia 11 bold", bg = "#f7f6a8",command = add_record)
	add_butt.grid(row = 5, column = 1, pady = 20)

	display = Label(frame, text = "",font = "Garamond 15 bold italic", fg = "blue",bg = "#f7f6a8")
	display.grid(row = 6, column = 1, padx = 15)



	#--------------------------TREEVIEW-------------------------------#

	tree = ttk.Treeview(exp, height = 17, columns = ["","","",""])
	tree.grid(row = 7, column = 0, columnspan = 3, padx = 20)

	tree.heading("#0",text = "ID")
	tree.column("#0",width = 80)

	tree.heading("#1",text = "Expense/Charge")
	tree.column("#1",width = 200)

	tree.heading("#2",text = "Amount Charged")
	tree.column("#2",width = 200)

	tree.heading("#3",text = "Date Charged")
	tree.column("#3",width = 200)

	tree.heading("#4",text = "Debited From")
	tree.column("#4",width = 150)


	style = ttk.Style()
	style.configure("Treeview.Heading",font = "Georgia 11 bold italic")

	#--------------------------SCROLLBAR-------------------------------#

	sb = Scrollbar(exp,command = tree.yview)
	sb.grid(row = 7, column = 2, sticky = NS, ipady = 3)

	#--------------------------MENUS AND SUBMENU-------------------------------#

	main_menu = Menu()
	submenu = Menu()

	main_menu.add_cascade(label = "File", menu = submenu)
	main_menu.add_cascade(label = "Add", command = add_record)
	main_menu.add_cascade(label = "Edit",command = edit_box)
	main_menu.add_cascade(label = "Delete", command = delete_record)	
	main_menu.add_cascade(label = "Help",command = helpp)
	main_menu.add_cascade(label = "Exit",command = exp.destroy)

	submenu.add_command(label = "Add Record", command = add_record)
	submenu.add_command(label = "Edit Record",command = edit_box)
	submenu.add_command(label = "Delete Record", command = delete_record)
	submenu.add_separator()
	submenu.add_command(label = "Help",command = helpp)
	submenu.add_command(label = "Exit",command = exp.destroy)

	exp.configure(menu = main_menu)

	#--------------------------TIME AND DATE-------------------------------#

	def tick():
		d = datetime.datetime.now()
		mydate = "{:%B - %d - %Y}".format(d)
		mytime = time.strftime("%I : %M : %S%p")
		lblInfo.config(text = mytime +"\t" + mydate)
		lblInfo.after(200,tick)
	lblInfo = Label(exp, font = "Georgia 11 bold italic", fg = "red", bg = "#c3f705")
	lblInfo.grid(row = 0, column = 1)
	tick()
	view_record()
	exp.mainloop()

#-------------------MERCHANTS DETAILS-------------------------


def merchant():
	mer = Toplevel(root)
	mer.title("Merchants")
	mer.geometry("1350x850")
	mer.configure(background = "#c3f705")



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
	

#-------------------INVENTORY DETAILS-------------------------


def inventory():
	inv = Toplevel(root)
	inv.geometry("1350x850")
	inv.title("Inventory")
	inv.configure(background = "#ed9972")



	#--------------FUNCTIONS-------------------------#

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
		query="SELECT * FROM inventory"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	#-------------------View Menu-----------------------------#
	
	def view_record_bb():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory WHERE inventory = 'Shoe bag(Big)'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_sb():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory WHERE inventory = 'Shoe bag(Small)'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_bbo():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory WHERE inventory = 'Shoe box(Big)'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_sbo():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory WHERE inventory = 'Shoe box(Small)'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_print():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory WHERE inventory = 'Printer Inks'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_a4():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory WHERE inventory = 'A4 Paper'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_pol():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory WHERE inventory = 'Shoe Polish'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_cell():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory WHERE inventory = 'Cellotape'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])




	#-------------------Sort Menu-----------------------------#

	def view_record_date():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory ORDER BY datee"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])
		display["text"] = "View Inventory(Newest)"

	def view_record_date1():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory ORDER BY datee DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])
		display["text"] = "View Inventory(Oldest)"

	def view_record_qtybig():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory ORDER BY qty DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_qtysmall():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory ORDER BY qty"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_qty1big():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory ORDER BY qty1 DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_qty1small():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory ORDER BY qty1"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_qty2big():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory ORDER BY qty2 DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])

	def view_record_qty2small():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query="SELECT * FROM inventory ORDER BY qty2"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text=data[0],values=data[1:])


	def validation():
		return len(inv_entry.get())!=0, len(date_entry.get())!=0, len(qty_entry.get())!=0, len(qty1_entry.get())!=0, len(qty2_entry.get())!=0


	def add_record():
		if validation():
			query = "INSERT INTO inventory VALUES(NULL,?,?,?,?,?)"
			parameters = (inv_entry.get(),date_entry.get(),qty_entry.get(),qty1_entry.get(),qty2_entry.get())
			run_query(query,parameters)
			display["text"] = "Record {} has been added".format(inv_entry.get())

			inv_entry.delete(0,END)
			date_entry.delete(0,END)
			qty_entry.delete(0,END)
			qty1_entry.delete(0,END)

		else:
			display["text"] = "Please fill all fields"
		view_record()

	def delete_record():
		tree.item(tree.selection())["values"][1]
		query = "DELETE FROM inventory WHERE ID=?"
		number = tree.item(tree.selection())["text"]
		run_query(query,(number,))
		display["text"] = "Record {} has been deleted".format(number)
		view_record()


	def edit_box():
		try:
			tree.item(tree.selection())["values"][0]
		except IndexError as e:
			display["text"] = "Please select a record to edit"

		inv_text = tree.item(tree.selection())["values"][0]
		date_text = tree.item(tree.selection())["values"][1]
		qty_text = tree.item(tree.selection())["values"][2]
		qty1_text = tree.item(tree.selection())["values"][3]
		qty2_text = tree.item(tree.selection())["values"][4]


		new_edit = Toplevel()
		new_edit.title("Edit New Record")

		Label(new_edit, text = "Old(Inventory)").grid(row = 0, column = 0)
		Entry(new_edit,textvariable=StringVar(new_edit,value=inv_text),state= "readonly").grid(row = 0, column = 1)
		Label(new_edit, text = "New(Inventory)").grid(row = 1, column = 0)
		new_inv = ttk.Combobox(new_edit,width = 30)
		new_inv.configure(values = ("Shoes","Shoe bag(Small)","Shoe bag(Big)","Shoes box(Small)","Shoe box(Big)","Printer Inks","A4 Paper","Shoe Polish","Cellotape","Shoe Bags","Mouse","Computer assessories","Stain Remover"))
		new_inv.grid(row = 1, column=1)

		Label(new_edit, text = "Old(Date)").grid(row = 2, column = 0)
		Entry(new_edit,textvariable=StringVar(new_edit,value=date_text),state= "readonly").grid(row = 2, column = 1)
		Label(new_edit, text = "New(Date)").grid(row = 3, column = 0)
		new_date = DateEntry(new_edit,width = 30)
		new_date.grid(row = 3, column = 1)

		Label(new_edit, text = "Old(Quantity Purchased").grid(row = 4, column = 0)
		Entry(new_edit,textvariable=StringVar(new_edit,value=qty_text),state= "readonly").grid(row = 4, column = 1)
		Label(new_edit, text = "New(Quantity Purchased)").grid(row = 5, column = 0)
		new_qty = Spinbox(new_edit,from_ = 0, to = 1000, width = 30, bd = 3)
		new_qty.grid(row = 5, column = 1)

		Label(new_edit, text = "Old(Quantity Remaining)").grid(row = 6, column = 0)
		Entry(new_edit,textvariable=StringVar(new_edit,value=qty1_text),state= "readonly").grid(row = 6, column = 1)
		Label(new_edit, text = "New(Quantity Remaining)").grid(row = 7, column = 0)
		new_qty1 = Spinbox(new_edit,from_ = 0, to = 1000,width = 30, bd = 3)
		new_qty1.grid(row = 7, column = 1)

		Label(new_edit, text = "Old(Total Quantity Remaining)").grid(row = 8, column = 0)
		Entry(new_edit,textvariable=StringVar(new_edit,value=qty2_text),state= "readonly").grid(row = 8, column = 1)
		Label(new_edit, text = "New(Total Quantity Remaining)").grid(row = 9, column = 0)
		new_qty2 = Spinbox(new_edit,from_ = 0, to = 1000,width = 30, bd = 3)
		new_qty2.grid(row = 9, column = 1)


		sc = Button(new_edit,text = "Save Changes", cursor= "hand2", command = lambda:edit_record(new_inv.get(),inv_text,new_date.get(),date_text,new_qty.get(),qty_text,new_qty1.get(),qty1_text,new_qty2.get(),qty2_text))
		sc.grid(row = 10, column = 1)
		new_edit.mainloop()

	def edit_record(new_inv,inv_text,new_date,date_text, new_qty,qty_text, new_qty1, qty1_text,new_qty2,qty2_text):
		query = "UPDATE inventory SET inventory=?,datee=?,qty=?,qty1=?,qty2=? WHERE inventory=? AND datee=? AND qty=? AND qty1=? AND qty2=?"
		parameters=(new_inv,new_date,new_qty,new_qty1,new_qty2, inv_text,date_text,qty_text,qty1_text,qty2_text)
		run_query(query,parameters)
		display["text"] = "Record {} has been updated to {}".format(inv_text,new_inv)
		view_record()

	def helpp():
		messagebox.showinfo("Help","This is Dean Winchester and I need your help")


	#-------------------IMAGES-------------------------#

	img = ImageTk.PhotoImage(Image.open("C:\\Icons\\inv1.png"))
	img_label = Label(inv, image = img, width = 590, height = 350)
	img_label.grid(row = 1, column = 1)

	#-------------------FRAMES-------------------------#

	frame = LabelFrame(inv, width = 50, bg = "#84db8b", pady = 10)
	frame.grid(row = 1, column = 0, padx = 50, sticky=W)

	#-------------------LABELS-------------------------#

	inv_label = Label(inv, text = "Inventory Management", font = "Rockwell 25 bold italic underline", bg = "#ed9972")
	inv_label.grid(row = 0, column = 0, pady = 10)

	label_inv = Label(frame, text = "Inventory", font = "Rockwell 15 bold italic", bg = "#84db8b")
	label_inv.grid(row = 1, column = 0, padx = 10, pady = 10)

	date_inv = Label(frame, text = "Date Purchased", font = "Rockwell 15 bold italic", bg = "#84db8b")
	date_inv.grid(row = 2, column = 0, padx = 30, pady = 10)

	qty_inv = Label(frame, text = "Quantity Purchased", font = "Rockwell 15 bold italic", bg = "#84db8b")
	qty_inv.grid(row = 3, column = 0, padx = 10, pady = 10)

	qty1_inv = Label(frame, text = "Quantity Left", font = "Rockwell 15 bold italic", bg = "#84db8b")
	qty1_inv.grid(row = 4, column = 0, padx = 10, pady = 10)

	qty2_inv = Label(frame, text = "Total Quantity Left", font = "Rockwell 15 bold italic", bg = "#84db8b")
	qty2_inv.grid(row = 5, column = 0, padx = 10, pady = 10)

	#----------------------ENTRIES--------------------------------------#

	inv_text = StringVar()
	inv_entry = ttk.Combobox(frame, textvariable = inv_text)
	inv_entry.config(values = ("Shoes","Shoe bag(Small)","Shoe bag(Big)","Shoe box(Small)","Shoe box(Big)","Printer Inks","A4 Paper","Shoe Polish","Cellotape","Shoe Bags","Mouse","Computer assessories","Stain Remover"))
	inv_entry.grid(row = 1, column = 1, padx = 10)

	date_text = StringVar()
	date_entry = DateEntry(frame, textvariable = date_text, width = 20, bd = 3)
	date_entry.grid(row = 2, column = 1, padx = 10, sticky = W)

	qty_text = StringVar()
	qty_entry = Spinbox(frame, textvariable = qty_text, from_ = 0, to = 1000, cursor = "hand2", width = 23, bd = 3)
	qty_entry.grid(row = 3, column = 1, padx = 10, sticky = W)

	qty1_text = StringVar()
	qty1_entry = Spinbox(frame, textvariable = qty1_text, from_ = 0, to = 1000,  cursor = "hand2", width = 23, bd = 3)
	qty1_entry.grid(row = 4, column = 1, padx = 10, sticky = W)

	qty2_text = StringVar()
	qty2_entry = Spinbox(frame, textvariable = qty2_text, from_ = 0, to = 1000,  cursor = "hand2", width = 23, bd = 3)
	qty2_entry.grid(row = 5, column = 1, padx = 10, sticky = W)

	add_butt = Button(frame, text = "Add Inventory",  cursor = "hand2", font = "Rockwell 15 bold italic", bg = "#84db8b",command = add_record)
	add_butt.grid(row = 6, column = 0, padx = 10, pady = 5)

	display = Label(frame, text = "",font = "Garamond 15 bold italic", fg = "blue",bg = "#84db8b")
	display.grid(row = 7, column = 1, padx = 15)


	#-------------------------TREEVIEW------------------------------------#

	tree = ttk.Treeview(inv, height = 15, columns = ["","","","",""])
	tree.grid(row =6, column = 0, columnspan = 2,padx = 10,pady = 10)
	style = ttk.Style()
	style.configure("Treeview.Heading", font = "Rockwell 12 bold italic")
	tree.heading("#0", text = "ID")
	tree.column("#0", width = 50)

	tree.heading("#1", text = "Inventory")
	tree.column("#1", width = 250)

	tree.heading("#2", text = "Date Purchased")
	tree.column("#2", width = 200)

	tree.heading("#3", text = "Quantity Purchased")
	tree.column("#3", width = 200)

	tree.heading("#4", text = "Quantity Remaining")
	tree.column("#4", width = 200)

	tree.heading("#5", text = "Total Quantity Left")
	tree.column("#5", width = 200)

	view_record()


	#----------------------SCROLLBAR-------------------------#

	sb = ttk.Scrollbar(inv, command = tree.yview)
	sb.grid(row = 6, column = 2, sticky = NS,ipady = 3)
	tree.config(yscrollcommand=sb.set)



	#----------------MENUS AND SUBMENUS----------------------#
	
	main_menu = Menu()
	submenu=Menu()
	sort_menu = Menu()
	sort_date = Menu()
	sort_qty = Menu()
	sort_qty1 = Menu()
	sort_qty2 = Menu()
	view_menu = Menu()


	main_menu.add_cascade(label = "File",menu= submenu)
	main_menu.add_cascade(label = "View", menu = view_menu)
	main_menu.add_cascade(label = "Sort", command = edit_box,menu = sort_menu)
	main_menu.add_cascade(label = "Delete", command = delete_record)
	main_menu.add_cascade(label = "Help", command = helpp)
	main_menu.add_cascade(label = "Exit", command = inv.destroy)

	submenu.add_command(label = "Add Record", command = add_record)
	submenu.add_command(label = "Edit Record", command = edit_box)
	submenu.add_command(label = "Delete Record", command = delete_record)
	submenu.add_separator()
	submenu.add_command(label = "Help", command = helpp)
	submenu.add_command(label = "Exit", command = inv.destroy)

	sort_menu.add_cascade(label = "By Date",menu = sort_date)
	sort_date.add_command(label = "Newest", command = view_record_date)
	sort_date.add_command(label = "Oldest", command = view_record_date1)

	sort_menu.add_cascade(label = "By Quantity Purchased", menu = sort_qty)
	sort_qty.add_command(label = "Most", command = view_record_qtybig)
	sort_qty.add_command(label = "Least", command = view_record_qtysmall)


	sort_menu.add_cascade(label = "By Quantity Left", menu = sort_qty1)
	sort_qty1.add_command(label = "Most", command = view_record_qty1big)
	sort_qty1.add_command(label = "Least", command = view_record_qty1small)

	sort_menu.add_cascade(label = "By Total Quantity Left", menu = sort_qty2)
	sort_qty2.add_command(label = "Most", command = view_record_qty2big)
	sort_qty2.add_command(label = "Least", command = view_record_qty2small)

	view_menu.add_command(label = "All Inventory", command = view_record)
	view_menu.add_command(label = "Big Bags", command= view_record_bb)
	view_menu.add_command(label = "Small Bags", command= view_record_sb)
	view_menu.add_command(label = "Big Boxes", command= view_record_bbo)
	view_menu.add_command(label = "Small Boxes", command= view_record_sbo)
	view_menu.add_command(label = "Printer Inks", command= view_record_print)
	view_menu.add_command(label = "A4 Paper", command= view_record_a4)
	view_menu.add_command(label = "Shoe Polish", command= view_record_pol)
	view_menu.add_command(label = "Cellotapes", command= view_record_cell)


	inv.config(menu = main_menu)


	#-----------------TIME AND DATE------------------#

	def tick():
		d = datetime.datetime.now()
		mytime = time.strftime("%I : %M : %S%p")
		mydate = "{:%B - %d - %Y}".format(d)
		lblInfo.config(text = mytime + "\t" + mydate)
		lblInfo.after(200,tick)

	lblInfo = Label(inv, font = "Rockwell 12 bold italic", bg = "#ed9972", fg = "blue")
	lblInfo.grid(row = 0, column = 1, sticky = N, pady = 10)
	tick()

	inv.mainloop()

#-------------------TRANSACTION DETAILS-------------------------

def trans():
	trans = Toplevel(root)
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

	def view_record_cus():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT orderr,name,address,location FROM trans"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:6])

	def view_record_lag():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE location = 'Lagos'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Lagos Orders"

	def view_record_notlag():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE location != 'Lagos'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Out of State Orders"

	def view_record_full():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE status = 'Fully Delivered'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Fully Delivered Orders"

	def view_record_partial():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE status = 'Partially Delivered'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Partially Delivered Orders"

	def view_record_cancel():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE status = 'Cancelled'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Cancelled Orders"

	def view_record_reject():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE status = 'Rejected'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Rejected Orders"

	def view_record_cash():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE pay = 'Cash'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Cash Orders"

	def view_record_pos():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE pay = 'POS'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View POS Orders"

	def view_record_paystack():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE pay = 'Paystack'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Paystack Orders"

	def view_record_courier():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE pay = 'Courier'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Courier-Paid Orders"

	def view_record_bt():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans WHERE pay = 'Bank Transfer'"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Bank Transfer Orders"

	def view_record_newest():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY datee;"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Orders(Newest to Oldest)"

	def view_record_oldest():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY datee DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Orders(Oldest to Newest)"


	def view_record_amo():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY amo DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Amounts(Biggest to Smallest)"

	def view_record_bigsize():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY size DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Shoe sizes(Biggest to Smallest)"

	def view_record_smallsize():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY size"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Shoe sizes(Smallest to Biggest)"


	def view_record_shoessold():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY nst DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Number of Shoes Sold(Biggest to Smallest)"


	def view_record_sortord():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY nso DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Number of Shoes Ordered(Biggest to Smallest)"

	def view_record_sortord1():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY nso"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Number of Shoes Ordered(Smallest to Biggest)"

	def view_record_sorttaken():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY nst DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Number of Shoes Taken(Biggest to Smallest)"

	def view_record_sorttaken1():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY nst"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Number of Shoes Taken(Smallest to Biggest)"

	def view_record_sortrej():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY nsr DESC"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Number of Shoes Rejected(Biggest to Smallest)"

	def view_record_sortrej1():
		record = tree.get_children()
		for element in record:
			tree.delete(element)
		query = "SELECT * FROM trans ORDER BY nsr"
		connect = run_query(query)
		for data in connect:
			tree.insert("",10000,text = data[0], values = data[1:])
			display["text"] = "View Sorted Number of Shoes Rejected(Smallest to Biggest)"




	def validation():
		return len(order_entry.get())!=0, len(name_entry.get())!=0, len(add_entry.get())!=0,len(loc_entry.get())!=0, len(email_entry.get())!=0, len(nso_entry.get())!=0, len(size_entry.get())!=0, len(nst_entry.get())!=0, len(nsr_entry.get())!=0, len(amo_entry.get())!=0, len(stat_entry.get())!=0, len(pay_entry.get())!=0, len(date_entry.get())!=0

	def add_record():
		if validation():
			query = "INSERT INTO trans VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
			parameters = (order_entry.get(),name_entry.get(),add_entry.get(),loc_entry.get(),phone_entry.get(),email_entry.get(),nso_entry.get(),size_entry.get(),nst_entry.get(),nsr_entry.get(),amo_entry.get(),stat_text.get(),pay_text.get(),date_entry.get())

			run_query(query,parameters)
			display["text"] = "Record {} has been added".format(name_entry.get())

			order_entry.delete(0,END)
			name_entry.delete(0,END)
			add_entry.delete(0,END)
			loc_entry.delete(0,END)
			phone_entry.delete(0,END)
			email_entry.delete(0,END)
			nso_entry.delete(0,END)
			size_entry.delete(0,END)
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
		loc_text = tree.item(tree.selection())["values"][3]
		phone_text = tree.item(tree.selection())["values"][4]
		email_text = tree.item(tree.selection())["values"][5]
		nso_text = tree.item(tree.selection())["values"][6]
		size_text = tree.item(tree.selection())["values"][7]
		nst_text = tree.item(tree.selection())["values"][8]
		nsr_text = tree.item(tree.selection())["values"][9]
		amo_text = tree.item(tree.selection())["values"][10]
		stat_text = tree.item(tree.selection())["values"][11]
		pay_text = tree.item(tree.selection())["values"][12]
		date_text = tree.item(tree.selection())["values"][13]


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

		Label(new_edit,text = "Old(Customer Location)").grid(row = 6, column = 0, padx = 10  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = loc_text),state = "readonly").grid(row=6, column = 1, padx = 10  )
		Label(new_edit,text = "New(Customer Location").grid(row = 7, column = 0, padx = 10  )
		new_loc = ttk.Combobox(new_edit,textvariable = loc_text, width = 30)
		new_loc.configure(values = ("Lagos","FCT","Rivers","Abia","Adamawa","Akwa-Ibom","Anambra","Bauchi","Bayelsa","Benue","Borno","Cross River","Delta","Ebonyi","Edo","Ekiti","Enugu","Gombe","Imo","Jigawa","Kaduna","Kano","Katsina","Kebbi","Kogi","Kwara","Nassarawa","Niger","Ogun","Osun","Oyo","Plateau","Sokoto","Taraba","Yobe","Ondo"))
		new_loc.grid(row = 7, column =1, padx = 10  )


		Label(new_edit,text = "Old(Phone Number)").grid(row = 8, column = 0, padx = 10  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = phone_text),state = "readonly").grid(row=8, column = 1, padx = 10  )
		Label(new_edit,text = "New(Phone Number").grid(row = 9, column = 0, padx = 10)
		new_phone = Entry(new_edit,bd = 3, width = 30)
		new_phone.grid(row = 9, column =1, padx = 10  )

		Label(new_edit,text = "Old(Email Address)").grid(row = 10, column = 0)
		Entry(new_edit, textvariable = StringVar(new_edit,value = email_text),state = "readonly").grid(row=10, column = 1, padx = 10)
		Label(new_edit,text = "New(Email Address").grid(row = 11, column = 0, padx = 10)
		new_email = Entry(new_edit,bd = 3, width = 30)
		new_email.grid(row = 11, column =1, padx = 10  )

		Label(new_edit,text = "Old(Shoes Ordered)").grid(row = 12, column = 0, padx = 10)
		Entry(new_edit, textvariable = StringVar(new_edit,value = nso_text),state = "readonly").grid(row=12, column = 1, padx = 10)
		Label(new_edit,text = "New(Shoes Ordered").grid(row = 13, column = 0, padx = 10)
		new_nso = Spinbox(new_edit,from_=0, to = 100, bd = 3, width = 30)
		new_nso.grid(row = 13, column =1, padx = 10,   )

		Label(new_edit,text = "Old(Shoe size)").grid(row = 14, column = 0, padx = 10  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = size_text),state = "readonly").grid(row=14, column = 1, padx = 10)
		Label(new_edit,text = "New(Shoe size").grid(row = 15, column = 0, padx = 10)
		new_size = Entry(new_edit, bd = 3, width = 30)
		new_size.grid(row = 15, column =1, padx = 10)

		Label(new_edit,text = "Old(Shoes Taken)").grid(row = 16, column = 0, padx = 10)
		Entry(new_edit, textvariable = StringVar(new_edit,value = nst_text),state = "readonly").grid(row=16, column = 1, padx = 10)
		Label(new_edit,text = "New(Shoes Taken").grid(row = 17, column = 0, padx = 10)
		new_nst = Spinbox(new_edit,from_=0, to = 100,bd = 3, width = 30)
		new_nst.grid(row = 17, column =1, padx = 10,  )

		Label(new_edit,text = "Old(Shoes Rejected)").grid(row = 18, column = 0, padx = 10)
		Entry(new_edit, textvariable = StringVar(new_edit,value = nsr_text),state = "readonly").grid(row=18, column = 1, padx = 10)
		Label(new_edit,text = "New(Shoes Rejected").grid(row = 19, column = 0, padx = 10)
		new_nsr = Spinbox(new_edit,from_=0, to = 100,bd = 3, width = 30)
		new_nsr.grid(row = 19, column =1, padx = 10)

		Label(new_edit,text = "Old(Amount Paid)").grid(row = 20, column = 0, padx = 10)
		Entry(new_edit, textvariable = StringVar(new_edit,value = amo_text),state = "readonly").grid(row=20, column = 1, padx = 10)
		Label(new_edit,text = "New(Amount Paid").grid(row = 21, column = 0, padx = 10)
		new_amount = Entry(new_edit,bd = 3, width = 30)
		new_amount.grid(row = 21, column =1, padx = 10)

		Label(new_edit,text = "Old(Status of Delivery)").grid(row = 22, column = 0, padx = 10)
		Entry(new_edit, textvariable = StringVar(new_edit,value = stat_text),state = "readonly").grid(row=22, column = 1, padx = 10,   )
		Label(new_edit,text = "New(Status of Delivery").grid(row = 23, column = 0, padx = 10  )
		new_status = ttk.Combobox(new_edit,textvariable = stat_text, width = 30)
		new_status.configure(values = ("Fully Delivered","Partially Delivered","Rejected","Cancelled","In Transit",))
		new_status.grid(row = 23, column =1, padx = 10)

		Label(new_edit,text = "Old(Payment Method)").grid(row = 24, column = 0, padx = 10,   )
		Entry(new_edit, textvariable = StringVar(new_edit,value = pay_text),state = "readonly").grid(row=24, column = 1, padx = 10  )
		Label(new_edit,text = "New(Payment Method").grid(row = 25, column = 0, padx = 10,   )
		new_pay = ttk.Combobox(new_edit,textvariable = pay_text, width = 30)
		new_pay.configure(values = ("Cash","POS","Paystack","Bank Transfer","Courier","Store Credit"))		
		new_pay.grid(row = 25, column =1, padx = 10)

		Label(new_edit,text = "Old(Date)").grid(row = 26, column = 0, padx = 10  )
		Entry(new_edit, textvariable = StringVar(new_edit,value = date_text),state = "readonly").grid(row=26, column = 1, padx = 10  )
		Label(new_edit,text = "New(Date").grid(row = 27, column = 0, padx = 10  )
		new_date = DateEntry(new_edit,width = 30)
		new_date.grid(row = 27, column =1, padx = 10)

		Button(new_edit, text = "Save Changes", cursor = "hand2", command = lambda:edit_record(new_order.get(),order_text,new_name.get(),name_text,new_add.get(),add_text,new_loc.get(),loc_text,new_phone.get(),phone_text,new_email.get(),email_text,new_nso.get(),nso_text,new_size.get(),size_text,new_nst.get(),nst_text,new_nsr.get(),nsr_text,new_amount.get(),amo_text,new_status.get(),stat_text,new_pay.get(),pay_text,new_date.get(),date_text)).grid(row = 28, column = 1)

		new_edit.mainloop()


		#sqlite3.OperationalError: near "WHERE": syntax error
		#Please ensure there are no commas before the WHERE clause
	def edit_record(new_order,order_text,new_name,name_text,new_add,add_text,new_loc,loc_text, new_phone,phone_text,new_email,email_text,new_nso,nso_text,new_size,size_text,new_nst,nst_text,new_nsr,nsr_text,new_amount,amo_text,new_status,stat_text,new_pay,pay_text,new_date,date_text):
		query = "UPDATE trans SET orderr = ?,  name = ?,  address = ?, location = ?, phone = ?,  email = ?,  nso = ?, size=?, nst = ?,  nsr = ?,  amo = ?,  status = ?,  pay = ?,  datee = ? WHERE orderr = ? AND name = ? AND address = ? AND location = ? AND phone = ? AND email = ? AND  nso = ? AND size = ? AND  nst = ? AND nsr = ? AND amo = ? AND status = ? AND pay = ? AND datee = ?"
		parameters = (new_order,new_name,new_add,new_loc,new_phone,new_email,new_nso,new_size,new_nst,new_nsr,new_amount,new_status,new_pay,new_date,order_text,name_text,add_text,loc_text,phone_text,email_text,nso_text,size_text,nst_text,nsr_text,amo_text,stat_text,pay_text,date_text)
		run_query(query,parameters)
		display["text"] = "Record {} has been updated to {}".format(new_name,name_text)			
		view_record()

	def helpp():
		messagebox.showinfo("Help!!!","This is Dean Winchester, and I need your help, Linwood Memorial Hospital")

					#LABELS 1

	top_label = Label(trans, text = "Transaction Details", font = "Garamond 30 bold italic underline", fg = "#4b3300", bg = "#e0ffff")
	top_label.grid(row = 0, column = 0)

	order_label = Label(frame, text = "Order Number", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	order_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)

	name_label = Label(frame, text = "Customer Name", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	name_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 10)

	add_label = Label(frame, text = "Customer Address", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	add_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 10)

	add_label = Label(frame, text = "Customer Location", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	add_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 10)

	phone_label = Label(frame, text = "Customer Phone number", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	phone_label.grid(row = 5, column = 0, sticky = W, padx = 10, pady = 10)

	email_label = Label(frame, text = "Customer Email address", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	email_label.grid(row = 6, column = 0, sticky = W, padx = 10, pady = 10)

	nso_label = Label(frame, text = "Number of Shoes Ordered", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	nso_label.grid(row = 7, column = 0, sticky = W, padx = 10, pady = 10)


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

	loc_text = StringVar()
	loc_entry = ttk.Combobox(frame, cursor = "hand2", textvariable = loc_text, width = 52)
	loc_entry.config(values = ("Lagos","FCT","Rivers","Abia","Adamawa","Akwa-Ibom","Anambra","Bauchi","Bayelsa","Benue","Borno","Cross River","Delta","Ebonyi","Edo","Ekiti","Enugu","Gombe","Imo","Jigawa","Kaduna","Kano","Katsina","Kebbi","Kogi","Kwara","Nassarawa","Niger","Ogun","Osun","Oyo","Plateau","Sokoto","Taraba","Yobe","Ondo"))
	loc_entry.grid(row = 4, column = 1, sticky = W)

	phone_text = StringVar()
	phone_entry = Entry(frame, textvariable = phone_text, width = 55, bd = 3)
	phone_entry.grid(row = 5, column = 1, sticky = W)

	email_text = StringVar()
	email_entry = Entry(frame, textvariable = email_text, width = 55, bd = 3)
	email_entry.grid(row = 6, column = 1, sticky = W)

	nso_text = StringVar()
	nso_entry = Spinbox(frame, textvariable = nso_text, cursor = "hand2", from_=0, to = 10000,width = 15, bd = 3)
	nso_entry.grid(row = 7, column = 1, sticky = W)


					#LABELS 2

	size_label = Label(frame, text = "Shoe Size", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	size_label.grid(row = 1, column = 2, sticky = W, padx = 121, pady = 10)

	nst_label = Label(frame, text = "Number of Shoes Taken", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	nst_label.grid(row = 2, column = 2, sticky = W, padx = 121, pady = 10)

	nsr_label = Label(frame, text = "Number of Shoes Rejected", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	nsr_label.grid(row = 3, column = 2, sticky = W, padx = 121, pady = 10)

	stat_label = Label(frame, text = "Status of Delivery ", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	stat_label.grid(row = 4, column = 2, sticky = W, padx = 121, pady = 10)

	amo_label = Label(frame, text = "Amount Paid", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	amo_label.grid(row = 5, column = 2, sticky = W, padx = 121, pady = 10)

	pay_label = Label(frame, text = "Payment Method", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	pay_label.grid(row = 6, column = 2, sticky = W, padx = 121, pady = 10)

	date_label = Label(frame, text = "Date", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
	date_label.grid(row = 7, column = 2, sticky = W, padx = 121, pady = 10)


				#ENTRY2

	size_text = StringVar()
	size_entry = Entry(frame, textvariable = size_text ,width = 15, bd = 3)
	size_entry.grid(row = 1, column = 3, sticky = W)

	nst_text = StringVar()
	nst_entry = Spinbox(frame, textvariable = nst_text, cursor = "hand2", from_=0, to = 10000,width = 15, bd = 3)
	nst_entry.grid(row = 2, column = 3, sticky = W)

	nsr_text = StringVar()
	nsr_entry = Spinbox(frame, textvariable = nsr_text,cursor = "hand2", from_=0, to = 10000,width = 15, bd = 3)
	nsr_entry.grid(row = 3, column = 3, sticky = W)

	amo_text = StringVar()
	amo_entry = Entry(frame, textvariable = amo_text, width = 15, bd = 3)
	amo_entry.grid(row = 5, column = 3, sticky = W)

	stat_text = StringVar()
	stat_entry = ttk.Combobox(frame, cursor = "hand2", textvariable = stat_text)
	stat_entry.config(values = ("Fully Delivered", "Partially Delivered","Rejected","Cancelled", "Rescheduled","In Transit"))
	stat_entry.grid(row = 4, column = 3, sticky = W)

	pay_text = StringVar()
	pay_entry = ttk.Combobox(frame, cursor = "hand2", textvariable = pay_text)
	pay_entry.config(values = ("Cash", "POS","Paystack","Bank Transfer", "Courier","Store Credit"))
	pay_entry.grid(row = 6, column = 3, sticky = W)

	date_text = StringVar()
	date_entry = DateEntry(frame, cursor = "hand2", textvariable = date_text, width = 15, bd = 3)
	date_entry.grid(row = 7, column = 3, sticky = W)

				#BUTTONS

	add_but = Button(frame, text = "Add Transaction",  cursor = "hand2", bd = 2, fg = "#ff00ad", bg = "#e0ffff", font = "Garamond 15 bold italic",command = add_record)
	add_but.grid(row = 8, column = 1, padx = 50, pady = (10,15))

	display = Label(frame, text = "",font = "Garamond 15 bold italic", fg = "blue")
	display.grid(row = 8, column = 2, padx = 15)

	#-----------------------TREEVIEW-------------------------------------#

	tree = ttk.Treeview(trans,height = 15, columns = ["","","","","","","","","","","","","","",])
	tree.grid(row=9, column = 0, columnspan = 2, padx = 25)

	style = ttk.Style()
	style.configure("Treeview.Heading", font = "Garamond 9 bold italic")

	tree.heading("#0",text = "ID")
	tree.column("#0", width = 50)

	tree.heading("#1",text = "Order #")
	tree.column("#1", width = 80)

	tree.heading("#2",text = "Name")
	tree.column("#2", width = 120)

	tree.heading("#3",text = "Address")
	tree.column("#3", width = 180)

	tree.heading("#4",text = "State")
	tree.column("#4", width = 60)

	tree.heading("#5",text = "Phone Number")
	tree.column("#5", width = 110)

	tree.heading("#6",text = "Email")
	tree.column("#6", width = 100)

	tree.heading("#7",text = "Shoes Ordered")
	tree.column("#7", width = 80)

	tree.heading("#8",text = "Size")
	tree.column("#8", width = 60)

	tree.heading("#9",text = "Shoes Taken")
	tree.column("#9", width = 80)

	tree.heading("#10",text = "Shoes Rejected")
	tree.column("#10", width = 80)

	tree.heading("#11",text = "Amount")
	tree.column("#11", width = 80)

	tree.heading("#12",text = "Status")
	tree.column("#12", width = 80)

	tree.heading("#13",text = "Payment Method")
	tree.column("#13", width = 100)

	tree.heading("#14",text = "Date")
	tree.column("#14", width = 60)
	view_record()


		#----------------------SCROLLBAR-------------------------#

	sb = ttk.Scrollbar(trans, command = tree.yview)
	sb.grid(row = 9, column = 2, sticky = NS,ipady = 3)
	tree.config(yscrollcommand=sb.set)





	#-------------------MENUS AND SUB MENUS--------------------------#

	main_menu = Menu()
	submenu = Menu()
	view_menu = Menu()
	sort_menu = Menu()
	transaction_menu = Menu()
	shoes_ordered_menu = Menu()
	shoes_taken_menu = Menu()
	shoes_rejected_menu = Menu()

	main_menu.add_cascade(label = "File",menu = submenu )
	main_menu.add_cascade(label = "View",menu = view_menu)
	main_menu.add_cascade(label = "Sort", menu = sort_menu)
	main_menu.add_cascade(label = "Statistics")
	main_menu.add_cascade(label = "Help",command = helpp)
	main_menu.add_cascade(label = "Exit",command = trans.destroy)

	submenu.add_command(label = "Add Record", command = add_record)
	submenu.add_command(label = "Edit Record",command = edit_box)
	submenu.add_command(label = "Delete Record", command = delete_record)
	submenu.add_separator()
	submenu.add_command(label = "Help",command = helpp)
	submenu.add_command(label = "Exit", command = trans.destroy)

	view_menu.add_command(label = "All Transactions", command = view_record)
	view_menu.add_command(label = "All Customers", command = view_record_cus)
	view_menu.add_command(label = "All Lagos Customers", command = view_record_lag)
	view_menu.add_command(label = "All Out-of-state Customers", command = view_record_notlag)
	view_menu.add_separator()
	view_menu.add_command(label = "Full Deliveries", command = view_record_full)
	view_menu.add_command(label = "Partial Deliveries", command = view_record_partial)
	view_menu.add_command(label = "Cancelled Orders", command = view_record_cancel)
	view_menu.add_command(label = "Rejected Orders", command = view_record_reject)

	view_menu.add_separator()
	view_menu.add_command(label = "Cash Orders", command = view_record_cash)
	view_menu.add_command(label = "POS Orders", command = view_record_pos)
	view_menu.add_command(label = "Paystack Orders", command = view_record_paystack)
	view_menu.add_command(label = "Bank Transfer Orders", command = view_record_bt)
	view_menu.add_command(label = "Courier-paid Orders", command = view_record_courier)

	sort_menu.add_cascade(label = "Order Transactions by", menu = transaction_menu)
	transaction_menu.add_command(label = "Newest", command = view_record_newest)
	transaction_menu.add_command(label = "Oldest", command = view_record_oldest)
	transaction_menu.add_command(label = "Amount Paid", command = view_record_amo)
	transaction_menu.add_command(label = "Shoe Size(Big)", command = view_record_bigsize)
	transaction_menu.add_command(label = "Shoe Size(Small)", command = view_record_smallsize)
	transaction_menu.add_command(label = "Number of shoes sold", command = view_record_shoessold)

	sort_menu.add_cascade(label = "Shoes Ordered", menu = shoes_ordered_menu)
	shoes_ordered_menu.add_command(label = "Highest",command = view_record_sortord)
	shoes_ordered_menu.add_command(label = "lowest",command = view_record_sortord1)

	sort_menu.add_cascade(label = "Shoes Taken", menu = shoes_taken_menu)
	shoes_taken_menu.add_command(label = "Highest",command = view_record_sorttaken)
	shoes_taken_menu.add_command(label = "lowest",command = view_record_sorttaken1)

	sort_menu.add_cascade(label = "Shoes Rejected", menu = shoes_rejected_menu)
	shoes_rejected_menu.add_command(label = "Highest",command = view_record_sortrej)
	shoes_rejected_menu.add_command(label = "lowest",command = view_record_sortrej1)


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



def overview():
	over = Toplevel(root)
	over.geometry("1250x1150+120+120")
	over.title("Heelz.com.ng Overview")
	over.configure(background = "#FF00FF")

			#LABELS
			
	over_label = Label(over, text = "Heels Overview", font = "Consolas 30 bold italic underline", bg = "#FF00FF", fg = "indigo")
	over_label.grid(row = 0, column = 0)

	brief_label = Label(over, text = "         Heels.com.ng is a premier female shoe megastore offering a wide selection of hand picked designer shoes.", font = "Garamond 15 bold", bg = "#FF00FF", fg = "indigo")
	brief_label.grid(row = 1, column = 0, padx = 10, pady = 20)

	loc_label = Label(over, text = "Location - 4A, Adewole Kuku Street, off Fola Osibo, Lekki Phase 1, Lagos, Nigeria", font = "Garamond 15 bold", bg = "#FF00FF", fg = "indigo")
	loc_label.grid(row = 2, column = 0, padx = 10, pady = 20)

	con_label = Label(over, text = "Contact details \n Mobile/Whatsapp - 08180000312 \n Email - support@heels.com.ng", font = "Garamond 15 bold", bg = "#FF00FF", fg = "indigo")
	con_label.grid(row = 3, column = 0, padx = 10, pady = 20)

	con_label = Label(over, text = "Social Media: \n Whatsapp: 08180000312\n Facebook: heelsng\nInstagram: @heelsloveng\n", font = "Garamond 15 bold", bg = "#FF00FF", fg = "indigo")
	con_label.grid(row = 4, column = 0, padx = 10, pady = 20)

	close_button = Button(over, text = "Close Window", width = 13, bg = "red", font = "Consolas 15 bold", command = over.destroy)
	close_button.grid(row = 6, column = 0)






def heels_window():
	global root
	root = Tk()
	root.geometry("1250x1150+120+120")
	root.title("Heelz.com.ng Dashboard")
	root.configure(background = "#FF00FF")

				#IMAGE

	img = ImageTk.PhotoImage(Image.open("C:\\Icons\\heelslogo3.png"))
	img_label = Label(root, image = img, height = 550)
	img_label.grid(row = 1, column = 1)


				#FRAMES

	frame = LabelFrame(root, width = 100, height = 80, bd = 4, relief = SUNKEN, bg = "#FF00FF", padx = 20, pady = 5)
	frame.grid(row = 1, column = 0, pady = 20, padx = 30)

	frame1 = LabelFrame(root, width = 100, height = 80, bd = 4, relief = SUNKEN, bg = "#FF00FF", padx = 20, pady = 5)
	frame1.grid(row = 1, column = 2, pady = 20, padx = 30)

				#LABELS

	title_label = Label(root, text = "Heels.com.ng Tool Kit", font = "papyrus 30 bold italic underline", bg = "#FF00FF", fg = "#8B0000")
	title_label.grid(row = 0, column = 1, pady = 15)

				#BUTTONS 1

	over_label = Button(frame, text = "Overview", width = 16,  cursor = "hand2",font = "Rockwell 20 bold italic", bg = "#663399", fg = "black", command = overview)
	over_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 20)

	tran_label = Button(frame, text = "Transaction Details",  cursor = "hand2",width = 16, font = "Rockwell 20 bold italic", bg = "#663399", fg = "black", command = trans)
	tran_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 20)

	inven_label = Button(frame, text = "Inventory", width = 16,  cursor = "hand2",font = "Rockwell 20 bold italic", bg = "#663399", fg = "black",command = inventory)
	inven_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 20)

	mer_label = Button(frame, text = "Merchant Details", width = 16, cursor = "hand2",font = "Rockwell 20 bold italic", bg = "#663399", fg = "black", command = merchant)
	mer_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 20)


				#BUTTONS 2
				
	exp_label = Button(frame1, text = "Expenses", width = 15, font = "Rockwell 20 bold italic", bg = "#663399", fg = "black", command = expenses)
	exp_label.grid(row = 1, column = 2, padx = 10, pady = 20, sticky = W)

	rev_label = Button(frame1, text = "Revenue", width = 15, font = "Rockwell 20 bold italic", bg = "#663399", fg = "black", command = revenue)
	rev_label.grid(row = 2, column = 2, sticky = W, padx = 10, pady = 20)

	prof_label = Button(frame1, text = "Profit/Loss", width = 15, font = "Rockwell 20 bold italic", bg = "#663399", fg = "black", command = profitloss)
	prof_label.grid(row = 3, column = 2, sticky = W, padx = 10, pady = 20)

	sales_label = Button(frame1, text = "Sales Report", width = 15, font = "Rockwell 20 bold italic", bg = "#663399", fg = "black", command = sales_report)
	sales_label.grid(row = 4, column = 2, sticky = W, padx = 10, pady = 20)

	close_window = Button(root, text = "Close Window", width = 15, height = 1, font = "Rockwell 13 bold italic", bg = "red",command = root.destroy)
	close_window.grid(row = 5, column = 1, pady = 10)



	root.mainloop()

heels_window()