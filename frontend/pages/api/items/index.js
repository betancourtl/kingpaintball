import client from '../../../utils/client'


export default async (req, res) => {
    if (req.method == 'GET') {
        try {
            const { status, data } = await client.post('items/', req.body);
            res.status(status).send(data)
        } catch ({ response: { status, data } }) {
            res.status(status).send(data)
        }
    }
    if (req.method == 'POST') {
        try {
            const { status, data } = await client.post('items/', req.body);
            res.status(status).send(data)
        } catch ({ response: { status, data } }) {
            res.status(status).send(data)
        }
    }
}
