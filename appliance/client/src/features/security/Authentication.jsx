import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";

import security from "./index";

const baseUrl = window.location.protocol + "//" + window.location.host;
const callbackPath = "/security/auth";

function Authentication({ settings, children }) {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    dispatch(
      security.actions.init({
        settings: {
          loadUserInfo: true,
          automaticSilentRenew: true,
          ...settings,
          callback_path: callbackPath,
          redirect_uri: baseUrl + callbackPath,
          post_logout_redirect_uri: baseUrl + callbackPath,
          silent_redirect_uri: baseUrl + callbackPath + "/silent",
        },
        navigate,
      })
    );
  }, [settings, dispatch, navigate]);

  return null;
}

export default Authentication;
