import getLogger from "./logging";

const log = getLogger("utils-promises");

export function waitUntil(condition, timeout = 2000) {
  const start = Date.now();
  return new Promise((resolve, reject) => {
    const checker = () => {
      if (condition()) return resolve();
      if (Date.now() - start < timeout) setTimeout(checker, 10);
      else reject(new Error("Timeout"));
    };
    checker();
  });
}

export function sleep(timeout = 1000) {
  return new Promise((resolve) => {
    setTimeout(resolve, timeout);
  });
}

export async function retryWhenFail(callback, maxRetries = 5, maxWait = 8000) {
  if (typeof callback !== "function")
    return Promise.reject(new Error("Callback is not a function."));
  let wait = 500;
  let lastException;
  let tries = 0;
  do {
    try {
      return await Promise.resolve(callback());
    } catch (err) {
      tries++;
      log.error("Failed to call", callback, "retry #" + tries, err);
      lastException = err;
      await sleep(wait);
      wait *= 2;
      if (wait > maxWait) wait = maxWait;
    }
  } while (tries < maxRetries);
  throw lastException;
}
