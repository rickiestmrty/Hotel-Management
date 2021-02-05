from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkFont
import time
import datetime
import mysql.connector
from  calendar import monthrange

root = Tk()
root.title("Reservation")
root.resizable(False,False)

DAYS = []
for day in range(0,31):
    DAYS.append(day+1)
MONTH = ["January","February","March","April","May","June",
"July","August","September","Ocotber","November","December"]
YEAR =[2021,2022,2023,2024,2025,2026,2027,2028,2029,2030]
ROOM_TYPE = ["Single","Double","Family"]
FAMROOM = ["F1","F2","F3","F4","N2"]
STDROOM = ["301","302","303","304","305","306"]

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.geometry("+{}+{}".format(positionRight-150,positionDown-200))
helv = tkFont.Font(family='Times New Roman', size=15)

root.config(bg="VioletRed4")
#Title
title_lbl = Label(root, text="N and F Guest House",font=("Courier",25),bg="VioletRed4",fg="burlywood1")
title_lbl.grid(columnspan=4, row=0, ipadx = 25, ipady = 25)

w=650
h=230
checkingFrame = LabelFrame(root,text="Check Availability",width=w,height=h,bg="burlywood1")
bookingFrame = LabelFrame(root,text="Guest Information",width=w,height=h,bg="burlywood1")
editFrame = LabelFrame(root,text="Edit Guest Information",width=w,height=h,bg="burlywood1")
displayFrame = LabelFrame(root,text="Guest List",width=w,height=h,bg="burlywood1")
searchFrame = LabelFrame(root,text="Search Guest Information",width=w,height=h,bg="burlywood1")
updateFrame = LabelFrame(root,text="Update Guest Payment",width=w,height=h,bg="burlywood1")
deleteFrame = LabelFrame(root,text="Delete Guest Information",width=w,height=h,bg="burlywood1")
statsFrame = LabelFrame(root,text="Statistics",width=w,height=h,bg="burlywood1")

miscFrame = LabelFrame(root,text="Navigation",bg="burlywood1")
miscFrame.grid(rowspan=2,column=0, ipadx=5,ipady=5,sticky=N+S)

for frame in (checkingFrame,bookingFrame,editFrame,displayFrame,searchFrame,updateFrame,deleteFrame,statsFrame):
    frame.grid(row=1,column=1, ipadx=5,ipady=5)
    frame.configure(height=frame["height"],width=frame["width"])
    frame.grid_propagate(0)

#SwitchFrames
def raise_frame(frame):
    frame.tkraise()

class roomInfo():
    curr_total = 0
    curr_guests = 0

    def __init__(self):
        pass

    def addInfo(self,total,guest_num):
        self.curr_total = self.curr_total + total
        self.curr_guests = self.curr_guests + guest_num
    
    def resetAttr(self):
        self.curr_total = 0
        self.curr_guests = 0
    
