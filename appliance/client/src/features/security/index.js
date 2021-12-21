import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import { UserManager } from "oidc-client";

import globals from "../../globals";

export { default as Authentication } from "./Authentication";
export { default as AuthenticationCallback } from "./AuthenticationCallback";

let _userManager, _navigate, _callbackPath;

const name = "security";
const { apiUrl } = globals;

const initialState = {
  initialized: false,
  token: null,
  profile: null,
  status: "idle",
};

function getUserManager() {
  if (!_userManager) throw new Error("Security feature is not initialized.");
  return _userManager;
}

const init = createAsyncThunk(
  `${name}/init`,
  async ({ settings, navigate }) => {
    if (!_userManager) {
      _userManager = new UserManager(settings);
      _navigate = navigate;
      _callbackPath = settings.callback_path;
    }
    const auth = await getUserManager().getUser();
    if (!auth) return null;
    if (auth.expired) return null;
    const { profile, access_token } = auth;
    await fetch(`${apiUrl}/users/me`, {
      headers: { Authorization: `Bearer ${access_token}` },
      credentials: "include",
    });
    return { profile, token: access_token };
  }
);

const login = createAsyncThunk(`${name}/login`, async () => {
  const { pathname } = window.location;
  const oidc = getUserManager();
  return oidc.signinRedirect({ state: { pathname } }).then((user) => {
    return { user };
  });
});

const logout = createAsyncThunk(`${name}/logout`, () => {
  const { pathname } = window.location;
  const oidc = getUserManager();
  return oidc
    .signoutRedirect({ state: { pathname } })
    .then()
    .catch(console.error);
});

const callback = createAsyncThunk(`${name}/callback`, () => {
  return getUserManager()
    .signinRedirectCallback()
    .then((payload) => {
      const { profile, state } = payload || {};
      return { profile, data: state };
    });
});

const silentCallback = createAsyncThunk(`${name}/silentCallback`, () => {
  return getUserManager()
    .signinSilentCallback()
    .then((payload) => {
      const { profile, state } = payload || {};
      return { profile, data: state };
    });
});

const securitySlice = createSlice({
  name,
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(init.fulfilled, (state, { payload }) => {
        const { profile, token } = payload || {};
        state.profile = profile;
        state.token = token;
        state.initialized = true;
      })
      .addCase(init.rejected, (state, { payload }) => {
        state.profile = null;
        state.token = null;
        state.initialized = true;
      });

    const callbackHandler = (state, { payload }) => {
      const { data, profile, access_token } = payload || {};
      state.profile = profile;
      state.token = access_token;
      if (data && data.pathname !== _callbackPath) _navigate(data.pathname);
      else _navigate("/");
    };
    const callbackRejectedHandler = (state, { payload }) => {
      state.profile = null;
      state.token = null;
      _navigate("/");
    };
    builder
      .addCase(callback.fulfilled, callbackHandler)
      .addCase(callback.rejected, callbackRejectedHandler);

    builder
      .addCase(silentCallback.fulfilled, callbackHandler)
      .addCase(silentCallback.rejected, callbackRejectedHandler);
  },
});

const actions = {
  init,
  callback,
  silentCallback,
  login,
  logout,
};

const selectors = {
  isInitialized: (state) => state[name].initialized,
  isAuthenticated: (state) => !!state[name].profile,
  getProfile: (state) => state[name].profile,
  getToken: (state) => state[name].token,
};

const security = {
  name,
  actions,
  selectors,
  reducer: securitySlice.reducer,
};

export default security;
