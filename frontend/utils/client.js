import axios from 'axios';

const client = axios.create({
    baseURL: 'http://backend:8000/api/',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token e445443750d77eb3b09522ad1312faa57f66523a'
    }
});

export default client
