import axios from 'axios';
import { environment } from '../environments/environment.js'

const API_Admin = environment.adminUrl;

export const authService = {
    login(data_login) {
        const url = API_Admin;
        return axios.post(url, data_login);
    },
}