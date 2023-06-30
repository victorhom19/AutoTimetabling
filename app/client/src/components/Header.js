import React, {useEffect} from 'react';
import 'src/scss/components/Header.scss'
import Modal from "./ui/Modal";
import Login from "../pages/Login/Login";
import {useSelector} from "react-redux";
import {useActions} from "../hooks/useActions";
import Signup from "../pages/Signup/Signup";
import {Avatar} from "@mui/material";
import useComponentVisible from "../hooks/useComponentVisible";
import Logout from "../pages/Logout/Logout";

const Header = () => {
    const [loginOpen, setLoginOpen] = React.useState(false)
    const handleLoginOpen = () => setLoginOpen(true)
    const handleLoginClose = () => setLoginOpen(false)

    const [signupOpen, setSignupOpen] = React.useState(false)
    const handleSignupOpen = () => setSignupOpen(true)
    const handleSignupClose = () => setSignupOpen(false)

    const {logged, username} = useSelector(state => state.auth)
    const project = useSelector(state => state.project)


    const {login} = useActions()

    useEffect(() => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/profile`, {
                    method: 'GET',
                    credentials: 'include'
                })
                .then(async res => {
                    if (200 <= res.status && res.status < 300) {
                        const data = await res.json()
                        login(data)
                    }
                })
    }, [])

    function stringToColor(string) {
        let hash = 0;
        let i;
        for (i = 0; i < string.length; i += 1) {
            hash = string.charCodeAt(i) + ((hash << 5) - hash);
        }
        let color = '#';
        for (i = 0; i < 3; i += 1) {
            const value = (hash >> (i * 8)) & 0xff;
            color += `00${value.toString(16)}`.slice(-2);
        }
        return color;
    }

    const {ref, isComponentVisible, setIsComponentVisible} = useComponentVisible(false)

    useEffect(() => {
        setIsComponentVisible(false)
    }, [logged])

    return (
        <div className={'Header'}>
            {logged
                ? <>
                    <> { project.id ? <div className={'ProjectName'}>{project.name}</div> : null}

                    </>
                    <div ref={ref} onClick={() => setIsComponentVisible(true)}>
                        {username}
                        <Avatar
                            sx={{ bgcolor: stringToColor(username) }}
                        >
                            {username.toUpperCase()[0]}
                        </Avatar>
                        {isComponentVisible && <Logout />}
                    </div>

                  </>
                : <>
                    <button onClick={handleLoginOpen}>Вход</button>


                    <Modal className={'Modal'} open={loginOpen} onClose={handleLoginClose}>
                        <Login onClose={handleLoginClose}/>
                    </Modal>

                    <button onClick={handleSignupOpen}>Регистрация</button>
                    <Modal className={'Modal'} open={signupOpen} onClose={handleSignupClose}>
                        <Signup onClose={handleSignupClose}/>
                    </Modal>
                </>
            }

        </div>
    );
};

export default Header;