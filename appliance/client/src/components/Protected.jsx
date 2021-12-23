import { useDispatch, useSelector } from "react-redux";

import { Box, Container } from "@mui/material";

import security from "../features/security";
import { useTranslation } from "react-i18next";

function Protected({ children }) {
  const { t } = useTranslation("security");
  const dispatch = useDispatch();

  const isInitialized = useSelector(security.selectors.isInitialized);
  const isAuthenticated = useSelector(security.selectors.isAuthenticated);

  if (!isAuthenticated) {
    if (isInitialized) dispatch(security.actions.login());
    return (
      <Container>
        <Box>{t("content_protected")}</Box>
      </Container>
    );
  }
  return children;
}

export default Protected;
