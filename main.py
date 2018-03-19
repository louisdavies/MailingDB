# usr/bin/python

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.EmailGen = tk.Button(self)
        self.EmailGen["text"] = "Hello World\n(click me)"
        self.EmailGen["command"] = self.GenerateEmails
        
        self.Add = tk.Button(self,text = "Add Supporter Details", command=self.AddPerson)
        
        self.SearchBox = tk.Entry(self)
        self.SearchBox.insert(0,"Search Term")
        self.SearchBox.focus_set()
        
        self.Search = tk.Button(self,text = "Search Database", command=self.Search(self.SearchBox.get()))
        # self.SearchBox["command"] = self"Search Term"

        self.EmailGen.pack(side="left",fill=None)
        self.SearchBox.pack(side="left", fill ="y",ipady=10)
        # self.pack(side = "bottom")
        self.Search.pack(side="left")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        # self.place(x = 20, y = 30 + i*30, width=120, height=25)
        self.quit.pack(side="bottom")

    def GenerateEmails(self):
        print("Generating emails")

    def AddPerson(self):
        print("Adding a person")

    def Search(self,SearchString=None):
        print("Searching for: %s"%SearchString)



root = tk.Tk()
root.geometry("600x400+100+100")
root.title("CICCU Database Manager")
# root.wm_iconbitmap("")
app = Application(master=root)
app.mainloop()

# if __name__ == "__main__":
# 	main()