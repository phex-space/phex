import React, { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import { Button, Container, Grid } from "@mui/material";

import imageApi from "../../features/imageApi";
import ImageInfo from "./ImageInfo";
import EditImageDialog from "./EditImageDialog";

function Manage(props) {
  const dispatch = useDispatch();

  const images = useSelector(imageApi.selectors.images);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editImage, setEditImage] = useState();

  const changed = useCallback(
    ({ target }) => {
      dispatch(imageApi.actions.upload(target));
    },
    [dispatch]
  );

  const edit = useCallback((image) => {
    setEditImage(image);
    setEditDialogOpen(true);
  }, []);

  const purge = useCallback(
    ({ id }) => {
      dispatch(imageApi.actions.purge(id));
    },
    [dispatch]
  );

  const editCancel = useCallback(() => {
    setEditImage();
    setEditDialogOpen(false);
  }, []);

  const editSubmit = useCallback(
    (data) => {
      dispatch(imageApi.actions.update(data));
      editCancel();
    },
    [editCancel, dispatch]
  );

  useEffect(() => {
    dispatch(imageApi.actions.refreshList());
  }, [dispatch]);

  return (
    <Container>
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
      <Grid container justifyContent="center">
        {images.map((image) => (
          <ImageInfo
            key={image.id}
            info={image}
            onEdit={edit}
            onDelete={purge}
          />
        ))}
      </Grid>
      {editImage && (
        <EditImageDialog
          image={editImage}
          open={editDialogOpen}
          onSubmit={editSubmit}
          onCancel={editCancel}
        />
      )}
    </Container>
  );
}

export default Manage;
