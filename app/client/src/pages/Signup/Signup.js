import React, {useState} from 'react';
import 'src/scss/pages/Signup/Signup.scss'
import {useActions} from "../../hooks/useActions";

const Signup = ({onClose}) => {

    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [repeatPassword, setRepeatPassword] = useState('')

    const [usernameError, setUsernameError] = useState(false)
    const [emailError, setEmailError] = useState(false)
    const [passwordError, setPasswordError] = useState(false)
    const [passwordRepeatError, setPasswordRepeatError] = useState(false)

    const validateUsername = () => username.match(/^[a-zA-Z]+[a-zA-Z0-9]*$/) && username.length > 5

    const validateEmail = () => email.match(/^[a-zA-Z]+[a-zA-Z0-9.]*@[a-z0-9-.]+$/)

    const validatePassword = () => password.match(/^[a-zA-Z0-9.-?!]{7,}$/)

    const {login} = useActions()

    const handleSignup = () => {
        let error = false
        setUsernameError(false)
        setEmailError(false)
        setPasswordError(false)
        setPasswordRepeatError(false)


        if (!validateUsername()) {
            setUsernameError(true)
            error = true
        }
        if (!validateEmail()) {
            setEmailError(true)
            error = true
        }
        if (!validatePassword()) {
            setPasswordError(true)
            error = true
        }
        if (password !== repeatPassword) {
            setPasswordError(true)
            setPasswordRepeatError(true)
            error = true
        }

        if (!error) {
            fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/register`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            }).then(() => {
                fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/login`, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: `username=${email}&password=${password}`
                })
                .then(res => {
                    if (200 <= res.status && res.status < 300) {
                        fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/profile`, {
                            method: 'GET',
                            credentials: 'include'
                        })
                            .then(res => res.json())
                            .then(login)
                            .then(onClose)
                    }
                })
            })
        }
    }

    return (
        <div className={'Signup'}>
            <h3>Регистрация в системе</h3>
            <div>
                <label htmlFor={'username'}>Имя пользователя:</label>
                <input
                    className={usernameError ? 'Error' : null}
                    name={'username'}
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                />
                <label htmlFor={'email'}>Электронная почта:</label>
                <input
                    className={emailError ? 'Error' : null}
                    name={'email'}
                    value={email}
                    onChange={e => setEmail(e.target.value)}/>
                <label htmlFor={'password'}>Пароль:</label>
                <input
                    className={passwordError ? 'Error' : null}
                    name={'password'}
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    type={'password'}
                />
                <label htmlFor={'passwordRepeat'}>Повторите пароль:</label>
                <input
                    className={passwordRepeatError ? 'Error' : null}
                    name={'passwordRepeat'}
                    value={repeatPassword}
                    onChange={e => setRepeatPassword(e.target.value)}
                    type={'password'}
                />
            </div>
            <button onClick={handleSignup}>Зарегистрироваться</button>
        </div>
    );
};

export default Signup;