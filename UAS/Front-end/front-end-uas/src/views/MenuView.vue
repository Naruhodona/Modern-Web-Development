<template>
    <div class="menus">
        <b-button v-b-modal.modal-1>Add Menu</b-button>
        <b-modal v-model="popupAdd" id="modal-1" title="Add Menu" centered hide-footer>
        <!-- Konten dari komponen popup di sini -->
            <template>
                <b-form-group label="Nama Menu">
                    <b-form-input type="text" v-model="namaMenu" required></b-form-input>
                </b-form-group>
                <b-form-group label="Harga Menu" class="mt-4">
                    <b-form-input type="text" v-model="hargaMenu" required></b-form-input>
                </b-form-group>
                <b-form-group label="Tipe Menu" class="mt-4">
                    <b-form-radio-group :options="['Makanan', 'Minuman']" v-model="tipeMenu" required></b-form-radio-group>
                </b-form-group>
                <b-form-group label="Gambar Menu" class="mt-4">
                    <b-form-file accept=".jpg, .jpeg, .png" @change="onFileChange" plain required></b-form-file>
                </b-form-group>
                <b-button class="center mt-4" variant="outline-primary" @click="addMenu()">Submit</b-button>
            </template>
        </b-modal>
        <b-modal v-model="popupEdit" id="modal-2" title="Edit Menu" centered hide-footer>
        <!-- Konten dari komponen popup di sini -->
            <template>
                <b-form-group label="Nama Menu">
                    <b-form-input type="text" v-model="editNama" required></b-form-input>
                </b-form-group>
                <b-form-group label="Harga Menu" class="mt-4">
                    <b-form-input type="text" v-model="editHarga" required></b-form-input>
                </b-form-group>
                <b-form-group label="Tipe Menu" class="mt-4">
                    <b-form-radio-group :options="['Makanan', 'Minuman']" v-model="editTipe" required></b-form-radio-group>
                </b-form-group>
                <b-form-group label="Gambar Menu" class="mt-4">
                    <b-form-file accept=".jpg, .jpeg, .png" @change="onFileEditChange" plain required></b-form-file>
                </b-form-group>
                <b-button class="center mt-4" variant="outline-primary" @click="updateMenu(id_temp)">Submit</b-button>
            </template>
        </b-modal>
        <table class="table">
            <thead>
                <tr>
                    <th>ID Menu</th>
                    <th>Nama Menu</th>
                    <th>Harga</th>
                    <th>Tipe</th>
                    <th>Gambar</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="menu in menus" :key="menu.id_menu">
                    <td>{{ menu.id_menu }}</td>
                    <td>{{ menu.nama_menu }}</td>
                    <td>{{ menu.harga }}</td>
                    <td>{{ menu.tipe }}</td>
                    <td><img :src="menu.image_base64" alt="Gambar Menu" width="25%"></td>
                    <td><b-button v-b-modal.modal-2 variant="primary" @click="editMenu(menu.id_menu)">Edit</b-button><b-button variant="danger" @click="deleteMenu(menu.id_menu)">Delete</b-button></td>
                </tr>
            </tbody>
        </table>
        
    </div> 
    
</template>

<script>
import { menuService } from '@/_services/menu-service';
export default {
    name: 'MenuView',
    data(){
        return {
            menus: [],
            popupAdd: false,
            popupEdit: false,
            namaMenu: null,
            hargaMenu: null,
            tipeMenu: null,
            gambarMenu: null,
            id_temp: null,
            editNama: null,
            editHarga: null,
            editTipe: null,
            editGambar: null,
        }
    },
    methods: {
        editMenu(id_menu) {
            menuService.fetchMenu(id_menu).then(response => {
                this.id_temp = response.data.id_menu;
                this.editNama = response.data.nama_menu;
                this.editHarga = response.data.harga;
                this.editTipe = response.data.tipe;
            });
        },
        updateMenu(id_temp){
            if (this.editNama && this.editHarga && this.editTipe) {
                const data = {
                    nama_menu: this.editNama,
                    harga: this.editHarga,
                    tipe: this.editTipe,
                    gambar: this.editGambar,
                };
                
                menuService.updateMenu(id_temp, data).then(() => {
                    this.refreshTable();
                    this.popupEdit = false;
                    this.editNama = null;
                    this.editHarga = null;
                    this.editTipe = null;
                    this.editGambar = null;
                });
            } else {
                alert('Fill the form properly');
            }
        },
        deleteMenu(id_menu) {
            menuService.deleteMenu(id_menu).then(() => {
                this.refreshTable();
            });
        },
        addMenu() {
            if (this.namaMenu && this.hargaMenu && this.tipeMenu && this.gambarMenu) {
                const data = {
                    namaMenu: this.namaMenu,
                    hargaMenu: this.hargaMenu,
                    tipeMenu: this.tipeMenu,
                    gambarMenu: this.gambarMenu,
                };
                
                menuService.addMenu(data).then(() => {
                    this.refreshTable();
                    this.popupAdd = false;
                    this.namaMenu = null;
                    this.hargaMenu = null;
                    this.tipeMenu = null;
                    this.gambarMenu = null;
                });
            } else {
                alert('Fill the form properly');
            }
        },
        onFileEditChange(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                this.editGambar = reader.result.split(',')[1];
            }
        },
        onFileChange(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                this.gambarMenu = reader.result.split(',')[1];
            }
        },
        refreshTable(){
            this.menus = [];
            menuService.fetchAllMenus()
                .then(response => {
                    this.menus = response.data.menus;
                });
            
        }
    },
    computed:{
        
    },
    mounted(){
        this.menus = this.$route.params.menus;
    }
}
</script>