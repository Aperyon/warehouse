class NotEnoughStock(Exception):
    pass


class InvalidTransactionMessage(Exception):
    def __init__(self, message):
        self.message = message
