import sqlite3

connect = sqlite3.connect('cards.db')
cursor = connect.cursor()
data = cursor.execute("""SELECT * FROM cards WHERE user_id=(?)""")
cursor.close()
connect.commit()
cursor = connect.cursor()
new_data = []
for i in range(len(data)):
    new_data.append(cursor.execute("""SELECT * FROM products WHERE id=(?)""", [data[i][1]]).fetchall())
cursor.close()
connect.commit()
connect.close()
new_data = [new_data[i][0] for i in range(len(new_data))]
