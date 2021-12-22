import React, { useEffect, useRef } from "react";
import { Link as RouterLink, useLocation } from "react-router-dom";

import { Box, Container, Link, styled, Toolbar } from "@mui/material";

const Footer = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.secondary.main,
  marginTop: "32px",
  paddingTop: "16px",
  paddingBottom: "48px",
}));

function FooterComponent(props) {
  const footerRef = useRef();
  const location = useLocation();

  useEffect(() => {
    if (footerRef.current) {
      const windowHeight = window.innerHeight;
      const { top } = footerRef.current.getBoundingClientRect();
      const diff = windowHeight - top;
      if (diff > 100) footerRef.current.style.minHeight = `${diff}px`;
      else footerRef.current.style.minHeight = "auto";
    }
  }, [footerRef, location]);

  return (
    <Footer ref={footerRef}>
      <Container>
        <Toolbar style={{ padding: 0 }}>
          <Box sx={{ display: "flex", flexDirection: "row" }}>
            <Link component={RouterLink} to="/impressum" sx={{ mr: 2 }}>
              Impressum
            </Link>
            <Link component={RouterLink} to="/privacy">
              Datenschutzerklärung
            </Link>
          </Box>
          <Box sx={{ flexGrow: 1 }} />
          <Box sx={{ display: "flex", flexDirection: "row" }}>
            &copy; {new Date().getFullYear()} Christian Dein - Alle Rechte
            vorbehalten.
          </Box>
        </Toolbar>
      </Container>
    </Footer>
  );
}

export default FooterComponent;
