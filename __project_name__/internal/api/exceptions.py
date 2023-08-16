import logging

from fastapi.responses import ORJSONResponse

from utils.exceptions import ExceptionBase


async def except_unknown(_, exc: ExceptionBase):
    logging.error(exc.detail)
    return ORJSONResponse({"message": exc.detail}, 500)


EXCEPTION_HANDLER_STACK = {
    ExceptionBase: except_unknown,
}
