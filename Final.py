#!/usr/bin/env python3

import sqlite3
import tkinter as tk
from tkinter import *
import prettytable as prettytable
import random as rnd
import copy
from functools import partial
from PIL import ImageTk,Image

POPULATION_SIZE = 9

MUTATION_RATE = 0.01

rooms = []

meeting_times = 23

instructors = []

courses = []

depts = []

def login_sucess():
	root.destroy()
	second = Tk()
	second.title('Welcome')

	second.geometry('300x250')
	Label(second, text="").pack()
	 
	btn1 = Button(second, text = 'Add details', command = add_info) 
	btn1.pack(side = 'top')
	Label(second, text="").pack()

	btn2 = Button(second, text = 'Show information', command = show_info) 
	btn2.pack(side = 'top')
	Label(second, text="").pack()

	btn3 = Button(second, text = 'Generate Timetable', command = main_tt) 
	btn3.pack(side = 'top')
	Label(second, text="").pack()

	second.mainloop() 

def add_info():

	third = Tk()
	third.geometry('300x250')


	def show():

		def insert_sql():
			popup.destroy()
			c.execute("INSERT INTO details VALUES (?,?,?,?)",(semdet.get(),cndet.get(),clicked.get(),clicked2.get()))
			conn.commit()

		popup = Tk()
		popup.geometry('200x150')
		popup.title("Data Added Sucessfully")
		msg = StringVar()
		msg = "Sem -> "+semdet.get()+"\n"+"Course Name -> "+cndet.get()+"\n"+"Faculty added -> "+clicked.get()+" , "+clicked2.get()
		label = Label(popup, text=msg)
		label.pack(side="top", fill="x", pady=10)
		B1 = Button(popup, text="Okay", command = insert_sql)
		B1.pack()
		popup.mainloop()   



	sem = Label(third, text="SEM")
	sem.pack()
	semdet = Entry(third, bd =5)
	semdet.pack()

	cn = Label(third, text="Course Name")
	cn.pack()
	cndet = Entry(third, bd =5)
	cndet.pack()

	options = []
	c.execute('SELECT * FROM Instructors_data')
	ins = c.fetchall()
	for i in range(len(ins)):
		instructor = []
		instructor.append(ins[i][0])
		instructor.append(ins[i][1])
		options.append(instructor)


	clicked = StringVar()
	clicked.set("Choose Faculty")

	drop = OptionMenu(third,clicked,*options).pack()

	clicked2 = StringVar()
	clicked2.set("Choose Faculty")

	drop2 = OptionMenu(third,clicked2,*options).pack()


	But = Button(third, text="ADD", width=10, height=1, command=show).pack()

	third.mainloop() 


def show_info():

	def disp_faculty():
		
		conn = sqlite3.connect('TT_GEN.db')
		c = conn.cursor()
		c.execute('SELECT * FROM Instructors_data')
		inst = c.fetchall()
		c.close()
		conn.close()
		T.insert(END, 'Faculty ID \t\t Faculty Abbr \t\t Faculty Name \n')
		T.insert(END, '-------------------------------------------------------------------------------------------------------\n')
		output = ''
		for x in inst:
			output = output+x[0]+'\t\t'+x[1]+'\t\t'+x[2]+'\n\n'
		return output

	def disp_course():

		conn = sqlite3.connect('TT_GEN.db')
		c = conn.cursor()
		c.execute('SELECT * FROM course_data')
		cou = c.fetchall()
		c.close()
		conn.close()
		T.insert(END, 'Semester \t\t Subject Name \t\t\t\t\t\t Subject Abbr \t\t Faculty Assigned \t\t\t\t Hour Assigned for Lec \t\t Hour assigned for practical \n\n')
		T.insert(END, '--------------------------------------------------------------------------------------------------------------------------------------------------\n')
		output = ''
		for x in cou:
			if x[4] == None:
				output = output+x[0]+'\t\t'+x[1]+'\t\t\t\t\t\t'+x[2]+'\t\t'+x[3]+'\t\t\t\t\t'+x[5]+'\t\t\t\t'+x[6]+'\n\n'
			if x[4] != None:
				output = output+x[0]+'\t\t'+x[1]+'\t\t\t\t\t\t'+x[2]+'\t\t'+x[3]+'\t\t'+x[4]+'\t\t\t'+x[5]+'\t\t\t\t'+x[6]+'\n\n'
		return output


	fourth = Tk()
	fourth.title('INFO')

	fourth.geometry('1250x1500')
	 
	btn1 = Button(fourth, text = 'Faculty Details',command = lambda: (T.delete(1.0,END) , T.insert(END, disp_faculty()))).grid(row=0,column=0) 

	btn2 = Button(fourth, text = 'Course Details',command = lambda: (T.delete(1.0,END) , T.insert(END, disp_course()))).grid(row=0,column=1)

	T = Text(fourth, height=250, width=200) 
	T.grid(row=2,columnspan=2) 

	fourth.mainloop()

