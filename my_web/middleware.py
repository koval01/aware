import logging

logger = logging.getLogger(__name__)


class Compressor_AWARE:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        try:
            if not response.streaming:
                for i in range(10):
                    response.content = response.content.decode("utf-8").replace(
                        '\n', '').replace('  ', ' ').replace('> <', '><')
        except Exception as e:
            logger.warning(e)
        return response

    def process_exception(self, request, exception):
        logger.error(f'Middleware Compressor: {exception}')