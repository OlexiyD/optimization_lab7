import tkinter.ttk as ttk

class Tableview(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Event for editing cell
        self.bind("<Double-1>", lambda event: self.onDoubleClick(event))

        # Coloring of table
        style = ttk.Style()
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
    
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

    def onDoubleClick(self, event):
        ''' Executed, when a row is double-clicked. Opens 
        read-only EntryPopup above the item's column, so it is possible
        to select text '''

        # close previous popups
        try:  # in case there was no previous popup
            self.entryPopup.destroy()
        except AttributeError:
            pass

        # what row and column was clicked on
        row_id = self.identify_row(event.y)
        column = self.identify_column(event.x)
        column_id = int(column[1:])-1

        # handle exception when header is double click
        if not row_id:
            return

        # get column position info
        x,y,width,height = self.bbox(row_id, column)

        # y-axis offset
        pady = height // 2

        # Place Entry popup properly
        text = self.item(row_id, 'values')[column_id]
        self.entryPopup = EntryPopup(self, row_id, column_id, text)
        self.entryPopup.place(x=x, y=y+pady, width=width, height=height, anchor='w')

class EntryPopup(ttk.Entry):
    def __init__(self, parent, iid, column, text, **kw):
        ttk.Style().configure('pad.TEntry', padding='1 1 1 1')
        super().__init__(parent, style='pad.TEntry', **kw)
        self.tv = parent
        self.iid = iid
        self.column = column

        self.insert(0, text) 
        self['exportselection'] = False

        self.focus_force()
        self.select_all()
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *ignore: self.destroy())


    def on_return(self, event):
        row_id = self.tv.focus()
        vals = self.tv.item(row_id, 'values')
        vals = list(vals)
        vals[self.column] = self.get()
        self.tv.item(row_id, values=vals)
        self.destroy()


    def select_all(self, *ignore):
        ''' Set selection on the whole text '''
        self.selection_range(0, 'end')

        # returns 'break' to interrupt default key-bindings
        return 'break'
    

# def read_data():
#    for index, line in enumerate(data):
#       tree.insert('', tk.END, iid = index,
#          values = line)
# columns = ("name", "age", "salary")

# tree= Tableview(root, columns=columns, show="headings", height=20)
# tree.pack(padx = 5, pady = 5)

# tree.heading('name', text='Name')
# tree.heading('age', text='Age')
# tree.heading('salary', text='Salary')