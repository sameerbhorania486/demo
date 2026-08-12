import sqlite3                         
                                            
conn = sqlite3.connect("contact.db")   
cursor = conn.cursor()                 
                                      
cursor.execute("""                     
CREATE TABLE IF NOT EXISTS contacts(   
        id INTEGER PRIMARY KEY,        
        name TEXT,                     
        phone TEXT
)
""")
conn.commit()

def add_contact(name, phone):
    cursor.execute("INSERT INTO contacts(name, phone) VALUES (?,?)",(name, phone))
    conn.commit()
    print(f"{name} Added Successfully...!")
    
def show_contacts():
    cursor.execute("SELECT * FROM contacts ")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
def update_contact(name, new_phone):
    cursor.execute("UPDATE contacts SET phone = ? WHERE name = ?",(new_phone, name))
    conn.commit()
    print(f"{name}'s number Updated Successfully...!")
    
def delete_contact(name):
    cursor.execute("DELETE FROM contacts WHERE name = ?",(name,))
    conn.commit()
    print(f"{name} Deleted Successfully...!")
    
add_contact("sameer",9876543210)
add_contact("naved",9867452301)

show_contacts()

update_contact("sameer",7896452310)
show_contacts()

delete_contact("naved")
show_contacts()

conn.close()