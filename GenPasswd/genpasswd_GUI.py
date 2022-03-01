from tkinter import *
import random

class MyWindow:
    # Code to generate tkinter window to interact with user
    def __init__(self, win):
        ''' Label field info '''
        self.lbl = Label(win, text="Enter password length:", fg='black', font=("Helvetica", 10))
        self.lbl.place(x=60, y=50)
        ''' Text field next to label '''
        self.txtfld1 = Entry(win, text="Length Numbers Only", bd=3)
        self.txtfld1.place(x=200, y=50, height=25, width=50)
        ''' Text field to display generated password '''
        self.txtfld2 = Entry()
        self.txtfld2.place(x=150, y=95, height=25, width=200)
        ''' Button to generate password '''
        self.btn = Button(win, text="Generate Password", fg='blue', command=self.GeneratePasswd)
        self.btn.place(x=150, y=140)
    # Code to generate random password, given a length in number
    def GeneratePasswd(self):
        ''' Variables to use '''
        L = 1
        passwd = []
        password = ''
        ''' Get length of password to generate '''
        length = int(self.txtfld1.get())
        ''' Randomly select charachters from lists
            alpha (alphabet), num (numbers), and spc (special characters) '''
        while L <= length:
            randnum = random.randint(1, 5)
            if ( randnum == 1 ):
                p = str(random.choice(alpha))
            elif ( randnum == 2 ):
                p = str(random.choice(num))
            elif ( randnum == 3 ):
                p = str(random.choice(spc))
            else:
                p = str(random.choice(alpha))
                p = p.lower()
            ''' Add random letters to a new list '''
            passwd.append(p)
            L = L + 1
        ''' Extract letters from list and display them in textfield '''    
        for i in passwd:
            password = str(password) + i
            self.txtfld2.delete(0, 'end')
            self.txtfld2.insert(END, str(password))

### ======================= MAIN ======================= ###        
alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
num = ['1','2','3','4','5','6','7','8','9','0']
spc = ['`','~','!','@','#','$','%','^','&','*','(',')','_','+','-','=','[',']','}','{','\\','|',':',';','"','\'','<',',','>','.','?','/']

window=Tk()
mywin=MyWindow(window)
window.title('GenPasswd')
window.geometry("400x175+10+20")
window.mainloop()
