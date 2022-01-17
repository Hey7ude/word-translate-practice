import csv_manager

class Word:
    def __init__(self, word: str, translate: str, is_learned: bool=False, answers: list=[]):
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
        self.words.append(Word(word, translate))
        self.export_csv()
        
    def get_unlearned_words(self):
        for word in self.words:
            if not word.is_learned:
                yield word
    
    def start(self):
        for word in self.get_unlearned_words():
            print(word.word)
            inp = input('type y if you know, type anything else if you dont:\n')
            if inp == 'y':
                word.answers.append(True)
            else:
                word.answers.append(False)
            if word.repeated() % self.repeat == 0:
                inp = input(f'You repeated this word for {word.repeated()} days.\nDid you learned this word? type y if you do:\n')
                if inp == 'y':
                    word.is_learned = True
            self.export_csv()
    
    def import_csv(self):
        csv_manager.import_csv(self.words, Word)
    
    def export_csv(self):
        csv_manager.export_csv(self.words)
    
    def __str__(self):
        return f'{self.name}'