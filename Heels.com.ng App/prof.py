from tkinter import *
from tkinter import ttk
from tkcalendar import *
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
import time
import sqlite3



def profitloss():
	prof = Tk()
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
	stat_radio = ttk.Combobox(frame, textvariable = stat_text, width = 40)
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

	main_menu.add_cascade(label = "File", menu = submenu)
	main_menu.add_cascade(label = "Add", command = add_record)
	main_menu.add_cascade(label = "Edit",command = edit_box)
	main_menu.add_cascade(label = "Delete", command = delete_record)	
	main_menu.add_cascade(label = "Help",command = helpp)
	main_menu.add_cascade(label = "Exit",command = prof.destroy)

	submenu.add_command(label = "Add Record", command = add_record)
	submenu.add_command(label = "Edit Record",command = edit_box)
	submenu.add_command(label = "Delete Record", command = delete_record)
	submenu.add_separator()
	submenu.add_command(label = "Help",command = helpp)
	submenu.add_command(label = "Exit",command = prof.destroy)

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
	








profitloss()