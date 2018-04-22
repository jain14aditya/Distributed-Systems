###### This is for the main server gui code , 

import tkinter
import socket
from tkinter import *
from tkinter import simpledialog
from tkinter.ttk import *
import calendar


# import tkinter.messagebox
# import ttkcalender
# import tkSimpleDialog.Dialog
ip = '192.168.0.11'
port = 12559		
E1 = None,E2 = None,E3 = None,DropBoxTo = None , DropBoxFrom = None ,Frame = None
		 

def CheckCallBack() :

	global E1,E2,E3,DropBoxTo,DropBoxFrom,Frame
	# here we need to take a message and parse it back to the central server
	# Create a socket object
	if (checkDate(E3.get()) ) == False :
		tkinter.messagebox.showinfo(" Please enter correct Date")
		return

	if E1.get().isdigit() == False or  (E1.get().isdigit() == True and (E1.get() < 1 or E1.get() > 10000 ) ) :
		tkinter.messagebox.showinfo(" Please enter correct Budget.Shouldnt exceed 10000")
		return

	if E2.get().isdigit() == False or  (E2.get().isdigit() == True and (E2.get() < 1 or E2.get() > 4 ) ) :	
		tkinter.messagebox.showinfo(" Please enter correct Budget.Shouldnt exceed 4 " )
		return

	s = socket.socket()			

	# connect to the server on local computer
	s.connect((ip, port))

	dicte = {}
	dicte['to'] = DropBoxTo.first_selected_option.text

	dicte['from'] = DropBoxFrom.first_selected_option.text

	dicte['budget'] = E1.get()
	dicte['date'] = E3.get()
	dicte['people'] = E2.get()
	dicte['type'] = 1

	dict =  json.dumps(dicte).encode('utf-8')
	
	s.sendall(dict)


def checkDate(date) :

	global E1,E2,E3,DropBoxTo,DropBoxFrom,Frame

	yy,mm,dd=E3.split('-')

	if yy.isdigit() == False or len(yy) !=4 :
		return False
	if mm.isdigit() == False or len(mm) !=2 :
		return False
	if dd.isdigit() == False or len(dd) !=2 :
		return False

	dd=int(dd)
	mm=int(mm)
	yy=int(yy)
	
	if(mm==1 or mm==3 or mm==5 or mm==7 or mm==8 or mm==10 or mm==12):
		max1=31
	elif(mm==4 or mm==6 or mm==9 or mm==11):
		max1=30
	elif(yy%4==0 and yy%100!=0 or yy%400==0):
		max1=29
	else:
		max1=28
	
	if(mm<1 or mm>12):
		return False

	elif(dd<1 or dd>max1):
		return False
	elif (yy < 1) :
		return False


	return True




def BookCallBack() :

	global E1,E2,E3,DropBoxTo,DropBoxFrom,Frame
	# here we need to take a message and parse it back to the central server
	# Create a socket object
	if (checkDate(E3.get()) ) == False :
		tkinter.messagebox.showinfo(" Please enter correct Date")
		return

	if E1.get().isdigit() == False or  (E1.get().isdigit() == True and (E1.get() < 1 or E1.get() > 10000 ) ) :
		tkinter.messagebox.showinfo(" Please enter correct Budget.Shouldnt exceed 10000")
		return

	if E2.get().isdigit() == False or  (E2.get().isdigit() == True and (E2.get() < 1 or E2.get() > 4 ) ) :	
		tkinter.messagebox.showinfo(" Please enter correct Budget.Shouldnt exceed 4 " )
		return

	s = socket.socket()			

	# connect to the server on local computer
	s.connect((ip, port))

	dicte = {}
	dicte['to'] = DropBoxTo.first_selected_option.text

	dicte['from'] = DropBoxFrom.first_selected_option.text

	dicte['budget'] = E1.get()
	dicte['date'] = E3.get()
	dicte['people'] = E2.get()
	dicte['type'] = 2

	dict =  json.dumps(dicte).encode('utf-8')
	
	s.sendall(dict)


def main() :

	global E1,E2,E3,DropBoxTo,DropBoxFrom,Frame

	top = tkinter.Tk()
	top.geometry("800x800+0+0")

	# use a colorful frame
	frame = tkinter.Frame(top, bg='green')
	frame.pack(fill='both', expand='yes')

	
	labelTo = Label(frame,width=10,text = "From",relief = RAISED)
	labelTo.place(x=100,y=200)

	labelFrom = Label(frame,width=10,text="To",relief = RAISED)
	labelFrom.place(x=100,y=300)


	variable = StringVar(frame)
	variable.set("A")

	variable2 = StringVar(frame)
	variable2.set("A")

	DropBoxTo = OptionMenu(frame,variable,"A","B","C","D")
	DropBoxTo.place(x=200,y=200)


	DropBoxFrom = OptionMenu(frame,variable2,"A","B","C","D")
	DropBoxFrom.place(x=200,y=300)

	L1 = Label(frame, text="Budget")
	L1.place(x=100,y=400)

	E1 = Entry(frame,width =10)
	E1.place(x=200,y=400)


	L2 = Label(frame, text="People")
	L2.place(x=300,y=400)

	E2 = Entry(frame,width =10)
	E2.place(x=400,y=400)


	L3 = Label(frame, text="Date")
	L3.place(x=300,y=300)

	E3 = Entry(frame,width =10)
	E3.place(x=400,y=300)

	checkButton = tkinter.Button(frame,text ="Check Availability",command = CheckCallBack,bg= 'yellow')
	checkButton.place(x=100,y=500)
	
	BookButton = tkinter.Button(frame,text ="Book Availability",command = BookCallBack,bg='yellow')
	BookButton.place(x=300,y=500)

	top.mainloop()



if __name__ == "__main__":
	main()