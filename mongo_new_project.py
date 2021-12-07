import os
import pymongo
if os.path.exists("env.py"):
    import env


MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("YYYYYYYAAAAAASSSSSSSS!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


def get_record():
    print()
    first = input("first name: ")
    last = input("last name: ")

    try:
        doc = coll.find_one({"first": first.lower(), "last": last.lower()})
    except:
        print("fail accessing db")
    
    if not doc:
        print("no results found")

    return doc


def show_menu():
    print()
    print("1. Add a record (C-REATE / INSERT_ONE)")
    print("2. Find a record (R-EAD / FIND)")
    print("3. Edit a record (U-PDATE / UPDATE_ONE)")
    print("4. Delete a record (D-ELETE / REMOVE_ONE)")
    print("5. Exit")

    user_choice = input("Enter option:")
    return user_choice


def add_record(coll):
    print()
    first = input("Enter First Name ")
    last = input("Enter last Name ")
    dob = input("Enter dob ")
    gender = input("Enter gender ")
    hair_colour = input("Enter hair_colour ")
    occupation = input("Enter occupation ")
    nationality = input("Enter nationality ")

    new_doc = {
        "first": first.lower,
        "last": last.lower,
        "dob": dob,
        "gender": gender,
        "hair_colour": hair_colour,
        "occupation": occupation,
        "nationality": nationality
    }

    try:
        coll.insert_one(new_doc)
        print()
        print("success! data inserted (lol)")
    except:
        print("you fucking retard! didn't work!")


def find_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())


def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        for k, v in doc.items():
            if k != "_id": #stops id being edited
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")

                if update_doc[k] == "":
                    update_doc[k] = v
                    
        try:
            coll.update_one(doc, {"$set": update_doc})
            print()
            print("update succesfull")
        except:
            print()
            print("error")


def delete_record():
    doc = get_record()
    if doc:
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())
        print()
        confirmation = input("Is this the document you want to delete?\nY or N > ")
        if confirmation.lower() == "y":
            try:
                coll.delete_one(doc)
                print("deleted!")
            except:
                print("error!")
        else:
            print("nothing changed, nothing deleted")


def main_loop(coll):
    while True:
        option = show_menu()
        if option == "1":
            print("ADDING A RECORD SCREEN")
            add_record(coll)
        elif option == "2":
            print("FIND A RECORD SCREEN")
            find_record()
        elif option == "3":
            print("EDIT RECORD SCREEN")
            edit_record()
        elif option == "4":
            print("DELETE RECORD:")
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Not a valid option, enter 1,2,3,4 or 5")
        print()
        

conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop(coll)