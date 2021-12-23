import { Box } from "@mui/material";
import React from "react";
import { Outlet } from "react-router-dom";
import Footer from "./components/Footer";

import { Navigation } from "./components/Navigation";

function App() {
  return (
    <div>
      <Navigation />
      <Box sx={{ mt: 3 }}>
        <Outlet />
      </Box>
      <Footer />
    </div>
  );
}

export default App;
