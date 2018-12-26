import tkinter as tk
import model 

class Menu:
    
    def startgame(self,parent, mode):
        Game(mode,parent)
        
    def __init__(self, parent = None):
        if parent != None:
            parent.destroy()
        self.root = tk.Tk()
        self.root.geometry('390x100')
        self.root.resizable(width=False, height=False)
        self.root.title('MySweeper')
        desc = tk.Label(master=self.root, text='Welcome to MySweeper!', font= 'Helvetica 18 bold').grid(row=0, column=1)
        inst = tk.Label(master=self.root, text= 'Select a difficulty below').grid(row=1, column=1)
        ebutton = tk.Button(master=self.root, text = 'Easy', command = lambda: self.startgame(self.root, 'Easy',)).grid(row=2, column=0, padx=10)
        mbutton = tk.Button(master=self.root,  text = 'Medium', command = lambda: self.startgame(self.root, 'Medium')).grid(row=2,column=1)
        hbutton = tk.Button(master=self.root,  text = 'Hard', command = lambda: self.startgame(self.root, 'Hard')).grid(row=2, column=2)
        self.root.mainloop()

class Game:
    
    
    def __init__(self,mode, parent):
        parent.destroy()
        self.setting = mode
        self.board =  model.new_game(mode)
        self.checkwin = 0
        self.clicked = [[False for i in  range(model.diff[mode][0])] for i in range(model.diff[mode][1])]
        self.flag_mode = False
        self.root = tk.Tk()
        self.root.geometry(model.diff[mode][3])
        self.root.resizable(width = False, height = False)
        self.root.title('MySweeper: {}'.format(mode))
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        
        frame=tk.Frame(self.root)
        frame.grid(row=0, column=0, sticky='NSEW')
        
        self.buttons = [[] for i in range(model.diff[mode][0])]
        for row_index in range(model.diff[mode][0]):
            tk.Grid.rowconfigure(frame, row_index, weight=1)
            for col_index in range(model.diff[mode][1]):
                tk.Grid.columnconfigure(frame, col_index, weight=1)
                label = tk.Label(master=frame,text=str(self.board[row_index][col_index]) if self.board[row_index][col_index] !=0 else '', \
                                                                                    fg='blue' if self.board[row_index][col_index]!='O' else 'red') \
                                                                                    .grid(row=row_index, column=col_index, sticky='NSEW')
                btn = tk.Button(master=frame, bg='white')
                btn['command'] = lambda r=row_index, c= col_index, b = btn: self.reveal(r,c,b)
                btn.grid(row=row_index, column=col_index, sticky='NSEW')  
                self.buttons[row_index].append(btn)
        
        quit_button = tk.Button(master=self.root, width = 0, text= 'Quit Game', command= self.root.destroy) .grid(row=3, column=0, padx=5, pady=10, sticky='w')
        reset = tk.Button(master=self.root, width = 0, text= 'Start Over', command= lambda: Menu(self.root)) .grid(row=4, column=0, padx=5, pady=10, sticky='w')
        flagbutton = tk.Button(master=self.root, width = 0, text = 'Flags', command = self.flag).grid(row = 3, column= 0, sticky='e', pady=10)
        self.flaglabel = tk.Label(master=self.root, width=0, text='Off')
        self.flaglabel.grid(row = 4, column = 0, sticky='se', pady=15)
        
        self.root.mainloop()
        
    def flag(self):
        self.flag_mode = not(self.flag_mode)
        self.flaglabel['text'] = ['Off','On'][int(self.flag_mode)]
    
    def reveal(self,row,col,button):
        if self.flag_mode == False:
            self.clicked[row][col] = True
            if self.board[row][col] == 0:
                for i in [(row,col-1),(row-1,col),(row-1,col-1),(row-1,col+1),(row+1,col-1),(row+1,col),(row,col+1),(row+1,col+1)]:
                        if model.inbounds(i[0],i[1], self.board) and self.clicked[i[0]][i[1]]==False :
                            self.reveal(i[0],i[1],self.buttons[i[0]][i[1]])
            elif self.board[row][col] == 'O':
                Loss(self.root)
            if self.clicked[row][col] == True:
                button.destroy()
                self.checkwin += 1
            if self.checkwin == model.diff[self.setting][0]*model.diff[self.setting][1] - model.diff[self.setting][2]:
                Win(self.root)
                
        else:
            if button['bg'] == 'red':
                button.config(bg = 'white')
            else:
                button.config(bg='red')
            
class Loss:

    def __init__(self,parent):
        self.root = tk.Toplevel()
        self.root.title('MySweeper')
        message = tk.Label(master=self.root, text='You lost!').pack(side='top', pady=10)
        self.again = tk.Button(master=self.root, text='Play again' , command = lambda: Menu(parent)).pack(side = 'left', padx = 10, pady = 10)
        quit = tk.Button(master=self.root, text='Quit', command = lambda: self.quit(parent)).pack(side = 'left', padx = 10, pady = 10)
        self.root.grab_set()

    def quit(self,parent):
        parent.destroy()
    
class Win(Loss):
    
    def __init__(self,parent):
        self.root = tk.Toplevel()
        self.root.title('MySweeper')
        message = tk.Label(master=self.root, text='You won!').pack(side='top', pady=10)
        self.again = tk.Button(master=self.root, text='Play again' , command = lambda: Menu(parent)).pack(side = 'left', padx = 10, pady = 10)
        quit = tk.Button(master=self.root, text='Quit', command = lambda: self.quit(parent)).pack(side = 'left', padx = 10, pady = 10)
        self.root.grab_set()
        
