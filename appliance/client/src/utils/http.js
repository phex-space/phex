export class HttpException extends Error {
  constructor(status, message, code) {
    super(message);
    this.status = status;
    this.code = code;
  }
}
export async function responseHandler(request) {
  const response = await request;
  if (response.status > 399) {
    const error = await response.json();
    if (typeof error.detail === "string")
      throw new HttpException(response.status, error.detail);
    if (typeof error.detail === "object" && error.detail.message)
      throw new HttpException(
        response.status,
        error.detail.message,
        error.detail.error
      );
    throw new HttpException(response.status, error.toString())
  }
  return response;
}
