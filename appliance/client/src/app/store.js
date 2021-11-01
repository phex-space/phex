import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';
import authenticationSlice from "../features/authentication/authenticationSlice";

export const store = configureStore({
  reducer: {
    auth: authenticationSlice.reducer,
    counter: counterReducer,
  },
});
