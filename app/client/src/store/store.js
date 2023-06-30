import {combineReducers, configureStore} from "@reduxjs/toolkit";
import {reducer as authReducer}  from 'src/store/auth/authSlice.js'
import {reducer as navReducer}  from 'src/store/nav/navSlice.js'
import {reducer as projectReducer}  from 'src/store/project/projectSlice.js'


const reducers = combineReducers({
    auth: authReducer,
    nav: navReducer,
    project: projectReducer
})

export const store = configureStore({
    reducer: reducers,
    devTools: true
})