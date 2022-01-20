import csv_manager

class Word:
    id = 0
    def __init__(self, word: str, translate: str, is_learned: bool=False, answers: list=[]):
        self.id = Word.id
        Word.id += 1
        self.word = word
        self.translate = translate
        self.is_learned = is_learned
        self.answers = answers
    
    def repeated(self):
        return len(self.answers)
    
    def __str__(self):
        return f'word: {self.word}, translate: {self.translate}'
    
class User:
    def __init__(self, name: str):
        self.name = name
        self.words = []
        self.repeat = 8
        self.import_csv()
    
    def add_word(self, word: str, translate: str):
        self.words.append(Word(word, translate, False, []))
        
    def get_unlearned_words(self):
        for word in self.words:
            if not word.is_learned:
                yield word
        
    def add_answer(self, word, answer: bool):
        word.answers.append(answer)
        
    def check_repeated(self, word):
        return True if word.repeated() % self.repeat == 0 else False
    
    def get_word_by_id(self, id: int):
        for word in self.words:
            if word.id == id:
                return word
        
    def learned(self, word):
        word.is_learned = True
    
    def import_csv(self):
        csv_manager.import_csv(self.words, Word)
    
    def export_csv(self):
        csv_manager.export_csv(self.words)
    
    def __str__(self):
        return f'{self.name}'