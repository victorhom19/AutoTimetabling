import {useDispatch} from "react-redux";
import {useMemo} from "react";
import bindActionCreators from "react-redux/es/utils/bindActionCreators";
import {actions as authActions} from 'src/store/auth/authSlice.js'
import {actions as navActions} from 'src/store/nav/navSlice.js'
import {actions as projectActions} from 'src/store/project/projectSlice.js'

const rootActions = {
    ...authActions,
    ...navActions,
    ...projectActions,
}

export const useActions = () => {
    const dispatch = useDispatch()

    return useMemo(() => bindActionCreators(rootActions, dispatch), [dispatch])
}