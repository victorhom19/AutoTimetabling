import React from 'react';
import ReactDOM from 'react-dom/client';
import './scss/global.scss';
import App from './App';
import {store} from "./store/store";
import {Provider} from "react-redux";
import { ApolloClient, InMemoryCache, ApolloProvider, gql } from '@apollo/client';

export const client = new ApolloClient({
    uri: `${process.env.REACT_APP_WEB_APP_URI}/graphql/`,
    cache: new InMemoryCache(),
    credentials: 'include'
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <ApolloProvider client={client}>
        <Provider store={store}>
            <App />
        </Provider>
    </ApolloProvider>

);
