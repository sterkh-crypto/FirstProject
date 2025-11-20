#Sterling Houpt
#Import database
import sqlite3
from contextlib import closing
conn = sqlite3.connect("FinalDatabase.sqlite")
conn.row_factory = sqlite3.Row

#Import GUI
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

#Import Date Time Fuction
from datetime import datetime
now = datetime.now()


#Put Main 
def main():

    root = tk.Tk()
    root.title("Sign In MTC")
    root.geometry("400x275")
    frame = ttk.Frame(root, padding="10 10 10 10")
    frame.pack(fill=tk.BOTH, expand=True)


#User Input
    
    #Input StudentID
    StudentIDLabel = ttk.Label(frame, text="Student ID:", width=20)
    StudentIDLabel.place(x=41,y=20)

    StudentIDText = tk.StringVar()
    StudentIDEntry = ttk.Entry(frame, width=25, textvariable=StudentIDText)
    StudentIDEntry.place(x=120,y=20)

    #Input Name
    NameLabel = ttk.Label(frame, text="Name:", width=20)
    NameLabel.place(x=63,y=50)

    NameText = tk.StringVar()
    NameEntry = ttk.Entry(frame, width=25, textvariable=NameText)
    NameEntry.place(x=120,y=50)

    #Input Major
    MajorLabel = ttk.Label(frame, text="Major:", width=20)
    MajorLabel.place(x=64,y=80)

    MajorText = tk.StringVar()
    MajorEntry = ttk.Entry(frame, width=25, textvariable=MajorText)
    MajorEntry.place(x=120,y=80)

    #Input Position
    PositionLabel = ttk.Label(frame, text="Student or Faculty:", width=27)
    PositionLabel.place(x=0,y=110)

    PositionText = tk.StringVar()
    PositionEntry = ttk.Entry(frame, width=25, textvariable=PositionText)
    PositionEntry.place(x=120,y=110)

    KeyLabel = ttk.Label(frame, text="Faculty Only PIN:", width=20)
    KeyLabel.place(x=10,y=140)

    KeyText = tk.StringVar()
    KeyEntry = ttk.Entry(frame, width=25, textvariable=KeyText)
    KeyEntry.place(x=120,y=140)

