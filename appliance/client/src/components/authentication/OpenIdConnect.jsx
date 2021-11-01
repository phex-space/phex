import React, {useState} from "react";

import {OidcClient, UserManager} from "oidc-client";
import {Route, Switch, useHistory} from "react-router-dom";

export const OpenIdConnectContext = React.createContext();
export const useOpenIdConnect = () => React.useContext(OpenIdConnectContext);

export default function OpenIdConnect({children, settings}) {
    const [api, setApi] = useState({});
    const [response, setResponse] = useState({});
    const history = useHistory();

    React.useEffect(() => {
        const client = new OidcClient(settings);
        const login = () => {
            client.createSigninRequest({state: {location: window.location.pathname}}).then(signinRequest => {
                window.location.assign(signinRequest.url);
            });
        };
        const logout = () => {
            client.createSignoutRequest({
                id_token_hint: response && response.id_token,
                state: {location: window.location.pathname}
            }).then(signoutRequest => {
                console.log(signoutRequest);
                window.location.assign(signoutRequest.url);
            });
        };
        const handleCallback = () => {
            if (window.location.href.indexOf("#") >= 0) {
                client.processSigninResponse().then(signinResponse => {
                    console.log(signinResponse);
                    setResponse(signinResponse);
                    localStorage.setItem("access_token", signinResponse.access_token);
                    if (signinResponse.state && signinResponse.state.location)
                        history.replace(signinResponse.state.location);
                    else
                        history.replace("/");
                });
            } else if (window.location.href.indexOf("?") >= 0) {
                client.processSignoutResponse().then(signoutResponse => {
                    setResponse({});
                    console.log(signoutResponse);
                    if (signoutResponse.state && signoutResponse.state.location)
                        history.replace(signoutResponse.state.location);
                    else
                        history.replace("/");
                });
            }
        };
        setApi({
            login, logout, handleCallback,
            accessToken: response.access_token, profile: response.profile, expiresAt: response.expires_at
        });
    }, [settings, history, response])

    return (
        <OpenIdConnectContext.Provider value={api}>
            {children}
            <Switch>
                <Route exact path={settings.callback_path} render={() => {
                    new UserManager().signinCallback();
                }}>
                </Route>
                <Route path="/"></Route>
            </Switch>
        </OpenIdConnectContext.Provider>
    );
}
