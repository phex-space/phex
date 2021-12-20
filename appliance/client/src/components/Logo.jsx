import React from "react";
import { Link } from "react-router-dom";

import { Box, Typography } from "@mui/material";

function Logo({ sx }) {
  return (
    <Link to="/">
      <Typography
        variant="h6"
        noWrap
        component="div"
        sx={{
          display: "flex",
          fontFamily: "bungee",
          alignItems: "center",
          color: "white",
          ...sx,
        }}
      >
        <Box
          sx={{
            mr: 1,
            bgcolor: "white",
            width: 39,
            height: 39,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: 1,
          }}
        >
          <img src="/assets/logo/symbol.svg" height={32} alt="phex.space" />
        </Box>
        phex.space
      </Typography>
    </Link>
  );
}

export default Logo;
