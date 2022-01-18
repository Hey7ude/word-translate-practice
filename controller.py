import models
import views

user = models.User('user')

win = views.UserPanel(user.words, user.add_word, user.add_answer, user.check_repeated, user.learned, user.export_csv)
win.mainloop()