def main_tt():

	def disp(lis,T,i):
		T.insert(END,'Day-Time \t\t 8:30-9:30 \t\t9:30-10:30 \t\t10:30-11:30 \t\t11:30-12:30 \t\t1:15-2:15 \t\t2:15-3:15 \t\t3:15-4:15\n')
		output = ''


		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
		output = output + "\t\t    "+lis[i+0][1] + "\t\t   "+lis[i+1][1]+"\t\t   "+lis[i+2][1]+"\t\t   "+lis[i+3][1]+"\t\t   "+lis[i+4][1]+"\t\t   "+lis[i+5][1]+"\t\t   "+lis[i+6][1]+"\n"
		output = output + "Monday \t\t    " + lis[i+0][2] + "\t\t   "+lis[1][2]+"\t\t   "+lis[i+2][2]+"\t\t   "+lis[i+3][2]+"\t\t   "+lis[i+4][2] +"\t\t   "+lis[i+5][2] +"\t\t   "+lis[i+6][2]+"\n"
		output = output + "\t\t    "+lis[i+0][0] +"\t\t   "+ lis[i+1][0] +"\t\t   "+ lis[i+2][0] +"\t\t   "+ lis[i+3][0] +"\t\t   "+ lis[i+4][0] +"\t\t   "+ lis[i+5][0] +"\t\t   "+ lis[i+6][0] +"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"

		output = output + "\t\t    "+lis[i+7][1] + "\t\t   "+lis[i+8][1]+"\t\t   "+lis[i+9][1]+"\t\t   "+lis[i+10][1]+"\t\t   "+lis[i+11][1]+"\t\t   "+lis[i+12][1]+"\t\t   "+lis[i+13][1]+"\n"
		output = output + "Tuesday \t\t    "+lis[i+7][2] + "\t\t   "+lis[i+8][2]+"\t\t   "+lis[i+9][2]+"\t\t   "+lis[i+10][2]+"\t\t   "+lis[i+11][2] +"\t\t   "+lis[i+12][2] +"\t\t   "+lis[i+13][2]+"\n"
		output = output + "\t\t   "+lis[i+7][0] +"\t\t   "+ lis[i+8][0] +"\t\t   "+ lis[i+9][0] +"\t\t   "+ lis[i+10][0] +"\t\t   "+ lis[i+11][0] +"\t\t   "+ lis[i+12][0] +"\t\t   "+ lis[i+13][0] +"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"

		output = output + "\t\t    "+lis[i+14][1] + "\t\t   "+lis[i+15][1]+"\t\t   "+lis[i+16][1]+"\t\t   "+lis[i+17][1]+"\t\t   "+lis[i+18][1]+"\t\t   "+lis[i+19][1]+"\t\t   "+lis[i+20][1]+"\n"
		output = output + "Wednesday \t\t    "+lis[i+14][2] + "\t\t   "+lis[i+15][2]+"\t\t   "+lis[i+16][2]+"\t\t   "+lis[i+17][2]+"\t\t   "+lis[i+18][2] +"\t\t   "+lis[i+19][2] +"\t\t   "+lis[i+20][2]+"\n"
		output = output + "\t\t    "+lis[i+14][0] +"\t\t   "+ lis[i+15][0] +"\t\t   "+ lis[i+16][0] +"\t\t   "+ lis[i+17][0] +"\t\t   "+ lis[i+18][0] +"\t\t   "+ lis[i+19][0] +"\t\t   "+ lis[i+20][0] +"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"		
		
		output = output + "\t\t    "+lis[i+21][1] + "\t\t   "+lis[i+22][1]+"\t\t   "+lis[i+23][1]+"\t\t   "+lis[i+24][1]+"\t\t   "+lis[i+25][1]+"\t\t   "+lis[i+26][1]+"\t\t   "+lis[i+27][1]+"\n"
		output = output + "Thursday \t\t    "+lis[i+21][2] + "\t\t   "+lis[i+22][2]+"\t\t   "+lis[i+23][2]+"\t\t   "+lis[i+24][2]+"\t\t   "+lis[i+25][2] +"\t\t   "+lis[i+26][2] +"\t\t   "+lis[i+27][2]+"\n"
		output = output + "\t\t    "+lis[i+21][0] +"\t\t   "+ lis[i+22][0] +"\t\t   "+ lis[i+23][0] +"\t\t   "+ lis[i+24][0] +"\t\t   "+ lis[i+25][0] +"\t\t   "+ lis[i+26][0] +"\t\t   "+ lis[i+27][0] +"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"

		output = output + "\t\t    "+lis[i+28][1] + "\t\t   "+lis[i+29][1]+"\t\t   "+lis[i+30][1]+"\t\t   "+lis[i+31][1]+"\t\t   "+lis[i+32][1]+"\t\t   "+lis[i+33][1]+"\t\t   "+lis[i+34][1]+"\n"
		output = output + "Friday \t\t    "+lis[i+28][2] + "\t\t   "+lis[i+29][2]+"\t\t   "+lis[i+30][2]+"\t\t   "+lis[i+31][2]+"\t\t   "+lis[i+32][2] +"\t\t  "+lis[i+33][2] +"\t\t   "+lis[i+34][2]+"\n"
		output = output + "\t\t    "+lis[i+28][0] +"\t\t   "+ lis[i+29][0] +"\t\t   "+ lis[i+30][0] +"\t\t   "+ lis[i+31][0] +"\t\t   "+ lis[i+32][0] +"\t\t   "+ lis[i+33][0] +"\t\t   "+ lis[i+34][0] +"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"


		return output

	def disp_A(lis,T,i):
		T.insert(END,'Day-Time \t\t 8:30-9:30 \t\t9:30-10:30 \t\t10:30-11:30 \t\t11:30-12:30 \t\t1:15-2:15 \t\t2:15-3:15 \t\t3:15-4:15\n')
		output = ''


		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
		output = output + "\t\t    "+"OSL-A1-DMD-L8-C31 " +"\t\t\t\t   "+lis[i+0][1]+"\t\t   "+lis[i+1][1]+"\t\t   "+lis[i+2][1]+"\t\t   "+lis[i+3][1]+"\t\t   "+lis[i+4][1]+"\n"
		output = output + "Monday \t\t    " + "OS-A2-SPK-L5-C33" + "\t\t   "+"\t\t   "+lis[i+0][2]+"\t\t   "+lis[i+1][2]+"\t\t   "+lis[i+2][2] +"\t\t   "+lis[i+3][2] +"\t\t   "+lis[i+4][2]+"\n"
		output = output + "\t\t    "+"COA-A3-DPK-L4-A31  " + ""+"\t\t   "+"\t\t   "+ lis[i+0][0] +"\t\t   "+ lis[i+1][0] +"\t\t   "+ lis[i+2][0] +"\t\t   "+ lis[i+3][0] +"\t\t   "+ lis[i+4][0] +"\n"
		output = output + "\t\t    "+"CG-A4-DSK-L5-C33"+"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"

		output = output + "\t\t    "+lis[i+5][1] + "\t\t   "+lis[i+6][1]+"\t\t   "+lis[i+7][1]+"\t\t   "+lis[i+8][1]+"\t\t   "+"   AOA-A1-/SS-L3-A32"+"\t\t\t\t   "+lis[i+9][1]+"\n"
		output = output + "Tuesday \t\t   "+lis[i+5][2] + "\t\t   "+lis[i+6][2]+"\t\t   "+lis[i+7][2]+"\t\t   "+lis[i+8][2]+"\t\t   "+"   CG-A2-DSK-L5-C33" +"\t\t\t\t   "+lis[i+9][2]+"\n"
		output = output + "\t\t   "+lis[i+5][0] +"\t\t   "+ lis[i+6][0] +"\t\t   "+ lis[i+7][0] +"\t\t   "+ lis[i+8][0] +"\t\t   "+ "   OS-A3-SPK-L5-C33 " +"\t\t\t\t   " +lis[i+9][0]  +"\n"
		output = output + "\t\t   "+"\t\t\t\t\t\t\t\t" + "      COA-A4-DPK-L4-A31"+"\t" +"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"

		output = output + "\t\t    "+"CG-A1-DSK-L5-C33"+"\t\t\t\t   "+lis[i+10][1]+"\t\t   "+lis[i+11][1]+"\t\t   "+lis[i+12][1]+"\t\t   "+"   COA-A1-DPK-L4-A31"+"\n"
		output = output + "Wednesday \t\t    "+"COA-A2-DPK-L4-A31"+"\t\t   "+"\t\t   "+lis[i+10][2]+"\t\t   "+lis[i+11][2]+"\t\t   "+lis[i+12][2] +"\t\t   "+"   OSL-A2-DMD-L8-C31"+"\n"
		output = output + "\t\t    "+"OSL-A3-DMD-L8-C31 "+"\t\t   "+"\t\t   "+lis[i+10][0] +"\t\t   "+ lis[i+11][0] +"\t\t   "+ lis[i+12][0] +"\t\t   "+"   AOA-A3-BNP-L3-A32 "+ "\n"
		output = output + "\t\t    "+"OS-A4-XYZ-L5-C33"+"\t\t\t\t\t\t\t\t\t\t"+ "      AOA-A4-/SS-L3-A32"+"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"		
		
		output = output + "\t\t    "+lis[i+13][1] + "\t\t   "+lis[i+14][1]+"\t\t   "+lis[i+15][1]+"\t\t   "+lis[i+16][1]+"\t\t   "+"   OS-A1-SPK-L5-C33"+"\t\t   "+"\n"
		output = output + "Thursday \t\t    "+lis[i+13][2] + "\t\t   "+lis[i+14][2]+"\t\t   "+lis[i+15][2]+"\t\t   "+lis[i+16][2]+"\t\t   "+"   AOA-A2-SS-L3-A32"+"\n"
		output = output + "\t\t    "+lis[i+13][0] +"\t\t   "+ lis[i+14][0] +"\t\t   "+ lis[i+15][0] +"\t\t   "+ lis[i+16][0] +"\t\t   "+ "   CG-A3-DSK-L6-C35 " +"\t\t   "+"\n"
		output = output + "\t\t    "+"\t\t\t\t\t\t\t\t" + "      OSL-A4-DMD-L8-C31"+"\t" +"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"

		output = output + "\t\t    "+lis[i+17][1] + "\t\t   "+lis[i+18][1]+"\t\t   "+lis[i+19][1]+"\t\t   "+lis[i+20][1]+"\t\t   "+lis[i+21][1]+"\t\t   "+lis[i+22][1]+"\t\t   "+"\n"
		output = output + "Friday \t\t    "+lis[i+17][2] + "\t\t   "+lis[i+18][2]+"\t\t   "+lis[i+19][2]+"\t\t   "+lis[i+20][2]+"\t\t   "+lis[i+21][2] +"\t\t  "+lis[i+22][2] +"\t\t   "+"\n"
		output = output + "\t\t    "+lis[i+17][0] +"\t\t   "+ lis[i+18][0] +"\t\t   "+ lis[i+19][0] +"\t\t   "+ lis[i+20][0] +"\t\t   "+ lis[i+21][0] +"\t\t   "+ lis[i+22][0] +"\t\t   " +"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"


		return output

	def disp_B(lis,T,i):
		T.insert(END,'Day-Time \t\t 8:30-9:30 \t\t9:30-10:30 \t\t10:30-11:30 \t\t11:30-12:30 \t\t1:15-2:15 \t\t2:15-3:15 \t\t3:15-4:15\n')
		output = ''


		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
		output = output + "\t\t    "+lis[i+0][1] + "\t\t   "+lis[i+1][1]+"\t\t   "+"COA-B1-/AL-L4-A31"+"\t\t\t\t   "+lis[i+2][1]+"\t\t   "+lis[i+3][1]+"\t\t   "+lis[i+4][1]+"\n"
		output = output + "Monday \t\t    " + lis[i+0][2] + "\t\t   "+lis[1][2]+"\t\t   "+"CG-B2-DSK-L6-C35"+"\t\t\t\t   "+lis[i+2][2] +"\t\t   "+lis[i+3][2] +"\t\t   "+lis[i+4][2]+"\n"
		output = output + "\t\t    "+lis[i+0][0] +"\t\t   "+ lis[i+1][0] +"\t\t   "+ "COA-B3-DPK-L4-A31 "+"\t\t\t\t   "+ lis[i+2][0] +"\t\t   "+ lis[i+3][0] +"\t\t   "+ lis[i+4][0] +"\n"
		output = output + "\t\t    "+"\t\t\t\t"+"   OS-B4-SPK-L5-C33" + "\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"

		output = output + "\t\t    "+lis[i+5][1] + "\t\t   "+lis[i+6][1]+"\t\t   "+lis[i+7][1]+"\t\t   "+lis[i+8][1]+"\t\t   "+lis[i+9][1]+"\t\t   "+" OSL-B1-DG-L8-C31"+"\n"
		output = output + "Tuesday \t\t    "+lis[i+5][2] + "\t\t   "+lis[i+6][2]+"\t\t   "+lis[i+7][2]+"\t\t   "+lis[i+8][2]+"\t\t   "+lis[i+9][2] +"\t\t   "+" COA-B2-/AL-L4-A31"+"\n"
		output = output + "\t\t   "+lis[i+5][0] +"\t\t   "+ lis[i+6][0] +"\t\t   "+ lis[i+7][0] +"\t\t   "+ lis[i+8][0] +"\t\t   "+ lis[i+9][0] +"\t\t   "+ " OS-B3-XYZ-L7-C32" +"\n"
		output = output + "\t\t   "+"\t\t\t\t\t\t\t\t\t\t" + "    OSL-B4-DG-L8-C31"+"\t" +"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"

		output = output + "\t\t    "+lis[i+10][1] + "\t\t   "+lis[i+11][1]+"\t\t   "+"OS-B1-SPK-L5-C33"+"\t\t\t\t   "+lis[i+12][1]+"\t\t   "+"CG-B1-DSK-L6-C35"+"\n"
		output = output + "Wednesday \t\t    "+lis[i+10][2] + "\t\t   "+lis[i+11][2]+"\t\t   "+"AOA-B2-SS-L3-A32"+"\t\t\t\t   "+lis[i+12][2] +"\t\t   "+"OS-B2-SPK-L5-C33"+"\n"
		output = output + "\t\t    "+lis[i+10][0] +"\t\t   "+ lis[i+11][0] +"\t\t   "+ "AOA-B3-BNP-L3-A32"+"\t\t\t\t   "+ lis[i+12][0] +"\t\t   "+ "CG-B3-XYZ-L6-C36"+"\n"
		output = output + "\t\t    "+"\t\t\t\t"+"   CG-B4-XYZ-L6-C36"+"\t\t\t\t\t\t"+"   COA-B4-DPK-L2-A31"+"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"		
		
		output = output + "\t\t    "+lis[i+13][1] + "\t\t   "+lis[i+14][1]+"\t\t   "+lis[i+15][1]+"\t\t   "+lis[i+16][1]+"\t\t   "+lis[i+17][1]+"\t\t   "+lis[i+18][1]+"\t\t   "+lis[i+19][1]+"\n"
		output = output + "Thursday \t\t    "+lis[i+13][2] + "\t\t   "+lis[i+14][2]+"\t\t   "+lis[i+15][2]+"\t\t   "+lis[i+16][2]+"\t\t   "+lis[i+17][2] +"\t\t   "+lis[i+18][2] +"\t\t   "+lis[i+19][2]+"\n"
		output = output + "\t\t    "+lis[i+13][0] +"\t\t   "+ lis[i+14][0] +"\t\t   "+ lis[i+15][0] +"\t\t   "+ lis[i+16][0] +"\t\t   "+ lis[i+17][0] +"\t\t   "+ lis[i+18][0] +"\t\t   "+ lis[i+19][0] +"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"

		output = output + "\t\t    "+"AOA-B1-BNP-L3-A32"+"\t\t\t\t   "+lis[i+20][1]+"\t\t   "+lis[i+21][1]+"\t\t   "+lis[i+22][1]+"\t\t   "+"\n"
		output = output + "Friday \t\t    "+"OSL-B2-DG-L8-C31"+"\t\t\t\t   "+lis[i+20][2]+"\t\t   "+lis[i+21][2]+"\t\t   "+lis[i+22][2] +"\t\t  "+"\n"
		output = output + "\t\t    "+"OSL-A1-DG-L8-C31  "+ "\t\t\t\t   "+ lis[i+20][0] +"\t\t   "+ lis[i+21][0] +"\t\t   "+ lis[i+22][0] +"\t\t   "+ "\n"
		output = output + "\t\t    "+"AOA-A2-BNP-L3-A32"+"\n"
		output = output + "-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n"


		return output


	def disp_prof():
		
		def pri(ins,idd,iname):
			list1 = indi_teacher(pop,ins)
			if ins == 'DMD':
				list1[0] = ['OSL-A1-SE-L8-C31',' ',' ']
				list1[1] = [' ',' ',' ']
				list1[28] = ['OSL-B2-SE-L8-C31',' ',' ']
				list1[29] = [' ',' ',' ']
				list1[14] = ['OSL-A3-SE-L8-C31',' ',' ']
				list1[15] = [' ',' ',' ']
				list1[12] = ['OSL-B4-SE-L8-C31',' ',' ']
				list1[13] = [' ',' ',' ']
			if ins == 'SPK':
				list1[0] = ['OS-A2-SE-L5-C33',' ',' ']
				list1[1] = [' ',' ',' ']
				list1[11] = ['OS-A3-SE-L5-C33',' ',' ']
				list1[12] = [' ',' ',' ']
				list1[25] = ['OS-A1-SE-L5-C33',' ',' ']
				list1[26] = [' ',' ',' ']
				list1[2] = ['OS-B1-SE-L5-C33',' ',' ']
				list1[3] = [' ',' ',' ']
				list1[16] = ['OS-B2-SE-L5-C33',' ',' ']
				list1[17] = [' ',' ',' ']
				list1[19] = ['OS-B4-SE-L5-C33',' ',' ']
				list1[20] = [' ',' ',' ']

			if ins == 'DPK':
				list1[0] = ['COA-A3-SE-L4-A31',' ',' ']
				list1[1] = [' ',' ',' ']
				list1[11] = ['COA-A4-SE-L4-A31',' ',' ']
				list1[12] = [' ',' ',' ']
				list1[14] = ['COA-A2-SE-L4-A31',' ',' ']
				list1[15] = [' ',' ',' ']
				list1[19] = ['COA-A1-SE-L4-A31',' ',' ']
				list1[20] = [' ',' ',' ']
				list1[2] = ['COA-B3-SE-L4-A31',' ',' ']
				list1[3] = [' ',' ',' ']
			if ins == 'DSK':
				list1[0] = ['CG-A4-SE-L5-C33',' ',' ']
				list1[1] = [' ',' ',' ']
				list1[11] = ['CG-A2-SE-L5-C33',' ',' ']
				list1[12] = [' ',' ',' ']
				list1[14] = ['CG-A1-SE-L5-C33',' ',' ']
				list1[15] = [' ',' ',' ']
				list1[25] = ['CG-A3-SE-L5-C33',' ',' ']
				list1[26] = [' ',' ',' ']
				list1[2] = ['CG-B1-SE-L5-C33',' ',' ']
				list1[3] = [' ',' ',' ']
				list1[19] = ['CG-B2-SE-L5-C33',' ',' ']
				list1[20] = [' ',' ',' ']
			if ins == '/SS':
				list1[11] = ['AOA-A1-SE-L3-A32',' ',' ']
				list1[12] = [' ',' ',' ']
				list1[19] = ['AOA-A4-SE-L3-A32',' ',' ']
				list1[20] = [' ',' ',' ']
				list1[25] = ['AOA-A2-SE-L3-A32',' ',' ']
				list1[26] = [' ',' ',' ']
				list1[28] = ['AOA-B1-SE-L3-A32',' ',' ']
				list1[29] = [' ',' ',' ']

			if ins == '/AL':
				list1[2] = ['COA-B1-SE-L4-A31',' ',' ']
				list1[3] = [' ',' ',' ']
				list1[12] = ['COA-B2-SE-L4-A31',' ',' ']
				list1[13] = [' ',' ',' ']
				list1[19] = ['COA-B4-SE-L4-A31',' ',' ']
				list1[20] = [' ',' ',' ']
			if ins == 'DG':
				list1[12] = ['OSL-B1-SE-L8-C31',' ',' ']
				list1[13] = [' ',' ',' ']
				list1[19] = ['OSL-A2-SE-L8-C31',' ',' ']
				list1[20] = [' ',' ',' ']
				list1[28] = ['OSL-B3-SE-L8-C31',' ',' ']
				list1[29] = [' ',' ',' ']
				list1[25] = ['OSL-A4-SE-L8-C31',' ',' ']
				list1[26] = [' ',' ',' ']
			if ins == 'BNP':
				list1[19] = ['AOA-A3-SE-L3-A32',' ',' ']
				list1[20] = [' ',' ',' ']
				list1[19] = ['AOA-B2-SE-L3-A32',' ',' ']
				list1[20] = [' ',' ',' ']
				list1[16] = ['AOA-B3-SE-L3-A32',' ',' ']
				list1[17] = [' ',' ',' ']
				list1[28] = ['AOA-B4-SE-L3-A32',' ',' ']
				list1[29] = [' ',' ',' ']



			T.delete(1.0,END)
			T.insert(END, '------------------------------------------'+iname+'----------------------------------------------\n\n')
			output = disp(list1,T,0)
			T.insert(END,output)

		six3 = Tk()
		six3.title('Prof Timetable')
		six3.geometry('1250x1300')
		j,k = -1,-1
		for i in range(len(instructors)):
			if i <= 4:
				b1 = tk.Button(six3, text=instructors[i][2],command=partial(pri,instructors[i][1],instructors[i][0],instructors[i][2])).grid(row=0,column=i,sticky=W)
			else:
				j=j+1
				b1 = tk.Button(six3, text=instructors[i][2],command=partial(pri,instructors[i][1],instructors[i][0],instructors[i][2])).grid(row=1,column=j,sticky=W)
											
		T = Text(six3, height=300, width=300) 
		T.grid(row=5,columnspan=len(instructors)) 
		
		six3.mainloop()

	def disp_room():

		def pri(rname):
			list2 = indi_room(pop,rname)
			T2.delete(1.0,END)
			T2.insert(END, '------------------------------------------'+rname+'----------------------------------------------\n\n')
			output = disp(list2,T2,0)
			T2.insert(END,output)

		six4 = Tk()
		six4.title('Room Timetable')
		six4.geometry('1000x1250')
		j=0
		for i in range(len(rooms)):
			if i <=1:
				b1 = tk.Button(six4, text=rooms[i],command=partial(pri,rooms[i])).grid(row=0,column=i,sticky=W)
			else:
				j=j+1
				b1 = tk.Button(six4, text=rooms[i],command=partial(pri,rooms[i])).grid(row=1,column=j-1,sticky=W)

		T2 = Text(six4, height=250, width=250) 
		T2.grid(row=2,columnspan=len(rooms)) 
			
		six4.mainloop()

	def disp_sem():
		def pri(p,cname,i):
			T3.delete(1.0,END)
			T3.insert(END, '------------------------------------------'+cname+'----------------------------------------------\n\n')
			if cname == "SEA":
				output = disp_A(p,T3,i)
			else:
				output = disp_B(p,T3,i)
			T3.insert(END,output)
		six5 = Tk()
		six5.title('Sem Timetable')
		six5.geometry('1000x1250')
		
		b1 = tk.Button(six5, text="SEA",command=partial(pri,pop[0][1],"SEA",0)).grid(row=0,column=0,sticky=W)
		b2 = tk.Button(six5, text="SEB",command=partial(pri,pop[0][1],"SEB",23)).grid(row=0,column=1,sticky=W)

		T3 = Text(six5, height=250, width=250) 
		T3.grid(row=1,columnspan=2) 
		six5.mainloop()

	def disp_lab():
		def pri(Lname):
			list1 = []
			for i in range(35):
				list1.append(['--','--','--'])
			if Lname == 'L3-A32':
				list1[11] = ['AOA-A1-SE-/SS',' ',' ']
				list1[12] = [' ',' ',' ']
				list1[19] = ['AOA-A4-SE-/SS','AOA-A3-SE-BNP ',' ']
				list1[20] = [' ',' ',' ']
				list1[25] = ['AOA-A2-SE-/SS',' ',' ']
				list1[26] = [' ',' ',' ']
				list1[28] = ['AOA-B1-SE-/SS','AOA-B4-SE-BNP ',' ']
				list1[29] = [' ',' ',' ']
				list1[16] = ['AOA-B3-SE-BNP',' ',' ']
				list1[17] = [' ',' ',' ']
			if Lname == 'L4-A31':
				list1[2] = ['COA-B1-SE-/AL','COA-B3-SE-DPK ',' ']
				list1[3] = [' ',' ',' ']
				list1[12] = ['COA-B2-SE-/AL',' ',' ']
				list1[13] = [' ',' ',' ']
				list1[19] = ['COA-B4-SE-/AL','COA-A1-SE-DPK ',' ']
				list1[20] = [' ',' ',' ']
				list1[0] = ['COA-A3-SE-DPK',' ',' ']
				list1[1] = [' ',' ',' ']
				list1[11] = ['COA-A4-SE-DPK',' ',' ']
				list1[14] = ['COA-A2-SE-DPK',' ',' ']
				list1[15] = [' ',' ',' ']
			if Lname == 'L5-C33':
				list1[0] = ['OS-A2-SE-SPK',' ',' ']
				list1[1] = [' ',' ',' ']
				list1[11] = ['OS-A3-SE-SPK',' ',' ']
				list1[12] = [' ',' ',' ']
				list1[25] = ['OS-A1-SE-SPK',' ',' ']
				list1[26] = [' ',' ',' ']
				list1[2] = ['OS-B1-SE-SPK',' ',' ']
				list1[3] = [' ',' ',' ']
				list1[16] = ['OS-B2-SE-SPK',' ',' ']
				list1[17] = [' ',' ',' ']
				list1[19] = ['OS-B4-SE-SPK',' ',' ']
				list1[20] = [' ',' ',' ']
			if Lname == 'L6-C34':
				list1[0] = ['CG-A4-SE-DSK',' ',' ']
				list1[1] = [' ',' ',' ']
				list1[11] = ['CG-A2-SE-DSK',' ',' ']
				list1[12] = [' ',' ',' ']
				list1[14] = ['CG-A1-SE-DSK',' ',' ']
				list1[15] = [' ',' ',' ']
				list1[25] = ['CG-A3-SE-DSK',' ',' ']
				list1[26] = [' ',' ',' ']
				list1[2] = ['CG-B1-SE-DSK',' ',' ']
				list1[3] = [' ',' ',' ']
				list1[19] = ['CG-B2-SE-DSK',' ',' ']
				list1[20] = [' ',' ',' ']
			if Lname == 'L8-C31':
				list1[0] = ['OSL-A1-SE-DMD',' ',' ']
				list1[1] = [' ',' ',' ']
				list1[28] = ['OSL-B2-SE-DMD','OSL-B3-SE-DG ',' ']
				list1[29] = [' ',' ',' ']
				list1[14] = ['OSL-A3-SE-DMD',' ',' ']
				list1[15] = [' ',' ',' ']
				list1[12] = ['OSL-B4-SE-DMD','OSL-B1-SE-DG ',' ']
				list1[13] = [' ',' ',' ']
				list1[19] = ['OSL-A2-SE-DG',' ',' ']
				list1[20] = [' ',' ',' ']
				list1[25] = ['OSL-A4-SE-DG',' ',' ']
				list1[26] = [' ',' ',' ']

			T3.delete(1.0,END)
			T3.insert(END, '------------------------------------------'+Lname+'----------------------------------------------\n\n')
			output = disp(list1,T3,0)
			T3.insert(END,output)

		six6 = Tk()
		six6.title('Lab Timetable')
		six6.geometry('1000x1250')
		b1 = tk.Button(six6, text='L3-A32',command=partial(pri,'L3-A32')).grid(row=0,column=0,sticky=W)
		b1 = tk.Button(six6, text='L4-A31',command=partial(pri,'L4-A31')).grid(row=0,column=1,sticky=W)
		b1 = tk.Button(six6, text='L5-C33',command=partial(pri,'L5-C33')).grid(row=0,column=2,sticky=W)
		b1 = tk.Button(six6, text='L8-C31',command=partial(pri,'L8-C31')).grid(row=1,column=1,sticky=W)
		b1 = tk.Button(six6, text='L6-C34',command=partial(pri,'L6-C34')).grid(row=1,column=0,sticky=W)
		T3 = Text(six6, height=250, width=250) 
		T3.grid(row=2,columnspan=4) 
		six6.mainloop()

	fifth = Tk()
	fifth.title('Select your Time-table')
	fifth.geometry('300x250')
	Label(fifth, text="").pack()

	button1 = Button(fifth, text='Prof. Timetable', width=25, command=disp_prof) 
	button1.pack(side = 'top')

	Label(fifth, text="").pack()

	button2 = Button(fifth, text='Room Timetable', width=25, command=disp_room) 
	button2.pack(side = 'top')

	Label(fifth, text="").pack()

	button3 = Button(fifth, text='Class Timetable', width=25, command=disp_sem) 
	button3.pack(side = 'top')

	Label(fifth, text="").pack()

	button4 = Button(fifth, text='Lab Timetable', width=25, command=disp_lab) 
	button4.pack(side = 'top')

	Label(fifth, text="").pack()



	def init_data():
		c.execute('SELECT * FROM room_data')
		rom = c.fetchall()
		for i in range(len(rom)):
			rooms.append(rom[i][0])
		print(rooms)

		c.execute('SELECT * FROM Instructors_data')
		ins = c.fetchall()
		for i in range(len(ins)):
			instructor = []
			instructor.append(ins[i][0])
			instructor.append(ins[i][1])
			instructor.append(ins[i][2])
			instructors.append(instructor)
		print(rooms)
		print(instructors)
		print(len(instructors))
		print()

		c.execute('SELECT * FROM course_data')
		cou = c.fetchall()
		for i in range(len(cou)):
			course = []
			course.append(cou[i][1])
			course.append(cou[i][2])
			instruct = []
			instruct.append(cou[i][3])
			if cou[i][4] != None:
				instruct.append(cou[i][4])
			course.append(instruct)
			courses.append(course)
		print(courses)

	def conflicts(li,j):
		num = 0
		return num
		c1,c2,c3,c4,c5,c6 = 0,0,0,0,0,0
		for i in range(j,j+23):
			if li[i][1] == "OOPM": c1 += 1
			if li[i][1] == "DS": c2 += 1
			if li[i][1] == "DM": c3 += 1
			if li[i][1] == "AM-3": c4 += 1
			if li[i][1] == "ECCF": c5 += 1
			if li[i][1] == "DLDA": c6 += 1
		if c1 != 2:
			num += 1
		if c2 != 4:
			num += 1
		if c3 != 4:
			num += 1
		if c4 != 5:
			num += 1
		if c5 != 4:
			num += 1
		if c6 != 4:
			num += 1

		return num

	def schedule_initialize():

		schedule = []
		for i in range(meeting_times):
			classes = []
			classes.append('B-31')
			cou = courses[rnd.randrange(0,len(courses))]
			classes.append(cou[1])
			classes.append(cou[2][rnd.randrange(0,len(cou[2]))])
			schedule.append(classes)
		for i in range(meeting_times,2*meeting_times):
			classes = []
			classes.append('B-32')
			cou = courses[rnd.randrange(0,len(courses))]
			classes.append(cou[1])
			classes.append(cou[2][rnd.randrange(0,len(cou[2]))])
			schedule.append(classes)
		return schedule

	def cal_fitness(li):
		number_of_conflicts = 0
		for i in range(0,23):
			if li[i][0] == li[i+23][0]: number_of_conflicts += 1
			if li[i][2][0] == li[i+23][2][0]: number_of_conflicts += 1


		number_of_conflicts += conflicts(li,0)
		number_of_conflicts += conflicts(li,23)

		return number_of_conflicts

	def get_fitness(sch):
		Popuation = []
		for i in range(0,POPULATION_SIZE):
			con = []
			con.append(cal_fitness(sch[i]))
			con.append(sch[i])
			Popuation.append(con)
		return Popuation

	def evolve(population): return mutate_population(crossover_population(population))

	def crossover_population(popu):
		crossover_pop = []
		for i in range(1):
			crossover_pop.append(popu[i][1])
		i = 1
		while i < POPULATION_SIZE:
			schedule1 = select_tournament_population(popu)[0][1]
			schedule2 = select_tournament_population(popu)[0][1]
			crossover_pop.append(crossover_schedule(schedule1,schedule2))
			i +=1
		return crossover_pop

	def select_tournament_population(popu):
		tournament_pop = []
		i=0
		while i < POPULATION_SIZE:
			tournament_pop.append(popu[rnd.randrange(0,POPULATION_SIZE)][1])
			i += 1
		tournament_pop = get_fitness(tournament_pop)
		tournament_pop.sort()
		return tournament_pop

	def crossover_schedule(schedule1, schedule2):
		crossoverSchedule = schedule_initialize()
		for i in range(0, len(crossoverSchedule)):
			if(rnd.random() > 0.5): crossoverSchedule[i] = schedule1[i]
			else: crossoverSchedule[i] = schedule2[i]
		return crossoverSchedule


	def mutate_population(schedules):
		for i in range(1, POPULATION_SIZE):
			schedules[i] = mutate_schedule(schedules[i])
		return schedules


	def mutate_schedule(mutateSchedule):
		schedule = schedule_initialize()
		flag=0
		for i in range(0, len(mutateSchedule)):
			if(MUTATION_RATE > rnd.random()): mutateSchedule[i] = schedule[i]
		return mutateSchedule

	def print_dept(depts):
		availableDeptsTable = prettytable.PrettyTable(['dept','courses'])
		for i in range(0, len(depts)):
			courses = depts[i][1]
			tempStr = "["
			for j in range(0, len(courses)-1):
				tempStr += str(courses[j]) + ", "
			tempStr += str(courses[len(courses) - 1]) + "]"
			availableDeptsTable.add_row([depts[i][0], tempStr])
		print(availableDeptsTable)

	def print_course(courses):
		availableCoursesTable = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'instructors'])
		for i in range(0, len(courses)):
			instructors = courses[i][2]
			tempStr = ""
			for j in range(0, len(instructors)-1):
				tempStr += instructors[j] + ", "
			tempStr += instructors[len(instructors) - 1]
			availableCoursesTable.add_row([courses[i][0], courses[i][1], tempStr])
		print(availableCoursesTable)

	def print_instructor(instructors):
		availableInstructorsTable = prettytable.PrettyTable(['id','instructor'])
		for i in range(0, len(instructors)):
			availableInstructorsTable.add_row([instructors[i][0], instructors[i][1]])
		print(availableInstructorsTable)

	def print_room(rooms):
		availableRoomsTable = prettytable.PrettyTable(['room #','max seating capacity'])
		for i in range(0, len(rooms)):
			availableRoomsTable.add_row([str(rooms[i][0])])
		print(availableRoomsTable)

	def print_schedule_as_table_A(classes,i):
		table = prettytable.PrettyTable(['Day/Time','8:30-9:30','9:30-10:30','10:30-11:30','11:30-12:30','Break','1:15-2:15','2:15-3:15','3:15-4:15'])
		table.add_row(['Monday', "LAB" + "\n",
					   "LAB" + "\n",
					 classes[i+0][1] + "\n" + classes[i+0][0] + "\n" + classes[i+0][2] +"\n",
					 classes[i+1][1] + "\n" + classes[i+1][0] + "\n" + classes[i+1][2] +"\n",
					 '',
					 classes[i+2][1] + "\n" + classes[i+2][0] + "\n" + classes[i+2][2] +"\n",
					 classes[i+3][1] + "\n" + classes[i+3][0] + "\n" + classes[i+3][2] +"\n",
					 classes[i+4][1] + "\n" + classes[i+4][0] + "\n" + classes[i+4][2] +"\n",])
		table.add_row(['Tuesday', classes[i+5][1] + "\n" + classes[i+5][0] + "\n" + classes[i+5][2] +"\n",
					 classes[i+6][1] + "\n" + classes[i+6][0] + "\n" + classes[i+6][2] +"\n",
					 classes[i+7][1] + "\n" + classes[i+7][0] + "\n" + classes[i+7][2] +"\n",
					 classes[i+8][1] + "\n" + classes[i+8][0] + "\n" + classes[i+8][2] +"\n",
					 '',
					 "LAB" + "\n",
					 "LAB" + "\n",
					 classes[i+9][1] + "\n" + classes[i+9][0] + "\n" + classes[i+9][2] +"\n",])
		table.add_row(['Wednesday', "LAB" + "\n",
					 "LAB" + "\n",
					 classes[i+10][1] + "\n" + classes[i+10][0] + "\n" + classes[i+10][2] +"\n",
					 classes[i+11][1] + "\n" + classes[i+11][0] + "\n" + classes[i+11][2] +"\n",
					 '',
					 classes[i+12][1] + "\n" + classes[i+12][0] + "\n" + classes[i+12][2] +"\n",
					 "----- " + "\n",
					 "-------" + "\n",])
		table.add_row(['Thursday', classes[i+13][1] + "\n" + classes[i+13][0] + "\n" + classes[i+13][2] +"\n",
					 classes[i+14][1] + "\n" + classes[i+14][0] + "\n" + classes[i+14][2] +"\n",
					 classes[i+15][1] + "\n" + classes[i+15][0] + "\n" + classes[i+15][2] +"\n",
					 classes[i+16][1] + "\n" + classes[i+16][0] + "\n" + classes[i+16][2] +"\n",
					 '',
					 "LAB" + "\n",
					 "LAB" + "\n",
					 "------" + "\n",])
		table.add_row(['Friday', classes[i+17][1] + "\n" + classes[i+17][0] + "\n" + classes[i+17][2] +"\n",
					 classes[i+18][1] + "\n" + classes[i+18][0] + "\n" + classes[i+18][2] +"\n",
					 classes[i+19][1] + "\n" + classes[i+19][0] + "\n" + classes[i+19][2] +"\n",
					 classes[i+20][1] + "\n" + classes[i+20][0] + "\n" + classes[i+20][2] +"\n",
					 '',
					 classes[i+21][1] + "\n" + classes[i+21][0] + "\n" + classes[i+21][2] +"\n",
					 classes[i+22][1] + "\n" + classes[i+22][0] + "\n" + classes[i+22][2] +"\n",
					 "-----" + "\n",])
		print(table)

	def print_schedule_as_table_B(classes,i):
		table = prettytable.PrettyTable(['Day/Time','8:30-9:30','9:30-10:30','10:30-11:30','11:30-12:30','Break','1:15-2:15','2:15-3:15','3:15-4:15'])
		table.add_row(['Monday',classes[i+0][1] + "\n" + classes[i+0][0] + "\n" + classes[i+0][2] +"\n",
					 classes[i+1][1] + "\n" + classes[i+1][0] + "\n" + classes[i+1][2] +"\n",
					   "LAB" + "\n",
					   "LAB" + "\n",
					 '',
					 classes[i+2][1] + "\n" + classes[i+2][0] + "\n" + classes[i+2][2] +"\n",
					 classes[i+3][1] + "\n" + classes[i+3][0] + "\n" + classes[i+3][2] +"\n",
					 classes[i+4][1] + "\n" + classes[i+4][0] + "\n" + classes[i+4][2] +"\n",])
		table.add_row(['Tuesday', classes[i+5][1] + "\n" + classes[i+5][0] + "\n" + classes[i+5][2] +"\n",
					 classes[i+6][1] + "\n" + classes[i+6][0] + "\n" + classes[i+6][2] +"\n",
					 classes[i+7][1] + "\n" + classes[i+7][0] + "\n" + classes[i+7][2] +"\n",
					 classes[i+8][1] + "\n" + classes[i+8][0] + "\n" + classes[i+8][2] +"\n",
					 '',
					 classes[i+9][1] + "\n" + classes[i+9][0] + "\n" + classes[i+9][2] +"\n",
					 "LAB" + "\n",
					 "LAB" + "\n",
					 ])
		table.add_row(['Wednesday',classes[i+10][1] + "\n" + classes[i+10][0] + "\n" + classes[i+10][2] +"\n",
					 classes[i+11][1] + "\n" + classes[i+11][0] + "\n" + classes[i+11][2] +"\n",
					 "LAB" + "\n",
					 "LAB" + "\n",
					 
					 '',
					 classes[i+12][1] + "\n" + classes[i+12][0] + "\n" + classes[i+12][2] +"\n",
					 "----- " + "\n",
					 "-------" + "\n",])
		table.add_row(['Thursday', classes[i+13][1] + "\n" + classes[i+13][0] + "\n" + classes[i+13][2] +"\n",
					 classes[i+14][1] + "\n" + classes[i+14][0] + "\n" + classes[i+14][2] +"\n",
					 classes[i+15][1] + "\n" + classes[i+15][0] + "\n" + classes[i+15][2] +"\n",
					 classes[i+16][1] + "\n" + classes[i+16][0] + "\n" + classes[i+16][2] +"\n",
					 '',
					 classes[i+17][1] + "\n" + classes[i+17][0] + "\n" + classes[i+17][2] +"\n",
					 classes[i+18][1] + "\n" + classes[i+18][0] + "\n" + classes[i+18][2] +"\n",
					 classes[i+19][1] + "\n" + classes[i+19][0] + "\n" + classes[i+19][2] +"\n",])
		table.add_row(['Friday', "LAB" + "\n",
					 "LAB" + "\n",
					 classes[i+20][1] + "\n" + classes[i+20][0] + "\n" + classes[i+20][2] +"\n",
					 classes[i+21][1] + "\n" + classes[i+21][0] + "\n" + classes[i+21][2] +"\n",
					 '',
					 classes[i+22][1] + "\n" + classes[i+22][0] + "\n" + classes[i+22][2] +"\n",
					 "-----" + "\n",
					 "------" + "\n",])
		print(table)

	def indi_teacher(tpop,ins):

		def mergee(l,i):
			for j in range(35):
				if l[i+j][0] != '--':
					list1[j] = l[i+j]
					list1[j][0] = "SEB"
			return list1

		def print_individual_tt(cpop,ins):
			for i in range(len(cpop)):
				if cpop[i][2] != ins:
					cpop[i][0] = "--"
					cpop[i][1] = "--"
					cpop[i][2] = "--"

			return cpop

		cpop = copy.deepcopy(tpop[0][1])

		cpop.insert(0,['--','--','--'])
		cpop.insert(1,['--','--','--'])
		cpop.insert(11,['--','--','--'])
		cpop.insert(12,['--','--','--'])
		cpop.insert(14,['--','--','--'])
		cpop.insert(15,['--','--','--'])
		cpop.insert(19,['--','--','--'])
		cpop.insert(20,['--','--','--'])
		cpop.insert(25,['--','--','--'])
		cpop.insert(26,['--','--','--'])
		cpop.insert(27,['--','--','--'])
		cpop.insert(34,['--','--','--'])
		cpop.insert(37,['--','--','--'])
		cpop.insert(38,['--','--','--'])
		cpop.insert(47,['--','--','--'])
		cpop.insert(48,['--','--','--'])
		cpop.insert(51,['--','--','--'])
		cpop.insert(52,['--','--','--'])
		cpop.insert(54,['--','--','--'])
		cpop.insert(55,['--','--','--'])
		cpop.insert(63,['--','--','--'])
		cpop.insert(64,['--','--','--'])
		cpop.append(['--','--','--'])
		cpop.append(['--','--','--'])


		teacher = print_individual_tt(cpop,ins)

		list1 = copy.deepcopy(teacher)
		for i in range(35):
			if list1[i][0] != "--":
				list1[i][0] = "SEA"

		list1 = mergee(list1,35)
		
		return list1

	def indi_room(rpop,ins):

		def mergee(l,i):
			for j in range(35):
				if l[i+j][1] != '--':
					list2[j] = l[i+j]
					list2[j][0] = "SEB"
			return list2

		def print_individual_tt(cpop,ins):
			for i in range(len(cpop)):
				if cpop[i][0] != ins:
					cpop[i][0] = "--"
					cpop[i][1] = "--"
					cpop[i][2] = "--"
			return cpop
		
		cpop = copy.deepcopy(rpop[0][1])
		cpop.insert(0,['--','--','--'])
		cpop.insert(1,['--','--','--'])
		cpop.insert(11,['--','--','--'])
		cpop.insert(12,['--','--','--'])
		cpop.insert(14,['--','--','--'])
		cpop.insert(15,['--','--','--'])
		cpop.insert(19,['--','--','--'])
		cpop.insert(20,['--','--','--'])
		cpop.insert(25,['--','--','--'])
		cpop.insert(26,['--','--','--'])
		cpop.insert(27,['--','--','--'])
		cpop.insert(34,['--','--','--'])


		cpop.insert(37,['--','--','--'])
		cpop.insert(38,['--','--','--'])
		cpop.insert(47,['--','--','--'])
		cpop.insert(48,['--','--','--'])
		cpop.insert(51,['--','--','--'])
		cpop.insert(52,['--','--','--'])
		cpop.insert(54,['--','--','--'])
		cpop.insert(55,['--','--','--'])
		cpop.insert(63,['--','--','--'])
		cpop.insert(64,['--','--','--'])
		cpop.append(['--','--','--'])
		cpop.append(['--','--','--'])

		rom = print_individual_tt(cpop,ins)

		list2 = copy.deepcopy(rom)

		for i in range(35):
			if list2[i][0] != "--":
				list2[i][0] = "SEA"

		list2 = mergee(list2,35)
		
		return list2

	init_data()

	Schedule = []
	for i in range(0,POPULATION_SIZE): Schedule.append(schedule_initialize())
	generationNumber = 0
	pop = get_fitness(Schedule)
	pop.sort()
	print(Schedule)
	while(pop[0][0] > 0):
		generationNumber +=1
		pop = evolve(pop)
		pop = get_fitness(pop)
		print("\n> Generation # " + str(generationNumber)+ "   "+ str(pop[0][0]))
		pop.sort()

		pop[0][1][0] = ['B-31','OSL','DMD']
		pop[0][1][23] = ['B-32','OSL','DMD']
		pop[0][1][34] = ['B-32','OSL','DMD']
		pop[0][1][1] = ['B-31','AM-4','/RG']
		pop[0][1][9] = ['B-31','AM-4','/RG']
		pop[0][1][11] = ['B-31','AM-4','/RG']
		pop[0][1][18] = ['B-31','AM-4','/RG']
		pop[0][1][23] = ['B-32','AM-4','/RG']
		pop[0][1][32] = ['B-32','AM-4','/RG']
		pop[0][1][33] = ['B-32','AM-4','/RG']
		pop[0][1][41] = ['B-32','AM-4','/RG']
		pop[0][1][10] = ['B-31','COA','DPK']
		pop[0][1][17] = ['B-31','COA','DPK']
		pop[0][1][40] = ['B-32','COA','DPK']

	print("\n> Generation # " + str(generationNumber)+ "   "+ str(pop[0][0]))
	print("-----------------------------------------------Timetable for SEA --------------------------------------")
	print(pop[0][1])
	print_schedule_as_table_A(pop[0][1],0)
	print("-----------------------------------------------Timetable for SEB --------------------------------------")
	print_schedule_as_table_B(pop[0][1],23)
	print()
	l = []



	fifth.mainloop() 

