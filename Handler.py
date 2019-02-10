from abc import abstractmethod


class Handler:

    def __init__(self):
        pass

    # Method to be specified by the user
    @abstractmethod
    def handle(self, request):
        pass
