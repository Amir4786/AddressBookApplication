class AddressNotFoundException(Exception):
    def __init__(self, address_id: int):
        self.address_id = address_id