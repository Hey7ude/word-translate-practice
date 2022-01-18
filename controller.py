import models
import views

user = models.User('user')

win = views.UserPanel(user.add_word)
win.mainloop()