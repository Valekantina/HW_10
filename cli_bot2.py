from collections import UserDict
import time

# creating AddressBook class that will take in information from UserDict
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

# creating a parent Field clas that will be passed onto Name, Phone and Record classes
class Field:
    pass

# creating Name class 
class Name(Field):
    def __init__(self, value):
        self.value = value

# creating Phone class    
class Phone(Field):
    def __init__(self, phone):
        self.value = phone

# creating Record class, where Name is a must, but phone number is optional
class Record(Field):
    def __init__(self, name, phone=None):
        self.name = Name(name)
        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []
    # defining add_phone function within class, that will add a phone number to a phones dictionary
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    # defining change_phone within class, that takes in old and new numbers and adds them to contact
    def change_phone(self, old_phone, new_phone):
        for i in self.phones:
            if i.value == old_phone:
                i.value = new_phone
    # definind delete function within class, that will remove the number from phones dictionary
    def delete(self, phone):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)

contacts = AddressBook()

def parser(user_input: str):
    comm = None #commands
    param = [] # parameters

#dict of all known to the bot operations
    operations = {
        "hello": hello,
        "hi": hello,
        "hey":hello,
        "help": help,
        "add": add,
        "change": change,
        "show all": show_all,
        "good bye": exit,
        "bye": exit,
        "close": exit,
        "exit": exit,
        "phone": phone_number,
        "delete": delete,
    }
    for k in operations:
        if user_input.lower().startswith(k):
            comm = operations[k]
            user_input = user_input.lstrip(k)
            for i in filter(lambda x: x!= "", user_input.split(" ")):
                param.append(i)
            return comm, param
    return comm, param
# creating simple functions for help, hello and exit, as they do not require error handler
def help(*args) -> str:
    return f"I know these commands: hello, help, add, change, delete, phone, show all, good bye, bye, close, exit"

def hello() -> str:
    return f"How can I help you?"

def exit():
    print(f"Good bye!")
    time.sleep(1.5) # added delay on quit() so the message "Good bye!" is visible
    quit()

# creating main function thar will interact with the user
def main():
    print(hello())
    while True:
        user_input = input("Input command: ")
        comm, param = parser(user_input)
        if comm:
            print(comm(*param))
        else:
            print (f"Sorry, I do not know this command, please try again. Or type'help' for help")
# creating error wrapper
def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError:
            return f"Please provide me with a name and a phone number or name, old number and new number"
        except IndexError:
            return f"Sorry, you have not provided enough arguments"
        except KeyError:
            return f"This name does not exist in contacts"
    return wrapper

# creating function to add new contacts
@input_error
def add(*args) -> str:
    name, number, *_ = args
    if not name in contacts:
        new_number = Record(name, number)
        contacts.add_record(new_number)
        return f"Contact was added successfully"
    else:
        contacts[name].add_phone(number)
        return f"The new number has been added to contact {name}"

# creating function to change existing contact
@input_error
def change(*args) -> str:
    name, old_number, new_number, *_ = args
    if name in contacts:
        contacts[name].change_phone(old_number, new_number)
    else:
        return f"There is no contact under name '{name}'. If you wish to add the contact, please choose 'add'"
    return f"Contact was changed successfully"

# creating function to display contacts_list
@input_error
def show_all() -> str:
    result = []
    for name, numbers in contacts.items():
        result.append(f"Name: {name} | Numbers: {', '.join(phone.value for phone in numbers.phones)}")
    if len(result) <1:
        return f"You have not added any contacts yet"
    return "\n".join(result)

# creating function to view phone number of a chosen person from contact_list
@input_error
def phone_number(*args) -> str:
    name = args[0]
    if name in contacts:
        for name, numbers in contacts.items():
            return f"Name: {name} | Numbers: {', '.join(phone.value for phone in numbers.phones)}"
    else:
        return f"There is no contact under name '{name}'. If you wish to add the contact, please choose 'add'"

# creating function to remove the phone number from the record
@input_error
def delete(name, phone) -> str:
    if name in contacts:
        contacts[name].delete(phone)
    else:
        return f"There is no contact under name '{name}'"
    return f"The phone number has been successfully removed"


# making sure the code will only run when .py file is executed as a script
if __name__ == "__main__":
    main()
