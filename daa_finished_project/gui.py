"""importing modules"""
from tkinter import *
import ctypes
from numpy.ctypeslib import ndpointer
from tkinter import messagebox
import time
import threading



controller  = True                              #used for breaking while loop of timer
array = [0 for i in range(0,81)] 
root = Tk()                                     #creaing object of tk
root.iconbitmap("gnome_sudoku.ico")             #setting icon
g = 0
r = 0
root.title("Sudoku")                            #title og gui
frame1 = Frame(root)                            #creating frames
frame1.pack(side=TOP,fill=X)        
frame2 = Frame(root)
frame2.pack(side=TOP,fill=X)
root.resizable(False,False)                     #disable resizig of window
Font_tuple = ("Comic Sans MS", 23, "bold")      #font used in gui
list  = [[0 for i in range(0,9)]for j in range(0,9)]                #declaring lists for various use
string_variables  = [[0 for i in range(0,9)]for j in range(0,9)]
text  = [[0 for i in range(0,9)]for j in range(0,9)]
ans  = [[0 for i in range(0,9)]for j in range(0,9)]


""" function to control what can be typed in sudoku """
def supervisor(*args):
    for l in range(0,9):
        for m in range(0,9):
            text[l][m] = string_variables[l][m].get()   #getting all 81 values in sudoku blocks
            try:
                text[l][m] = int(text[l][m])
                if(text[l][m] == 0):
                    list[l][m].delete(0,"end")          #preventing user from typing zero
                    text[l][m] = ""
            except:
                list[l][m].delete(0,"end")
                text[l][m] = ""
            text[l][m] = str(text[l][m])
            if(len(text[l][m])>1):
                string_variables[l][m].set((text[l][m])[:1])      #preventing user from typing multiple digits in same block

"""function to show the output on sudoku"""
def solve():
    global ans
    ans1 = [[0 for i in range(0,9)]for j in range(0,9)]
    ans1 = get_ans()                        #calling get_ans() to get the solved sudoku
    for i in range(0,9):
        for j in range (0,9): 
            ans[i][j] = ans1[j%9+i*9]       #converting to 2d array for simplicity
    
    for i in range(0,9):
        for j in range (0,9):
            if(list[i][j].cget('state') != "disabled"):
                string_variables[i][j].set(ans[i][j])       #showing output in sudoku
                time.sleep(0.2)                             

    check()            #calling check() to to know if the output is correct 
                
"""many threads are created in this script 
   when creating gui if we do not use threading
   the gui becomes unresponsive"""
def thread_for_solve():                     #thread for the function sove()
    t2 = threading.Thread(target = solve)
    t2.start()

"""function to change the fore-ground color of all 81 blocks to black"""
def make_black():
    time.sleep(5)
    for i in range(0,9):
        for j in range (0,9):
            list[i][j].config(fg = "black")


"""function to get the solution for sudoku"""
def  get_ans():
    global array
    global ans
    ans2 = array
    ans1 = [0 for i in range(0,81)]
    lib = ctypes.CDLL('./sudoku_generator.so')                  #sudoku_generator.so is shared file object containing the functions of c file sudoku_generator.c 
    lib.get_answer.restype = ndpointer(dtype=ctypes.c_int, shape=(81,)) #specifying return type
    Array = ctypes.c_int * 81                       #converting to array of c from list of python 
    parameter_array = Array(*ans2)
    ans1 = lib.get_answer(parameter_array)          #calling  get_answer() from .so file
    return ans1

"""function to change the color of fore-ground to 
   red or green depending on if answer is coreect or wrong"""
