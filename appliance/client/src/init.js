import getLogger, { Level } from "./utils/logging";

import globals from "./globals";

const { isDevelopment } = globals;

const log = getLogger("root", {
  level: isDevelopment ? Level.Debug : Level.Information,
});
log.info("Start phex app.");
