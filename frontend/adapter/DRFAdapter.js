
const to_session = (session) => ({
    ...session,
    sessionToken: session.session_token,
    expires: new Date(session.expires)
});

/** @return { import("next-auth/adapters").Adapter } */
export default function DRFAdapter(client, options = {}) {
    return {
        async createUser(user) {
            try {
                const { data } = await client.post('users/', user)
                return data;
            } catch (err) {
                console.log('createUser error', err)
                return null
            }

        },
        async getUser(id) {
            try {
                const { data } = await client.get(`users/${id}/`)

                return data
            } catch (err) {
                console.log('getUser', err)
            }

        },
        async getUserByEmail(email) {
            try {
                const { data: userData } = await client.get(`users/`, {
                    params: { email, }
                })
                if (userData.count == 0) return

                const user = userData.results[0]
                return user;


            } catch (err) {
                console.log('getUserByEmail')
            }
        },
        async getUserByAccount({ provider, providerAccountId }) {
            try {
                const { data: accountData } = await client.get('accounts/', {
                    params: {
                        provider: provider,
                        providerAccountId: providerAccountId,
                    }
                })

                if (accountData.count == 0) return

                const account = accountData.results[0];

                const { data: userData } = await client.get(`users/${account.userId}/`)

                return userData.id ? userData : null

            } catch (err) {
                console.log('getUserByAccount', err)
            }
        },
        async updateUser(user) {
            try {
                const { data } = await client.patch(`users/${user.id}`, { user })
                return data;
            } catch (err) {
                console.log('updateUser')
            }
        },
        async deleteUser(userId) {
            try {
                await client.delete(`users/${user.id}/`)
                return
            } catch (err) {
                console.log('deleteUser')
            }
        },
        async linkAccount(account) {
            try {
                const { data } = await client.post(`accounts/`, account)
                return data
            } catch (err) {
                console.log('linkAccount error', err)
            }
        },
        async unlinkAccount({ provider, providerAccountId }) {
            try {
                const { data: accountData } = client.get('accounts/', {
                    params: {
                        provider,
                        providerAccountId
                    }
                })

                if (!accountData) return null

                await client.delete('/accounts/', {
                    params: {
                        id: accountData.id,
                    }
                })
                return
            } catch (err) {
                console.log('unlinkAccount')
            }
        },
        async createSession({ sessionToken, userId, expires }) {
            try {
                const { data: sessionData } = await client.post(`sessions/`, {
                    session_token: sessionToken,
                    userId: userId,
                    expires: expires.toJSON(),
                })

                return to_session(sessionData);

            } catch (err) {
                console.log('createSession')
            }
        },
        async getSessionAndUser(sessionToken) {
            try {
                const { data: sessionData } = await client.get(`sessions/`, {
                    params: {
                        session_token: sessionToken
                    }
                })

                if (sessionData.count == 0) return null

                const session = sessionData.results[0];

                const { data: userData } = await client.get(`users/${session.userId}/`);

                return {
                    session: to_session(session),
                    user: userData,
                }
            } catch (err) {
                console.log('getSessionAndUser')
            }
        },
        async updateSession({ sessionToken, expires }) {
            try {
                const { data: sessionData } = await client.get(`sessions/`, {
                    params: {
                        session_token: sessionToken
                    }
                })

                if (sessionData.count == 0) return

                const oldSession = sessionData.results[0];

                const { data: newSessionData } = await client.patch(`sessions/${oldSession.id}/`, {
                    expires,
                    session_token: sessionToken
                })

                return to_session(newSessionData)
            } catch (err) {
                console.log('updateSession')
            }
        },
        async deleteSession(sessionToken) {
            try {

                const { data: sessionData } = await client.get(`sessions/`, {
                    params: {
                        session_token: sessionToken
                    }
                })

                if (sessionData.count == 0) return

                session = sessionData.results[0]

                await client.delete(`sessions/${session.id}/`)
            } catch (err) {
                console.log('deleteSession')
            }
        },
        async createVerificationToken({ identifier, expires, token }) {
            try {
                const { data: vtData } = await client.post('verification-tokens/', {
                    identifier,
                    expires,
                    token
                })

                return vtData
            } catch (err) {
                console.log('createVerificationToken')
            }
        },
        async useVerificationToken({ identifier, token }) {
            try {
                const { data: vtData } = await client.get('verification-tokens/', {
                    params: {
                        identifier,
                        token
                    }
                })

                if (vtData.count !== 1) return null

                await client.delete(`verification-tokens/${vtData.id}`)

                return vtData
            } catch (err) {
                console.log('useVerificationToken')
            }
        },
    }
}
