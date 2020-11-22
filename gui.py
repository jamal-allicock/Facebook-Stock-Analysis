from tkinter import *
import mpt


class StartPage(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self)
        label = Label(self, text="Start Page")
        self.names_label=[]
        self.codes_label=[]
        self.names=[]
        self.codes=[]
        self.num=0
        label.grid(row=0)

        graph=Button(self,text='Graph Price History',
                command=lambda: self.grapher(self.entry_startdate.get(), self.entry_enddate.get(),False)).grid(row=0,column=0)

        graph2=Button(self,text='Graph Efficient Frontier',
                command=lambda: self.grapher(None,None,True)).grid(row=0,column=1)
        but=Button(self, text='+', command=self.AddCompany).grid(row=5)
        but2=Button(self, text='-', command=self.RemoveCompany).grid(row=5,column=1)

        label_date = Label(self, text='Starting date').grid(row=3)
        self.entry_startdate = Entry(self)
        self.entry_startdate.grid(row=3,column=1)

        label_enddate = Label(self, text='Ending date').grid(row=4)
        self.entry_enddate = Entry(self)
        self.entry_enddate.grid(row=4,column=1)

        self.weights=Label(text='')
        self.weights.grid(row=0,column=3)


    def AddCompany(self):
        if self.num==10:
            return

        name_label = Label(self, text='Company Name')
        code_label = Label(self, text='Stock Code')
        name_entry = Entry(self)
        code_entry = Entry(self)
        
        name_label.grid(row=6+2*self.num)
        code_label.grid(row=7+2*self.num)
        name_entry.grid(row=6+2*self.num, column=1)
        code_entry.grid(row=7+2*self.num, column=1)

        self.names_label.append(name_label)
        self.codes_label.append(code_label)
        self.names.append(name_entry)
        self.codes.append(code_entry)

        self.num+=1
    
    def RemoveCompany(self):
        try:
            self.names_label[-1].destroy()
            self.names_label.pop()

            self.codes_label[-1].destroy()
            self.codes_label.pop()

            self.names[-1].destroy()
            self.names.pop()

            self.codes[-1].destroy()
            self.codes.pop()
            
            self.num-=1
        except IndexError:
            pass

    def grapher(self,starting,ending,eff):
        stock = []
        assets = []
        n_assets=len(assets)
        for entry in self.names:
            assets.append(entry.get())
        for entry in self.codes:
            stock.append(entry.get())
        if not eff:
            f=mpt.data_frame(stock, assets, starting, ending)
            plt=mpt.plotter(f[0],f[1])
            plt.show()
        elif eff:
            f=mpt.data_frame(stock, assets, starting, ending)
            plt=mpt.eff_frontier(f[0])
            s=''
            w=plt[1]#.tolist()
            n_assets=len(assets)
            print(w)
            for i in range(n_assets):
                print(w[i])
                s+=f'Invest {round(w[i]*100,2)}% in {assets[i]}\n'
            self.weights.config(text=s)
            plt[0].show()

# class PageOne(Frame):

#     def __init__(self, parent, controller):
#         Frame.__init__(self, parent)
#         label = Label(self, text="Page One!!!")
#         label.pack(pady=10,padx=10)

#         entry1=Entry(self).pack()

#         button1 = Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
#         button1.pack()

#         button2 = Button(self, text="Page Two", command=lambda: controller.show_frame(PageTwo))
#         button2.pack()


# class PageTwo(Frame):

#     def __init__(self, parent, controller):
#         Frame.__init__(self, parent)
#         label = Label(self, text="Page Two!!!")
#         label.pack(pady=10,padx=10)

#         button1 = Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
#         button1.pack()

#         button2 = Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
#         button2.pack()

app = StartPage()
app.geometry('400x550')
app.title('Portfolio Optimization')
app.mainloop()