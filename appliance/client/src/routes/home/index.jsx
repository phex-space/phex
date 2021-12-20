import React from "react";
import { useDispatch } from "react-redux";

import { Button, Container } from "@mui/material";

import security from "../../features/security";

function Home(props) {
    const colors = [
      "primary",
      "secondary",
      "error",
      "warning",
      "success",
      "info",
    ];
    const dispatch = useDispatch();
  return (
    <Container sx={{ mt: 3 }}>
      {colors.map((color) => (
        <Button
          key={color}
          color={color}
          variant="contained"
          sx={{ mr: 1 }}
          onClick={() => dispatch(security.actions.login())}
        >
          Klicken
        </Button>
      ))}
    </Container>
  );
}

export default Home;
