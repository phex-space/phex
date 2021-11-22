import uuid

from starlette.middleware.base import BaseHTTPMiddleware

from phex.logging import trace_id_context


class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        trace_id = request.headers.get("X-Trace-Id", None)
        if trace_id is None:
            trace_id = str(uuid.uuid4())
        trace_id_context.set(trace_id)
        response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id
        return response
