import { useSession, getSession } from 'next-auth/react'
import Layout from '../../components/layout'
import client from '../../utils/client'
import axios from 'axios';
import Link from 'next/link';

const handleDeleteItem = id => async (e) => {
    e.preventDefault();
    console.log('clicked')
    try {
        const { data, status } = await axios.delete(`/api/items/${id}`)
        console.log(status)
        console.log(data)
    } catch (err) {
        console.log(err)
    }
}

export default function ListItem({ items = [] }) {

    // As this page uses Server Side Rendering, the `session` will be already
    // populated on render without needing to go through a loading stage.
    // This is possible because of the shared context configured in `_app.js` that
    // is used by `useSession()`.
    const { data: session, status } = useSession()
    const loading = status === 'loading'

    return (
        <Layout>
            <h1>List Items</h1>

            {items.map(x => (
                <div key={x.id}>
                    <div>
                        <div>
                            <img src={x.user.image} />
                            <p style={{ fontWeight: 'bold' }}>Id: <span style={{ fontWeight: 'normal' }}>{x.id}</span></p>
                            <p style={{ fontWeight: 'bold' }}>Name: <span style={{ fontWeight: 'normal' }}>{x.user.name}</span></p>
                        </div>
                        <div>
                            <button>
                                <Link href={`/items/${x.id}`}>
                                    Edit
                                </Link>
                            </button>
                            <button onClick={handleDeleteItem(x.id)}>Delete</button>
                        </div>
                        <p style={{ fontWeight: 'bold' }}>Title: <span style={{ fontWeight: 'normal' }}>{x.title}</span></p>
                        <p style={{ fontWeight: 'bold' }}>Sold: <span style={{ fontWeight: 'normal' }}>{`${x.sold}`}</span></p>
                        <p style={{ fontWeight: 'bold' }}>Description: <span style={{ fontWeight: 'normal' }}>{x.description}</span></p>
                        <p style={{ fontWeight: 'bold' }}>Year: <span style={{ fontWeight: 'normal' }}>{x.year}</span></p>
                        <p style={{ fontWeight: 'bold' }}>price: <span style={{ fontWeight: 'normal' }}>{x.price}</span></p>
                        <p style={{ fontWeight: 'bold' }}>Category: <span style={{ fontWeight: 'normal' }}>{x.category.name}</span></p>
                        <p style={{ fontWeight: 'bold' }}>Brand: <span style={{ fontWeight: 'normal' }}>{x.brand.name}</span></p>
                        <p style={{ fontWeight: 'bold' }}>Images: <span style={{ fontWeight: 'normal' }}>{x.images.length}</span></p>
                        <p style={{ fontWeight: 'bold' }}>Likes: <span style={{ fontWeight: 'normal' }}>{x.likes.length}</span></p>
                        <p style={{ fontWeight: 'bold' }}>Comments: <span style={{ fontWeight: 'normal' }}>{x.comments.length}</span></p>
                        <p style={{ fontWeight: 'bold' }}>Condition: <span style={{ fontWeight: 'normal' }}>{x.condition.name}</span></p>
                        <hr />
                    </div>

                </div>
            ))}

        </Layout>
    )
}

// Export the `session` prop to use sessions with Server Side Rendering
export async function getServerSideProps(context) {
    const { data: items } = await client.get('items/')

    return {
        props: {
            session: await getSession(context),
            items: items['results']
        }
    }
}
