import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useLocation } from "react-router-dom";

import security from "./index";

const baseUrl = window.location.protocol + "//" + window.location.host;
const callbackPath = "/security/auth";

function Authentication({ settings, children }) {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(
      security.actions.init({
        settings: {
          loadUserInfo: true,
          ...settings,
          automaticSilentRenew: false,
          callback_path: callbackPath,
          redirect_uri: baseUrl + callbackPath,
          post_logout_redirect_uri: baseUrl + callbackPath,
          silent_redirect_uri: baseUrl + callbackPath + "/silent",
        },
      })
    );
  }, [settings, dispatch]);

  return null;
}

export default Authentication;
