from dataclasses import dataclass
from typing import Any, Optional

from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer

User = get_user_model()


class Service:

    def __init__(self, dto: Any):
        self.dto = dto


@dataclass
class SerializerDTO:
    serializer: Serializer
    user: Optional[User] = None


def service_layer(service_class, to: str = "serializer"):
    """
    add service layer to any Class(e.g. View, Serializer, ...)
    """

    def wrapper(cls):
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            try:
                dto = getattr(self, "dto")
            except AttributeError:
                dto = None

                # build default dto when decorating serializer
                if to.lower() == "serializer":
                    dto = SerializerDTO(
                        serializer=self,
                        user=getattr(self.context["request"], "user", None)
                    )

            self.service = service_class(dto)

        cls.__init__ = __init__
        return cls

    return wrapper
