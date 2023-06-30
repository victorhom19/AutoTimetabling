import React from 'react';
import 'src/scss/components/ui/Modal.scss'

const Modal = ({open, onClose, children}) => {
    return (<>
        {open
            ?
            <div className={'Modal'} onClick={onClose}>
                <div className={'Content'} onClick={e => e.stopPropagation()}>
                    {children}
                </div>
            </div>
            : null
        }
    </>

    );
};

export default Modal;