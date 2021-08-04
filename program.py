#sumaya ferreira de almeida
#OOP - assessment - Bank Management App
#due date: 02/08/2021


from datastore import Datastore 
from usermenu import UserMenu

#instantiate datastore object (the initializer creates a empty list of customer accounts and load the list of customer accounts from the file )
datastore = Datastore()
user_menu = UserMenu()


user_menu.do_user_menu(datastore)
