export const Level = Object.freeze({
  Off: -1,
  Error: 0,
  Warning: 1,
  Information: 2,
  Debug: 3,
  Trace: 4,
  "-1": "Off",
  0: "Error",
  1: "Warning",
  2: "Information",
  3: "Debug",
  4: "Trace",
  toNumber: (level) => (typeof level === "number" ? level : Level[level]),
  toString: (level) => (typeof level === "string" ? level : Level[level]),
});

export class Logger {
  static root = new Logger("root", Level.Information);

  constructor(name, level) {
    level = level != null ? level : Logger.root.level;
    this.name = name;
    this.level = Level.toNumber(level);
  }

  isEnabled = (level) => Level.toNumber(level) <= this.level;

  error = (message, ...args) => {
    this.#doLog(Level.Error, message, ...args);
  };

  warn = (message, ...args) => {
    this.#doLog(Level.Warning, message, ...args);
  };

  info = (message, ...args) => {
    this.#doLog(Level.Information, message, ...args);
  };

  debug = (message, ...args) => {
    this.#doLog(Level.Debug, message, ...args);
  };

  trace = (message, ...args) => {
    this.#doLog(Level.Trace, message, ...args);
  };

  #doLog(level, ...args) {
    if (!this.isEnabled(level)) return;
    let log;
    switch (Level.toNumber(level)) {
      case Level.Error:
        log = console.error;
        break;
      case Level.Warning:
        log = console.warn;
        break;
      case Level.Information:
        log = console.info;
        break;
      case Level.Trace:
        log = console.debug;
        break;
      default:
        log = console.log;
    }
    let lvl = Level.toString(level).toUpperCase();
    if (lvl.length > 5) lvl = " " + lvl.substr(0, 4);
    log(`${new Date().toISOString()} ${lvl} [${this.name}] -`, ...args);
  }
}

const loggers = {};

function getLogger(name, config) {
  if (config) {
    Logger.root = new Logger("root", config.level);
  }
  if (!loggers[name]) loggers[name] = new Logger(name);
  return loggers[name];
}

export default getLogger;
