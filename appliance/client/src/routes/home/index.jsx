import React from "react";

import { Container, Typography } from "@mui/material";

function Home(props) {
  return (
    <Container>
      <Typography variant="h3">Willkommen bei phex.space</Typography>
      <Typography variant="subtitle2">
        Hier können Sie demnächst Ihre Fotos in einer Ausstellung präsentieren.
      </Typography>
      <Typography variant="body1" sx={{ mt: 1 }}>
        Präsentieren Sie Ihre Impressionen in einer durch Sie erstellte
        Ausstellung. Sie bestimmen den Zeitpunkt und wie lange Ihre Austellung
        gezeigt wird. Laden Sie Ihre Familie, Freunde oder Bekannten ein Ihre
        Arbeit zu wertschätzen.
      </Typography>
      <Typography variant="body1" sx={{ mt: 1 }}>
        Die Plattform befindet sich noch in der Entwicklung.
      </Typography>

      <Typography variant="body1" sx={{ mt: 2 }}>
        Liebe Grüße,
        <br />
        Dein phex.space-Team
      </Typography>
    </Container>
  );
}

export default Home;
