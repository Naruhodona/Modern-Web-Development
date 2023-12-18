<template>
    <div class="orders">
        <table class="table">
            <thead>
                <tr>
                    <th>ID Order</th>
                    <th>Nama Reservasi</th>
                    <th>Nomor Meja</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="order in orders" :key="order.kode_order">
                    <td>{{ order.order_id }}</td>
                    <td>{{ order.nama_reservasi }}</td>
                    <td>{{ order.no_meja }}</td>
                    <td><b-button variant="primary" @click="changeStatusOrder(order.order_id, order.no_meja)">Close Order</b-button></td>
                </tr>
            </tbody>
        </table>
        
    </div> 
    
</template>

<script>
import { orderService } from '@/_services/order-service';
export default {
    name: 'OrderView',
    data(){
        return {
            orders: [],
        }
    },
    methods: {
        refreshTable(){
            this.orders = [];
            orderService.fetchAllOrders()
                .then(response => {
                    const temp_data = response.data.orders_with_details;
                    temp_data.forEach((order) => {
                        const orderExists = this.orders.some(existingOrder => existingOrder.order_id === order.order_id);
                        
                        if (!orderExists) {
                            this.orders.push(order);
                        }
                    })
                });
            
        },
        changeStatusOrder(order_id, no_meja){
            const data = {
                no_meja: no_meja,
            };
            orderService.closeOrder(order_id,data).then(() => {
                this.refreshTable();
            });
        }
    },
    mounted(){
        const temp_data = this.$route.params.orders;
        temp_data.forEach((order) => {
            const orderExists = this.orders.some(existingOrder => existingOrder.order_id === order.order_id);
            
            if (!orderExists) {
                this.orders.push(order);
            }
        })
    }
}
</script>

<style scoped>
    table td {
        vertical-align: middle;
    }
</style>