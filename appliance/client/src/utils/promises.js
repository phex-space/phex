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
