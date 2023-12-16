from flask import Flask, render_template, request, make_response, session, redirect, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import base64

app = Flask(__name__)
CORS(app)

app.secret_key = 'UASWeb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/restoran'
app.config['SQLALCHEMT_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model untuk tabel Admin
class Admin(db.Model):
    id_admin = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Model untuk tabel Meja
class Meja(db.Model):
    no_meja = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=True)

# Model untuk tabel Menu
class Menu(db.Model):
    id_menu = db.Column(db.String(11), primary_key=True)
    nama_menu = db.Column(db.String(255), nullable=True)
    harga = db.Column(db.Integer, nullable=True)
    tipe = db.Column(db.String(255), nullable=True)
    gambar = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, id_menu, nama_menu, harga, tipe, gambar):
        self.id_menu = id_menu
        self.nama_menu = nama_menu
        self.harga = harga
        self.tipe = tipe
        self.gambar = gambar

# Model untuk tabel Order
class Order(db.Model):
    order_id = db.Column(db.String(100), primary_key=True)
    status_order = db.Column(db.String(255))
    id_menu = db.Column(db.String(11), db.ForeignKey('menu.id_menu'))
    no_meja = db.Column(db.Integer, db.ForeignKey('meja.no_meja'))
    nama_reservasi = db.Column(db.String(255))

# Pengambilan data dalam bentuk JSON
@app.route('/admin-login', methods=['POST'])
def login():
    data = request.json 
    username = data.get('username')

    admin = Admin.query.filter_by(username=username).first()

    if admin:
        admin_data = {
            'id_admin': admin.id_admin,
            'username': admin.username,
            'password': admin.password
        }
        return jsonify({'admin': admin_data}), 200
    else:
        return jsonify({'message': 'Admin not found'}), 404

@app.route('/admin_login')
def admin_login():
    return render_template('staff_login.html')

