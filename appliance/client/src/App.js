import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Outlet } from "react-router-dom";
import Footer from "./components/Footer";

import { Navigation } from "./components/Navigation";
import imageApi from "./features/imageApi";
import security from "./features/security";

function App({ children }) {
  const dispatch = useDispatch();
  const isInitialized = useSelector(security.selectors.isInitialized);

  useEffect(() => {
    if (isInitialized) {
      console.log("Refresh");
      dispatch(imageApi.actions.refreshList());
    }
  }, [isInitialized, dispatch]);

  return (
    <div>
      <Navigation />
      <Outlet />
      <Footer />
    </div>
  );
}

export default App;
