from tkinter import *
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
import time
import sqlite3



def sales_report():
	sr = Tk()
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
	tree.column("#1",width = 200)

	tree.heading("#2",text = "Merchant Name")
	tree.column("#2",width = 200)

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
	








sales_report()