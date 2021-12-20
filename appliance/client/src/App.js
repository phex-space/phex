import React from "react";
import { Outlet } from "react-router-dom";
import Footer from "./components/Footer";

import { Navigation } from "./components/Navigation";

function App({ children }) {
  return (
    <div>
      <Navigation />
      <Outlet />
      <Footer />
    </div>
  );
}

export default App;