def password_not_recognised():
	Label(root, text = "Invalid Password").pack()

def user_not_found():
	Label(root, text = "Invalid Username").pack()

def login_verify():
	user = username_verify.get()
	pas = password_verify.get()
	c.execute('select * from login')
	rows = c.fetchall()
	for i in range(len(rows)):
		if rows[i][0] == user:
			if rows[i][1] == pas:
				login_sucess()
			else:
				password_not_recognised()
	else:
		user_not_found()

def login_screen():
	global root,username_login_entry,password_login_entry,second,third,fourth,fifth,six6,six5,six4,six3,six2,six1,T
	root = tk.Tk()
	root.geometry("300x250")
	root.title('Account Login')

	#canvas = Canvas(root,width=300,height=250)
	#image = ImageTk.PhotoImage(Image.open("tt2.png"))
	#canvas.create_image(0,0,anchor=NW,image=image)


	global username_verify, password_verify

	username_verify = StringVar()
	password_verify = StringVar()

	photo = PhotoImage(file = r"user.png") 
	photoimage = photo.subsample(6, 6) 
	Label(root, text = 'Username', image = photoimage, compound = LEFT).pack(side = TOP) 

	#Label(root, text="Username ").pack()
	username_login_entry = Entry(root,textvariable = username_verify).pack()
	Label(root, text="").pack()

	photo2 = PhotoImage(file = r"lock.png") 
	photoimage2 = photo2.subsample(6, 6) 
	Label(root, text = 'Password', image = photoimage2, compound = LEFT).pack(side = TOP)

	password_login_entry = Entry(root, textvariable=password_verify, show='*').pack()
	Label(root, text="").pack()
	Button(root, text="LOGIN", width=10, height=1, command = login_verify).pack()
	#canvas.pack()

	root.mainloop()

conn = sqlite3.connect('TT_GEN.db')
c = conn.cursor()
login_screen()
conn.close()