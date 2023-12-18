import axios from 'axios';
import { environment } from '../environments/environment.js'

const API_Order = environment.orderUrl;

export const orderService = {
    fetchAllOrders() {
        const url = API_Order;
        return axios.get(url);
    },
    closeOrder(order_id, data) {
        const url = API_Order + '/' + order_id;
        return axios.put(url, data);
    },
    createOrder(data){
        const url = API_Order;
        return axios.post(url, data);
    }
}