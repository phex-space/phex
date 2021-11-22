import contextvars
import logging

trace_id_context = contextvars.ContextVar("X-Trace-Id", default="unknown")
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s]:[%(traceid)s]:" + logging.BASIC_FORMAT,
    style='%',
)


class PhexLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.traceid = trace_id_context.get()


logging.setLogRecordFactory(PhexLogRecord)
