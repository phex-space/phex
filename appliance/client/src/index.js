import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router} from "react-router-dom";
import {Provider} from 'react-redux';

import {store} from './app/store';
import App from './App';
import * as serviceWorker from './serviceWorker';

import './index.css';
import Authentication from "./features/authentication/Authentication";

const oidcConfig = {
    authority: 'https://identity.phex.local/auth/realms/phex',
    client_id: 'client',
    response_type: 'id_token token',
    scope: 'openid offline_access',
};

ReactDOM.render(
    <React.StrictMode>
        <Router>
            <Provider store={store}>
                <Authentication settings={oidcConfig}>
                    <App/>
                </Authentication>
            </Provider>
        </Router>
    </React.StrictMode>,
    document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
