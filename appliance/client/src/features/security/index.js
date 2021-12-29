import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import { UserManager } from "oidc-client";

import globals from "../../globals";
import getLogger from "../../utils/logging";
import { waitUntil } from "../../utils/promises";

export { default as Authentication } from "./Authentication";
export { default as AuthenticationCallback } from "./AuthenticationCallback";

let _userManager;

const name = "security";
const { apiUrl } = globals;

const log = getLogger(name);

const initialState = {
  initialized: false,
  token: null,
  profile: null,
  data: null,
  status: "idle",
};

function getUserManager() {
  if (!_userManager) throw new Error("Security feature is not initialized.");
  return _userManager;
}

function scheduleRefresh({ dispatch }, timeout) {
  log.debug("Schedule refresh in", (timeout / 1000 / 60).toFixed(3), "minutes");
  setTimeout(() => {
    log.debug("Should refresh token");
    dispatch(silent());
  }, timeout);
}

async function handleUser(thunk) {
  const auth = await getUserManager().getUser();
  if (!auth) return null;
  if (auth.expired) return null;
  log.debug("Got authentication object", auth);
  const { profile, access_token, expires_at } = auth;
  try {
    await fetch(`${apiUrl}/users/me`, {
      headers: { Authorization: `Bearer ${access_token}` },
      credentials: "include",
    });
  } catch (err) {
    log.error(err);
  }
  scheduleRefresh(thunk, expires_at * 1000 - Date.now() - 60 * 1000);
  return {
    profile,
    token: access_token,
  };
}

const init = createAsyncThunk(`${name}/init`, async ({ settings }, thunk) => {
  log.debug("Initializing", settings);
  if (!_userManager) {
    _userManager = new UserManager(settings);
  }
  const { pathname } = window.location;
  const { callback_path: callbackPath } = settings;
  if (pathname === callbackPath + "/silent") return;
  return await handleUser(thunk);
});

const login = createAsyncThunk(`${name}/login`, async (_, thunk) => {
  log.debug("Login");
  const { pathname } = window.location;
  try {
    await waitUntil(() => selectors.isInitialized(thunk.getState()));
    const state = { pathname };
    log.debug("Start login. State:", state);
    const user = await getUserManager().signinRedirect({ state });
    return { user };
  } catch (e) {
    log.error("Failed login", e);
  }
});

const silent = createAsyncThunk(`${name}/silent`, async (_, thunk) => {
  const oidc = getUserManager();
  try {
    const result = await oidc.signinSilent({ state: { pathname: "/" } });
    log.debug("We got silent data:", result);
    return await handleUser(thunk);
  } catch (e) {
    log.error("Failed silent signin", e);
  }
});

const logout = createAsyncThunk(`${name}/logout`, async () => {
  const { pathname } = window.location;
  const oidc = getUserManager();
  return await oidc.signoutRedirect({ state: { pathname } });
});

const callback = createAsyncThunk(`${name}/callback`, async () => {
  const result = await getUserManager().signinRedirectCallback();
  const { profile, state } = result || {};
  log.debug("Callback from login. State:", state);
  return { profile, data: state };
});

const silentCallback = createAsyncThunk(`${name}/silentCallback`, async () => {
  const result = await getUserManager().signinSilentCallback();
  const { profile, state } = result || {};
  log.debug("Callback from silent signin. Result:", result);
  return { profile, data: state };
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
        state.data = null;
        log.debug("Initialized", state);
      })
      .addCase(init.rejected, (state, { payload }) => {
        state.profile = null;
        state.token = null;
        state.initialized = true;
        state.data = null;
        log.debug("Initialized", state);
      });

    const callbackHandler = (state, { payload }) => {
      const { data, profile, access_token } = payload || {};
      state.profile = profile;
      state.token = access_token;
      state.data = data;
    };
    const callbackRejectedHandler = (state, { payload }) => {
      state.profile = null;
      state.token = null;
      state.data = null;
    };
    builder
      .addCase(callback.fulfilled, callbackHandler)
      .addCase(callback.rejected, callbackRejectedHandler);

    builder
      .addCase(silent.fulfilled, callbackHandler)
      .addCase(silent.rejected, () => {});
    builder
      .addCase(silentCallback.fulfilled, callbackHandler)
      .addCase(silentCallback.rejected, callbackRejectedHandler);
  },
});

const actions = {
  init,
  callback,
  login,
  logout,
  silent,
  silentCallback,
};

const selectors = {
  isInitialized: (state) => state[name].initialized,
  isAuthenticated: (state) => !!state[name].profile,
  getProfile: (state) => state[name].profile,
  getToken: (state) => state[name].token,
  getData: (state) => state[name].data,
};

const security = {
  name,
  actions,
  selectors,
  reducer: securitySlice.reducer,
};

export default security;
