class Function:
    def __init__(self, func, *args, **kwargs):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class SetFunction(Function):
    def __init__(self, func, *args, **kwargs):
        super().__init__(func)

        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.func(*self.args, **self.kwargs)