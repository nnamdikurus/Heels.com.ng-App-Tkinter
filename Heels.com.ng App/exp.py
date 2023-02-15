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
	








expenses()