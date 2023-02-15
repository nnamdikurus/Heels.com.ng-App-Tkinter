from tkinter import *
from tkcalendar import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter.scrolledtext import *
import datetime
import time
import sqlite3
import csv
import excel


root = Tk()
root.geometry("1600x820+0+0")
root.title("Heelz.com.ng Dashboard")
root.configure(background = "#FF00FF")

	#===================DASHBOARD TAB=====================

	#=============MANAGE TABS(NOTEBOOK)==================

style = ttk.Style()

style.theme_create( "yummy", parent="alt", settings={
      "TNotebook": {"configure": {"tabmargins": [15, 85, 40, 300] } },
 			"TNotebook.Tab": {
           "configure": {"padding": [18, 15], "background": '#663399', "foreground":'black'},
            "map":       {"background": [("selected", "lightgrey")],
                          "expand": [("selected", [1, 1, 1, 1])] } } } )


style.theme_use("yummy")
style.configure("lefttab.TNotebook", tabposition = "ws",background = "#FF00FF")
style.configure("TNotebook.Tab", font = "Rockwell 20 bold italic",background = "#663399")

notebook = ttk.Notebook(root, style = "lefttab.TNotebook")

tab_home = ttk.Frame(notebook)
tab_trans = ttk.Frame(notebook)
tab_inv = ttk.Frame(notebook)
tab_mer = ttk.Frame(notebook)
tab_exp = ttk.Frame(notebook)
tab_rev = ttk.Frame(notebook)
tab_prof = ttk.Frame(notebook)
tab_sr = ttk.Frame(notebook)

notebook.add(tab_home, text = "Home")
notebook.add(tab_trans, text = "Transactions")
notebook.add(tab_inv, text = "Inventory")
notebook.add(tab_mer, text = "Merchants")
notebook.add(tab_exp, text = "Expenses")
notebook.add(tab_rev, text = "Revenue")
notebook.add(tab_prof, text = "Profit/Loss")
notebook.add(tab_sr, text = "Sales Report")

notebook.grid(row=0,column=0, sticky=N)


#===================HOME IMAGE=============================#

img_home = ImageTk.PhotoImage(Image.open("C:\\Icons\\heelslogo3.png"))
img_label_home = Label(tab_home, image = img_home, height = 720, width = 1000)
img_label_home.grid(row = 1, column = 1, sticky=N, columnspan=2, rowspan=1,padx=(190,0))

#===================HOME LABELS================================================#

title_label = Label(tab_home, text = "Heels.com.ng Tool Kit", font = "papyrus 30 bold italic underline", bg = "#FF00FF", fg = "#8B0000")
title_label.grid(row = 0, column = 1, padx=(210,0), pady = 15)


#===================SALES REPORT TAB================================================================================


def run_query(query,parameters=()):
	conn = sqlite3.connect("Heels.com.ng.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_sr():
	record = tree_sr.get_children()
	for element in record:
		tree_sr.delete(element)
	query = "SELECT * FROM sr"
	connect = run_query(query)
	for data in connect:
		tree_sr.insert("",10000,text = data[0], values = data[1:])


def validation_sr():
	return len(month_entry.get())!=0,len(name_entry.get())!=0,len(nos_entry.get())!=0,len(amount_entry.get())!=0,len(amount1_entry.get())!=0,len(status_entry.get())!=0,len(date_entry.get())!=0

def add_record_sr():
	if validation_sr():
		query = "INSERT INTO sr VALUES(NULL,?,?,?,?,?,?,?)"
		parameters = (month_entry.get(),name_entry.get(),nos_entry.get(),amount_entry.get(),amount1_entry.get(),status_entry.get(),date_entry.get())
		run_query(query,parameters)
		display_sr["text"] = "Record {} has been added".format(month_entry.get())

		month_entry.delete(0,END)
		name_entry.delete(0,END)
		nos_entry.delete(0,END)
		amount_entry.delete(0,END)
		amount1_entry.delete(0,END)
		status_entry.delete(0,END)
		date_entry.delete(0,END)

	else:
		display_sr["text"] = "Please fill all entries"

def add():
	pop = messagebox.askquestion("Adding New Record", "Do you want to add this record?")
	if pop == "yes":
		add_record_sr()
	else:
		display_sr["text"] = "Record was not added"

	view_record_sr()


def delete_record_sr():
	pop = messagebox.askquestion("Deleting Record","Do you want to delete record? This action cannot be undone")
	if pop == 'yes':
		try:
			tree_sr.item(tree_sr.selection())["values"][1]
		except IndexError as e:
			display_sr["text"] = "Please select a record to delete"
		query = "DELETE FROM sr WHERE ID=?"
		number = tree_sr.item(tree_sr.selection())["text"]
		run_query(query,(number,))
		display_sr["text"] = "Record {} deleted".format(number)
	else:
		display_sr["text"] = "Record not deleted"

		view_record_sr()


def edit_box_sr():
	try:
		tree_sr.item(tree_sr.selection())["values"][0]
	except IndexError as e:
		display_sr["text"] = "Please select a record to edit"
	month_text = tree_sr.item(tree_sr.selection())["values"][0]
	name_text = tree_sr.item(tree_sr.selection())["values"][1]
	nos_text = tree.item(tree_sr.selection())["values"][2]
	amount_text = tree_sr.item(tree_sr.selection())["values"][3]
	amount1_text = tree_sr.item(tree_sr.selection())["values"][4]
	status_text = tree_sr.item(tree_sr.selection())["values"][5]
	date_text = tree_sr.item(tree_sr.selection())["values"][6]

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

	Button(new_edit, text = "Save Changes", cursor = "hand2", command = lambda:edit_record_sr(new_month.get(),month_text,new_name.get(),name_text,new_nos.get(),nos_text,new_amount.get(),amount_text,new_amount1.get(),amount1_text,new_status.get(),status_text,new_date.get(),date_text)).grid(row = 14, column = 1)


	new_edit.mainloop()

def edit_record_sr(new_month,month_text,new_name,name_text,new_nos,nos_text,new_amount,amount_text,new_amount1,amount_text1,new_status,status_text,new_date,date_text):
		query = "UPDATE sr SET month = ?,  name = ?,  nos = ?,  amount = ?,  amount1 = ?, status = ?, datee = ? WHERE  month = ? AND  name = ? AND nos = ? AND amount = ? AND amount1 = ? AND status = ? AND datee = ?"
		parameters = (new_month,new_name,new_nos,new_amount,new_amount1,new_status,new_date,month_text,name_text,nos_text,amount_text,amount_text1,status_text,date_text)
		run_query(query,parameters)
		display_sr["text"] = "Record {} has been changed to {}".format(month_text,new_month)


		view_record_sr()


#--------------------------IMAGES-------------------------------#

img_sr = ImageTk.PhotoImage(Image.open("C:\\Icons\\salesreport1.png"))
img_label_sr = Label(tab_sr, image = img_sr, width = 550, height = 335)
img_label_sr.grid(row = 1, column = 1, sticky=SW)

#--------------------------FRAMES-------------------------------#

frame_sr = LabelFrame(tab_sr, width = 50, bd = 3, bg = "#97e8e1", padx = 10)
frame_sr.grid(row = 1, column = 0, padx = 10, pady = 5)

	#--------------------------LABELS-------------------------------#

topic_label = Label(tab_sr,text = "Merchants Sales Report Summary", font = "Georgia 30 bold underline", bg = "#c93073")
topic_label.grid(row = 0, column = 0, padx = 1, pady = 20, sticky=W)

month_label = Label(frame_sr,text = "Month", font = "Georgia 11 bold", bg = "#97e8e1")
month_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 5)

mn_label = Label(frame_sr,text = "Merchant Name", font = "Georgia 11 bold", bg = "#97e8e1")
mn_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 5)

nos_label = Label(frame_sr,text = "Number of Shoes sold", font = "Georgia 11 bold", bg = "#97e8e1")
nos_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 5)

amount_label = Label(frame_sr,text = "Amount to Merchant", font = "Georgia 11 bold", bg = "#97e8e1")
amount_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 5)

amount1_label = Label(frame_sr,text = "Amount Profited to Heels", font = "Georgia 11 bold", bg = "#97e8e1")
amount1_label.grid(row = 5, column = 0, sticky = W, padx = 10, pady = 5)

status_label = Label(frame_sr,text = "Status of Payment", font = "Georgia 11 bold", bg = "#97e8e1")
status_label.grid(row = 6, column = 0, sticky = W, padx = 10, pady = 5)

date_label = Label(frame_sr,text = "Date Reconciled", font = "Georgia 11 bold", bg = "#97e8e1")
date_label.grid(row = 7, column = 0, sticky = W, padx = 10, pady = 5)


	#--------------------------ENTRIES-------------------------------#

month_text = StringVar()
month_entry = ttk.Combobox(frame_sr,  cursor = "hand2", textvariable = month_text)
month_entry.config(values = ("January","February","March","April","May","June","July","August","September","October","November","December",))
month_entry.grid(row = 1, column = 1, sticky = W)

name_text = StringVar()
name_entry = Entry(frame_sr, textvariable = name_text, width = 40, bd = 3)
name_entry.grid(row = 2, column = 1, sticky = W)

nos_text = StringVar()
nos_entry = Spinbox(frame_sr,cursor = "hand2", textvariable = nos_text, from_=1, to = 100, width = 40, bd = 3)
nos_entry.grid(row = 3, column = 1, sticky = W)

amount_text = StringVar()
amount_entry = Entry(frame_sr, textvariable = amount_text, width = 40,cursor = "hand2")
amount_entry.grid(row = 4, column = 1, sticky = W)


amount1_text = StringVar()
amount1_entry = Entry(frame_sr, textvariable = amount1_text, width = 40,cursor = "hand2")
amount1_entry.grid(row = 5, column = 1, sticky = W)


status_text = StringVar()
status_entry = ttk.Combobox(frame_sr,  cursor = "hand2", textvariable = status_text, width = 15)
status_entry.config(values = ("Paid","Not Yet Paid"))
status_entry.grid(row = 6, column = 1, sticky = W)

date_text = StringVar()
date_entry = DateEntry(frame_sr,  cursor = "hand2", textvariable = date_text, width = 15, bd = 3)
date_entry.grid(row = 7, column = 1, sticky = W)

				#BUTTONS

#--------------------------BUTTONS-------------------------------#


add_butt_sr = Button(frame_sr, text = "Add Record",  cursor = "hand2", font = "Georgia 11 bold", bg = "#97e8e1",command = add)
add_butt_sr.grid(row = 8, column = 1, pady = 10)

edit_butt_sr = Button(frame_sr, text = "Edit Record",  cursor = "hand2", font = "Georgia 11 bold", bg = "teal",command = edit_box_sr)
edit_butt_sr.grid(row = 8, column = 0, pady = 10)

