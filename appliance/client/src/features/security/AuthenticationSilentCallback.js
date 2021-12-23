import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLocation, useNavigate } from "react-router-dom";
import getLogger from "../../utils/logging";

import security from "./index";

const log = getLogger("AuthenticationCallback");

export default function AuthenticationSilentCallback() {
  const location = useLocation();
  const dispatch = useDispatch();

  const isInitialized = useSelector(security.selectors.isInitialized);

  useEffect(() => {
    if (isInitialized && location.pathname === "/security/auth/silent")
      dispatch(security.actions.silentCallback());
  }, [isInitialized, location, dispatch]);

  return null;
}
