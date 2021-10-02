from typing import Any

from django.contrib.auth import get_user_model

User = get_user_model()


class Service:

    def __init__(self, dto: Any):
        self.dto = dto


def service_layer(service_class, dto=None):
    """
    add service layer to Serializer
    """

    def wrapper(cls):
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            assert self.context.get("service") is not None, (
                f"{self.__class__.__name__} should retrieve service context from view."
            )

            service = self.context["service"]
            assert isinstance(service, service_class), (
                f"{self.__class__.__name__}: The service injected from view and the service declared in the decorator are not the same."
            )

            if dto:
                assert isinstance(service.dto, dto), (
                    f"{self.__class__.__name__}: The dto injected from view and the dto declared in the decorator are not the same."
                )

            setattr(self, "service", service)

        cls.__init__ = __init__
        return cls

    return wrapper