del_butt_sr = Button(frame_sr, text = "Delete Record",  cursor = "hand2", font = "Georgia 11 bold", bg = "tomato",command = delete_record_sr)
del_butt_sr.grid(row = 8, column = 2, pady = 10)

display_sr = Label(frame_sr, text = "",font = "Garamond 11 bold italic", fg = "blue", bg = "#97e8e1")
display_sr.grid(row = 9, column = 1, padx = 15)



#--------------------------TREEVIEW-------------------------------#

tree_sr = ttk.Treeview(tab_sr, height = 19, columns = ["","","","","","",""])
tree_sr.grid(row = 9, column = 0, columnspan = 2, padx = 10, pady = 10)

tree_sr.heading("#0",text = "ID")
tree_sr.column("#0",width = 80, anchor = "n")

tree_sr.heading("#1",text = "Month")
tree_sr.column("#1",width = 100, anchor = "n")

tree_sr.heading("#2",text = "Merchant Name")
tree_sr.column("#2",width = 200, anchor = "n")

tree_sr.heading("#3",text = "Number of Shoes Sold")
tree_sr.column("#3",width = 200, anchor = "n")

tree_sr.heading("#4",text = "Amount to Merchant")
tree_sr.column("#4",width = 200, anchor = "n")

tree_sr.heading("#5",text = "Amount to Heels")
tree_sr.column("#5",width = 150, anchor = "n")

tree_sr.heading("#6",text = "Status")
tree_sr.column("#6",width = 100, anchor = "n")

tree_sr.heading("#7",text = "Date")
tree_sr.column("#7",width = 100, anchor = "n")

view_record_sr()


#--------------------------SCROLLBAR-------------------------------#

sb_sr = Scrollbar(tab_sr,command = tree_sr.yview)
sb_sr.grid(row = 8, column = 1, padx = (440,0), rowspan = 4, sticky = NS, ipady = 2)


def tick():
	d = datetime.datetime.now()
	mydate = "{:%B - %d - %Y}".format(d)
	mytime = time.strftime("%I : %M : %S%p")
	lblInfo.config(text = mytime +"\t" + mydate)
	lblInfo.after(200,tick)
lblInfo = Label(tab_sr, font = "Georgia 11 bold italic", fg = "red", bg = "#c3f705")
lblInfo.grid(row = 0, column = 1)
tick()



#===================PROFIT/LOSS TAB================================================================================


def run_query(query,parameters=()):
	conn = sqlite3.connect("Heels.com.ng.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_prof():
	record = tree_prof.get_children()
	for element in record:
		tree_prof.delete(element)
	query = "SELECT * FROM prof"
	connect = run_query(query)
	for data in connect:
		tree_prof.insert("",10000,text = data[0], values = data[1:])
	


def validation_prof():
	return len(month_entry.get())!=0,len(rev_entry.get())!=0,len(exp_entry.get())!=0,len(net_entry.get())!=0,len(stat_text.get())!=0,len(date_entry.get())!=0

def add_record_prof():
	if validation_prof():
		query = "INSERT INTO prof VALUES(NULL,?,?,?,?,?,?)"
		parameters = (month_entry.get(),rev_entry.get(),exp_entry.get(),net_entry.get(),stat_text.get(),date_entry.get())
		run_query(query,parameters)
		display_prof["text"] = "Record {} added".format(month_entry.get())

		month_entry.delete(0,END)
		rev_entry.delete(0,END)
		exp_entry.delete(0,END)
		net_entry.delete(0,END)
		stat_radio.delete(0,END)
		date_entry.delete(0,END)

	else:
		display_prof["text"] = "Please fill all entries"


def add():
	pop = messagebox.askquestion("Adding New Record", "Do you want to add this record?")
	if pop == "yes":
		add_record_prof()
	else:
		display_prof["text"] = "Record was not added"

	view_record_prof()


def delete_record_prof():
	pop = messagebox.askquestion("Deleting Record","Do you want to delete record? This action cannot be undone")
	if pop == 'yes':

		try:
			tree_prof.item(tree_prof.selection())["values"][1]
		except IndexError as e:
			display_prof["text"] = "Please select a record to delete"
		query = "DELETE FROM prof WHERE ID=?"
		number = tree_prof.item(tree_prof.selection())["text"]
		run_query(query,(number,))
		display_prof["text"] = "Record {} deleted".format(number)
	else:
		display_prof["text"] = "Record not deleted"

	view_record_prof()



def edit_box_prof():
	try:
		tree_prof.item(tree_prof.selection())["values"][0]
	except IndexError as e:
		display_prof["text"] = "Please select a record to edit"
	month_text = tree_prof.item(tree_prof.selection())["values"][0]
	rev_text = tree_prof.item(tree_prof.selection())["values"][1]
	exp_text = tree_prof.item(tree_prof.selection())["values"][2]
	net_text = tree_prof.item(tree_prof.selection())["values"][3]
	stat_text = tree_prof.item(tree_prof.selection())["values"][4]
	date_text = tree_prof.item(tree_prof.selection())["values"][5]

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

def edit_record_prof(new_month,month_text,new_rev,rev_text,new_exp,exp_text,new_net,net_text,stat_radio,stat_text,new_date,date_text):
		query = "UPDATE prof SET month = ?,  rev = ?,  exp = ?,  net = ?, status = ?, datee = ? WHERE  month = ? AND  rev = ? AND exp = ? AND net = ? AND status = ? AND datee = ?"
		parameters = (new_month,new_rev,new_exp,new_net,stat_radio,new_date,month_text,rev_text,exp_text,net_text,stat_text,date_text)
		run_query(query,parameters)
		display["text"] = "Record {} has been changed to {}".format(month_text,new_month)

		view_record()


	#--------------------------IMAGES-------------------------------#

img_prof = ImageTk.PhotoImage(Image.open("C:\\Icons\\profitloss1.png"))
img_label_prof = Label(tab_prof, image = img_prof, width = 600, height = 350)
img_label_prof.grid(row = 1, column = 1)

	#--------------------------FRAMES-------------------------------#

frame_prof = LabelFrame(tab_prof, width = 50, bd = 3, bg = "#97e8e1", padx = 20, pady = 20)
frame_prof.grid(row = 1, column = 0, padx = 30, pady = 5)

	#--------------------------LABELS-------------------------------#

topic_label = Label(tab_prof,text = "Profit/Loss Summary", font = "Georgia 30 bold underline", bg = "#c93073")
topic_label.grid(row = 0, column = 0, padx = 1, pady = 20, sticky=W)

month_label = Label(frame_prof,text = "Month", font = "Georgia 11 bold", bg = "#97e8e1")
month_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 5)

rev_label = Label(frame_prof,text = "All Revenue", font = "Georgia 11 bold", bg = "#97e8e1")
rev_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 5)

exp_label = Label(frame_prof,text = "All Expenses", font = "Georgia 11 bold", bg = "#97e8e1")
exp_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 5)

net_label = Label(frame_prof,text = "Net Amount", font = "Georgia 11 bold", bg = "#97e8e1")
net_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 5)

status_label = Label(frame_prof,text = "Status", font = "Georgia 11 bold", bg = "#97e8e1")
status_label.grid(row = 5, column = 0, sticky = W, padx = 10, pady = 5)

date_label = Label(frame_prof,text = "Date Reconciled", font = "Georgia 11 bold", bg = "#97e8e1")
date_label.grid(row = 6, column = 0, sticky = W, padx = 10, pady = 5)

	#--------------------------ENTRIES-------------------------------#

month_text = StringVar()
month_entry = ttk.Combobox(frame_prof, textvariable = month_text)
month_entry.configure(values = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))
month_entry.grid(row = 1, column = 1, sticky = W)

rev_text = StringVar()
rev_entry = Entry(frame_prof, textvariable = rev_text, width = 40, bd = 3)
rev_entry.grid(row = 2, column = 1, sticky = W)

exp_text = StringVar()
exp_entry = Entry(frame_prof, textvariable = exp_text, width = 40, bd = 3)
exp_entry.grid(row = 3, column = 1, sticky = W)

net_text = StringVar()
net_entry = Entry(frame_prof, textvariable = net_text, width = 40, bd = 3)
net_entry.grid(row = 4, column = 1, sticky = W)

stat_text = StringVar()
stat_radio = ttk.Combobox(frame_prof, textvariable = stat_text, width = 37)
stat_radio.configure(value = ("Profit","Loss","Even",))
stat_radio.grid(row = 5, column = 1, sticky = W)

date_text = StringVar()
date_entry = DateEntry(frame_prof, textvariable = date_text,  cursor = "hand2", width = 15, bd = 3)
date_entry.grid(row = 6, column = 1, sticky = W)


	#--------------------------BUTTONS-------------------------------#


add_butt_prof = Button(frame_prof, text = "Add Summary",  cursor = "hand2", font = "Georgia 11 bold", bg = "#97e8e1",command = add)
add_butt_prof.grid(row = 7, column = 1, pady = 20)

edit_butt_prof = Button(frame_prof, text = "Edit Summary",  cursor = "hand2", font = "Georgia 11 bold", bg = "lightblue",command = edit_box_prof)
edit_butt_prof.grid(row = 7, column = 0, pady = 20)

del_butt_prof = Button(frame_prof, text = "Delete Summary",  cursor = "hand2", font = "Georgia 11 bold", bg = "crimson",command = delete_record_prof)
del_butt_prof.grid(row = 7, column = 2, pady = 20)

display_prof = Label(frame_prof, text = "",font = "Garamond 11 bold italic", fg = "blue", bg = "#97e8e1")
display_prof.grid(row = 8, column = 1, padx = 15)



	#--------------------------TREEVIEW-------------------------------#

tree_prof = ttk.Treeview(tab_prof, height = 15, columns = ["","","","","",""])
tree_prof.grid(row = 9, column = 0, columnspan = 3, padx = 30, pady = 20)

tree_prof.heading("#0",text = "ID")
tree_prof.column("#0",width = 80, anchor = "n")

tree_prof.heading("#1",text = "Month")
tree_prof.column("#1",width = 200, anchor = "n")

tree_prof.heading("#2",text = "All Revenue")
tree_prof.column("#2",width = 200, anchor = "n")

tree_prof.heading("#3",text = "All Expenses")
tree_prof.column("#3",width = 200, anchor = "n")

tree_prof.heading("#4",text = "Net Amount")
tree_prof.column("#4",width = 150, anchor = "n")

tree_prof.heading("#5",text = "Status")
tree_prof.column("#5",width = 150, anchor = "n")

tree_prof.heading("#6",text = "Date")
tree_prof.column("#6",width = 150, anchor = "n")

view_record_prof()

	#--------------------------SCROLLBAR-------------------------------#

sb_prof = Scrollbar(tab_prof,command = tree_prof.yview)
sb_prof.grid(row = 8, column = 1, padx = (500,0), rowspan = 4, sticky = NS, ipady = 2)



