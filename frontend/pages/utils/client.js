import axios from 'axios';

const client = axios.create({
    baseURL: 'http://backend:8000/api/',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQwNTU0NDQ0LCJpYXQiOjE2NDA1NTQxNDQsImp0aSI6IjBjZjI2NDdmYTRlYTRiODg4ZmZiOWI0Y2RhYmI0ODZjIiwidXNlcl9pZCI6MX0.R8mV9Xr7FLRHZqWw7HHD7vGIhG7--bMxcyivFZocDFY'
    }
});

export default client
