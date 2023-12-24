import axios from 'axios';
import { environment } from '../environments/environment.js'

const API_Meja = environment.mejaUrl;

export const mejaService = {
    fetchAllTables() {
        const url = API_Meja;
        return axios.get(url);
    },
    fetchMenu(id_meja) {
        const url = API_Meja + '/' + id_meja;
        return axios.get(url);
    },
    updateMenu(id_meja, data){
        const url = API_Meja + '/' + id_meja;
        return axios.put(url, data);
    }
}