def tick():
	d = datetime.datetime.now()
	mydate = "{:%B - %d - %Y}".format(d)
	mytime = time.strftime("%I : %M : %S%p")
	lblInfo.config(text = mytime +"\t" + mydate)
	lblInfo.after(200,tick)
lblInfo = Label(tab_prof, font = "Georgia 11 bold italic", fg = "red", bg = "#c3f705")
lblInfo.grid(row = 0, column = 1)
tick()


	#===================REVENUE TAB================================================================================

def run_query(query,parameters=()):
	conn = sqlite3.connect("Heels.com.ng.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_rev():
	record = tree_rev.get_children()
	for element in record:
		tree_rev.delete(element)
	query = "SELECT * FROM rev"
	connect = run_query(query)
	for data in connect:
		tree_rev.insert("",10000,text = data[0], values = data[1:])

def validation_rev():
	return len(order_entry.get())!=0,len(name_entry.get())!=0,len(amount_entry.get())!=0,len(mode_entry.get())!=0,len(date_entry.get())!=0

def add_record_rev():
	if validation_rev():
		query = "INSERT INTO rev VALUES(NULL,?,?,?,?,?)"
		parameters = (order_entry.get(),name_entry.get(),amount_entry.get(),mode_entry.get(),date_entry.get())
		run_query(query,parameters)
		display_rev["text"] = "Record {} added".format(order_entry.get())

		order_entry.delete(0,END)
		name_entry.delete(0,END)
		amount_entry.delete(0,END)
		mode_entry.delete(0,END)
		date_entry.delete(0,END)

	else:
		display_rev["text"] = "Please fill all entries"


def add():
	pop = messagebox.askquestion("Adding New Record", "Do you want to add this record?")
	if pop == "yes":
		add_record_rev()
	else:
		display_rev["text"] = "Record was not added"

	view_record_rev()


def delete_record_rev():
	pop = messagebox.askquestion("Deleting Record","Do you want to delete record? This action cannot be undone")
	if pop == 'yes':

		try:
			tree_rev.item(tree_rev.selection())["values"][1]
		except IndexError as e:
			display_rev["text"] = "Please select a record to delete"
		query = "DELETE FROM rev WHERE ID=?"
		number = tree_rev.item(tree_rev.selection())["text"]
		run_query(query,(number,))
		display_rev["text"] = "Record {} deleted".format(number)

	else:
		display_rev["text"] = "Record not deleted"

		view_record_rev()


def edit_box_rev():
	try:
		tree_rev.item(tree_rev.selection())["values"][0]
	except IndexError as e:
		display_rev["text"] = "Please select a record to edit"
	order_text = tree_rev.item(tree_rev.selection())["values"][0]
	name_text = tree_rev.item(tree_rev.selection())["values"][1]
	amount_text = tree_rev.item(tree_rev.selection())["values"][2]
	mode_text = tree_rev.item(tree_rev.selection())["values"][3]
	date_text = tree_rev.item(tree_rev.selection())["values"][4]

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

def edit_record_rev(new_order,order_text,new_name,name_text,new_amount,amount_text,new_mode,mode_text,new_date,date_text):
		query = "UPDATE rev SET orderr = ?,  name = ?,  amount = ?,  mode = ?,  datee = ? WHERE  orderr = ? AND  name = ? AND amount = ? AND mode = ? AND datee = ?"
		parameters = (new_order,new_name,new_amount,new_mode,new_date,order_text,name_text,amount_text,mode_text,date_text)
		run_query(query,parameters)
		display_rev["text"] = "Record {} changed to {}".format(order_text,new_order)
		view_record_rev()

	#--------------------------IMAGES-------------------------------#

img_rev = ImageTk.PhotoImage(Image.open("C:\\Icons\\profitloss1.png"))
img_label_rev = Label(tab_rev, image = img_rev, width = 600, height = 300)
img_label_rev.grid(row = 1, column = 1)

	#--------------------------FRAMES-------------------------------#

frame_rev = LabelFrame(tab_rev, width = 50, bd = 3, bg = "#97e8e1", padx = 20, pady = 10)
frame_rev.grid(row = 1, column = 0, padx = 30, pady = 5)

	#--------------------------LABELS-------------------------------#

topic_label = Label(tab_rev,text = "Revenue Summary", font = "Georgia 30 bold underline", bg = "#c93073")
topic_label.grid(row = 0, column = 0, padx = 10, pady = 20, sticky=W)

order_label = Label(frame_rev,text = "Order Number", font = "Georgia 11 bold", bg = "#97e8e1")
order_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 5)

cus_label = Label(frame_rev,text = "Customer Name", font = "Georgia 11 bold", bg = "#97e8e1")
cus_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 5)

amo_label = Label(frame_rev,text = "Amount", font = "Georgia 11 bold", bg = "#97e8e1")
amo_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 5)

mode_label = Label(frame_rev,text = "Mode of Payment", font = "Georgia 11 bold", bg = "#97e8e1")
mode_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 5)

date_label = Label(frame_rev,text = "Date Reconciled", font = "Georgia 11 bold", bg = "#97e8e1")
date_label.grid(row = 5, column = 0, sticky = W, padx = 10, pady = 5)

	#--------------------------ENTRIES-------------------------------#

order_text = StringVar()
order_entry = Entry(frame_rev, textvariable = order_text)
order_entry.grid(row = 1, column = 1, sticky = W)

name_text = StringVar()
name_entry = Entry(frame_rev, textvariable = name_text, width = 40, bd = 3)
name_entry.grid(row = 2, column = 1, sticky = W)

amount_text = StringVar()
amount_entry = Entry(frame_rev, textvariable = amount_text, width = 40, bd = 3)
amount_entry.grid(row = 3, column = 1, sticky = W)

mode_text = StringVar()
mode_entry = ttk.Combobox(frame_rev, textvariable = mode_text, width = 40,cursor = "hand2")
mode_entry.config(values = ("Cash","POS","Courier","Paystack","Bank Transfer","Store Credit"))
mode_entry.grid(row = 4, column = 1, sticky = W)


date_text = StringVar()
date_entry = DateEntry(frame_rev,  cursor = "hand2", textvariable = date_text, width = 15, bd = 3)
date_entry.grid(row = 5, column = 1, sticky = W)


	#--------------------------BUTTONS-------------------------------#


add_butt_rev = Button(frame_rev, text = "Add Record",  cursor = "hand2", font = "Georgia 11 bold", bg = "#97e8e1",command = add)
add_butt_rev.grid(row = 6, column = 1, pady = 20)

edit_butt_rev = Button(frame_rev, text = "Edit Record",  cursor = "hand2", font = "Georgia 11 bold", bg = "teal",command = edit_box_rev)
edit_butt_rev.grid(row = 6, column = 0, pady = 20)

del_butt_rev = Button(frame_rev, text = "Delete Record",  cursor = "hand2", font = "Georgia 11 bold", bg = "crimson",command = delete_record_rev)
del_butt_rev.grid(row = 6, column = 2, pady = 20)

display_rev = Label(frame_rev, text = "",font = "Garamond 11 bold italic", fg = "blue", bg = "#97e8e1")
display_rev.grid(row = 7, column = 1, padx = 15)



	#--------------------------TREEVIEW-------------------------------#

tree_rev = ttk.Treeview(tab_rev, height = 18, columns = ["","","","",""])
tree_rev.grid(row = 8, column = 0, columnspan = 3, padx = 20, pady = 20)

tree_rev.heading("#0",text = "ID")
tree_rev.column("#0",width = 80, anchor = "n")

tree_rev.heading("#1",text = "Order Number")
tree_rev.column("#1",width = 200, anchor = "n")

tree_rev.heading("#2",text = "Customer Name")
tree_rev.column("#2",width = 250, anchor = "n")

tree_rev.heading("#3",text = "Amount")
tree_rev.column("#3",width = 150, anchor = "n")

tree_rev.heading("#4",text = "Mode of Payment")
tree_rev.column("#4",width = 180, anchor = "n")

tree_rev.heading("#5",text = "Date")
tree_rev.column("#5",width = 150, anchor = "n")

view_record_rev()


	#--------------------------SCROLLBAR-------------------------------#

sb_rev = Scrollbar(tab_rev,command = tree_rev.yview)
sb_rev.grid(row = 8, column = 1, padx = (380,0),rowspan = 4, sticky = NS, ipady = 2)




def tick():
	d = datetime.datetime.now()
	mydate = "{:%B - %d - %Y}".format(d)
	mytime = time.strftime("%I : %M : %S%p")
	lblInfo.config(text = mytime +"\t" + mydate)
	lblInfo.after(200,tick)
lblInfo = Label(tab_rev, font = "Georgia 11 bold italic", fg = "red", bg = "#c3f705")
lblInfo.grid(row = 0, column = 1)
tick()



	#===================EXPENSES TAB=====================


	#--------------------------FUNCTIONS-------------------------------#

def run_query(query,parameters=()):
	conn = sqlite3.connect("Heels.com.ng.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_exp():
	record = tree_exp.get_children()
	for element in record:
		tree_exp.delete(element)
	query = "SELECT * FROM exp"
	connect = run_query(query)
	for data in connect:
		tree_exp.insert("",10000,text = data[0], values = data[1:])


def validation_exp():
	return len(exp_entry.get())!=0,len(amo_entry.get())!=0,len(date_entry.get())!=0,len(debit_entry.get())!=0

def add_record_exp():
	if validation_exp():
		query = "INSERT INTO exp VALUES(NULL,?,?,?,?)"
		parameters = (exp_entry.get(),amo_entry.get(),date_entry.get(),debit_entry.get())
		run_query(query,parameters)
		display_exp["text"] = "Record {} has been added".format(exp_entry.get())

		exp_entry.delete(0,END)
		amo_entry.delete(0,END)
		date_entry.delete(0,END)
		debit_entry.delete(0,END)

	else:
		display_exp["text"] = "Please fill all entries"


def add():
	pop = messagebox.askquestion("Adding New Record", "Do you want to add this record?")
	if pop == "yes":
		add_record_exp()
	else:
		display_exp["text"] = "Record was not added"

	view_record_exp()


def delete_record_exp():
	pop = messagebox.askquestion("Deleting Record","Do you want to delete record? This action cannot be undone")
	if pop == 'yes':

		try:
			tree_exp.item(tree_exp.selection())["values"][1]
		except IndexError as e:
			display_exp["text"] = "Please select a record to delete"
		query = "DELETE FROM exp WHERE ID=?"
		number = tree_exp.item(tree_exp.selection())["text"]
		run_query(query,(number,))
		display_exp["text"] = "Record {} has been deleted".format(number)

	else:
		display_exp["text"] = "Record not deleted"

		view_record_exp()


def edit_box_exp():
	try:
		tree_exp.item(tree_exp.selection())["values"][0]
	except IndexError as e:
		display_exp["text"] = "Please select a record to edit"
	exp_text = tree_exp.item(tree_exp.selection())["values"][0]
	amo_text = tree_exp.item(tree_exp.selection())["values"][1]
	date_text = tree_exp.item(tree_exp.selection())["values"][2]
	debit_text = tree_exp.item(tree_exp.selection())["values"][3]

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

def edit_record_exp(new_exp,exp_text,new_amo,amo_text,new_date,date_text,new_debit,debit_text):
		query = "UPDATE exp SET expense = ?,  amount = ?,  datee = ?,  debit = ? WHERE  expense = ? AND  amount = ? AND datee = ? AND debit = ?"
		parameters = (new_exp,new_amo,new_date,new_debit,exp_text,amo_text,date_text,debit_text)
		run_query(query,parameters)
		display_exp["text"] = "Record {} has been changed to {}".format(exp_text,new_exp)
		view_record_exp()



	#--------------------------IMAGES-------------------------------#


img_exp = ImageTk.PhotoImage(Image.open("C:\\Icons\\expenses.png"))
img_label_exp = Label(tab_exp, image = img_exp, width = 400, height = 270)
img_label_exp.grid(row = 1, column = 1)

	#--------------------------FRAMES-------------------------------#

frame_exp = LabelFrame(tab_exp, width = 50, bd = 3, bg = "#f7f6a8", padx = 20, pady = 20)
frame_exp.grid(row = 1, column = 0, padx = 30, pady = 10)

	#--------------------------LABELS-------------------------------#

topic_label = Label(tab_exp,text = "Detailed Expenses/Charges", font = "Georgia 30 bold underline", bg = "#c3f705")
topic_label.grid(row = 0, column = 0, padx = 10, pady = 20, sticky=W)

exp_label = Label(frame_exp,text = "Expense/Charge", font = "Georgia 11 bold", bg = "#f7f6a8")
exp_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 5)

