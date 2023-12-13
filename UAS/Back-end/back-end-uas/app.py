from flask import Flask, render_template, request, make_response, session, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import base64

app = Flask(__name__)

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
    id_order = db.Column(db.String(100), primary_key=True)
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

# Pengambilan data melalui FORM
# @app.route('/admin-login', methods=['POST'])
# def login():
#     username = request.form.get('username')  # Menggunakan request.form untuk mengambil data dari form

#     admin = Admin.query.filter_by(username=username).first()

#     if admin:
#         admin_data = {
#             'id_admin': admin.id_admin,
#             'username': admin.username,
#             'password': admin.password
#         }
#         return jsonify({'admin': admin_data}), 200
#     else:
#         return jsonify({'message': 'Admin not found'}), 404


@app.route('/admin_login')
def admin_login():
    return render_template('staff_login.html')

# Pengambilan data dalam bentuk FORM
# @app.route('/menu-insert', methods=['POST'])
# def insert_menu():
#     try:
#         idMenu = request.form['idMenu']
#         namaMenu = request.form['namaMenu']
#         hargaMenu = int(request.form['hargaMenu'])
#         tipeMenu = request.form['tipeMenu']
#         gambarMenu = request.files['gambarMenu'].read()  # Ambil data dari file

#         menu = Menu(
#             id_menu=idMenu,
#             nama_menu=namaMenu,
#             harga=hargaMenu,
#             tipe=tipeMenu,
#             gambar=gambarMenu
#         )
#         db.session.add(menu)
#         db.session.commit()

#         return jsonify({'message': 'Menu inserted successfully'}), 200
#     except Exception as e:
#         return jsonify({'message': str(e)}), 500

# Pengambilan data dalam bentuk JSON
@app.route('/menu-insert', methods=['POST'])
def insert_menu():
    try:
        idMenu = request.form['idMenu']
        namaMenu = request.form['namaMenu']
        hargaMenu = int(request.form['hargaMenu'])
        tipeMenu = request.form['tipeMenu']
        gambarMenu = request.files['gambarMenu'].read()
        
        # Konversi gambar ke dalam format Base64
        gambarMenu_base64 = base64.b64encode(gambarMenu).decode('utf-8')

        # Simpan ke dalam database
        menu = Menu(
            id_menu=idMenu,
            nama_menu=namaMenu,
            harga=hargaMenu,
            tipe=tipeMenu,
            gambar=base64.b64decode(gambarMenu_base64)  # Dekode Base64 ke format BLOB
        )
        db.session.add(menu)
        db.session.commit()

        return jsonify({'message': 'Menu inserted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
@app.route('/insert-menu')
def menu_insert():
    return render_template('menu_insert.html')

@app.route('/show-inserted-menu', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True)