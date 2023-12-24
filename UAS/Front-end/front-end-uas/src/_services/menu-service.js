import axios from 'axios';
import { environment } from '../environments/environment.js'

const API_Menu = environment.menuUrl;

export const menuService = {
    fetchAllMenus() {
        const url = API_Menu;
        return axios.get(url);
    },
    addMenu(data) {
        const url = API_Menu;
        return axios.post(url, data)
    },
    deleteMenu(id_menu) {
        const url = API_Menu + '/' + id_menu;
        return axios.delete(url)
    },
    fetchMenu(id_menu) {
        const url = API_Menu + '/' + id_menu;
        return axios.get(url);
    },
    updateMenu(id_menu, data){
        const url = API_Menu + '/' + id_menu;
        return axios.put(url, data);
    }
}