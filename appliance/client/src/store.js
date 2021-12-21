import { configureStore } from "@reduxjs/toolkit";

import imageApi from "./features/imageApi";
import security from "./features/security";

export const store = configureStore({
  reducer: {
    [imageApi.name]: imageApi.reducer,
    [security.name]: security.reducer,
  },
});
