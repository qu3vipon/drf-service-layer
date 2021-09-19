from typing import Any


class Service:
    """
    Inherit this class to create service class.

    Example:
        class FooService(ServiceBase):
            # Implement your business logics.
    """

    def __init__(self, dto: Any = None):
        self.dto = dto
