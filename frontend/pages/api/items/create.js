import client from "../../utils/client"

export default async function handler(req, res) {
    if (req.method == 'POST') {
        console.log(req.body)
        const { data } = await client.post('items/', req.body)
        res.status(200).json(data)
    } else {
        res.status(200).json({ name: 'GET' })
    }
}
