import client from '../../../utils/client'


export default async (req, res) => {
    const { id } = req.query

    if (req.method == 'DELETE') {
        try {
            const { status, data } = await client.delete(`items/${id}/`);
            res.status(status).send(data)
        } catch ({ response: { status, data } }) {
            res.status(status).send(data)
        }
    }
    if (req.method == 'PATCH') {
        try {
            const { status, data } = await client.patch(`items/${id}/`, req.body);
            res.status(status).send(data)
        } catch ({ response: { status, data } }) {
            res.status(status).send(data)
        }
    }
}
