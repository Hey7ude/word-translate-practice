from tkinter import Entry, Label, Tk, Button, Toplevel

class UserPanel(Tk):
    def __init__(self, callback1):
        super(UserPanel, self).__init__()
        self.title('Word Translate Practice')
        self.callback1 = callback1
        Button(self, text='Add word', command=self.add_word).grid(row=1, column=1)
        
    def add_word(self):
        p = AddWordPanel(self)
        word = p.get_word()
        translate = p.get_translate()
        self.callback1(word, translate)
        
        
class AddWordPanel(Toplevel):
    def __init__(self, master):
        super(AddWordPanel, self).__init__(master)
        self.word = None
        self.translate = None
        Label(self, text='Word:').grid(row=1, column=1)
        Label(self, text='Translate:').grid(row=2, column=1)
        self.ent_word = Entry(self)
        self.ent_translate = Entry(self)
        self.ent_word.grid(row=1, column=2)
        self.ent_translate.grid(row=2, column=2)
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

