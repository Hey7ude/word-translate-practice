from tkinter import END, Entry, Frame, Label, Scrollbar, Tk, Button, Toplevel
from tkinter.messagebox import showinfo
from tkinter.ttk import Treeview


class UserPanel(Tk):
    def __init__(self, words_list, add_word_callback, add_answer_callback, check_repeated_callback, learned_callback, export_csv_callback, import_csv_callback):
        super(UserPanel, self).__init__()
        self.title('Word Translate Practice')
        self.words_list = words_list
        self.callback1 = add_word_callback
        self.add_answer = add_answer_callback
        self.check_repeated = check_repeated_callback
        self.learned = learned_callback
        self.export_csv = export_csv_callback
        self.import_csv = import_csv_callback
        self.rowconfigure([1,2,3], minsize=50, weight=1)
        self.columnconfigure(1, minsize=50, weight=1)
        self.frm_labels =Frame(self)
        Label(self.frm_labels, text='Word Translate Practice').grid(row=1, column=1)
        Label(self.frm_labels, text='You can use commands listed below:').grid(row=2,column=1)
        self.frm_labels.grid(row=1, column=1, sticky='ns')
        self.frm_buttons = Frame(self)
        Button(self.frm_buttons, text='Add word', command=self.add_word).grid(row=1, column=1)
        Button(self.frm_buttons, text='Start Day', command=self.start_day).grid(row=1, column=2)
        self.frm_buttons.grid(row=2,column=1, sticky='ns')
        self.columns = ('word', 'translate', 'is_learned', 'answers')
        self.tree_view = Treeview(self, columns=self.columns, show='headings')
        self.tree_view.heading('word', text='Word')
        self.tree_view.heading('translate', text='Translate')
        self.tree_view.heading('is_learned', text='is_learned')
        self.tree_view.heading('answers', text='Answers')
        self.add_to_tree()
        self.tree_view.bind('<<TreeviewSelect>>', self.item_selected)
        self.tree_view.grid(row=3, column=1, sticky='nsew')
        self.vscrollbar = Scrollbar(self, orient='vertical', command=self.tree_view.yview)
        self.vscrollbar.grid(row=3, column=2, sticky='ns')
        self.hscrollbar = Scrollbar(self, orient='horizontal', command=self.tree_view.xview)
        self.hscrollbar.grid(row=4, column=1, sticky='ew')
        self.tree_view.configure(yscroll=self.vscrollbar.set, xscroll=self.hscrollbar.set)
        
    def add_to_tree(self):
        for i in self.tree_view.get_children():
            self.tree_view.delete(i)
        for word in self.words_list:
            values = (word.word, word.translate, word.is_learned, word.answers)
            self.tree_view.insert('', 'end', values=values)

    def item_selected(self, event):
        for selected_item in self.tree_view.selection():
            item = self.tree_view.item(selected_item)
            record = item['values']
            showinfo(title='Information', message=f"""
                     Word: {record[0]}
                     Translate: {record[1]}
                     Learned: {record[2]}
                     Answers: {record[3]}
                     """)
            
    def add_word(self):
        p = AddWordPanel(self)
        word = p.get_word()
        translate = p.get_translate()
        if word and translate:
            self.callback1(word, translate)
            self.add_to_tree()
            self.export_csv()
        
    def start_day(self):
        for word in self.words_list:
            if not word.is_learned:
                r = WordCheck(self, word).get_response()
                if r is not None:
                    self.add_answer(word, r)
                if self.check_repeated(word) == True and len(word.answers) != 0:
                    if WordLearn(self, word).get_response() == True:
                        self.learned(word)
        self.add_to_tree()
        self.export_csv()
        
        
class AddWordPanel(Toplevel):
    def __init__(self, master):
        super(AddWordPanel, self).__init__(master)
        self.title('Add Word')
        self.word = None
        self.translate = None
        self.rowconfigure([1,2,3], minsize=50, weight=1)
        self.columnconfigure([1,2], minsize=50, weight=1)
        Label(self, text='Word:').grid(row=1, column=1, sticky='e', padx=5)
        Label(self, text='Translate:').grid(row=2, column=1, sticky='e', padx=5)
        self.ent_word = Entry(self)
        self.ent_translate = Entry(self)
        self.ent_word.grid(row=1, column=2, sticky='w', padx=5)
        self.ent_translate.grid(row=2, column=2, sticky='w', padx=5)
        Button(self, text='Add', command = self.add).grid(row=3, column=2, sticky='w')
        
    def add(self):
        self.word = self.ent_word.get()
        self.translate = self.ent_translate.get()
        if self.word and self.translate:
            self.destroy()
            
    def get_word(self):
        self.word is None and self.winfo_exists() and self.wait_window()
        return self.word
    
    def get_translate(self):
        self.translate is None and self.winfo_exists() and self.wait_window()
        return self.translate
            
            
class WordCheck(Toplevel):
    def __init__(self, master, word):
        super(WordCheck, self).__init__(master)
        Label(self, text= word.word).grid(row=1, column=1)
        Button(self, text='Yes', command=self.yes).grid(row=2, column=2)
        Button(self, text='No', command=self.no).grid(row=2, column=1)
        self.response = None
        
    def yes(self):
        self.response = True
        self.destroy()
    
    def no(self):
        self.response = False
        self.destroy()
        
    def get_response(self):
        self.response is None and self.winfo_exists() and self.wait_window()
        return self.response
    
class WordLearn(Toplevel):
    def __init__(self, master, word):
        super(WordLearn, self).__init__(master)
        self.response = None
        Label(self, text=f'You repeated this word for {word.repeated()} days.\nDid you learned this word?').grid(row=1, column=1)
        Button(self, text='Yes', command=self.yes).grid(row=2, column=2)
        Button(self, text='No', command=self.no).grid(row=2, column=1)
        
    def yes(self):
        self.response = True
        self.destroy()
    
    def no(self):
        self.response = False
        self.destroy()
        
    def get_response(self):
        self.response is None and self.wait_window()
        return self.response