import { useState, useEffect } from 'react'
import { useSession, getSession } from 'next-auth/react'
import Layout from '../../components/layout'
import AccessDenied from '../../components/access-denied'
import client from '../../utils/client'
import axios from 'axios'

const handleSubmit = id => (async e => {
    e.preventDefault()
    const formData = new FormData(e.target);

    const _data = [...formData.entries()]
        .reduce((acc, [k, v]) => ({ ...acc, ...{ [k]: v } }), {})

    try {
        const { data: item } = await axios.patch(`/api/items/${id}/`, _data);
        console.log('item', item)
    } catch (err) {
        console.log(err)
    }
});

export default function UpdateItem({
    brands = [],
    conditions = [],
    categories = [],
    item = {}
}) {
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
            <h1>Edit Item</h1>
            <form name="myForm" onSubmit={handleSubmit(item.id)}>
                <div>
                    <label>
                        Title
                    </label>
                    <input name="title" type="text" defaultValue={item.title} />
                </div>
                <div>
                    <label>
                        Description
                    </label>
                    <br />
                    <textarea name="description" defaultValue={item.description} />
                </div>
                <div>
                    <label>
                        Brand
                    </label>
                    <select name="brand" defaultValue={item.brand}>
                        {brands.map((x, i) => (
                            <option
                                key={x.id}
                                value={x.id}
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
                    <select name="category" defaultValue={item.category}>
                        {categories.map((x, i) => (
                            <option
                                key={x.id}
                                value={x.id}
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
                    <select name="condition" defaultValue={item.condition}>
                        {conditions.map((x, i) => (
                            <option
                                key={x.id}
                                value={x.id}
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
                    <input name="sold" type="checkbox" defaultChecked={item.sold} />
                </div>
                <div>
                    <label >
                        price
                    </label>
                    <input name="price" type="number" defaultValue={item.price} />
                </div>
                <div>
                    <label>
                        year
                    </label>
                    <input name="year" type="number" defaultValue={item.year} />
                </div>
                <div>
                    <input name="userId" type="hidden" value="id" />
                </div>
                <input
                    type="submit"
                    value="Update"
                />
            </form>
        </Layout>
    )
}

export async function getServerSideProps(context) {
    const { query } = context;
    const { id } = query;
    const { data: { results: brands } } = await client.get('brands/')
    const { data: { results: conditions } } = await client.get('conditions/')
    const { data: { results: categories } } = await client.get('categories/')
    const { data: item } = await client.get(`items/${id}`)

    return {
        props: {
            session: await getSession(context),
            brands,
            conditions,
            categories,
            item,
        }
    }
}
