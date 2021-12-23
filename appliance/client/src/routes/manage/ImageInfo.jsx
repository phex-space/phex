import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  CardMedia,
  Grid,
  Typography,
} from "@mui/material";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import DateFormat from "../../components/DateFormat";
import globals from "../../globals";
import { fireEvent } from "../../utils/events";

const { apiUrl } = globals;

const source = `lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam
nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam
erat sed diam voluptua At vero eos et accusam et justo duo dolores
et ea rebum stet clita kasd gubergren no sea takimata sanctus est
Lorem ipsum dolor sit amet lorem ipsum dolor sit amet consetetur
sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore
et dolore magna aliquyam erat sed diam voluptua At vero eos et
accusam et justo duo dolores et ea rebum Stet clita kasd gubergren,
no sea takimata sanctus est Lorem ipsum dolor sit amet`.split(" ");

function getText(maxLength = source.length, minLength = 5) {
  const rnd = Math.random();
  const size = parseInt(rnd * (maxLength - minLength) + minLength, 10);
  return source.filter((_, index) => index < size).join(" ");
}

const styles = {
  card: {
    padding: 0,
    margin: 1,
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
  },
};

function ImageInfo({ info, onEdit, onDelete }) {
  const { t } = useTranslation();

  const edit = useCallback(() => {
    fireEvent(onEdit, info);
  }, [info, onEdit]);

  const purge = useCallback(() => {
    fireEvent(onDelete, info);
  }, [info, onDelete]);

  return (
    <Grid component={Card} item xs={12} sm={6} md={3} sx={styles.card}>
      <CardMedia
        component="img"
        height="194"
        image={`${apiUrl}/images/${info.id}?thumb=true`}
        alt={info.title || info.name || info.id}
      />
      <CardHeader
        title={info.title || getText(10, 2) || info.name || info.id}
        subheader={<DateFormat value={info.modified} />}
      />
      {/* {info.description && ( */}
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography variant="body2" color="text.secondary">
          {info.description || getText()}
        </Typography>
      </CardContent>
      {/* )} */}
      <CardActions>
        <Button size="small" onClick={edit}>
          {t("edit")}
        </Button>
        <Button size="small" onClick={purge}>
          {t("delete")}
        </Button>
      </CardActions>
    </Grid>
  );
}

export default ImageInfo;
