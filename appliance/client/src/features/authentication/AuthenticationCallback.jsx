import {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {useRouteMatch} from "react-router-dom";

import {authCallback, authIsInitialized} from "./authenticationSlice";

export default function AuthenticationCallback() {
    const route = useRouteMatch();
    const dispatch = useDispatch();
    const isInitialized = useSelector(authIsInitialized);
    useEffect(() => {
        if (isInitialized && route.path === "/auth")
            dispatch(authCallback());
        if (isInitialized && route.path === "/auth-silent")
            dispatch(authCallback());
    }, [isInitialized]);

    return null;
}