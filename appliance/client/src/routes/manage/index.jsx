import React, { useCallback } from "react";
import { useSelector } from "react-redux";

import { Button } from "@mui/material";

import security from "../../features/security";
import { FileUpload } from "../../utils/FileUpload";

function Manage(props) {
  const token = useSelector(security.selectors.getToken);
  // const [image, setImage] = useState();

  const changed = useCallback(
    ({ target }) => {
      console.log(target.files);
      const upload = new FileUpload("image", target.files);
      upload.setHeader("Authorization", `Bearer ${token}`);
      upload.send("https://api.phex.local/images").then((responses) => {
        console.log(responses.map((xhr) => JSON.parse(xhr.responseText)));
      });
    },
    [token]
  );

  return (
    <div>
      <input
        accept="image/*"
        style={{ display: "none" }}
        id="raised-button-file"
        multiple
        type="file"
        onChange={changed}
      />
      <label htmlFor="raised-button-file">
        <Button variant="raised" component="span">
          Upload
        </Button>
      </label>
    </div>
  );
}

export default Manage;
