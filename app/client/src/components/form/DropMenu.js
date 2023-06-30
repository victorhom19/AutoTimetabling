import React from 'react';

const DropMenu = (children) => {

    return (
        <div className={'DropMenu'}>
            <div className={'Header'}></div>
            <ul className={'OptionList'}>
                {children.map(child => <li className={'Option'}>

                </li> )}
            </ul>
        </div>
    );
};

export default DropMenu;