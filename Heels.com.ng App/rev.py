from tkinter import *
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
import time
import sqlite3



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
	tree.column("#3",width = 200)

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

	main_menu.add_cascade(label = "File", menu = submenu)
	main_menu.add_cascade(label = "Add", command = add_record)
	main_menu.add_cascade(label = "Edit",command = edit_box)
	main_menu.add_cascade(label = "Delete", command = delete_record)	
	main_menu.add_cascade(label = "Help",command = helpp)
	main_menu.add_cascade(label = "Exit",command = rev.destroy)

	submenu.add_command(label = "Add Record", command = add_record)
	submenu.add_command(label = "Edit Record",command = edit_box)
	submenu.add_command(label = "Delete Record", command = delete_record)
	submenu.add_separator()
	submenu.add_command(label = "Help",command = helpp)
	submenu.add_command(label = "Exit",command = rev.destroy)

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
	








revenue()