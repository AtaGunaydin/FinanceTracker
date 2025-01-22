import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5005', // Backend portu 5005 olarak ayarlandı
});

export default api;
