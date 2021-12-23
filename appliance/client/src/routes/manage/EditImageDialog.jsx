import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
} from "@mui/material";
import globals from "../../globals";
import { fireEvent } from "../../utils/events";

const { apiUrl } = globals;

function EditImageDialog({ image, open, onSubmit, onCancel }) {
  const { t } = useTranslation("manage");

  const [data, setData] = useState({
    id: image.id,
    title: image.title,
    description: image.description,
  });

  const change = useCallback(
    ({ target }) => {
      setData({ ...data, [target.name]: target.value });
    },
    [data]
  );

  const submit = useCallback(
    () => {
      fireEvent(onSubmit, data);
    },
    [data, onSubmit]
  );

  return (
    <Dialog open={open} onClose={onCancel} fullWidth maxWidth="md">
      <DialogTitle>{t("editDialog.title")}</DialogTitle>
      <DialogContent>
        <DialogContentText>
          <img
            src={`${apiUrl}/images/${image.id}?thumb=True`}
            align="right"
            style={{ marginLeft: 16, marginBottom: 16, maxWidth: "100%" }}
            alt={image.name}
          />
          {t("editDialog.content")}
        </DialogContentText>
        <TextField
          autoFocus
          margin="dense"
          id="titleInput"
          name="title"
          label={t("editDialog.titleInputLabel")}
          type="text"
          fullWidth
          variant="standard"
          onChange={change}
        />
        <TextField
          margin="dense"
          id="descriptionInput"
          name="description"
          label={t("editDialog.descriptionInputLabel")}
          type="text"
          fullWidth
          multiline
          rows={10}
          variant="standard"
          onChange={change}
        />
      </DialogContent>
      <DialogActions>
        <Button color="secondary" onClick={onCancel}>
          {t("cancel", { ns: "common" })}
        </Button>
        <Button
          onClick={submit}
          disabled={
            data.title === image.title && data.description === image.description
          }
        >
          {t("ok", { ns: "common" })}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default EditImageDialog;