amo_label = Label(frame_exp,text = "Amount", font = "Georgia 11 bold", bg = "#f7f6a8")
amo_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 5)

date_label = Label(frame_exp,text = "Date Charged", font = "Georgia 11 bold", bg = "#f7f6a8")
date_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 5)

debit_label = Label(frame_exp,text = "Debited from", font = "Georgia 11 bold", bg = "#f7f6a8")
debit_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 5)

	#--------------------------ENTRIES-------------------------------#


exp_text = StringVar()
exp_entry = Entry(frame_exp, textvariable = exp_text, width = 40, bd = 3)
exp_entry.grid(row = 1, column = 1, sticky = W)

amo_text = StringVar()
amo_entry = Entry(frame_exp, textvariable = amo_text, width = 40, bd = 3)
amo_entry.grid(row = 2, column = 1, sticky = W)

date_text = StringVar()
date_entry = DateEntry(frame_exp, textvariable = date_text, width = 20, bd = 3)
date_entry.grid(row = 3, column = 1, sticky = W)

debit_text = StringVar()
debit_entry = Entry(frame_exp, textvariable = debit_text, width = 40, bd = 3)
debit_entry.grid(row = 4, column = 1, sticky = W)


	#--------------------------BUTTONS-------------------------------#

add_butt_mer = Button(frame_exp, text = "Add Expense",  cursor = "hand2", font = "Georgia 11 bold", bg = "#f7f6a8",command = add)
add_butt_mer.grid(row = 5, column = 1, pady = 20)

edit_butt_mer = Button(frame_exp, text = "Edit Expense",  cursor = "hand2", font = "Georgia 11 bold", bg = "mediumturquoise",command = edit_box_exp)
edit_butt_mer.grid(row = 5, column = 0, pady = 20)

del_butt_mer = Button(frame_exp, text = "Delete Expense",  cursor = "hand2", font = "Georgia 11 bold", bg = "tomato",command = delete_record_exp)
del_butt_mer.grid(row = 5, column = 2, pady = 20)

display_exp = Label(frame_exp, text = "",font = "Garamond 11 bold italic", fg = "blue",bg = "#f7f6a8")
display_exp.grid(row = 6, column = 1, padx = 15)



	#--------------------------TREEVIEW-------------------------------#

tree_exp = ttk.Treeview(tab_exp, height = 17, columns = ["","","",""])
tree_exp.grid(row = 7, column = 0, columnspan = 3, padx = 20)

tree_exp.heading("#0",text = "ID")
tree_exp.column("#0",width = 80, anchor = "n")

tree_exp.heading("#1",text = "Expense/Charge")
tree_exp.column("#1",width = 200, anchor = "n")

tree_exp.heading("#2",text = "Amount Charged")
tree_exp.column("#2",width = 200, anchor = "n")

tree_exp.heading("#3",text = "Date Charged")
tree_exp.column("#3",width = 200, anchor = "n")

tree_exp.heading("#4",text = "Debited From")
tree_exp.column("#4",width = 150, anchor = "n")
view_record_exp()


	#--------------------------SCROLLBAR-------------------------------#
sb_exp = Scrollbar(tab_exp,command = tree_exp.yview)
sb_exp.grid(row = 7, column = 1, padx = (200,0), sticky = NS, ipady = 3)



def tick():
	d = datetime.datetime.now()
	mydate = "{:%B - %d - %Y}".format(d)
	mytime = time.strftime("%I : %M : %S%p")
	lblInfo.config(text = mytime +"\t" + mydate)
	lblInfo.after(200,tick)
lblInfo = Label(tab_exp, font = "Georgia 11 bold italic", fg = "red", bg = "#c3f705")
lblInfo.grid(row = 0, column = 1)
tick()







	#===================MERCHANT TAB=====================

	#===================FUNCTIONS=============================#


def run_query(query,parameters=()):
	conn = sqlite3.connect("Heels.com.ng.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_mer():
	record = tree_mer.get_children()
	for element in record:
		tree_mer.delete(element)
	query = "SELECT * FROM mer"
	connect = run_query(query)
	for data in connect:
		tree_mer.insert("",10000,text = data[0], values = data[1:])


def validation_mer():
	return len(name_entry.get())!=0,len(phone_entry.get())!=0,len(email_entry.get())!=0,len(code_entry.get())!=0,len(acc_entry.get())!=0,len(stat_entry.get())!=0,len(date_entry.get())!=0 

def add_record_mer():
	if validation_mer():
		query = "INSERT INTO mer VALUES(NULL,?,?,?,?,?,?,?)"
		parameters = (name_entry.get(),phone_entry.get(),email_entry.get(),code_entry.get(),acc_entry.get(),stat_entry.get(),date_entry.get())
		run_query(query,parameters)
		display_mer["text"] = "Record {} added".format(name_entry.get())

		name_entry.delete(0,END)
		phone_entry.delete(0,END)
		email_entry.delete(0,END)
		code_entry.delete(0,END)
		acc_entry.delete(0,END)
		stat_entry.delete(0,END)
		date_entry.delete(0,END)

	else:
		display_mer["text"] = "Please fill all entries"



def add():
	pop = messagebox.askquestion("Adding New Record", "Do you want to add this record?")
	if pop == "yes":
		add_record_mer()
	else:
		display_mer["text"] = "Record was not added"

	view_record_mer()


def delete_record_mer():
	pop = messagebox.askquestion("Deleting Record","Do you want to delete record? This action cannot be undone")
	if pop == 'yes':

		try:
			tree_mer.item(tree_mer.selection())["values"][1]
		except IndexError as e:
			display_mer["text"] = "Please select a record to delete"
		query = "DELETE FROM mer WHERE ID=?"
		number = tree_mer.item(tree_mer.selection())["text"]
		run_query(query,(number,))
		display_mer["text"] = "Record {} deleted".format(number)

	else:
		display_mer["text"] = "Record not deleted"

		view_record_mer()


def edit_box_mer():
	try:
		tree_mer.item(tree_mer.selection())["values"][0]
	except IndexError as e:
		display["text"] = "Please select a record to edit"
	name_text = tree_mer.item(tree_mer.selection())["values"][0]
	phone_text = tree_mer.item(tree_mer.selection())["values"][1]
	email_text = tree_mer.item(tree_mer.selection())["values"][2]
	code_text = tree_mer.item(tree_mer.selection())["values"][3]
	acc_text = tree_mer.item(tree_mer.selection())["values"][4]
	stat_text = tree_mer.item(tree_mer.selection())["values"][5]
	date_text = tree_mer.item(tree_mer.selection())["values"][6]

	new_edit_mer = Toplevel()
	new_edit_mer.title("Edit Record")

	Label(new_edit_mer, text = "Old(Merchant Name)").grid(row = 0, column = 0)
	Entry(new_edit_mer, textvariable = StringVar(new_edit_mer,value = name_text), state = "readonly").grid(row = 0, column = 1)
	Label(new_edit_mer, text = "New(Merchant Name)").grid(row = 1, column = 0)
	new_name = Entry(new_edit_mer, width = 30, bd = 3)
	new_name.grid(row = 1, column = 1)

	Label(new_edit_mer, text = "Old(Merchant Phone Number)").grid(row = 2, column = 0)
	Entry(new_edit_mer, textvariable = StringVar(new_edit_mer,value = phone_text), state = "readonly").grid(row = 2, column = 1)
	Label(new_edit_mer, text = "New(Merchant Phone Number)").grid(row = 3, column = 0)
	new_phone = Entry(new_edit_mer, width = 30, bd = 3)
	new_phone.grid(row = 3, column = 1)

	Label(new_edit_mer, text = "Old(Merchant Email)").grid(row = 4, column = 0)
	Entry(new_edit_mer, textvariable = StringVar(new_edit_mer,value = email_text), state = "readonly").grid(row = 4, column = 1)
	Label(new_edit_mer, text = "New(Merchant Email)").grid(row = 5, column = 0)
	new_email = Entry(new_edit_mer, width = 30, bd = 3)
	new_email.grid(row = 5, column = 1)

	Label(new_edit_mer, text = "Old(Merchant Code)").grid(row = 6, column = 0)
	Entry(new_edit_mer, textvariable = StringVar(new_edit_mer,value = code_text), state = "readonly").grid(row = 6, column = 1)
	Label(new_edit_mer, text = "New(Merchant Code)").grid(row = 7, column = 0)
	new_code = Entry(new_edit_mer, width = 30, bd = 3)
	new_code.grid(row = 7, column = 1)

	Label(new_edit_mer, text = "Old(Merchant Account Details)").grid(row = 8, column = 0)
	Entry(new_edit_mer, textvariable = StringVar(new_edit_mer,value = acc_text), state = "readonly").grid(row = 8, column = 1)
	Label(new_edit_mer, text = "New(Merchant Account Details)").grid(row = 9, column = 0)
	new_acc = Entry(new_edit_mer, width = 30, bd = 3)
	new_acc.grid(row = 9, column = 1)

	Label(new_edit_mer, text = "Old(Merchant Status)").grid(row = 10, column = 0)
	Entry(new_edit_mer, textvariable = StringVar(new_edit_mer,value = stat_text), state = "readonly").grid(row = 10, column = 1)
	Label(new_edit_mer, text = "New(Merchant Status)").grid(row = 11, column = 0)
	new_status = ttk.Combobox(new_edit_mer, textvariable = stat_text, width = 30)
	new_status.configure(values= ("Active","Dormant"))
	new_status.grid(row = 11, column = 1)

	Label(new_edit_mer, text = "Old(Date Enrolled)").grid(row = 12, column = 0)
	Entry(new_edit_mer, textvariable = StringVar(new_edit_mer,value = date_text), state = "readonly").grid(row = 12, column = 1)
	Label(new_edit_mer, text = "New(Date Enrolled)").grid(row = 13, column = 0)
	new_date = DateEntry(new_edit_mer, width = 30, bd = 3)
	new_date.grid(row = 13, column = 1)

	Button(new_edit_mer, text = "Save Changes", cursor = "hand2", command = lambda:edit_record(new_name.get(),name_text,new_phone.get(),phone_text,new_email.get(),email_text,new_code.get(),code_text,new_acc.get(),acc_text,new_status.get(),stat_text,new_date.get(),date_text)).grid(row = 14, column = 1)


	new_edit_mer.mainloop()

def edit_record_mer(new_name,name_text,new_phone,phone_text,new_email,email_text,new_code,code_text,new_acc,acc_text,new_status,stat_text,new_date,date_text):
		query = "UPDATE mer SET name = ?,  phone = ?,  email = ?,  code = ?,  acc = ?,  status = ?,  datee = ? WHERE  name = ? AND  phone = ? AND email = ? AND code = ? AND acc = ? AND status = ? AND datee = ?"
		parameters = (new_name,new_phone,new_email,new_code,new_acc,new_status,new_date,name_text,phone_text,email_text,code_text,acc_text,stat_text,date_text)
		run_query(query,parameters)
		display_mer["text"] = "Record {} has been changed to {}".format(name_text,new_name)
		view_record_mer()


	#--------------------------IMAGES_MER-------------------------------#


img_mer = ImageTk.PhotoImage(Image.open("C:\\Icons\\mer.png"))
img_label_mer = Label(tab_mer, image = img_mer, width = 370, height = 340)
img_label_mer.grid(row = 1, column = 1, sticky = N)

	#--------------------------FRAMES_MER-------------------------------#

frame_mer = LabelFrame(tab_mer, width = 50, bd = 3, bg = "#f7f6a8", padx = 10)
frame_mer.grid(row = 1, column = 0, padx = 20, pady = 10, sticky = W)

	#--------------------------LABELS_MER-------------------------------#

topic_label = Label(tab_mer,text = "Merchant Catalogue", font = "Georgia 30 bold underline", bg = "#c3f705")
topic_label.grid(row = 0, column = 0, padx = 1, pady = 20)

name_label = Label(frame_mer,text = "Merchant Name", font = "Georgia 11 bold", bg = "#f7f6a8")
name_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 5)