class SideBar:
    for frame in (checkingFrame,bookingFrame,editFrame,displayFrame,searchFrame,updateFrame,deleteFrame,statsFrame):
        for i in range(9):
            frame.rowconfigure(i,weight=1)
            frame.columnconfigure(i,weight=1)
    

    btn_home = Button(miscFrame,text="Home",bg="VioletRed4",fg="burlywood1")
    btn_guest_table = Button(miscFrame, text="Display Guest List",bg="VioletRed4",fg="burlywood1")
    btn_stats = Button(miscFrame,text="Statistics",bg="VioletRed4",fg="burlywood1")
    btn_search = Button(miscFrame,text="Search Guest",bg="VioletRed4",fg="burlywood1")
    btn_edit = Button(miscFrame,text="Edit Guest Info",bg="VioletRed4",fg="burlywood1")
    btn_update = Button(miscFrame,text="Update Payment",bg="VioletRed4",fg="burlywood1")
    btn_delete = Button(miscFrame,text="Delete Guest",bg="VioletRed4",fg="burlywood1")
    separatelbl = Label(miscFrame,text="-----",bg="burlywood1")

    btn_home.grid(row=0,sticky=W+E)
    btn_guest_table.grid(row=1,sticky=W+E)
    btn_stats.grid(row=2,sticky=W+E)
    separatelbl.grid(row=3,sticky=W+E)
    btn_search.grid(row=4,sticky=W+E)
    btn_edit.grid(row=5,sticky=W+E)
    btn_update.grid(row=6,sticky=W+E)
    btn_delete.grid(row=7,sticky=W+E)

    guest_name_entry = Entry(editFrame)
    guest_contact_entry = Entry(editFrame)
    guest_roomnum_entry = Entry(editFrame)
    guest_balance_entry = Entry(editFrame)
    guest_checkIn_entry = Entry(editFrame)
    guest_checkOut_entry = Entry(editFrame)
    guest_payments_entry = Entry(editFrame)
    guest_name_lbl = Label(editFrame, text="Name",font=("Arial",9))
    guest_contactlbl = Label(editFrame, text="Contact",font=("Arial",9))
    guest_roomnum_lbl = Label(editFrame, text="Room Number",font=("Arial",9))
    guest_balance_lbl = Label(editFrame, text="Balance",font=("Arial",9))
    guest_checkIn_lbl = Label(editFrame, text="Check In",font=("Arial",9))
    guest_checkOut_lbl = Label(editFrame, text="Check Out",font=("Arial",9))
    guest_payment_lbl = Label(editFrame, text="Payment",font=("Arial",9))
    guest_edit_btn = Button(editFrame, text="Save changes")

    scrollable_frame = Frame(searchFrame)
    canvas = Canvas(scrollable_frame)
    vscrollbar = Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    hscrollbar = Scrollbar(scrollable_frame, orient=HORIZONTAL, command=canvas.xview)
    tableFrame  = Frame(canvas)
    searchlabel = Label(searchFrame,text="",anchor="w",bg="burlywood1",fg="VioletRed4")

    guest_id_lbl1 = Label(updateFrame,text="",font=("Arial",12),bg="burlywood1",fg="VioletRed4",anchor="w")
    guest_id_lbl2 = Label(updateFrame,text="",font=("Arial",12),bg="burlywood1",fg="VioletRed4",anchor="w")
    guest_total_lbl = Label(updateFrame,text="",font=("Arial",12),bg="burlywood1",fg="VioletRed4",anchor="w")
    guest_total_entry =  Entry(updateFrame)
    guest_total_btn = Button(updateFrame,text="Update",bg="VioletRed4",fg="burlywood1")

    thisframe = Frame(statsFrame)
    room_f1 = roomInfo()
    room_f2 = roomInfo()
    room_f3 = roomInfo()
    room_f4 = roomInfo()
    room_n2 = roomInfo()
    room_301 = roomInfo()
    room_302 = roomInfo()
    room_303 = roomInfo()
    room_304 = roomInfo()
    room_305 = roomInfo()
    room_306 = roomInfo()
    

    def guestForget(self):
        self.guest_name_entry.destroy()
        self.guest_balance_entry.destroy()
        self.guest_checkIn_entry.destroy()
        self.guest_checkOut_entry.destroy()
        self.guest_payments_entry.destroy()
        self.guest_contact_entry.destroy()
        self.guest_roomnum_entry.destroy()
        self.guest_name_lbl.destroy()
        self.guest_contactlbl.destroy()
        self.guest_roomnum_lbl.destroy()
        self.guest_balance_lbl.destroy()
        self.guest_checkIn_lbl.destroy()
        self.guest_checkOut_lbl.destroy()
        self.guest_payment_lbl.destroy()
        self.guest_edit_btn.destroy()

        self.scrollable_frame.destroy()
        self.canvas.destroy()
        self.vscrollbar.destroy()
        self.hscrollbar.destroy()
        self.tableFrame.destroy()
        self.searchlabel.destroy()

        self.guest_id_lbl1.destroy()
        self.guest_id_lbl2.destroy()
        self.guest_total_lbl.destroy()
        self.guest_total_entry.destroy()
        self.guest_total_btn.destroy()

        self.thisframe.destroy()
        self.room_f1.resetAttr()
        self.room_f2.resetAttr()
        self.room_f3.resetAttr()
        self.room_f4.resetAttr()
        self.room_n2.resetAttr()
        self.room_301.resetAttr()
        self.room_302.resetAttr()
        self.room_303.resetAttr()
        self.room_304.resetAttr()
        self.room_305.resetAttr()
        self.room_306.resetAttr()

    def  changeMonth(self,month):
        i = 0
        for monthI in self.MONTH_STATS:
            if month == monthI:
                break
            i+=1
        return i

    def displayStat3(self):
        COLUMN_LEGEND = ['Room Number','Total Payment','Times Booked']
        self.thisframe = Frame(statsFrame)
        self.thisframe.grid(row=1,columnspan=5)

        row_i = 0
        column_i = 0
        new_column = 0
        count = 0
        roomnum = ""
        room_class = ""

        for l in range(13):
            if l>=1 and l<=11:
                roomnum = self.ROOM_NUMBER[l-1]
                room_class = self.ROOM_NUMBER_CLASS[l-1]
            if l >= 7:
                roomnum = self.ROOM_NUMBER[l-2]
                room_class = self.ROOM_NUMBER_CLASS[l-2]
            for k in range(0,3):
                e = Entry(self.thisframe,width=15)
                if row_i == 0:
                    e.insert(END,COLUMN_LEGEND[k])  
                else:
                    if column_i == new_column:
                        e.insert(END,roomnum)
                        #print(roomnum)  
                    elif column_i == new_column+1: 
                        e.insert(END,room_class.curr_total)
                    else:
                        e.insert(END,room_class.curr_guests)  
                e.grid(row=row_i,column=column_i,sticky=W+E)
                e.config(state=DISABLED)
                column_i+=1             
            row_i += 1
            if row_i == 7:
                row_i = 0
                new_column = 3
            column_i = new_column
            count+=1
        totalP = 0
        totalG = 0
        for j in self.ROOM_NUMBER_CLASS:
            totalP  = totalP + j.curr_total
            totalG = totalG + j.curr_guests
            print(totalP,totalG)
        for l in range(3):
            
            e = Entry(self.thisframe,width=15)
            if l==0:
                e.insert(END,"Total") 
            elif l==1: 
                e.insert(END,totalP)
            else:
                e.insert(END,totalG)
            e.grid(row=6,column=l+3,sticky=W+E)
            e.config(state=DISABLED)    

    def displayStats2(self):
        self.guestForget()
        month = self.changeMonth(self.varDefaultMonth.get())
        month2 = self.changeMonth(self.varDefaultMonth.get())
        year = self.varDefaultYear.get()
        if month == 0:
            month = 1
            month2 = 12
        
        days = monthrange(year,month2)[1]
        string = ""

        payment = 0

        self.ROOM_NUMBER_CLASS = [self.room_f1,self.room_f2,self.room_f3,self.room_f4,self.room_n2,
                    self.room_301,self.room_302,self.room_303,self.room_304,self.room_305,self.room_306]
        self.ROOM_NUMBER = ["F1","F2","F3","F4","N2","301","302","303","304","305","306"]

        try:
            string = f"{year}-{month}-01"
            string2 = f"{year}-{month2}-{days}"
            db = mysql.connector.connect(host="localhost",user="root",passwd="pokeblack1",db="guest_list")
            cur = db.cursor()
            cur.execute(f"SELECT * FROM guest_list.guests WHERE CheckIn >= '{string}' AND CheckOut <= '{string2}'")
            for row in cur.fetchall():
                payment = row[8]
                for room_class, roomnum in zip(self.ROOM_NUMBER_CLASS,self.ROOM_NUMBER):
                    if (row[4]) == roomnum:
                        room_class.addInfo(payment,1)
            self.displayStat3()
            db.close()
        except EXCEPTION as e:
            print(e)

    def displayStats(self):
        self.MONTH_STATS  = ['ALL MONTHS','JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']

        raise_frame(statsFrame)
        top_frame = Frame(statsFrame,bg="burlywood1")
        top_frame.grid(row=0,column=0,columnspan=9,sticky=W)
        guest_name_label = Label(top_frame,text="Show statistics for ",anchor="w",bg="burlywood1",fg="VioletRed4")
        guest_name_label.grid(row=0,column=0)

        self.varDefaultMonth = StringVar(root)
        self.varDefaultMonth.set(self.MONTH_STATS[0])
        self.month_stat = OptionMenu(top_frame,self.varDefaultMonth,*self.MONTH_STATS)
        self.month_stat.config(bg="VioletRed4",fg="burlywood1")
        self.month_stat.grid(row=0,column=1)

        self.varDefaultYear = IntVar(root)
        self.varDefaultYear.set(YEAR[0])
        self.year_stat = OptionMenu(top_frame,self.varDefaultYear,*YEAR)
        self.year_stat.config(bg="VioletRed4",fg="burlywood1")
        self.year_stat.grid(row=0,column=2)

        guest_name_btn = Button(top_frame,text="Search",command=lambda:self.displayStats2(),bg="VioletRed4",fg="burlywood1",width=10)
        guest_name_btn.grid(row=0,column=3,sticky=N+S)

    def deleteGuest(self):
        result = messagebox.askquestion("Delete",f"Are you sure you want to delete Guest Id {self.guest_id}?",icon="warning")
        if result == 'yes':
            try:
                db = mysql.connector.connect(host="localhost",user="root",passwd="pokeblack1",db="guest_list")
                cur = db.cursor()
                cur.execute(f"DELETE FROM guest_list.guests WHERE idGuest = {self.guest_id}")
                db.commit()
                db.close()
                messagebox._show("Successful",f"Guest Id {self.guest_id} deleted")
                raise_frame(checkingFrame)
            except EXCEPTION as e:
                print(e)

    def searchGuest2(self):
        self.guestForget()
        guest_name = self.guest_name_entry2.get()
        if guest_name == "":
            messagebox.showerror("Error","Please input valid name")
        else:
            self.scrollable_frame = Frame(searchFrame)
            self.scrollable_frame.grid(row=2, column=0, sticky=NW)
            self.canvas = Canvas(self.scrollable_frame)
            self.canvas.grid(row=0, column=0)

            self.vscrollbar = Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)
            self.vscrollbar.grid(row=0, column=1, sticky=NS)
            self.canvas.configure(yscrollcommand=self.vscrollbar.set)

            self.hscrollbar = Scrollbar(self.scrollable_frame, orient=HORIZONTAL, command=self.canvas.xview)
            self.hscrollbar.grid(row=1, column=0, sticky=EW)
            self.canvas.configure(xscrollcommand=self.hscrollbar.set)

            self.tableFrame  = Frame(self.canvas)            
            for i in range(9):
                self.tableFrame.columnconfigure(i,weight=1)

            self.searchlabel = Label(searchFrame,text="There are no records",anchor="w",bg="burlywood1",fg="VioletRed4")
            self.searchlabel.grid(row=1,sticky=W)
            rows_showed = 5
            try:
                query = f"SELECT * FROM guest_list.guests WHERE Name = '{guest_name}' ORDER BY CheckIn DESC"
                self.showTable(self.tableFrame,self.canvas,query,self.searchlabel,rows_showed)
            except Exception as e:
                messagebox.showerror("Error","Something went wrong. Check input and try again.")

    def searchGuest(self):
        raise_frame(searchFrame)
        self.guestForget()
        top_frame = Frame(searchFrame,bg="burlywood1")
        top_frame.grid(row=0,column=0,columnspan=9,sticky=W)
        guest_name_label = Label(top_frame,text="Guest Name:",anchor="w",bg="burlywood1",fg="VioletRed4")
        guest_name_label.grid(row=0,column=0)
        self.guest_name_entry2 = Entry(top_frame)
        self.guest_name_entry2.grid(row=0,column=1)

        guest_name_btn = Button(top_frame,text="Search",command=lambda:self.searchGuest2(),bg="VioletRed4",fg="burlywood1")
        guest_name_btn.grid(row=0,column=2)

    def updateGuest2(self,total,balance):
        result = messagebox.askquestion("Update", "Are You Sure?", icon='warning')
        if result == "yes":
            add_payment = self.guest_total_entry.get()
            try:
                balance = balance - float(add_payment)
                total = total + float(add_payment)
                db = mysql.connector.connect(host="localhost",user="root",passwd="pokeblack1",db="guest_list")
                cur = db.cursor()
                cur.execute(f"UPDATE guest_list.guests SET TotalPayment = {total}, Balance = {balance} WHERE idGuest = {self.guest_id}")
                db.commit()
                db.close()
                messagebox._show("Successful",f"Payments updated.\nNew Balance: {balance}")
                raise_frame(checkingFrame)
                pass
            except Exception as e:
                messagebox.showerror("Error","Something went wrong. Check input and try again.")
            
    def updateGuest(self,name,checkIn,checkOut,balance,total_payments):
        days = (checkOut - checkIn).days
        string = f"{name} with Guest id ({self.guest_id}), staying for {days} day/s, has a balance of Php {balance}"
        self.guest_id_lbl1 = Label(updateFrame,text=string,font=("Arial",12),bg="burlywood1",fg="VioletRed4",anchor="w")
        self.guest_id_lbl1.grid(row=1,columnspan=8,sticky=W+E)
        self.guest_id_lbl2 = Label(updateFrame,text=f"{name} has paid Php {total_payments}",font=("Arial",12),bg="burlywood1",fg="VioletRed4",anchor="w")
        self.guest_id_lbl2.grid(row=2,columnspan=8,sticky=W+E)
        self.guest_total_lbl = Label(updateFrame,text="Add Payment",font=("Arial",12),bg="burlywood1",fg="VioletRed4",anchor="w")
        self.guest_total_lbl.grid(row=3,column=1,sticky=W+E)
        self.guest_total_entry =  Entry(updateFrame)
        self.guest_total_entry.grid(row=3,column=2,sticky=W+E)
        self.guest_total_btn = Button(updateFrame,text="Update",bg="VioletRed4",fg="burlywood1",command=lambda:self.updateGuest2(total_payments,balance))
        self.guest_total_btn.grid(row=3,column=3,sticky=W+E)

    def showTable(self,frame,canvas,query,label,rows_showed):
        TABLE_COLUMNS = ['Guest Id','Name','Contact','Type','Room','Check In','Check Out','Balance','Payments']

        db = mysql.connector.connect(host="localhost",user="root",passwd="pokeblack1",db="guest_list")
        cur = db.cursor()
        cur.execute(query)
        i=2
        count = 0
        for guest in cur.fetchall():
            if i == 2:
                for j in range(9):
                    e = Label(frame,text=TABLE_COLUMNS[j],width=10,anchor="w")
                    if j == 0:
                        e.config(width=6)
                    if j == 1:
                        e.config(width=11)
                    e.grid(row=1,column=j,sticky=W+E)
            for j in range(len(guest)):
                e = Entry(frame,width=10)
                if j == 0:
                    e.config(width=6)
                if j == 1:
                    e.config(width=11)
                e.grid(row=i,column=j,sticky=W+E)
                e.insert(END,guest[j])
                e.config(state=DISABLED)
            i+=1
            count+=1
        if count <= 0:
            messagebox.showerror("Error","No records found")
            if rows_showed == 5:
                self.searchGuest()
            else:
                raise_frame(checkingFrame)
        else:
            canvas.create_window((0, 0), window=frame, anchor="nw")
            frame.update_idletasks()
            bbox = canvas.bbox(ALL)
            zw, zh = bbox[2]-bbox[1], bbox[3]-bbox[1]
            if count <= 3:
                rows_showed = 3
            dw, dh = int((zw/9) * 8), int((zh/count) * rows_showed)
            canvas.configure(scrollregion=bbox, width=dw, height=dh)
            if i!=1:
                label.config(text=f"Showing {count} result/s. This list is sorted by the Check In dates")
        
        db.close()

    def displayGuestList(self):
        raise_frame(displayFrame)
        self.guestForget()
        self.scrollable_frame = Frame(displayFrame)
        self.scrollable_frame.grid(row=1, column=0, sticky=NW)
        self.canvas = Canvas(self.scrollable_frame)
        self.canvas.grid(row=0, column=0)

        self.vscrollbar = Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)
        self.vscrollbar.grid(row=0, column=1, sticky=NS)
        self.canvas.configure(yscrollcommand=self.vscrollbar.set)

        self.hscrollbar = Scrollbar(self.scrollable_frame, orient=HORIZONTAL, command=self.canvas.xview)
        self.hscrollbar.grid(row=1, column=0, sticky=EW)
        self.canvas.configure(xscrollcommand=self.hscrollbar.set)
        self.tableFrame  = Frame(self.canvas)

        for i in range(9):
            self.tableFrame.columnconfigure(i,weight=1)
        label = Label(displayFrame,text="There are no records",anchor="w",bg="burlywood1",fg="VioletRed4")
        label.grid(row=0,columnspan=9,sticky=W)
        rows_showed = 7
        try:
            query = "SELECT * FROM guest_list.guests ORDER BY CheckIn DESC"
            self.showTable(self.tableFrame,self.canvas,query,label,rows_showed)
        except Exception as e:
            print(e)

    def editGuestInsert(self,name,contact,roomnum,balance,checkIn,checkOut,total):
        sql = "UPDATE guest_list.guests SET Name = %s,ContactNumber = %s,RoomNumber = %s,"+\
                    "CheckIn = %s,CheckOut = %s,Balance = %s,TotalPayment = %s WHERE idGuest = %s;"
        val = [name,contact,roomnum,str(checkIn),str(checkOut),str(balance),str(total),str(self.guest_id)]
        db = mysql.connector.connect(host="localhost",user="root",passwd="pokeblack1",db="guest_list")
        cur = db.cursor()
        cur.execute(sql,val)
        db.commit()
        db.close()

    def editGuestGetValues(self):
        result = messagebox.askquestion("Save Changes","Are you sure?",icon="warning")
        if result == "yes":
            name = self.guest_name_entry.get()
            contact = self.guest_contact_entry.get()
            roomnum = self.guest_roomnum_entry.get()
            balance = self.guest_balance_entry.get()
            checkIn = self.guest_checkIn_entry.get()
            checkOut = self.guest_checkOut_entry.get()
            total = self.guest_payments_entry.get()

            try:
                datetime.datetime.strptime(checkIn,"%Y-%m-%d")
                datetime.datetime.strptime(checkOut,"%Y-%m-%d")
                float(balance)
                float(total)
                self.editGuestInsert(name,contact,roomnum,balance,checkIn,checkOut,total)
                messagebox._show("Success","Changes saved successfully")
                raise_frame(checkingFrame)
            except Exception as e:
                print(e)
                messagebox.showerror("Error","Check your input again")

    def editGuestEntry(self,name,contact,roomnum,balance,checkIn,checkOut,total):
        #Entries
        self.guest_name_entry = Entry(editFrame)
        self.guest_name_entry.insert(END,name)
        self.guest_contact_entry = Entry(editFrame)
        self.guest_contact_entry.insert(END,contact)
        self.guest_roomnum_entry = Entry(editFrame)
        self.guest_roomnum_entry.insert(END,roomnum)
        self.guest_balance_entry = Entry(editFrame)
        self.guest_balance_entry.insert(END,balance)
        self.guest_checkIn_entry = Entry(editFrame)
        self.guest_checkIn_entry.insert(END,checkIn)
        self.guest_checkOut_entry = Entry(editFrame)
        self.guest_checkOut_entry.insert(END,checkOut)
        self.guest_payments_entry = Entry(editFrame)
        self.guest_payments_entry.insert(END,total)
        self.guest_name_entry.grid(row=2,column=1,columnspan=2,sticky=W+E)
        self.guest_contact_entry.grid(row=3,column=1,columnspan=2,sticky=W+E)
        self.guest_roomnum_entry.grid(row=4,column=1,columnspan=2,sticky=W+E)
        self.guest_balance_entry.grid(row=5,column=1,columnspan=2,sticky=W+E)
        self.guest_checkIn_entry.grid(row=2,column=4,columnspan=2,sticky=W+E)
        self.guest_checkOut_entry.grid(row=3,column=4,columnspan=2,sticky=W+E)
        self.guest_payments_entry.grid(row=4,column=4,columnspan=2,sticky=W+E)
        #Label
        self.guest_name_lbl = Label(editFrame, text="Name",font=("Arial",9),bg="burlywood1",fg="VioletRed4")
        self.guest_contactlbl = Label(editFrame, text="Contact",font=("Arial",9),bg="burlywood1",fg="VioletRed4")
        self.guest_roomnum_lbl = Label(editFrame, text="Room Number",font=("Arial",9),bg="burlywood1",fg="VioletRed4")
        self.guest_balance_lbl = Label(editFrame, text="Balance",font=("Arial",9),bg="burlywood1",fg="VioletRed4")
        self.guest_checkIn_lbl = Label(editFrame, text="Check In",font=("Arial",9),bg="burlywood1",fg="VioletRed4")
        self.guest_checkOut_lbl = Label(editFrame, text="Check Out",font=("Arial",9),bg="burlywood1",fg="VioletRed4")
        self.guest_payment_lbl = Label(editFrame, text="Payment",font=("Arial",9),bg="burlywood1",fg="VioletRed4")
        self.guest_name_lbl.grid(row=2,column=0,sticky=E)
        self.guest_contactlbl.grid(row=3,column=0,sticky=E)
        self.guest_roomnum_lbl.grid(row=4,column=0,sticky=E)
        self.guest_balance_lbl.grid(row=5,column=0,sticky=E)
        self.guest_checkIn_lbl.grid(row=2,column=3,sticky=E)
        self.guest_checkOut_lbl.grid(row=3,column=3,sticky=E)
        self.guest_payment_lbl.grid(row=4,column=3,sticky=E)
        #Button
        self.guest_edit_btn = Button(editFrame, text="Save changes",command=lambda:self.editGuestGetValues(),bg="VioletRed4",fg="burlywood1")
        self.guest_edit_btn.grid(row=5,column=4,sticky=E+W)

    def editGuestSearch(self,function):
        name =  ""
        contact = ""
        roomnum = ""
        balance = ""
        checkIn = ""
        checkOut = ""
        total = ""
        self.guest_id = self.guest_id_entry.get()
        if self.guest_id.isnumeric() is True:
            self.guest_id = int(self.guest_id)
            db = mysql.connector.connect(host="localhost",user="root",passwd="pokeblack1",db="guest_list")
            cur = db.cursor()
            cur.execute(f"SELECT * FROM guest_list.guests WHERE idGuest = {self.guest_id};")
            i=0
            for row in cur.fetchall():
                name =  row[1]
                contact = row[2]
                roomnum = row[4]
                balance = row[7]
                checkIn = row[5]
                checkOut = row[6]
                total = row[8]
                i+=1          
            db.close()
            if i==0:
                messagebox.showerror("Error",f"There are no guests with Guest Id {str(self.guest_id)}")
            else:
                if function == "edit":
                    self.editGuestEntry(name,contact,roomnum,balance,checkIn,checkOut,total)
                elif function == "update":
                    self.updateGuest(name,checkIn,checkOut,balance,total)
                else:
                    self.deleteGuest()

        else:
            messagebox.showerror("Error","Please input valid id number")

    def searchguestid(self,frame,function):
        raise_frame(frame)
        self.guestForget()
        guest_id_lbl = Label(frame,text="Guest Id:",font=("Arial",12),bg="burlywood1",fg="VioletRed4")
        self.guest_id_entry = Entry(frame)
        guest_id_btn = Button(frame,text="Search",command=lambda:self.editGuestSearch(function),bg="VioletRed4",fg="burlywood1")
        
        guest_id_lbl.grid(row=0,column=0,sticky=W)
        self.guest_id_entry.grid(row=0,column=1,columnspan=6,sticky=W+E)
        guest_id_btn.grid(row=0,column=7,sticky=E+W)
    
    def assignCommand(self):
        self.btn_home.config(command=lambda:raise_frame(checkingFrame))
        self.btn_edit.config(command=lambda:self.searchguestid(editFrame,"edit"))
        self.btn_search.config(command=lambda:self.searchGuest())
        self.btn_guest_table.config(command=lambda:self.displayGuestList())
        self.btn_update.config(command=lambda:self.searchguestid(updateFrame,"update"))
        self.btn_delete.config(command=lambda:self.searchguestid(deleteFrame,"delete"))
        self.btn_stats.config(command=lambda:self.displayStats())
        
