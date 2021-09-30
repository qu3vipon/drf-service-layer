from typing import Any


class Service:

    def __init__(self, dto: Any):
        self.dto = dto


def service_layer(cls):
    """
    add service layer to Serializer
    """

    original_init = cls.__init__

    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        assert self.context.get("service") is not None, (
            "'%s' should retrieve service context from view."
            % self.__class__.__name__
        )

        self.service = self.context["service"]

    cls.__init__ = __init__
    return cls
