import React from 'react';
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";

import Callback from "./components/authentication/Callback";
import {Counter} from './features/counter/Counter';
import './App.css';
import {authLogin, authLogout} from "./features/authentication/authenticationSlice";
import {useDispatch} from "react-redux";

function App() {
    const dispatch = useDispatch();

    return (
        <>
            <Counter/>
            <button onClick={() => dispatch(authLogin())}>Login</button>
            <button onClick={() => dispatch(authLogout())}>Logout</button>
        </>
    );
}

export default App;
