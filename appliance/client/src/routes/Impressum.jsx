import React from "react";
import { Container } from "@mui/material";

function Impressum(props) {
  return (
    <Container>
      <h1>Impressum</h1>

      <h2>Angaben gem&auml;&szlig; &sect; 5 TMG</h2>
      <p>
        Christian Dein
        <br />
        Hauptstra&szlig;e 73
        <br />
        67705 Trippstadt
      </p>

      <h2>Kontakt</h2>
      <p>
        Telefon: +49 (0) 179 448 0 558
        <br />
        E-Mail: christian.dein@dein-hosting.de
      </p>

      <p>
        Quelle:{" "}
        <a href="https://www.e-recht24.de/impressum-generator.html">
          https://www.e-recht24.de/impressum-generator.html
        </a>
      </p>
    </Container>
  );
}

export default Impressum;
