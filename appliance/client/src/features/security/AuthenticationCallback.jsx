import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLocation } from "react-router-dom";

import security from "./index";

export default function AuthenticationCallback() {
  const location = useLocation();
  const dispatch = useDispatch();
  const isInitialized = useSelector(security.selectors.isInitialized);
  useEffect(() => {
    if (isInitialized && location.pathname === "/security/auth")
      dispatch(security.actions.callback());
    if (isInitialized && location.pathname === "/security/auth/silent")
      dispatch(security.actions.silentCallback());
  }, [isInitialized, location, dispatch]);

  return null;
}
