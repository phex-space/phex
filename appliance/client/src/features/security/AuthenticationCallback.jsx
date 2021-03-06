import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useLocation, useNavigate } from "react-router-dom";
import getLogger from "../../utils/logging";

import security from "./index";

const log = getLogger("AuthenticationCallback");

export default function AuthenticationCallback() {
  const location = useLocation();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const isInitialized = useSelector(security.selectors.isInitialized);
  const data = useSelector(security.selectors.getData);

  useEffect(() => {
    if (isInitialized && location.pathname === "/security/auth")
      dispatch(security.actions.callback());
    if (isInitialized && location.pathname === "/security/auth/silent")
      dispatch(security.actions.silentCallback());
  }, [isInitialized, location, dispatch]);

  useEffect(() => {
    log.trace("IsInitialized:", isInitialized, "State:", data);
    if (!isInitialized || !data) return;
    if (!["/security/auth", "/security/auth/silent"].includes(data.pathname))
      navigate(data.pathname);
    else navigate("/");
  }, [isInitialized, data, navigate]);

  return null;
}