#Functions
    
    #Sign In Button Function
    def SignInUser():
        mtcID=StudentIDText.get()
        Name=NameText.get()
        Major=MajorText.get()
        Position=PositionText.get()
        Key=KeyText.get()
        Time = now.strftime("%H:%M:%S")
        
        if Position.lower()=="student":
            with closing(conn.cursor()) as c:
                sql = '''INSERT INTO SignIns (mtcID, Name, Major,Position,Time) VALUES (?, ?, ?, ?, ?)'''
                c.execute(sql, (mtcID, Name, Major, Position, Time))
                conn.commit()
            print(Name,"was added")
        
            student_Functions()
        elif Position.lower()=="faculty":
            if Key=="1111":
                with closing(conn.cursor()) as c:
                    sql = '''INSERT INTO SignIns (mtcID, Name, Major,Position,Time) VALUES (?, ?, ?, ?, ?)'''
                    c.execute(sql, (mtcID, Name, Major, Position, Time))
                    conn.commit()
                print(Name,"was added")
                faculty_Functions()
            else:
                checkKey()
        else:
            checkPosition()
            
    #CheckStudentOrFaculty
    def checkPosition():
            tkinter.messagebox.showinfo("Error","Invalid Information, try again.")

    #StudentSignIn
    def student_Functions():
        new_root = tk.Tk()
        new_root.title("Welcome to MTC Student!")
        new_root.geometry("300x300")
        ttk.Button(new_root, text="Tuition Calculator", command=TuitionCalc, width=25).pack()
        ttk.Button(new_root, text="Display MTC Majors", command=showMajors, width=25).pack()
        ttk.Button(new_root, text="Display MTC Advisors", command=showAdvisors, width=25).pack()
        ttk.Button(new_root, text="Close window", command=lambda: close_window(new_root)).pack() 

    #FacultySignIn
    def faculty_Functions():
        new_root = tk.Tk()
        new_root.title("Welcome to MTC Faculty!")
        new_root.geometry("300x300")
        
        ttk.Button(new_root, text="Display All Users", width=20, command=displayAll).pack()
        ttk.Button(new_root, text="Update User", width=20, command=updateButton).pack()
        ttk.Button(new_root, text="Delete User", width=20, command=deleteButton).pack()
        ttk.Button(new_root, text="Close window", command=lambda: close_window(new_root)).pack() 

    #FacultyDeleteUser
    def deleteButton():
        mtcID = int(input("Enter a MTC ID to Delete: "))
        with closing(conn.cursor()) as c:
            sql ='''DELETE FROM SignIns WHERE mtcID = ?'''
            c.execute(sql, (mtcID,))
            conn.commit()
        print(mtcID, " deleted.")
        
    #FacultyUpdateUser
    def updateButton():
        mtcID = int(input("Enter a MTC ID to update: "))
        Name = input("Enter an updated Name: ")
        Position = input("Enter an updated Position: ")
        Major = input("Enter an updated Major: ")
        
        with closing(conn.cursor()) as c:
            sql = '''UPDATE SignIns SET Name=?, Position=?, Major = ? WHERE mtcID = ?'''
            c.execute(sql, (Name, Position, Major, mtcID))
            conn.commit()
        print(Name, "updated.")

    #FacultyDisplayAll 
    def displayAll():
        try:
            with closing(conn.cursor()) as c:
                query = '''SELECT * FROM SignIns'''
                c.execute(query)
                mtcSignInDB = c.fetchall()
        except sqlite3.OperationalError as e:
            print("Error reading database -", e)
            mtcSignInDB = None
            
        if mtcSignInDB != None:
            print("mtcID", "Name", "Position", "Major", "Time")
            for SignIns in mtcSignInDB:
                print(SignIns["mtcID"], "|", SignIns["Name"], "|", SignIns["Position"], "|", SignIns["Major"], "|" , SignIns["Time"])
            print()
            
    #FacultyCheckPIN
    def checkKey():
            tkinter.messagebox.showinfo("Error","Incorrect Code, try again.")
    #StudentTuitionCalculator
    def TuitionCalc():
        again="y"
        while again=="y":
            Credits=int(input("How many credit hours do you have?"))
            if Credits<=13:
                CreditAmount = Credits*200
            elif Credits>=13 and int(Credits)<=18:
                CreditAmount = 2600
            else:
                CreditAmount = Credits*170
            print("You have around $", CreditAmount, "of tuition")
            again=input("Again?(y/n):")


    #StudentMajors
    def showMajors():
        win=tk.Tk() #creating the main window and storing the window object in 'win'
        win.title('MTC Majors') #setting title of the window
        win.geometry("200x170") #geometry(str)
        
        lb = tk.Listbox(win, foreground="black", background="light blue", width=30)
        lb.insert(1, 'Majors:\n')
        lb.insert(2, '---------------------------------------------------------')
        lb.insert(3, 'Arts & Sciences') 
        lb.insert(4, 'Business') 
        lb.insert(5, 'Engineering Technologies') 
        lb.insert(6, 'Health Technologies')
        lb.insert(7, 'Information Technologies')
        lb.insert(8, 'Public Services')
        lb.place(x=0,y=0)
        
        itm = lb.get
        win.title(itm)
        winButton=ttk.Button(win, text="Close window", command=lambda: close_win(win))
        winButton.place(x=20,y=130)
    #StudentAdvisors
    def showAdvisors():
        win=tk.Tk()
        win.title('MTC Advisors')
        win.geometry("400x200")
        
        lb = tk.Listbox(win, foreground="black", background="light blue", width=60)
        lb.insert(1, 'Advisor - Major - Email')
        lb.insert(2, '---------------------------------------------------------')
        lb.insert(3, 'Laura Emerick - Advising - emerickl@mtc.edu') 
        lb.insert(4, 'Mandy Knight - Nursing, Arts & Sciences - knightm@mtc.edu') 
        lb.insert(5, 'Brandy Page - Health IT, Medical Assisting - pageb@mtc.edu') 
        lb.insert(6, 'Amanda Robinson - Business, Engineering, IT - robinsona@mtc.edu')
        lb.place(x=0,y=0)
        
        itm = lb.get
        win.title(itm)
        winButton=ttk.Button(win, text="Close window", command=lambda: close_win(win))
        winButton.place(x=20,y=125)

    #NewWindowClose
    def close_window(new_root):
        new_root.destroy()
    def exit_window():
        root.destroy()
    def close_win(win):
        win.destroy()
#Buttons
        
    #Sign In Button
    signIn=ttk.Button(frame,text="Sign In", width=10,command=SignInUser)
    signIn.place(x=160,y=170)

    #Exit Button
    exitButton = ttk.Button(root, text="Exit", width=10, command=exit_window)
    exitButton.place(x=170,y=210)

#main
if __name__ == "__main__":
    main()
