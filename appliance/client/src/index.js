import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Provider } from "react-redux";

import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";

import "./init";
import "./i18n";

import { store } from "./store";
import * as serviceWorker from "./serviceWorker";

import "./index.css";
import { Authentication, AuthenticationCallback } from "./features/security";

import App from "./App";
import Home from "./routes/home";
import Impressum from "./routes/Impressum";
import Privacy from "./routes/Privacy";
import Manage from "./routes/manage";

let theme = createTheme({
  palette: {
    primary: {
      light: "#823799",
      main: "#52006A",
      dark: "#27003e",
    },
    secondary: {
      light: "#f3e2f8",
      main: "#c0b0c5",
      dark: "#908194",
    },
    // secondary: {
    //   light: "#825eff",
    //   main: "#4631d8",
    //   dark: "#0000a5",
    // },
    error: {
      light: "#ff5565",
      main: "#CD113B",
      dark: "#940016",
    },
    warning: {
      light: "#ffa741",
      main: "#FF7600",
      dark: "#c54600",
      contrastText: "#fff",
    },
    success: {
      light: "#79af81",
      main: "#4b7f54",
      dark: "#1e522b",
    },
    info: {
      light: "#51b0cf",
      main: "#00809e",
      dark: "#51b0cf",
    },
  },
});

const oidcConfig = {
  authority: "https://identity.phex.space/auth/realms/phex",
  client_id: "ui",
  response_type: "id_token token",
  scope: "openid offline_access",
};

ReactDOM.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <Router>
        <Provider store={store}>
          <Authentication settings={oidcConfig} />
          <CssBaseline />

          <Routes>
            <Route element={<App />}>
              <Route index path="/" element={<Home />} />
              <Route path="/manage" element={<Manage />} />
              <Route path="/impressum" element={<Impressum />} />
              <Route path="/privacy" element={<Privacy />} />

              <Route
                index
                path="/security/auth"
                element={<AuthenticationCallback />}
              />
              <Route
                index
                path="/security/auth/silent"
                element={<AuthenticationCallback />}
              />
            </Route>
          </Routes>
        </Provider>
      </Router>
    </ThemeProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