def check():
    ans1 = [0 for i in range(0,81)]
    inp  = [[0 for i in range(0,9)]for j in range(0,9)]
    ans1 = get_ans()
    for i in range(0,9):
        for j in range (0,9): 
            ans[i][j] = ans1[j%9+i*9]
            inp[i][j] = (string_variables[i][j].get())
    for i in range(0,9):
        for j in range (0,9):
            if inp[i][j] == '':
                messagebox.showinfo("Sudoku", "Check after completing sudoku")   #prevent user from checking before he fills all values of sudoku
                return
    for i in range(0,9):
        for j in range (0,9): 
            inp[i][j] = int(inp[i][j])
    for i in range(0,9):
        for j in range (0,9):
            if(inp[i][j] == ans[i][j]):
                list[i][j].config(fg = "green") #make fg green
            else:
                list[i][j].config(fg = "red")  #make fg red
    
    if(inp == ans):
        global t6
        global controller
        global r
        controller = False
        if(t6[r].is_alive()):               #break timer thread 
            t6[r].join()
        controller = True
        r=r+1
        time = timer_label["text"]
        messagebox.showinfo("Sudoku", f"Sudoku solved in {time}!!!")
    t = threading.Thread(target = make_black)
    t.start()                                       #convert fg to black after some seconds
    
"""function to get the question"""
def get_puzzle():
    global array
    start_button.config(text = "reset")     #change button text from start to reset
    d = difficulty.get()                    #get difficulty level
    thread_for_clock()                      #start clock 
    d = int(d)
    if(d>3 or d<1):
        messagebox.showinfo("Sudoku", "Enter a valid value")
        return
    lib = ctypes.CDLL('./sudoku_generator.so')
    lib.get_question.restype = ndpointer(dtype=ctypes.c_int, shape=(81,))
    array = lib.get_question(d)             #calling get_question() function from .so file
    question = [[0 for i in range(0,9)] for j in range(0,9)]
    for i in range(0,9):
        for j in range (0,9):
            question[i][j] = array[j%9+i*9]
    for l in range(0,9):
        for m in range(0,9):
            string_variables[l][m].set("")
            if(question[l][m] != 0):
                string_variables[l][m].set(str(question[l][m]))
                list[l][m].config(state='disabled')
            if(question[l][m] == 0):                            #disabling the blocks which contain question
                list[l][m].config(state='normal')
    

""" creating sudoku blocks and assigning string variables to supervisor()"""
for i in range(1,10):
    for j in range(1,10):
        string_variables[i-1][j-1] = StringVar()
        string_variables[i-1][j-1].trace("w",supervisor)
        list[i-1][j-1] =Entry(frame1,width = 3,font = Font_tuple,textvariable=string_variables[i-1][j-1])
        if(i%3 == 0):
            list[i-1][j-1].grid(row=i,column=j,pady=(0,8))
        if(j%3 == 0):
            list[i-1][j-1].grid(row=i,column=j,padx=(0,8))
        if(i%3 != 0 and j%3 != 0):
            list[i-1][j-1].grid(row=i,column=j,padx=0,pady=0)


"""labels and buttons"""
difficulty = StringVar()
start_button = Button(frame2,text = "Start",height = 2,width = 6,command = get_puzzle)
start_button.pack(side=LEFT,padx=5,pady=5)
difficulty_level = Entry(frame2,width = 27,textvariable =difficulty,font = ("Comic Sans MS", 15, "bold")) 
difficulty.set("Enter difficulty level (1 ,2 or 3)")
difficulty_level.pack(side=LEFT,pady=5)
check_button = Button(frame2,text = "Check",height = 2,width = 6,command =check)
check_button.pack(side=LEFT,padx=5,pady=5)
solve_button = Button(frame2,text = "Solve",height = 2,width = 6,command = thread_for_solve)
solve_button.pack(side=LEFT,padx=5,pady=5) 
timer_label = Label(frame2,text = "0:0:0",height = 2,width = 6)
timer_label.pack(side=LEFT,padx=5,pady=5) 

"""thread to clock and also to break the thread and start new clock"""
def thread_for_clock():
    global t6
    global controller
    global r
    controller = False
    if(t6[r].is_alive()):
        t6[r].join()
    controller = True
    r=r+1
    t6[r].start()


"""clock to show time"""
def clock():
    seconds = 0
    minutes = 0
    hours = 0
    while(True):
        global controller
        output = f"{hours} "+":"+f"{minutes} "+":"+f"{seconds} "
        timer_label.config(text = output)
        time.sleep(1)
        seconds+=1
        if(seconds == 60):    
            seconds = 0    
            minutes+=1    
        if(minutes == 60):    
            minutes = 0    
            hours+=1  
        if(controller == False):
            break  

t6 = [threading.Thread(target = clock) for q in range (0,81)] #creating 

root.mainloop() #loop gui