class BookingInfo:
    bookingFrame.columnconfigure(1,weight=1)
    for i in range(0,8):
        bookingFrame.rowconfigure(i,weight=1)

    guestId = Label(bookingFrame, text="NF",font=("Arial",12),bg="burlywood1",fg="VioletRed4")
    nameLbl = Label(bookingFrame, text="Name",font=("Arial",12),anchor="e",bg="burlywood1",fg="VioletRed4")
    contactLbl = Label(bookingFrame, text="Contact Number",font=("Arial",12),anchor="e",bg="burlywood1",fg="VioletRed4")
    roomLbl = Label(bookingFrame, text="Room Number",font=("Arial",12),anchor="e",bg="burlywood1",fg="VioletRed4")
    paymentLbl = Label(bookingFrame, text="Payment",font=("Arial",12),anchor="e",bg="burlywood1",fg="VioletRed4")
    chargeLbl = Label(bookingFrame, text="Charge",font=("Arial",12),anchor="e",bg="burlywood1",fg="VioletRed4")
    chargeL = Label(bookingFrame, text="Php",font=("Arial",12),anchor="e",bg="burlywood1",fg="VioletRed4")
    bookingbtn = Button(bookingFrame, text="Book Guest",font=helv,bg="VioletRed4",fg="burlywood1")
    cancelbtn = Button(bookingFrame, text="Cancel",font=helv,bg="VioletRed4",fg="burlywood1")

    guestId.grid(column=0,row=0,sticky="e")
    nameLbl.grid(column=0,row=1,sticky="e")
    contactLbl.grid(column=0,row=2,sticky="e")
    roomLbl.grid(column=0,row=3,sticky="e")
    paymentLbl.grid(column=0,row=4,sticky="e")
    chargeLbl.grid(column=0,row=5,sticky="e")
    chargeL.grid(column=2,row=5,sticky="w")
    
    def __init__(self,ROOMS,charge,date_start,date_end,room_type):
        self.ROOMS = ROOMS
        self.charge = charge
        self.date_start = date_start
        self.date_end = date_end
        self.room_type =room_type
        self.createWidgets1()

    def checkMaxId(self):
        self.guest_id  = 1
        db = mysql.connector.connect(host="localhost",user="root",passwd="pokeblack1",db="guest_list")
        cur = db.cursor()
        cur.execute("SELECT * FROM guest_list.guests ORDER BY idGuest DESC LIMIT 1;")
        for row in cur.fetchall():
            self.guest_id = row[0]+1
        db.close()

    def insertMySql(self):
        db = mysql.connector.connect(host="localhost",user="root",passwd="pokeblack1",db="guest_list")
        sql = "INSERT INTO guest_list.guests (idGuest,Name,ContactNumber,RoomType,"+\
                "RoomNumber,CheckIn,CheckOut,Balance,TotalPayment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        val = [str(self.guest_id),self.guest_name,self.guest_contact,self.room_type,self.room_number,
                    str(self.date_start),str(self.date_end),str(self.balance),str(self.guest_payment)]
        try:
            cur = db.cursor()
            cur.execute(sql,val)
            messagebox._show("Success","Booking successful")
            CheckAvailability()
            raise_frame(checkingFrame)
        except Exception as e:
            print(e)
            messagebox.showerror("Error","Something went wrong")
        db.commit()
        db.close()
        
    def getValues(self):
        self.guest_name = self.nameEntry.get()
        self.guest_contact = self.contactEntry.get()
        self.guest_payment = self.paymentEntry.get()
        self.room_number = self.varDefaultRoomNum.get()

        if self.guest_payment.isnumeric() is True:
            self.balance = self.charge - int(self.guest_payment)
            if self.room_number == "Room Number":
                messagebox.showerror("Error","Please choose a room number")
            else:
                self.insertMySql()
                pass
        else:
            messagebox.showerror("Error","Please check payment input")

    def createWidgets1(self):
        self.checkMaxId()

        self.varDefaultRoomNum = StringVar(root)
        self.varDefaultRoomNum.set("Room Number")
        self.room_num = OptionMenu(bookingFrame,self.varDefaultRoomNum,*self.ROOMS)
        self.room_num.grid(row=3,columnspan=3,column=2,sticky=W)
        self.room_num.config(width=75,height=1,bg="VioletRed4",fg="burlywood1")

        self.nameEntry = Entry(bookingFrame)
        self.nameEntry.grid(row=1,columnspan=3,column=2)
        self.setpadxpady(self.nameEntry)

        self.contactEntry = Entry(bookingFrame)
        self.contactEntry.grid(row=2,columnspan=3,column=2)
        self.setpadxpady(self.contactEntry)

        self.paymentEntry = Entry(bookingFrame)
        self.paymentEntry.grid(row=4,columnspan=3,column=2)
        self.setpadxpady(self.paymentEntry)

        self.bookingbtn.grid(column=3,row=5,sticky=E)
        self.bookingbtn.config(command=lambda:self.getValues())
        self.cancelbtn.grid(column=4,row=5,sticky=W)
        self.cancelbtn.config(command=lambda:raise_frame(checkingFrame))

        self.chargeL.config(text=f"Php {self.charge}")
        self.guestId.config(text=f"NF-{self.guest_id}")

    def setpadxpady(self,widget):
        widget.grid(ipadx=185,ipady=5,sticky=W)