phone_label = Label(frame_mer,text = "Merchant Phone Number", font = "Georgia 11 bold", bg = "#f7f6a8")
phone_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 5)

email_label = Label(frame_mer,text = "Merchant Email Address", font = "Georgia 11 bold", bg = "#f7f6a8")
email_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 5)

code_label = Label(frame_mer,text = "Merchant Code", font = "Georgia 11 bold", bg = "#f7f6a8")
code_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 5)

account_label = Label(frame_mer,text = "Merchant Bank Accout Details", font = "Georgia 11 bold", bg = "#f7f6a8")
account_label.grid(row = 5, column = 0, sticky = W, padx = 10, pady = 5)

stat_label = Label(frame_mer,text = "Status of Enrollment", font = "Georgia 11 bold", bg = "#f7f6a8")
stat_label.grid(row = 6, column = 0, sticky = W, padx = 10, pady = 5)

date_label = Label(frame_mer,text = "Date Enrolled", font = "Georgia 11 bold", bg = "#f7f6a8")
date_label.grid(row = 7, column = 0, sticky = W, padx = 10, pady = 5)

	#--------------------------ENTRIES_MER-------------------------------#

name_text = StringVar()
name_entry = Entry(frame_mer, textvariable = name_text, width = 40, bd = 3)
name_entry.grid(row = 1, column = 1, sticky = W)

phone_text = StringVar()
phone_entry_mer = Entry(frame_mer, textvariable = phone_text, width = 40, bd = 3)
phone_entry_mer.grid(row = 2, column = 1, sticky = W)

email_text = StringVar()
email_entry_mer = Entry(frame_mer, textvariable = email_text, width = 40, bd = 3)
email_entry_mer.grid(row = 3, column = 1, sticky = W)

code_text = StringVar()
code_entry = Entry(frame_mer, textvariable = code_text, width = 40, bd = 3)
code_entry.grid(row = 4, column = 1, sticky = W)

acc_text = StringVar()
acc_entry = Entry(frame_mer, textvariable = acc_text, width = 40, bd = 3)
acc_entry.grid(row = 5, column = 1, sticky = W)

stat_text = StringVar()
stat_entry = ttk.Combobox(frame_mer,textvariable = stat_text)
stat_entry.configure(values = ("Active", "Dormant"))
stat_entry.grid(row = 6, column = 1, sticky = W)

date_text = StringVar()
date_entry_mer = DateEntry(frame_mer, textvariable = date_text)
date_entry_mer.grid(row = 7, column = 1, sticky = W)


	#--------------------------BUTTONS_MER-------------------------------#

add_butt_mer = Button(frame_mer, text = "Add Merchant",  cursor = "hand2", font = "Georgia 11 bold", bg = "#f7f6a8", command = add)
add_butt_mer.grid(row = 9, column = 1, pady = 20)

edit_butt_mer = Button(frame_mer, text = "Edit Merchant",  cursor = "hand2", font = "Georgia 11 bold", bg = "lightblue", command = edit_box_mer)
edit_butt_mer.grid(row = 9, column = 0, pady = 20)

del_butt_mer = Button(frame_mer, text = "Delete Merchant",  cursor = "hand2", font = "Georgia 11 bold", bg = "firebrick", command = delete_record_mer)
del_butt_mer.grid(row = 9, column = 2, pady = 20)

display_mer = Label(frame_mer, text = "",font = "Garamond 11 bold italic", fg = "blue", bg = "#f7f6a8")
display_mer.grid(row = 8, column = 1, padx = 15)


	#--------------------------TREEVIEW_MER-------------------------------#

tree_mer = ttk.Treeview(tab_mer, height = 15, columns = ["","","","","","",""])
tree_mer.grid(row = 10, column = 0, columnspan = 3, padx = 20)

tree_mer.heading("#0",text = "ID")
tree_mer.column("#0",width = 80, anchor = "n")

tree_mer.heading("#1",text = "Merchant Name")
tree_mer.column("#1",width = 200, anchor = "n")

tree_mer.heading("#2",text = "Phone Number")
tree_mer.column("#2",width = 200, anchor = "n")

tree_mer.heading("#3",text = "Email Address")
tree_mer.column("#3",width = 200, anchor = "n")

tree_mer.heading("#4",text = "Code")
tree_mer.column("#4",width = 50, anchor = "n")

tree_mer.heading("#5",text = "Account Details")
tree_mer.column("#5",width = 300, anchor = "n")

tree_mer.heading("#6",text = "Status")
tree_mer.column("#6",width = 100, anchor = "n")

tree_mer.heading("#7",text = "Date")
tree_mer.column("#7",width = 100, anchor = "n")

view_record_mer()

	#--------------------------SCROLLBAR_MER-------------------------------#

sb_mer = Scrollbar(tab_mer,command = tree_mer.yview)
sb_mer.grid(row = 10, column = 2, padx = (100,0), sticky = NS, ipady = 3)

def tick():
	d = datetime.datetime.now()
	mydate = "{:%B - %d - %Y}".format(d)
	mytime = time.strftime("%I : %M : %S%p")
	lblInfo.config(text = mytime +"\t" + mydate)
	lblInfo.after(200,tick)
lblInfo = Label(tab_mer, font = "Georgia 11 bold italic", fg = "red", bg = "#c3f705")
lblInfo.grid(row = 0, column = 1)
tick()






	#===================INVENTORY TAB=====================

	#--------------FUNCTIONS_INV-------------------------#

