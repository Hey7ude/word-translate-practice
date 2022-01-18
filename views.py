from tkinter import END, Entry, Frame, Label, Listbox, Tk, Button, Toplevel


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
        self.frm_labels.grid(row=1, column=1)
        self.frm_buttons = Frame(self)
        Button(self.frm_buttons, text='Add word', command=self.add_word).grid(row=1, column=1)
        Button(self.frm_buttons, text='Start Day', command=self.start_day).grid(row=1, column=2)
        self.frm_buttons.grid(row=2,column=1)
        self.frm_list_box = Frame(self)
        self.list_box = Listbox(self.frm_list_box)
        self.list_box.grid(row=1, column=1)
        self.add_to_listbox()
        self.frm_list_box.grid(row=3, column=1)
        
    def add_to_listbox(self):
        self.list_box.delete(0, END)
        for word in self.words_list:
            self.list_box.insert('end', f'word: {word.word} - repeated: {word.repeated()}')
            
    def add_word(self):
        p = AddWordPanel(self)
        word = p.get_word()
        translate = p.get_translate()
        self.callback1(word, translate)
        self.add_to_listbox()
        self.export_csv()
        
    def start_day(self):
        for word in self.words_list:
            if not word.is_learned:
                self.add_answer(word, WordCheck(self, word).get_response())
                if self.check_repeated(word) == True:
                    if WordLearn(self, word).get_response() == True:
                        self.learned(word)
        self.add_to_listbox()
        self.export_csv()
        
        
class AddWordPanel(Toplevel):
    def __init__(self, master):
        super(AddWordPanel, self).__init__(master)
        self.title('Add Word')
        self.word = None
        self.translate = None
        self.frm_word = Frame(self)
        self.frm_translate = Frame(self)
        Label(self.frm_word, text='Word:').grid(row=1, column=1)
        Label(self.frm_translate, text='Translate:').grid(row=1, column=1)
        self.ent_word = Entry(self.frm_word)
        self.ent_translate = Entry(self.frm_translate)
        self.ent_word.grid(row=1, column=2)
        self.ent_translate.grid(row=1, column=2)
        self.frm_word.grid(row=1, column=1)
        self.frm_translate.grid(row=2, column=1)
        Button(self, text='Add', command = self.add).grid(row=3, column=1)
        
    def add(self):
        self.word = self.ent_word.get()
        self.translate = self.ent_translate.get()
        if self.word and self.translate:
            self.destroy()
            
    def get_word(self):
        self.word is None and self.wait_window()
        return self.word
    
    def get_translate(self):
        self.translate is None and self.wait_window()
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
        self.response is None and self.wait_window()
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