import React, {useEffect} from "react";
import {Route, Switch, useHistory} from "react-router-dom";
import {useDispatch} from "react-redux";

import {authInit} from "./authenticationSlice";
import AuthenticationCallback from "./AuthenticationCallback";

const baseUrl = window.location.protocol + "//" + window.location.hostname;
const callbackPath = "/auth";

export default function Authentication({settings, children}) {
    const dispatch = useDispatch();
    const history = useHistory();
    useEffect(() => {
        if (history)
            dispatch(authInit({
                settings: {
                    loadUserInfo: false,
                    automaticSilentRenew: true,
                    ...settings,
                    callback_path: callbackPath,
                    redirect_uri: baseUrl + callbackPath,
                    post_logout_redirect_uri: baseUrl + callbackPath,
                    silent_redirect_uri: baseUrl + callbackPath + '-silent',
                }, history
            }));
    }, [dispatch, settings, history])
    return (
        <>
            {children}
            <Switch>
                <Route exact path="/auth" component={AuthenticationCallback}/>
                <Route exact path="/auth-silent" component={AuthenticationCallback}/>
            </Switch>
        </>
    );
}