class CheckAvailability:
    #Dropdown_CheckIn
    checkInLbl = Label(checkingFrame, text="Check In",font=("Arial",12),anchor="e",bg="burlywood1",fg="VioletRed4")

    varDefaultCiM = StringVar(root)
    varDefaultCiM.set(MONTH[0])
    checkInMon = OptionMenu(checkingFrame,varDefaultCiM,*MONTH)
    checkInMon.config(bg="VioletRed4",fg="burlywood1")

    varDefaultCiD = IntVar(root)
    varDefaultCiD.set(DAYS[0])
    checkInDay = OptionMenu(checkingFrame,varDefaultCiD,*DAYS)
    checkInDay.config(bg="VioletRed4",fg="burlywood1")

    varDefaultCiY = IntVar(root)
    varDefaultCiY.set(YEAR[0])
    checkInYear = OptionMenu(checkingFrame,varDefaultCiY,*YEAR)
    checkInYear.config(bg="VioletRed4",fg="burlywood1")

    #Dropdown_CheckOut
    checkOutLbl = Label(checkingFrame, text="Check Out",font=("Arial",12),anchor="e",bg="burlywood1",fg="VioletRed4")
    
    varDefaultCoM = StringVar(root)
    varDefaultCoM.set(MONTH[0])
    checkOutMon = OptionMenu(checkingFrame,varDefaultCoM,*MONTH)
    checkOutMon.config(bg="VioletRed4",fg="burlywood1")

    varDefaultCoD = IntVar(root)
    varDefaultCoD.set(DAYS[0])
    checkOutDay = OptionMenu(checkingFrame,varDefaultCoD,*DAYS)
    checkOutDay.config(bg="VioletRed4",fg="burlywood1")

    varDefaultCoY = IntVar(root)
    varDefaultCoY.set(YEAR[0])
    checkOutYear = OptionMenu(checkingFrame,varDefaultCoY,*YEAR)
    checkOutYear.config(bg="VioletRed4",fg="burlywood1")

    #Dropdown_RoomType
    varDefaultRoom = StringVar(root)
    varDefaultRoom.set("Room Type")
    roomType = OptionMenu(checkingFrame,varDefaultRoom,*ROOM_TYPE)
    roomType.config(bg="VioletRed4",fg="burlywood1")

    #CheckBox_AdditionalPerson
    varDefaultCB = IntVar()
    varDefaultCB.set(0)
    cbAdditionalPerson = Checkbutton(checkingFrame,variable=varDefaultCB,
                            onvalue=1,offvalue=0,text="Additional Person",borderwidth=2, relief="groove")
    cbAdditionalPerson.config(bg="VioletRed4",fg="burlywood1")
 

    #Button_Check
    checkAvailability = Button(checkingFrame,text="Check Availability",font=helv,width=1)
    checkAvailability.config(bg="VioletRed4",fg="burlywood1")

    def changeMonth(self,month):
        i = 1
        for monthI in MONTH:
            if month == monthI:
                break
            i+=1
        return i

    def checkLeapYear(self, year):
        leap_year = False

        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    leap_year = True
                else:
                    leap_year = False
            else:
                leap_year = True
        else:
            leap_year = False
        
        return leap_year

    def checkValidDate(self,month,day,year):
        day = int(day)
        year = int(year)
        check = False
        leap_year = self.checkLeapYear(year)

        i=1
        for monthI in MONTH:
            if month == monthI:
                break
            i+=1

        if (i==1 or i==3 or i==5 or i==7 or i==8 or i==10 or i==12) and day <= 31:
            check = True
            
        if (i==4 or i==6 or i==9 or i==11) and day <= 30:
            check = True
        if (i==2 and day <= 29 and leap_year is True) or (i==2 and day <= 28 and leap_year is False):
            check = True
        
        return check

    def isAvailable(self,date_start,date_end):
        availability = False

        SHWROOM_USED = []
        SHWROOM_UNUSED = []

        num_room = 6
        string = ""
        if self.room_type == "Family":
            num_room = 5
            string = "RoomType = 'Family'"
        if self.room_type == 'Double' or self.room_type == 'Single':
            string = "RoomType = 'Single' OR RoomType = 'Double'"

        db = mysql.connector.connect(host="localhost",user="root",passwd="pokeblack1",db="guest_list")
        cur = db.cursor()
        cur.execute("SELECT * FROM guest_list.guests WHERE "+string+";")
        
        for row in cur.fetchall():
            
            curr_date_start = row[5]
            curr_date_end = row[6]
            latestStart = max(date_start,curr_date_start)
            earliestEnd = min(date_end,curr_date_end)
            delta  = (earliestEnd-latestStart).days+1
            overlap = max(0,delta)
            if overlap > 0:
                num_room -= 1
                
                curr_room_num = row[4]
                if self.room_type == "Family":
                    for room in FAMROOM:
                        if curr_room_num == room:
                            SHWROOM_USED.append(room)
                else:
                    for room in STDROOM:
                        if curr_room_num == room:
                            SHWROOM_USED.append(room)

        db.close()
        if self.room_type == "Family":
            self.charge = 1500
            SHWROOM_UNUSED = set(FAMROOM).symmetric_difference(set(SHWROOM_USED))
        else:
            SHWROOM_UNUSED = set(STDROOM).symmetric_difference(set(SHWROOM_USED))
            if self.room_type == "Single":
                self.charge = 1000
            else:
                self.charge = 1200
        messagebox._show("Available",f"There are {num_room} available rooms for {self.room_type} Rooms.")
        if num_room > 0:
            availability = True
        SHWROOM_UNUSED=sorted(SHWROOM_UNUSED)
        
        return availability, SHWROOM_UNUSED
            
    def setDates(self):
        date_start = datetime.date(month=self.ciMonth,day=self.ciDay,year=self.ciYear)
        date_end = datetime.date(month=self.coMonth,day=self.coDay,year=self.coYear)
        if date_start < date_end:
            is_available, ROOMS = self.isAvailable(date_start,date_end)
            if is_available is True:
                total_days = int(str(date_end - date_start).split(" day")[0])
                self.charge = (self.charge*total_days) + (self.add_person*total_days)
                raise_frame(bookingFrame)
                BookingInfo(ROOMS,self.charge,date_start,date_end,self.room_type)
            else:
                messagebox.showerror("Unavailable","There are no vacancies")
        else:
            messagebox.showerror("Error","Incorrect date input. Try again")

    def getCheckValues(self):
        self.charge = 0
        self.ciMonth = self.changeMonth(self.varDefaultCiM.get())
        self.ciDay = self.varDefaultCiD.get()
        self.ciYear = self.varDefaultCiY.get()
        self.coMonth = self.changeMonth(self.varDefaultCoM.get())
        self.coDay = self.varDefaultCoD.get()
        self.coYear = self.varDefaultCoY.get()
        self.room_type = self.varDefaultRoom.get()
        self.add_person = self.varDefaultCB.get()

        if self.add_person == 1:
            self.add_person = 300

        if self.checkValidDate(self.varDefaultCiM.get(),self.ciDay,self.ciYear) is True and self.checkValidDate(self.varDefaultCoM.get(),self.coDay,self.coYear) is True:
            if self.room_type != "Room Type":
                self.setDates()
            else:
                messagebox.showerror("Error","Please choose a room type")
        else:
            messagebox.showerror("Error","Incorrect date input. Try again")

    def placeWidgets0(self):

        self.checkInLbl.grid(row=1,column=0,ipadx = 20, ipady = 10,sticky="e")
        self.checkInMon.config(width=7)
        self.checkInMon.grid(row=1,column=1, ipadx = 40, ipady = 10)
        self.checkInDay.config(width=7)
        self.checkInDay.grid(row=1,column=2, ipadx = 40, ipady = 10)
        self.checkInYear.config(width=7)
        self.checkInYear.grid(row=1,column=3, ipadx = 40, ipady = 10)
        self.checkInMon.config(width=7)
        self.checkOutLbl.grid(row=2,column=0,ipadx = 25, ipady = 10,sticky="e")
        self.checkOutMon.config(width=7)
        self.checkOutMon.grid(row=2,column=1, ipadx = 40, ipady = 10)
        self.checkOutDay.config(width=7)
        self.checkOutDay.grid(row=2,column=2, ipadx = 40, ipady = 10)
        self.checkOutYear.config(width=7)
        self.checkOutYear.grid(row=2,column=3, ipadx = 40, ipady = 10)
        
        self.roomType.config(width=11)
        self.roomType.grid(row=3,column=0,columnspan=2, ipadx = 90, ipady = 8,sticky=W+E)
        self.cbAdditionalPerson.config(width=20)
        self.cbAdditionalPerson.grid(row=3,column=2,columnspan=2, ipadx = 83, ipady = 10,sticky="w")
        self.checkAvailability.grid(row=4,columnspan=4, ipady = 10,sticky=W+E+N+S)
        self.checkAvailability.config(command=lambda:self.getCheckValues())

raise_frame(checkingFrame)
CheckAvailability().placeWidgets0()
SideBar().assignCommand()

root.mainloop()