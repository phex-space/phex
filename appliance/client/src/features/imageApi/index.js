import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import security from "../security";

const name = "images";

const initialState = {};

const refreshList = createAsyncThunk(
  `${name}/refreshList`,
  async (_, thunk) => {
    console.log("Start refresh");
    const token = security.selectors.getToken(thunk.getState());
    console.log("Fetch");
    try {
      // const response = await fetch("https://api.phex.local/images", {
      //   // headers: { Authorization: `Bearer ${token}` },
      //   credentials: "include",
      // });
      // console.log(await response.json());
    } catch (e) {
      console.error(e);
    }
  }
);

const imagesSlice = createSlice({
  name,
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(refreshList.fulfilled, (state, { payload }) => {})
      .addCase(refreshList.rejected, (state, { payload }) => {});
  },
});

const actions = {
  refreshList,
};

const imageApi = {
  name,
  actions,
  reducer: imagesSlice.reducer,
};

export default imageApi;
