import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useTranslation } from "react-i18next";

import { Button, IconButton, Menu, MenuItem } from "@mui/material";
import AccountCircle from "@mui/icons-material/AccountCircle";

import security from "../../features/security";

function UserMenu(props) {
  const { t } = useTranslation("navigation");
  const dispatch = useDispatch();

  const isAuthenticated = useSelector(security.selectors.isAuthenticated);
  const profile = useSelector(security.selectors.getProfile);

  const [anchorEl, setAnchorEl] = useState(null);

  const menuId = "primary-user-menu";
  const isMenuOpen = Boolean(anchorEl);

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return isAuthenticated ? (
    <>
      <IconButton
        size="large"
        edge="end"
        aria-label="account of current user"
        aria-controls={menuId}
        aria-haspopup="true"
        onClick={handleProfileMenuOpen}
        color="inherit"
      >
        <AccountCircle />
      </IconButton>
      {profile ? (
        <Menu
          anchorEl={anchorEl}
          anchorOrigin={{
            vertical: "top",
            horizontal: "right",
          }}
          id={menuId}
          keepMounted
          transformOrigin={{
            vertical: "top",
            horizontal: "right",
          }}
          open={isMenuOpen}
          onClose={handleMenuClose}
        >
          <MenuItem disabled>
            {profile.name || profile.preferred_username}
          </MenuItem>
          <MenuItem onClick={() => dispatch(security.actions.logout())}>
            {t("signout")}
          </MenuItem>
        </Menu>
      ) : null}
    </>
  ) : (
    <Button
      variant="outlined"
      sx={{ color: "white" }}
      onClick={() => dispatch(security.actions.login())}
    >
      Anmelden
    </Button>
  );
}

export default UserMenu;
