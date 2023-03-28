from flask import Flask, render_template, request, redirect, url_for, flash, abort
import sqlite3
from urllib.parse import quote


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY AUTOINCREMENT, supplier_name TEXT NOT NULL, contact_person TEXT, telephone_1 TEXT, telephone_2 TEXT, telephone_3 TEXT, mobile_1 TEXT, mobile_2 TEXT, fax TEXT, email TEXT, website TEXT, address TEXT, term TEXT, notes TEXT)')
    conn.close()

init_database()


def create_product_table():
    # Connect to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS product_pricing
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_id INTEGER,
                product TEXT,
                size TEXT,
                code TEXT,
                brand TEXT,
                price REAL,
                unit TEXT,
                other_details TEXT,
                date TEXT,
                FOREIGN KEY (supplier_id) REFERENCES supplier(id)
                )''')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
create_product_table()


@app.route('/')
def index():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM suppliers').fetchall()
    conn.close()
    return render_template('index.html', rows=rows)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        supplier_name = request.form['supplier_name']
        contact_person = request.form['contact_person']
        telephone_1 = request.form['telephone_1']
        telephone_2 = request.form['telephone_2']
        telephone_3 = request.form['telephone_3']
        mobile_1 = request.form['mobile_1']
        mobile_2 = request.form['mobile_2']
        fax = request.form['fax']
        email = request.form['email']
        website = request.form['website']
        address = request.form['address']
        term = request.form['term']
        notes = request.form['notes']
        conn = get_db_connection()
        conn.execute('INSERT INTO suppliers (supplier_name, contact_person, telephone_1, telephone_2, telephone_3, mobile_1, mobile_2, fax, email, website, address, term, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (supplier_name, contact_person, telephone_1, telephone_2, telephone_3, mobile_1, mobile_2, fax, email, website, address, term, notes))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM suppliers WHERE id = ?', (id,)).fetchone()
    conn.close()
    if request.method == 'POST':
        supplier_name = request.form['supplier_name']
        contact_person = request.form['contact_person']
        telephone_1 = request.form['telephone_1']
        telephone_2 = request.form['telephone_2']
        telephone_3 = request.form['telephone_3']
        mobile_1 = request.form['mobile_1']
        mobile_2 = request.form['mobile_2']
        fax = request.form['fax']
        email = request.form['email']
        website = request.form['website']
        address = request.form['address']
        term = request.form['term']
        notes = request.form['notes']
        conn = get_db_connection()
        conn.execute('UPDATE suppliers SET supplier_name = ?, contact_person = ?, telephone_1 = ?, telephone_2 = ?, telephone_3 = ?, mobile_1 = ?, mobile_2 = ?, fax = ?, email = ?, website = ?, address = ?, term = ?, notes = ? WHERE id = ?', (supplier_name, contact_person, telephone_1, telephone_2, telephone_3, mobile_1, mobile_2, fax, email, website, address, term, notes, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('edit.html', row=row)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM suppliers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        conn = get_db_connection()
        cur = conn.execute('SELECT * FROM suppliers WHERE supplier_name LIKE ? OR contact_person LIKE ? OR email LIKE ? OR address LIKE ? ORDER BY id DESC',
                          ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        rows = cur.fetchall()
        conn.close()
        return render_template('index.html', rows=rows)
    return redirect(url_for('index'))

@app.route('/view/<int:id>')
def view(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM suppliers WHERE id=?', (id,))
    supplier_data = c.fetchone()
    conn.close()
    return render_template('view.html', supplier=supplier_data)

@app.route('/product_pricing/<int:supplier_id>', methods=['GET', 'POST'])
def product_pricing(supplier_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if request.method == 'POST':
        product = request.form['product']
        size = request.form['size']
        code = request.form['code']
        brand = request.form['brand']
        price = request.form['price']
        unit = request.form['unit']
        other_details = request.form['other_details']
        date = request.form['date']

        # Insert the new product pricing into the database
        c.execute('''INSERT INTO product_pricing
                     (supplier_id, product, size, code, brand, price, unit, other_details, date)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (supplier_id, product, size, code, brand, price, unit, other_details, date))
        conn.commit()
    # Get the list of product pricing for the selected supplier
    # c.execute('''SELECT * FROM product_pricing WHERE supplier_id = ?''', (supplier_id,))
    c.execute("SELECT * FROM product_pricing WHERE supplier_id = ?", (supplier_id,))
    product_pricing = c.fetchall()

    # Get the supplier details
    c.execute('''SELECT * FROM suppliers WHERE id = ?''', (supplier_id,))
    supplier = c.fetchone()

    conn.close()
    return render_template('product_pricing.html', supplier=supplier, product_pricing=product_pricing)
    


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)


