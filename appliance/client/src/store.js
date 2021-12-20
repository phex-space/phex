import { configureStore } from '@reduxjs/toolkit';

import security from "./features/security"

export const store = configureStore({
  reducer: {
    [security.name]: security.reducer
  },
});
