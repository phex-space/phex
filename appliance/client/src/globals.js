const isDevelopment = process.env.NODE_ENV === "development";
const apiUrl = isDevelopment
  ? "https://api.phex.local"
  : "https://api.phex.space";

const globals = {
  isDevelopment,
  apiUrl,
};

export default globals;
