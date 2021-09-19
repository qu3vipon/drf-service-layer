from typing import Any

from rest_framework import generics, mixins


class GenericServiceAPIView(generics.GenericAPIView):
    """
    Service-layered GenericAPIView.
    """

    service_class = None
    service = None
    dto = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.connect_service(request)

    def connect_service(self, request):
        """
        Instantiate `self.service` using `self.service_class` and `self.dto`
        """

        assert self.service_class is not None, (
            "'%s' should provide a `service_class` attribute."
            % self.__class__.__name__
        )

        self.dto = self.create_dto(request)
        self.service = self.service_class(self.dto)

    def create_dto(self, request) -> Any:  # noqa
        """
        DTO(Data transfer object) can be any type you want to use for service.
        """
        return None


class CreateAPIView(mixins.CreateModelMixin,
                    GenericServiceAPIView):
    """
    Service-layered view for creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(mixins.ListModelMixin,
                  GenericServiceAPIView):
    """
    Service-layered view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(mixins.RetrieveModelMixin,
                      GenericServiceAPIView):
    """
    Service-layered view for retrieving a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyAPIView(mixins.DestroyModelMixin,
                     GenericServiceAPIView):
    """
    Service-layered view for deleting a model instance.
    """

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateAPIView(mixins.UpdateModelMixin,
                    GenericServiceAPIView):
    """
    Service-layered view for updating a model instance.
    """

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericServiceAPIView):
    """
    Service-layered view for listing a queryset or creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            GenericServiceAPIView):
    """
    Service-layered view for retrieving, updating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveDestroyAPIView(mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             GenericServiceAPIView):
    """
    Service-layered view for retrieving or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericServiceAPIView):
    """
    Service-layered view for retrieving, updating or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
