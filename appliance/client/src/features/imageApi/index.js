import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import globals from "../../globals";
import { FileUpload } from "../../utils/FileUpload";
import { responseHandler } from "../../utils/http";
import getLogger, { Logger } from "../../utils/logging";
import { retryWhenFail } from "../../utils/promises";
import security from "../security";

const { apiUrl } = globals;

const name = "images";
const log = getLogger(name);

const initialState = {
  images: [],
};

const refreshList = createAsyncThunk(
  `${name}/refreshList`,
  async (_, thunk) => {
    const isAuthenticated = security.selectors.isAuthenticated(
      thunk.getState()
    );
    if (!isAuthenticated) return;
    log.debug("Start refresh");
    const response = await retryWhenFail(() =>
      responseHandler(
        fetch(`${apiUrl}/images`, {
          headers: {
            Authorization: `Bearer ${security.selectors.getToken(
              thunk.getState()
            )}`,
          },
        })
      )
    );
    const result = await response.json();
    log.debug("Refresh image list result:", result);
    return result;
  }
);

const upload = createAsyncThunk(`${name}/upload`, async (options, thunk) => {
  const token = security.selectors.getToken(thunk.getState());
  const fileUpload = new FileUpload("image", options.files);
  fileUpload.setHeader("Authorization", `Bearer ${token}`);
  const newImagesData = (await fileUpload.send(`${apiUrl}/images`))
    .map((xhr) => {
      if (xhr.status === 200) {
        return JSON.parse(xhr.responseText);
      }
      return null;
    })
    .filter((image) => !!image);
  return newImagesData;
});

const purge = createAsyncThunk(`${name}/purge`, async (id, thunk) => {
  const token = security.selectors.getToken(thunk.getState());
  const response = await fetch(`${apiUrl}/images/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.status === 200 ? id : null;
});

const update = createAsyncThunk(`${name}/update`, async (data, thunk) => {
  log.debug("Update image:", data);
  const token = security.selectors.getToken(thunk.getState());
  const response = await fetch(`${apiUrl}/images/${data.id}`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  const result = await response.json();
  log.debug("Image update", result);
  return response.status === 200 ? result : null;
});

const imagesSlice = createSlice({
  name,
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(refreshList.fulfilled, (state, { payload }) => {
        state.images = payload || [];
      })
      .addCase(refreshList.rejected, (state, { payload }) => {
        state.images = [];
      });

    builder
      .addCase(upload.fulfilled, (state, { payload }) => {
        state.images = [...state.images, ...payload];
      })
      .addCase(upload.rejected, (state, { payload }) => {});

    builder
      .addCase(update.fulfilled, (state, { payload }) => {
        state.images = [...state.images];
        const index = state.images.findIndex(
          (entry) => entry.id === payload.id
        );
        if (index > -1) state.images[index] = payload;
        else state.images.push(payload);
      })
      .addCase(update.rejected, (state, { payload }) => {});

    builder
      .addCase(purge.fulfilled, (state, { payload }) => {
        state.images = state.images.filter((image) => image.id !== payload);
      })
      .addCase(purge.rejected, (state, { payload }) => {});
  },
});

const actions = {
  purge,
  refreshList,
  update,
  upload,
};

const selectors = {
  images: (state) => state[name].images,
};

const imageApi = {
  name,
  actions,
  reducer: imagesSlice.reducer,
  selectors,
};

export default imageApi;
