class HttpError(Exception):
    def __init__(self, code: int = 400, msg: str = 'Not found.', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.code = code
