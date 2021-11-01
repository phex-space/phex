import { useEffect } from "react";
import { useOpenIdConnect } from "./OpenIdConnect";

export default function Callback() {
    const { handleCallback } = useOpenIdConnect();

    useEffect(() => {
        if (typeof handleCallback === "function")
            handleCallback();
    }, [handleCallback])

    return <div></div>
}