def run_query(query,parameters=()):
	conn = sqlite3.connect("Heels.com.ng.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_inv():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])


def validation_inv():
	return len(inv_entry.get())!=0, len(date_entry.get())!=0, len(qty_entry.get())!=0, len(qty1_entry.get())!=0, len(qty2_entry.get())!=0


def add_record_inv():
	if validation_inv():
		query = "INSERT INTO inventory VALUES(NULL,?,?,?,?,?)"
		parameters = (inv_entry.get(),date_entry.get(),qty_entry.get(),qty1_entry.get(),qty2_entry.get())
		run_query(query,parameters)
		display_inv["text"] = "Record {} added".format(inv_entry.get())

		inv_entry.delete(0,END)
		date_entry.delete(0,END)
		qty_entry.delete(0,END)
		qty1_entry.delete(0,END)

	else:
		display_inv["text"] = "Please fill all fields"

def add():
	pop = messagebox.askquestion("Adding New Record", "Do you want to add this record?")
	if pop == "yes":
		add_record_inv()
	else:
		display_inv["text"] = "Record was not added"

	view_record_inv()

def delete_record_inv():
	pop = messagebox.askquestion("Deleting Record","Do you want to delete record? This action cannot be undone")
	if pop == 'yes':

		tree_inv.item(tree_inv.selection())["values"][1]
		query = "DELETE FROM inventory WHERE ID=?"
		number = tree_inv.item(tree_inv.selection())["text"]
		run_query(query,(number,))
		display_inv["text"] = "Record {} deleted".format(number)

	else:
		display_inv["text"] = "Record not deleted"

		view_record_inv()


def edit_box_inv():
	global new_edit_inv
	try:
		tree_inv.item(tree_inv.selection())["values"][0]
	except IndexError as e:
		display_inv["text"] = "Please select a record to edit"

	inv_text = tree_inv.item(tree_inv.selection())["values"][0]
	date_text = tree_inv.item(tree_inv.selection())["values"][1]
	qty_text = tree_inv.item(tree_inv.selection())["values"][2]
	qty1_text = tree_inv.item(tree_inv.selection())["values"][3]
	qty2_text = tree_inv.item(tree_inv.selection())["values"][4]


	new_edit_inv = Toplevel()
	new_edit_inv.title("Edit New Record")

	Label(new_edit_inv, text = "Old(Inventory)").grid(row = 0, column = 0)
	Entry(new_edit_inv,textvariable=StringVar(new_edit_inv,value=inv_text),state= "readonly").grid(row = 0, column = 1)
	Label(new_edit_inv, text = "New(Inventory)").grid(row = 1, column = 0)
	new_inv = ttk.Combobox(new_edit_inv,width = 30)
	new_inv.configure(values = ("Shoes","Shoe bag(Small)","Shoe bag(Big)","Shoes box(Small)","Shoe box(Big)","Printer Inks","A4 Paper","Shoe Polish","Cellotape","Shoe Bags","Mouse","Computer assessories","Stain Remover"))
	new_inv.grid(row = 1, column=1)

	Label(new_edit_inv, text = "Old(Date)").grid(row = 2, column = 0)
	Entry(new_edit_inv,textvariable=StringVar(new_edit_inv,value=date_text),state= "readonly").grid(row = 2, column = 1)
	Label(new_edit_inv, text = "New(Date)").grid(row = 3, column = 0)
	new_date = DateEntry(new_edit_inv,width = 30)
	new_date.grid(row = 3, column = 1)

	Label(new_edit_inv, text = "Old(Quantity Purchased").grid(row = 4, column = 0)
	Entry(new_edit_inv,textvariable=StringVar(new_edit_inv,value=qty_text),state= "readonly").grid(row = 4, column = 1)
	Label(new_edit_inv, text = "New(Quantity Purchased)").grid(row = 5, column = 0)
	new_qty = Spinbox(new_edit_inv,from_ = 0, to = 1000, width = 30, bd = 3)
	new_qty.grid(row = 5, column = 1)

	Label(new_edit_inv, text = "Old(Quantity Remaining)").grid(row = 6, column = 0)
	Entry(new_edit_inv,textvariable=StringVar(new_edit_inv,value=qty1_text),state= "readonly").grid(row = 6, column = 1)
	Label(new_edit_inv, text = "New(Quantity Remaining)").grid(row = 7, column = 0)
	new_qty1 = Spinbox(new_edit_inv,from_ = 0, to = 1000,width = 30, bd = 3)
	new_qty1.grid(row = 7, column = 1)

	Label(new_edit_inv, text = "Old(Total Quantity Remaining)").grid(row = 8, column = 0)
	Entry(new_edit_inv,textvariable=StringVar(new_edit_inv,value=qty2_text),state= "readonly").grid(row = 8, column = 1)
	Label(new_edit_inv, text = "New(Total Quantity Remaining)").grid(row = 9, column = 0)
	new_qty2 = Spinbox(new_edit_inv,from_ = 0, to = 1000,width = 30, bd = 3)
	new_qty2.grid(row = 9, column = 1)


	sc = Button(new_edit_inv,text = "Save Changes", cursor= "hand2", command = lambda:edit_record_inv(new_inv.get(),inv_text,new_date.get(),date_text,new_qty.get(),qty_text,new_qty1.get(),qty1_text,new_qty2.get(),qty2_text))
	sc.grid(row = 10, column = 1)
	new_edit_inv.mainloop()

def edit_record_inv(new_inv,inv_text,new_date,date_text, new_qty,qty_text, new_qty1, qty1_text,new_qty2,qty2_text):
	global new_edit_inv
	query = "UPDATE inventory SET inventory=?,datee=?,qty=?,qty1=?,qty2=? WHERE inventory=? AND datee=? AND qty=? AND qty1=? AND qty2=?"
	parameters=(new_inv,new_date,new_qty,new_qty1,new_qty2, inv_text,date_text,qty_text,qty1_text,qty2_text)
	run_query(query,parameters)
	new_edit_inv.destroy()
	display_inv["text"] = "Record updated"
	view_record_inv()

def helpp():
	messagebox.showinfo("Help","This is Dean Winchester and I need your help")


#==================FUNCTION(INVENTORY TAB)================================#
#==========================================================================


def view_record_inv_bb():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory WHERE inventory = 'Shoe bag(Big)'"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Shoe bag(Big)"

def view_record_sb():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory WHERE inventory = 'Shoe bag(Small)'"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Shoe bag(Small)"

def view_record_inv_bbo():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory WHERE inventory = 'Shoe box(Big)'"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Shoe box(Big)"

def view_record_inv_sbo():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory WHERE inventory = 'Shoe box(Small)'"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Shoe box(Small)"

def view_record_inv_print():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory WHERE inventory = 'Printer Inks'"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Printer Inks"

def view_record_inv_a4():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory WHERE inventory = 'A4 Paper'"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View A4 Paper"

def view_record_inv_pol():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory WHERE inventory = 'Shoe Polish'"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Shoe Polish"

def view_record_inv_cell():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory WHERE inventory = 'Cellotape'"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Cellotapes"




	#-------------------Sort Menu-----------------------------#

def view_record_inv_date():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory ORDER BY datee"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Inventory(Newest)"

def view_record_inv_date1():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory ORDER BY datee DESC"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Inventory(Oldest)"

def view_record_inv_qtybig():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory ORDER BY qty DESC"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View New Quantity (Descending)"

def view_record_inv_qtysmall():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory ORDER BY qty"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View New Quantity(Ascending)"

def view_record_inv_qty1big():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory ORDER BY qty1 DESC"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Quantity left(Descending)"

def view_record_inv_qty1small():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory ORDER BY qty1"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Quantity left(Ascending)"

def view_record_inv_qty2big():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory ORDER BY qty2 DESC"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Total Quantity(Descending)"

def view_record_inv_qty2small():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query="SELECT * FROM inventory ORDER BY qty2"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("",10000,text=data[0],values=data[1:])
	display_inv["text"] = "View Total Quantity(Ascending)"

#==========================================================================
#==========================================================================
#==========================================================================



	#-------------------IMAGES_INV-------------------------#

img = ImageTk.PhotoImage(Image.open("C:\\Icons\\inv1.png"))
img_label = Label(tab_inv, image = img, width = 590, height = 350)
img_label.grid(row = 1, column = 1)

	#-------------------FRAMES_INV-------------------------#

frame = LabelFrame(tab_inv, width = 50, bg = "#84db8b", pady = 10)
frame.grid(row = 1, column = 0, padx = 50, sticky=W)

	#-------------------LABELS_INV-------------------------#

inv_label = Label(tab_inv, text = "Inventory Management", font = "Rockwell 25 bold italic underline", bg = "#ed9972")
inv_label.grid(row = 0, column = 0, pady = 20)

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

	#----------------------ENTRIES_INV--------------------------------------#

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
	
	#-------------------------BUTTONS_INV------------------------------------#

add_butt_inv = Button(frame, text = "Add Inventory",  cursor = "hand2", font = "Rockwell 15 bold italic", bg = "#84db8b",command = add)
add_butt_inv.grid(row = 6, column = 1, padx = 10, pady = 10)

edit_butt_inv = Button(frame, text = "Edit Inventory",  cursor = "hand2", font = "Rockwell 11 bold italic", bg = "powderblue",command = edit_box_inv)
edit_butt_inv.grid(row = 6, column = 0, padx = 10, pady = 10)

del_butt_inv = Button(frame, text = "Delete Inventory",  cursor = "hand2", font = "Rockwell 11 bold italic", bg = "firebrick",command = delete_record_inv)
del_butt_inv.grid(row = 6, column = 2, padx = 10, pady = 10)

display_inv = Label(frame, text = "",font = "Garamond 11 bold italic", fg = "blue",bg = "#84db8b")
display_inv.grid(row = 7, column = 1, padx = 15)

	#-------------------------TREEVIEW_INV------------------------------------#

tree_inv = ttk.Treeview(tab_inv, height = 15, columns = ["","","","",""])
tree_inv.grid(row =6, column = 0, columnspan = 2,padx = 10,pady = 10)

style = ttk.Style()
style.configure("Treeview.Heading", font = "Rockwell 13 bold italic")
style.configure("Treeview", font = "Rockwell 9 bold italic")

tree_inv.heading("#0", text = "ID")
tree_inv.column("#0", width = 50, anchor = "n")

tree_inv.heading("#1", text = "Inventory")
tree_inv.column("#1", width = 250, anchor = "n")

tree_inv.heading("#2", text = "Date Purchased")
tree_inv.column("#2", width = 200, anchor = "n")

tree_inv.heading("#3", text = "Quantity Purchased")
tree_inv.column("#3", width = 200, anchor = "n")

tree_inv.heading("#4", text = "Quantity Remaining")
tree_inv.column("#4", width = 200, anchor = "n")

tree_inv.heading("#5", text = "Total Quantity Left")
tree_inv.column("#5", width = 200, anchor = "n")

view_record_inv()


	#----------------------SCROLLBAR_INV-------------------------#

sb = ttk.Scrollbar(tab_inv, command = tree_inv.yview)
sb.grid(row = 6, column = 1, padx = (500,0),sticky = NS,ipady = 3)
tree_inv.config(yscrollcommand=sb.set)


def tick():
	d = datetime.datetime.now()
	mytime = time.strftime("%I : %M : %S%p")
	mydate = "{:%B - %d - %Y}".format(d)
	lblInfo.config(text = mytime + "\t" + mydate)
	lblInfo.after(200,tick)
lblInfo = Label(tab_inv, font = "Garamond 11 bold italic", fg = "blue", bg = "#e0ffff")
lblInfo.grid(row = 0, column = 1)
tick()



#========================TRANSACTION TAB===========================================================

#==================FUNCTION(TRANSACTION TAB)================================#

def run_query(query,parameters=()):
	conn = sqlite3.connect("Heels.com.ng.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_trans():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])



def view_record_trans_cus():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT orderr,name,address,location FROM trans"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:6])


def view_record_trans_lag():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE location = 'Lagos'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Lagos Orders"

def view_record_trans_notlag():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE location != 'Lagos'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Out of State Orders"

def view_record_trans_full():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE status = 'Fully Delivered'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Fully Delivered Orders"

def view_record_trans_partial():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE status = 'Partially Delivered'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Partially Delivered Orders"

def view_record_trans_cancel():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE status = 'Cancelled'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Cancelled Orders"

def view_record_trans_reject():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE status = 'Rejected'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Rejected Orders"

def view_record_trans_cash():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE pay = 'Cash'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Cash Orders"

def view_record_trans_pos():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE pay = 'POS'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View POS Orders"

def view_record_trans_paystack():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE pay = 'Paystack'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Paystack Orders"

def view_record_trans_courier():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE pay = 'Courier'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Courier-Paid Orders"

def view_record_trans_bt():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans WHERE pay = 'Bank Transfer'"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Bank Transfer Orders"

def view_record_trans_newest():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY datee;"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Orders(Newest to Oldest)"

def view_record_trans_oldest():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY datee DESC"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Orders(Oldest to Newest)"


def view_record_trans_amo():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY amo DESC"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Amounts(Biggest to Smallest)"

def view_record_trans_bigsize():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY size DESC"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Shoe sizes(Biggest to Smallest)"

def view_record_trans_smallsize():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY size"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Shoe sizes(Smallest to Biggest)"


def view_record_trans_shoessold():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY nst DESC"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Number of Shoes Sold(Biggest to Smallest)"


def view_record_trans_sortord():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY nso DESC"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Number of Shoes Ordered(Biggest to Smallest)"

def view_record_trans_sortord1():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY nso"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Number of Shoes Ordered(Smallest to Biggest)"

def view_record_trans_sorttaken():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY nst DESC"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Number of Shoes Taken(Biggest to Smallest)"

def view_record_trans_sorttaken1():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY nst"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Number of Shoes Taken(Smallest to Biggest)"

def view_record_trans_sortrej():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY nsr DESC"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Number of Shoes Rejected(Biggest to Smallest)"

def view_record_trans_sortrej1():
	record = tree_trans.get_children()
	for element in record:
		tree_trans.delete(element)
	query = "SELECT * FROM trans ORDER BY nsr"
	connect = run_query(query)
	for data in connect:
		tree_trans.insert("",10000,text = data[0], values = data[1:])
		display_trans["text"] = "View Sorted Number of Shoes Rejected(Smallest to Biggest)"





#==========================================================================

def validation_trans():
	return len(order_entry.get())!=0, len(name_entry.get())!=0, len(add_entry.get())!=0,len(loc_entry.get())!=0, len(email_entry.get())!=0, len(nso_entry.get())!=0, len(size_entry.get())!=0, len(nst_entry.get())!=0, len(nsr_entry.get())!=0, len(amo_entry.get())!=0, len(stat_entry.get())!=0, len(pay_entry.get())!=0, len(date_entry.get())!=0

def add_record_trans():
	if validation_trans():

		query = "INSERT INTO trans VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
		parameters = (order_entry.get(),name_entry.get(),add_entry.get(),loc_entry.get(),phone_entry.get(),email_entry.get(),nso_entry.get(),size_entry.get(),nst_entry.get(),nsr_entry.get(),amo_entry.get(),stat_text.get(),pay_text.get(),date_entry.get())

		run_query(query,parameters)
		display_trans["text"] = "Record {} added".format(name_entry.get())

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
		display_trans["text"] = "Please fill all entries"


def add():
	pop = messagebox.askquestion("Adding New Record", "Do you want to add this record?")
	if pop == "yes":
		add_record_trans()
	else:
		display_trans["text"] = "Record was not added"



	view_record_trans()


def delete_record_trans():
	pop = messagebox.askquestion("Deleting Record","Do you want to delete record? This action cannot be undone")
	if pop == 'yes':
		try:
			tree_trans.item(tree_trans.selection())["values"][1]
		except IndexError as e:
			display_trans["text"] = "Please select a record to delete"
		query = "DELETE FROM trans WHERE ID = ?"
		number = tree_trans.item(tree_trans.selection())["text"]
		run_query(query,(number,))
		display_trans["text"] = "Record {} deleted".format(number)

	else:
		display_trans["text"] = "Record not deleted"

		view_record_trans()

def edit_box_trans():
	global new_edit
	try:
		tree_trans.item(tree_trans.selection())["values"][0]
	except IndexError as e:
		display_trans["text"]= "Please select a record to edit"

	order_text = tree_trans.item(tree_trans.selection())["values"][0]
	name_text = tree_trans.item(tree_trans.selection())["values"][1]
	add_text = tree_trans.item(tree_trans.selection())["values"][2]
	loc_text = tree_trans.item(tree_trans.selection())["values"][3]
	phone_text = tree_trans.item(tree_trans.selection())["values"][4]
	email_text = tree_trans.item(tree_trans.selection())["values"][5]
	nso_text = tree_trans.item(tree_trans.selection())["values"][6]
	size_text = tree_trans.item(tree_trans.selection())["values"][7]
	nst_text = tree_trans.item(tree_trans.selection())["values"][8]
	nsr_text = tree_trans.item(tree_trans.selection())["values"][9]
	amo_text = tree_trans.item(tree_trans.selection())["values"][10]
	stat_text = tree_trans.item(tree_trans.selection())["values"][11]
	pay_text = tree_trans.item(tree_trans.selection())["values"][12]
	date_text = tree_trans.item(tree_trans.selection())["values"][13]


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

	Button(new_edit, text = "Save Changes", cursor = "hand2", command = lambda:edit_record_trans(new_order.get(),order_text,new_name.get(),name_text,new_add.get(),add_text,new_loc.get(),loc_text,new_phone.get(),phone_text,new_email.get(),email_text,new_nso.get(),nso_text,new_size.get(),size_text,new_nst.get(),nst_text,new_nsr.get(),nsr_text,new_amount.get(),amo_text,new_status.get(),stat_text,new_pay.get(),pay_text,new_date.get(),date_text)).grid(row = 28, column = 1)

	new_edit.mainloop()


		#sqlite3.OperationalError: near "WHERE": syntax error
		#Please ensure there are no commas before the WHERE clause
def edit_record_trans(new_order,order_text,new_name,name_text,new_add,add_text,new_loc,loc_text, new_phone,phone_text,new_email,email_text,new_nso,nso_text,new_size,size_text,new_nst,nst_text,new_nsr,nsr_text,new_amount,amo_text,new_status,stat_text,new_pay,pay_text,new_date,date_text):
	global new_edit
	query = "UPDATE trans SET orderr = ?,  name = ?,  address = ?, location = ?, phone = ?,  email = ?,  nso = ?, size=?, nst = ?,  nsr = ?,  amo = ?,  status = ?,  pay = ?,  datee = ? WHERE orderr = ? AND name = ? AND address = ? AND location = ? AND phone = ? AND email = ? AND  nso = ? AND size = ? AND  nst = ? AND nsr = ? AND amo = ? AND status = ? AND pay = ? AND datee = ?"
	parameters = (new_order,new_name,new_add,new_loc,new_phone,new_email,new_nso,new_size,new_nst,new_nsr,new_amount,new_status,new_pay,new_date,order_text,name_text,add_text,loc_text,phone_text,email_text,nso_text,size_text,nst_text,nsr_text,amo_text,stat_text,pay_text,date_text)
	run_query(query,parameters)
	new_edit.destroy()
	display_trans["text"] = "Record {} updated to {}".format(name_text,new_name)			
	view_record_trans()

def helpp():
	messagebox.showinfo("Help!!!","This is Dean Winchester, and I need your help, Linwood Memorial Hospital")



frame_trans = LabelFrame(tab_trans, width = 50, height = 30, bd = 4, padx = 35)
frame_trans.grid(row = 1, column = 0, columnspan = 6, padx = (80,0), pady=10,sticky = W)


top_label = Label(tab_trans, text = "Transaction Details", font = "Garamond 30 bold italic underline", fg = "#4b3300", bg = "#e0ffff")
top_label.grid(row = 0, column = 0,padx=(190,0), pady = 20)

order_label = Label(frame_trans, text = "Order Number", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
order_label.grid(row = 1, column = 0, sticky = W, padx = 2, pady = 10)

name_label = Label(frame_trans, text = "Customer Name", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
name_label.grid(row = 2, column = 0, sticky = W, padx = 2, pady = 10)

add_label = Label(frame_trans, text = "Customer Address", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
add_label.grid(row = 3, column = 0, sticky = W, padx = 2, pady = 10)

add_label = Label(frame_trans, text = "Customer Location", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
add_label.grid(row = 4, column = 0, sticky = W, padx = 2, pady = 10)

phone_label = Label(frame_trans, text = "Customer Phone number", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
phone_label.grid(row = 5, column = 0, sticky = W, padx = 2, pady = 10)

email_label = Label(frame_trans, text = "Customer Email address", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
email_label.grid(row = 6, column = 0, sticky = W, padx = 2, pady = 10)

nso_label = Label(frame_trans, text = "Number of Shoes Ordered", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
nso_label.grid(row = 7, column = 0, sticky = W, padx = 2, pady = 10)


	#-----------------------ENTRIES 1-------------------------------------#

order_text = StringVar()
order_entry = Entry(frame_trans, textvariable = order_text, width = 35, bd = 3)
order_entry.grid(row = 1, column = 1, sticky = W)

name_text = StringVar()
name_entry = Entry(frame_trans, textvariable = name_text, width = 35, bd = 3)
name_entry.grid(row = 2, column = 1, sticky = W)

add_text = StringVar()
add_entry = Entry(frame_trans, textvariable = add_text, width = 35, bd = 3)
add_entry.grid(row = 3, column = 1, sticky = W)

loc_text = StringVar()
loc_entry = ttk.Combobox(frame_trans, cursor = "hand2", textvariable = loc_text, width = 35, state= "readonly")
loc_entry.config(values = ("Lagos","FCT","Rivers","Overseas","Abia","Adamawa","Akwa-Ibom","Anambra","Bauchi","Bayelsa","Benue","Borno","Cross River","Delta","Ebonyi","Edo","Ekiti","Enugu","Gombe","Imo","Jigawa","Kaduna","Kano","Katsina","Kebbi","Kogi","Kwara","Nassarawa","Niger","Ogun","Osun","Oyo","Plateau","Sokoto","Taraba","Yobe","Ondo"))
loc_entry.grid(row = 4, column = 1, sticky = W)

phone_text = StringVar()
phone_entry = Entry(frame_trans, textvariable = phone_text, width = 35, bd = 3)
phone_entry.grid(row = 5, column = 1, sticky = W)

email_text = StringVar()
email_entry = Entry(frame_trans, textvariable = email_text, width = 35, bd = 3)
email_entry.grid(row = 6, column = 1, sticky = W)

nso_text = StringVar()
nso_entry = Spinbox(frame_trans, textvariable = nso_text, cursor = "hand2", from_=0, to = 10000,width = 15, bd = 3)
nso_entry.grid(row = 7, column = 1, sticky = W)


	#-----------------------LABEL 2-------------------------------------#

size_label = Label(frame_trans, text = "Shoe Size", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
size_label.grid(row = 1, column = 2, sticky = W, padx = 20, pady = 10)

nst_label = Label(frame_trans, text = "Number of Shoes Taken", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
nst_label.grid(row = 2, column = 2, sticky = W, padx = 20, pady = 10)

nsr_label = Label(frame_trans, text = "Number of Shoes Rejected", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
nsr_label.grid(row = 3, column = 2, sticky = W, padx = 20, pady = 10)

stat_label = Label(frame_trans, text = "Status of Delivery ", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
stat_label.grid(row = 4, column = 2, sticky = W, padx = 20, pady = 10)

amo_label = Label(frame_trans, text = "Amount Paid", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
amo_label.grid(row = 5, column = 2, sticky = W, padx = 20, pady = 10)

pay_label = Label(frame_trans, text = "Payment Method", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
pay_label.grid(row = 6, column = 2, sticky = W, padx = 20, pady = 10)

date_label = Label(frame_trans, text = "Date", font = "Garamond 15 bold italic", fg = "#ff00ad", bg = "#e0ffff")
date_label.grid(row = 7, column = 2, sticky = W, padx = 20, pady = 10)


	#-----------------------ENTRIES 2-------------------------------------#

size_text = StringVar()
size_entry = Entry(frame_trans, textvariable = size_text ,width = 15, bd = 3)
size_entry.grid(row = 1, column = 3, sticky = W)

nst_text = StringVar()
nst_entry = Spinbox(frame_trans, textvariable = nst_text, cursor = "hand2", from_=0, to = 10000,width = 15, bd = 3)
nst_entry.grid(row = 2, column = 3, sticky = W)

nsr_text = StringVar()
nsr_entry = Spinbox(frame_trans, textvariable = nsr_text,cursor = "hand2", from_=0, to = 10000,width = 15, bd = 3)
nsr_entry.grid(row = 3, column = 3, sticky = W)

amo_text = StringVar()
amo_entry = Entry(frame_trans, textvariable = amo_text, width = 15, bd = 3)
amo_entry.grid(row = 5, column = 3, sticky = W)

stat_text = StringVar()
stat_entry = ttk.Combobox(frame_trans, cursor = "hand2", textvariable = stat_text, state= "readonly")
stat_entry.config(values = ("Fully Delivered", "Partially Delivered","Rejected","Cancelled", "Rescheduled","In Transit"))
stat_entry.grid(row = 4, column = 3, sticky = W)

pay_text = StringVar()
pay_entry = ttk.Combobox(frame_trans, cursor = "hand2", textvariable = pay_text, state= "readonly")
pay_entry.config(values = ("Cash", "POS","Paystack","Bank Transfer", "Courier","Store Credit"))
pay_entry.grid(row = 6, column = 3, sticky = W)

date_text = StringVar()
date_entry = DateEntry(frame_trans, cursor = "hand2", textvariable = date_text, width = 15, bd = 3)
date_entry.grid(row = 7, column = 3, sticky = W)

	#-----------------------BUTTONS-------------------------------------#

add_but_trans = Button(frame_trans, text = "Add Transaction",  cursor = "hand2", bd = 2, fg = "#ff00ad", bg = "#e0ffff", font = "Garamond 15 bold italic",command = add)
add_but_trans.grid(row = 8, column = 1, padx=(20,130), pady = 10)

but_delete_trans = Button(frame_trans, text = "Delete Record",  cursor = "hand2", bd = 2, bg = "crimson", font = "Garamond 15 bold italic", command = delete_record_trans)
but_delete_trans.grid(row = 8, column = 2, pady = 10)

but_edit_trans = Button(frame_trans, text = "Edit Record",  cursor = "hand2", bd = 2, fg = "snow", bg = "teal", font = "Garamond 15 bold italic",command = edit_box_trans)
but_edit_trans.grid(row = 8, column = 0, padx=(20,170), pady = 10)

display_trans = Label(frame_trans, text = "",font = "Garamond 11 bold italic", fg = "navy")
display_trans.grid(row = 9, column = 2, padx = 5)

	#-----------------------TREEVIEW-------------------------------------#

tree_trans = ttk.Treeview(tab_trans, height = 12, columns = ["","","","","","","","","","","","","","",])
tree_trans.grid(row=10, column = 0, columnspan = 2, padx = 10)

tree_trans.heading("#0",text = "ID")
tree_trans.column("#0", width = 50, anchor = "n")

tree_trans.heading("#1",text = "Order #")
tree_trans.column("#1", width = 80, anchor = "n")

tree_trans.heading("#2",text = "Name")
tree_trans.column("#2", width = 120, anchor = "n")

tree_trans.heading("#3",text = "Address")
tree_trans.column("#3", width = 180, anchor = "n")

tree_trans.heading("#4",text = "State")
tree_trans.column("#4", width = 60, anchor = "n")

tree_trans.heading("#5",text = "Phone")
tree_trans.column("#5", width = 110, anchor = "n")

tree_trans.heading("#6",text = "Email")
tree_trans.column("#6", width = 85, anchor = "n")

tree_trans.heading("#7",text = "S - O")
tree_trans.column("#7", width = 80, anchor = "n")

tree_trans.heading("#8",text = "Size")
tree_trans.column("#8", width = 60, anchor = "n")

tree_trans.heading("#9",text = "S - T")
tree_trans.column("#9", width = 80, anchor = "n")

tree_trans.heading("#10",text = "S - R")
tree_trans.column("#10", width = 80, anchor = "n")

tree_trans.heading("#11",text = "Amount")
tree_trans.column("#11", width = 80, anchor = "n")

tree_trans.heading("#12",text = "Status")
tree_trans.column("#12", width = 80, anchor = "n")

tree_trans.heading("#13",text = "M.O.P")
tree_trans.column("#13", width = 80, anchor = "n")

tree_trans.heading("#14",text = "Date")
tree_trans.column("#14", width = 60, anchor = "n")
view_record_trans()


	#-----------------------SCROLLBAR-------------------------------------#

sb_trans = ttk.Scrollbar(tab_trans, command = tree_trans.yview)
sb_trans.grid(row = 10, column = 2, padx = (0,100), sticky = NS,ipady = 3)
tree_trans.config(yscrollcommand=sb.set)


	#-------------------MENUS AND SUB MENUS--------------------------#


def tick():
	d = datetime.datetime.now()
	mytime = time.strftime("%I : %M : %S%p")
	mydate = "{:%B - %d - %Y}".format(d)
	lblInfo.config(text = mytime + "\t" + mydate)
	lblInfo.after(200,tick)
lblInfo = Label(tab_trans, font = "Garamond 15 bold italic", fg = "blue", bg = "#e0ffff")
lblInfo.grid(row = 0, column = 1)
tick()




#===================MENU AND SUB-MENUS=============================#

#===================ORDER TRANSACTION MENU AND SUB-MENUS=============================#

menu_bar = Menu()
trans_options = Menu()
view_options = Menu()
order_trans = Menu()
order_options = Menu()
so_options = Menu()
st_options = Menu()
sr_options = Menu()




menu_bar.add_cascade(label = "File")

menu_bar.add_cascade(label = "Transactions", menu = trans_options)
trans_options.add_cascade(label = "View", menu = view_options)
view_options.add_command(label = "All Transactions",command = view_record_trans)
view_options.add_command(label = "All Customers",command = view_record_trans_cus)
view_options.add_command(label = "All Lagos Customers",command = view_record_trans_lag)
view_options.add_command(label = "All Out of State Customers",command = view_record_trans_notlag)
view_options.add_separator()
view_options.add_command(label = "Full Deliveries",command = view_record_trans_full)
view_options.add_command(label = "Partial Deliveries",command = view_record_trans_partial)
view_options.add_command(label = "Cancelled Orders",command = view_record_trans_cancel)
view_options.add_command(label = "Rejected Orders",command = view_record_trans_reject)
view_options.add_separator()
view_options.add_command(label = "Cash Orders",command = view_record_trans_cash)
view_options.add_command(label = "POS Orders",command = view_record_trans_pos)
view_options.add_command(label = "Paystack Orders",command = view_record_trans_paystack)
view_options.add_command(label = "Bank Transfer Orders",command = view_record_trans_bt)
view_options.add_command(label = "Courier Paid Orders",command = view_record_trans_courier)


trans_options.add_cascade(label = "Sort", menu = order_trans)
order_trans.add_cascade(label = "Order Transaction by", menu = order_options)
order_options.add_command(label = "Newest",command = view_record_trans_newest)
order_options.add_command(label = "Oldest",command = view_record_trans_oldest)
order_options.add_command(label = "Amount Paid",command = view_record_trans_amo)
order_options.add_command(label = "Shoe Size(Big)",command = view_record_trans_bigsize)
order_options.add_command(label = "Shoe Size(Small)",command = view_record_trans_smallsize)
order_options.add_command(label = "Number of shoes sold",command = view_record_trans_shoessold)


order_trans.add_cascade(label = "Shoes Ordered by", menu = so_options)
so_options.add_command(label = "Highest",command = view_record_trans_sortord)
so_options.add_command(label = "Lowest",command = view_record_trans_sortord1)


order_trans.add_cascade(label = "Shoes Taken by", menu = st_options)
st_options.add_command(label = "Highest",command = view_record_trans_sorttaken)
st_options.add_command(label = "Lowest",command = view_record_trans_sorttaken1)

order_trans.add_cascade(label = "Shoes Rejected by", menu = sr_options)
sr_options.add_command(label = "Highest",command = view_record_trans_sortrej)
sr_options.add_command(label = "Lowest",command = view_record_trans_sortrej)

trans_options.add_command(label = "Statistics")


#===================INVENTORY MENU AND SUB-MENUS=============================#

inv_menu = Menu()
inv_options = Menu()
sort_options = Menu()
date_options = Menu()
qty_options = Menu()
qty1_options = Menu()
qty2_options = Menu()



menu_bar.add_cascade(label = "Inventory", menu = inv_menu)
inv_menu.add_cascade(label = "View", menu = inv_options)
inv_options.add_command(label = "All Inventory", command = view_record_inv)
inv_options.add_command(label = "Big Bags", command = view_record_inv_bb)
inv_options.add_command(label = "Small Bags", command = view_record_sb)
inv_options.add_command(label = "Big Boxes", command = view_record_inv_bbo)
inv_options.add_command(label = "Small Boxes", command = view_record_inv_sbo)
inv_options.add_command(label = "Printer Inks", command = view_record_inv_print)
inv_options.add_command(label = "A4 Paper", command = view_record_inv_a4)
inv_options.add_command(label = "Shoe Polish", command = view_record_inv_pol)
inv_options.add_command(label = "Cellotape", command = view_record_inv_cell)

inv_menu.add_cascade(label = "Sort", menu = sort_options)
sort_options.add_cascade(label = "By Date", menu = date_options)
date_options.add_command(label = "Newest", command = view_record_inv_date)
date_options.add_command(label = "Oldest", command = view_record_inv_date1)

sort_options.add_cascade(label = "By Quantity Purchased", menu = qty_options)
qty_options.add_command(label = "Newest", command = view_record_inv_qtybig)
qty_options.add_command(label = "Oldest", command = view_record_inv_qtysmall)

sort_options.add_cascade(label = "By Quantity Left", menu = qty1_options)
qty1_options.add_command(label = "Newest", command = view_record_inv_qty1big)
qty1_options.add_command(label = "Oldest", command = view_record_inv_qty1small)

sort_options.add_cascade(label = "By Total Quantity Left", menu = qty2_options)
qty2_options.add_command(label = "Newest", command = view_record_inv_qty2big)
qty2_options.add_command(label = "Oldest", command = view_record_inv_qty2small)


#===================MERCHANT MENU AND SUB-MENUS=============================#

menu_bar.add_cascade(label = "Merchants")




menu_bar.add_cascade(label = "Expenses")
menu_bar.add_cascade(label = "Revenue")
menu_bar.add_cascade(label = "Reconciliation")
menu_bar.add_cascade(label = "Sales Report")
menu_bar.add_cascade(label = "About")
menu_bar.add_cascade(label = "Exit", command = root.destroy)



root.configure(menu = menu_bar)










root.mainloop()



















