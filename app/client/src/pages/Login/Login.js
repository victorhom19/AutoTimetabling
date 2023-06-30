import React, {useState} from 'react';
import 'src/scss/pages/Login/Login.scss'
import {useDispatch} from "react-redux";
import {useActions} from "../../hooks/useActions";

const Login = ({onClose}) => {

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(false)
    const [success, setSuccess] = useState(false)

    const {login} = useActions()

    const handleLogin = async () => {
        setLoading(true)
        setError(false)
        setSuccess(false)

        await fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/login`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `username=${username}&password=${password}`
        })
        .then(res => {
            setLoading(false)
            if (200 <= res.status && res.status < 300) {
                setSuccess(true)
                fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/profile`, {
                    method: 'GET',
                    credentials: 'include'
                })
                .then(res => res.json())
                .then(login)
                .then(onClose)
            } else {
                setError(true)
            }
        })

    }

    const handleKeyPressed = async (e) => {
        if (e.key === 'Enter') {
            await handleLogin()
        }
    }


    return (
        <div className={'Login'} onKeyPress={handleKeyPressed}>
            <h3>Вход в систему</h3>
            <div>
                <label htmlFor={'login'}>Почта:</label>
                <input
                    name={'login'}
                    placeholder={'example@mail.com'}
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                />
                <label htmlFor={'login'}>Пароль:</label>
                <input
                    name={'password'}
                    placeholder={'Пароль'}
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    type={'password'}
                />
            </div>

            <button onClick={handleLogin} className={error ? 'Error' : null}>Вход</button>
        </div>
    );
};

export default Login;