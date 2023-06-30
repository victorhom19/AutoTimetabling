import React from 'react';
import 'src/scss/pages/Home/Home.scss'
import previewImage from 'src/assets/images/preview.svg'
import {useSelector} from "react-redux";

const Home = () => {

    const {logged} = useSelector(state => state.auth)

    return (
        <div className={'Home'}>
            {logged ? <img src={previewImage}/> : <div>Войдите в систему или зарегистрируйтесь</div>}
        </div>
    );
};

export default Home;