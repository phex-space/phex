import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {Log, UserManager} from "oidc-client";

Log.logger = console;
Log.level = Log.DEBUG;

let _userManager;
let _history;
let _callbackPath;

function getUserManager() {
    if (!_userManager) throw new Error("Authentication feature is not initialized.");
    return _userManager;
}

export const initialState = {
    initialized: false,
    user: null,
}

export const authIsInitialized = state => state.auth.initialized;

export const authInit = createAsyncThunk("auth/init", async ({settings, history}) => {
    _userManager = new UserManager(settings);
    _history = history;
    _callbackPath = settings.callback_path;
    const auth = await getUserManager().getUser();
    if (!auth)
        return null;
    console.log("Expires", auth.expires_in, auth.expires_in / 60);
    if (auth.expired)
        return null;
    const {profile} = auth;
    return profile;
});

export const authLogin = createAsyncThunk("auth/login", () => {
    const {pathname} = window.location;
    const oidc = getUserManager();
    return oidc.signinRedirect({state: {pathname}}).then(user => {
        return {user};
    })
});

export const authLogout = createAsyncThunk("auth/logout", () => {
    const {pathname} = window.location;
    const oidc = getUserManager();
    return oidc.signoutRedirect({state: {pathname}}).then().catch(console.error);
});

export const authCallback = createAsyncThunk("auth/callback", () => {
    return getUserManager().signinRedirectCallback().then((payload) => {
        const {profile, state} = payload || {};
        return {profile, data: state};
    });
});

export const authCallbackSilent = createAsyncThunk("auth/callback-silent", () => {
    return getUserManager().signinSilentCallback().then((payload) => {
        const {profile, state} = payload || {};
        return {profile, data: state};
    });
});

const authenticationSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder.addCase(authInit.fulfilled, (state, {payload}) => {
            state.user = payload;
            state.initialized = true;
        }).addCase(authInit.rejected, (state, {payload}) => {
            state.user = null;
            state.initialized = true;
        }).addCase(authCallback.fulfilled, (state, {payload}) => {
            const {data, profile} = payload || {};
            state.user = profile;
            if (data && data.pathname !== _callbackPath)
                _history.push(data.pathname);
            else
                _history.push("/");
        }).addCase(authCallback.rejected, (state, {payload}) => {
            _history.push("/");
        }).addCase(authCallbackSilent.fulfilled, (state, {payload}) => {
            const {data, profile} = payload || {};
            state.user = profile;
            if (data && data.pathname !== _callbackPath)
                _history.push(data.pathname);
            else
                _history.push("/");
        }).addCase(authCallbackSilent.rejected, (state, {payload}) => {
            _history.push("/");
        });
    }
});
export default authenticationSlice;
