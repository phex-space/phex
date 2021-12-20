import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import { UserManager } from "oidc-client";

export { default as Authentication } from "./Authentication";
export { default as AuthenticationCallback } from "./AuthenticationCallback";

let _userManager, _navigate, _callbackPath;

const name = "security";

const initialState = {
  initialized: false,
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
    const { profile } = auth;
    return profile;
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
        state.profile = payload;
        state.initialized = true;
      })
      .addCase(init.rejected, (state, { payload }) => {
        state.profile = null;
        state.initialized = true;
      });

    builder
      .addCase(callback.fulfilled, (state, { payload }) => {
        const { data, profile } = payload || {};
        state.profile = profile;
        if (data && data.pathname !== _callbackPath) _navigate(data.pathname);
        else _navigate("/");
      })
      .addCase(callback.rejected, (state, { payload }) => {
        state.profile = null;
        _navigate("/");
      });

    builder
      .addCase(silentCallback.fulfilled, (state, { payload }) => {
        const { data, profile } = payload || {};
        state.profile = profile;
        if (data && data.pathname !== _callbackPath) _navigate(data.pathname);
        else _navigate("/");
      })
      .addCase(silentCallback.rejected, (state, { payload }) => {
        state.profile = null;
        _navigate("/");
      });
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
};

const security = {
  name,
  actions,
  selectors,
  reducer: securitySlice.reducer,
};

export default security;