# Pengambilan data dalam bentuk JSON
@app.route('/menu-insert', methods=['POST'])
def insert_menu():
    try:
        data = request.json  # Mengambil data JSON dari permintaan

        namaMenu = data['namaMenu']
        hargaMenu = int(data['hargaMenu'])
        tipeMenu = data['tipeMenu']

        # Ambil gambar dari data JSON sebagai string Base64
        gambarMenu_base64 = data['gambarMenu']

        # Konversi gambar dari Base64 ke bentuk binary
        gambarMenu = base64.b64decode(gambarMenu_base64)
        jumlah_menu = Menu.query.filter_by(tipe=tipeMenu).count()
        
        if tipeMenu == 'Minuman':
            id_menu = 'B' + str(jumlah_menu + 1)
        else:
            id_menu = 'F' + str(jumlah_menu + 1)

        # Simpan data menu ke dalam database
        menu = Menu(
            id_menu=id_menu,
            nama_menu=namaMenu,
            harga=hargaMenu,
            tipe=tipeMenu,
            gambar=gambarMenu 
        )
        db.session.add(menu)
        db.session.commit()

        return jsonify({'message': 'Menu inserted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
@app.route('/insert-menu')
def menu_insert():
    return render_template('menu_insert.html')

# Rute untuk mengedit menu
@app.route('/menu-update/<id_menu>', methods=['PUT'])
def update_menu(id_menu):
    try:
        data = request.json 

        menu = Menu.query.filter_by(id_menu=id_menu).first()

        if menu:
            menu.nama_menu = data.get('namaMenu', menu.nama_menu)
            menu.harga = int(data.get('hargaMenu', menu.harga))
            menu.tipe = data.get('tipeMenu', menu.tipe)

            # Update gambar jika ada perubahan
            if 'gambarMenu' in data:
                gambarMenu_base64 = data['gambarMenu']
                gambarMenu = base64.b64decode(gambarMenu_base64)
                menu.gambar = gambarMenu

            db.session.commit()

            return jsonify({'message': 'Menu updated successfully'}), 200
        else:
            return jsonify({'message': 'Menu not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Rute pengambilan menu yang ingin di edit sesuai dengan id nya
@app.route('/get-menu/<id_menu>', methods=['GET'])
def get_menu(id_menu):
    try:
        menu = Menu.query.filter_by(id_menu=id_menu).first()

        if menu:
            # Mengubah data gambar BLOB ke format base64
            if menu.gambar:
                image_base64 = base64.b64encode(menu.gambar).decode('utf-8')
                menu.image_base64 = f"data:image/jpeg;base64,{image_base64}"

            return jsonify({
                'id_menu': menu.id_menu,
                'nama_menu': menu.nama_menu,
                'harga': menu.harga,
                'tipe': menu.tipe,
                'gambar': menu.image_base64 if menu.gambar else None
            }), 200
        else:
            return jsonify({'message': 'Menu not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Rute uji coba untuk mengecek apakah editnya berfungsi atau tidak
@app.route('/menu-edit/<id_menu>', methods=['GET'])
def show_edit_menu(id_menu):
    return render_template('menu_edit.html', id_menu=id_menu)

@app.route('/menu-delete/<id_menu>', methods=['DELETE'])
def delete_menu(id_menu):
    try:
        menu = Menu.query.filter_by(id_menu=id_menu).first()

        if menu:
            db.session.delete(menu)
            db.session.commit()
            return jsonify({'message': 'Menu deleted successfully'}), 200
        else:
            return jsonify({'message': 'Menu not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/show-menu', methods=['GET'])
def show_inserted_menu():
    try:
        menus = Menu.query.all()

        for menu in menus:
            if menu.gambar:
                # Mengubah data gambar BLOB ke format base64
                image_base64 = base64.b64encode(menu.gambar).decode('utf-8')
                menu.image_base64 = f"data:image/jpeg;base64,{image_base64}"

        return render_template('menu.html', menus=menus)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/order')
def order():
    menus = Menu.query.all()

    # Mengambil nomor meja dengan status 'AVAILABLE'
    available_tables = Meja.query.filter_by(status='AVAILABLE').all()

    # Membuat list untuk nama menu dan nomor meja yang tersedia
    available_menu_names = [menu.nama_menu for menu in menus]
    available_table_numbers = [table.no_meja for table in available_tables]
    
    return render_template("order.html", menu_names=available_menu_names, table_numbers=available_table_numbers)

    
@app.route('/submit_order', methods=['POST'])
def submit_order():
    if request.method == 'POST':
  
        data = request.get_json()  
        nama_reservasi = data.get('reservasi')
        nomor_meja = data.get('tables')
        status_order = data.get('status_order')
        menu_selected = data.get('selected_menu[]')
        meja = Meja.query.filter_by(no_meja=nomor_meja).first()
        if meja:
            meja.status = 'OCCUPIED'
        
        # Get the count of orders in the Order table
        count_orders = Order.query.count()

        # Fetch all menus based on the names of the menus selected
        menus = Menu.query.filter(Menu.nama_menu.in_(menu_selected)).all()
        if not menus:
            return jsonify({'error': 'Menus not found'}), 404

        # Extract all id_menu from the list of menus
        id_menus = [menu.id_menu for menu in menus]

        # Inserting data into the Order table for each menu selected
        for id_menu in id_menus:
            new_id_order = f"ORD-{count_orders + 1}"
            new_order = Order(
                order_id=new_id_order,
                status_order=status_order,
                id_menu=id_menu,
                no_meja=nomor_meja,
                nama_reservasi=nama_reservasi
            )
            db.session.add(new_order)
          
        db.session.commit()

        # Create a dictionary with the data
        response_data = {
            'message': 'Order submitted successfully',
            'nama_reservasi': nama_reservasi,
            'nomor_meja': nomor_meja,
            'status_order': status_order,
            'selected_menu': menu_selected
            # Add more data as needed
        }

        return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)