import { useState, useEffect } from 'react'
import { useSession, getSession } from 'next-auth/react'
import Layout from '../../components/layout'
import AccessDenied from '../../components/access-denied'
import client from '../../utils/client'
import axios from 'axios'

const handleSubmit = (async e => {
    e.preventDefault()
    const formData = new FormData(e.target);

    const _data = [...formData.entries()]
        .reduce((acc, [k, v]) => ({ ...acc, ...{ [k]: v } }), {})

    try {
        const { data: item } = await axios.post('/api/items/', _data);
        console.log('item', item)
    } catch (err) {
        console.log(err)
    }
});

export default function CreateItem({ brands = [], conditions = [], categories = [] }) {
    const { data: session, status } = useSession()
    const loading = status === 'loading'
    const [content, setContent] = useState()

    // Fetch content from protected route
    useEffect(() => {
        const fetchData = async () => {
            const res = await fetch('/api/examples/protected')
            const json = await res.json()
            if (json.content) { setContent(json.content) }
        }
        fetchData()
    }, [session])

    // When rendering client side don't display anything until loading is complete
    if (typeof window !== 'undefined' && loading) return null

    // If no session exists, display access denied message
    if (!session) { return <Layout><AccessDenied /></Layout> }

    // If session exists, display content
    return (
        <Layout>
            <h1>Create Item</h1>
            <form name="myForm" onSubmit={handleSubmit}>
                <div>
                    <label>
                        Title
                    </label>
                    <input name="title" type="text" defaultValue="Planet Eclipse For Sale" />
                </div>
                <div>
                    <label>
                        Description
                    </label>
                    <br />
                    <textarea name="description" defaultValue="Buy it now!" />
                </div>
                <div>
                    <label>
                        Brand
                    </label>
                    <select name="brand">
                        {brands.map((x, i) => (
                            <option
                                key={x.id}
                                value={x.id}
                                defaultValue={i == 0}
                            >
                                {x.name}
                            </option>
                        )
                        )}
                    </select>
                </div>
                <div>
                    <label>
                        Categories
                    </label>
                    <select name="category">
                        {categories.map((x, i) => (
                            <option
                                key={x.id}
                                value={x.id}
                                defaultValue={i == 0}
                            >
                                {x.name}
                            </option>
                        ))}
                    </select>
                </div>
                <div>
                    <label>
                        Conditions
                    </label>
                    <select name="condition">
                        {conditions.map((x, i) => (
                            <option
                                key={x.id}
                                value={x.id}
                                defaultValue={i == 0}
                            >
                                {x.name}
                            </option>
                        ))}
                    </select>
                </div>
                <div>
                    <label>
                        Sold
                    </label>
                    <input name="sold" type="checkbox" defaultChecked={true} />
                </div>
                <div>
                    <label >
                        price
                    </label>
                    <input name="price" type="number" defaultValue={199.99} />
                </div>
                <div>
                    <label>
                        year
                    </label>
                    <input name="year" type="number" defaultValue={2009} />
                </div>
                <div>
                    <input name="userId" type="hidden" value="id" />
                </div>
                <input
                    type="submit"
                    value="create"
                />
            </form>
        </Layout>
    )
}

export async function getServerSideProps(context) {
    const { req, res } = context;
    const { data: { results: brands } } = await client.get('brands/')
    const { data: { results: conditions } } = await client.get('conditions/')
    const { data: { results: categories } } = await client.get('categories/')

    return {
        props: {
            session: await getSession(context),
            brands,
            conditions,
            categories,

        }
    }
}
