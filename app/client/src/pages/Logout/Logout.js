import React from 'react';
import 'src/scss/pages/Logout/Logout.scss'
import {useActions} from "../../hooks/useActions";

const Logout = () => {

    const {logout, selectProject} = useActions()

    const handleLogout = () => {
        fetch('http://localhost:8000/auth/logout', {
            method: 'POST',
            credentials: 'include'
        }).then(() => {
            logout()
            selectProject({id: null, name: null})
        })
    }

    return (
        <div className={'Logout'} onClick={handleLogout}>
            Выйти из аккаунта
        </div>
    );
};

export default Logout;