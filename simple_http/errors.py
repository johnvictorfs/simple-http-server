class HttpErrorNotFound404(Exception):
    def __init__(self, msg='Not found.', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
