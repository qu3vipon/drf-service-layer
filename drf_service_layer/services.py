from typing import Any

from django.contrib.auth import get_user_model

User = get_user_model()


class Service:

    def __init__(self, dto: Any):
        self.dto = dto


def service_layer(service_class):
    """
    add service layer to Serializer
    """

    def wrapper(cls):
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            assert self.context.get("service") is not None, (
                "'%s' should retrieve service context from view."
                % self.__class__.__name__
            )

            service = self.context["service"]
            assert isinstance(service, service_class), (
                "Injected service from view and declared service from decorator are not matched in '%s'."
                % self.__class__.__name__
            )

            setattr(self, "service", service)

        cls.__init__ = __init__
        return cls

    return wrapper
