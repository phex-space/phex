export function fireEvent(callback, ...args) {
  if (typeof callback !== "function") return Promise.resolve();
  return Promise.resolve(callback(...args));
}
