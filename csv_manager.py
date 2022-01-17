import csv 

def open_file_or_create(name: str, mode):
    try:
        return open(name, mode)
    except:
        f = open(name, 'a')
        f.close()
        return open(name, mode)

def import_csv(words_list: list, class_name, filename = 'data.csv'):
    csv_file = open_file_or_create(filename, 'r')
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        word = line['word']
        translate = line['translate']
        is_learned = True if line['is_learned'] == 'True' else False
        answers = line['answers'][1:-1].replace(' ', '').split(',')
        print(len(answers))
        for i in range(len(answers)):
            if answers[i] == 'True':
                answers[i] = True
            elif answers[i] == 'False':
                answers[i] = False
            else:
                answers = []
        words_list.append(class_name(word=word, translate=translate, is_learned=is_learned, answers=answers))
    csv_file.close()
      
def export_csv(words_list: list, file_name='data.csv'):
        csv_file = open_file_or_create(file_name, 'w') 
        csv_writer = csv.DictWriter(csv_file, fieldnames=words_list[0].__dict__.keys())
        csv_writer.writeheader()
        for i in range(len(words_list)):
            csv_writer.writerow(words_list[i].__dict__)
        csv_file.close()
        
            
            
