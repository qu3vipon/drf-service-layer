# DRF-Service-Layer

Simple package which supports service-layered design for Django REST Framework.

<br>

## Why service layer?

Have you ever wondered where to put your business logic when you use Django & DRF? There are several solutions with
their pros and cons. Let's check them one by one.

1. Fat Models, Skinny Views <br>
   This is one of the most popular ways to split business logic from views. To keep your views light, all the heavy
   codes go into "fat" models. The problem is that as your project gets bigger, there are too many codes in your models
   and models get too many responsibilities. Besides, there are some cases when your business logic doesn't require any
   database access. There is no reason for them to be in models, which is not quite reasonable.


2. QuerySet/Managers <br>
   It might be preferable to move your business logic from models to queryset or managers. But still, this solution is
   not a good choice like the "Fat Models approach" if your business logic doesn't need to communicate with databases.


3. Forms or Serializers <br>
   Probably the worst option. They each have their own purpose. Please don't do this.


4. Fat Views <br>
   If all of your business logic stays in views, you'll have trouble understanding the flow of your views in a very
   short period of time. And if you inherit one of your fat views, the parent view and the child view are too strongly
   coupled. So you'll have a hard time when you want to extract the legacy apis from your project.


5. Service layer <br>
   Split your business logic into functions and put them in a separate layer which ties models and views. To manage
   functions efficiently and improve the cohesion of codes, combine them into classes. In this way, views become easier
   to read and business logic becomes much more maintainable. Even though this may not be a standard design pattern from
   Django convention, some big companies
   like [Doordash](https://doordash.engineering/2017/05/15/tips-for-building-high-quality-django-apps-at-scale/) are
   already using this pattern by implementing it on their own.

<br>

## How to use DRF-Service-Layer in View

### Steps

1. Install package

   ```python
   pip install drf-service-layer
   ```
   > 💡 If you don't need to use any data when implementing business logic, skip step 2&3.
2. Decide a type of DTO.

   > 💁 What is DTO? <br> [DTO(Data Transfer Object)](https://en.wikipedia.org/wiki/Data_transfer_object) is an object that carries data between processes. <br> In DRF-Service-Layer, DTO is an object used for transferring data necessary for your business logic.

   DTO works between views and the service layer. If you want to transfer any data from a view to a service, implement
   `create_dto()` in your view that inherits GenericServiceAPIView from DRF-Service-Layer. We'll cover this
   shortly. <br>

   Let's implement DTO. There are several container types you can use. If you want to validate your DTO before transfer,
   you can use 3rd party library like [Pydantic](https://pydantic-docs.helpmanual.io/).

    - DTO as dataclass
      ```python
      # services.py
      from dataclasses import dataclass
      from typing import Union
      
      
      @dataclass
      class OrderDTO:
          user_id: int
          sort: Union[str, None]
          is_paid: bool
      ```

    - DTO as dictionary
    - DTO as list
    - or any type you want...

3. Implement `create_dto()` in views.

   If you decide to use dataclass as DTO:
   ```python
   # views.py
   from drf_service_layer.views import GenericServiceAPIView
   
   
   class OrderAPIView(GenericServiceAPIView):
   
       @property
       def dto(self) -> OrderDTO:
           order_id = self.kwargs['order_id']
           order = get_object_or_404(Order, pk=order_id)
   
           return OrderDTO(
               user_id=self.request.user.id,
               sort=self.request.query_params.get("sort"),
               is_paid=order.is_paid
           )   
   ```

4. Create a service class and implement business logic as an instance function.

   ```python
   # services.py
   from drf_service_layer.services import Service
   
   
   class OrderService(Service):
   
       def any_business_function(self):
           user_id = self.dto.user_id
           sort = self.dto.sort
           is_paid = self.dto.is_paid
           # business logic goes here. 
   ```

5. Specify a service class into a view as `service_class`.

   ```python
   # views.py
   class OrderAPIView(GenericServiceAPIView):
       service_class = OrderService  # new
   
       @property
       def dto(self) -> OrderDTO:
           # ...
   ```

6. Use service layer in a view.

   ```python
   # views.py
   class OrderAPIView(GenericServiceAPIView):
       service_class = OrderService
   
       @property
       def dto(self) -> OrderDTO:
           # ...
   
       def get(self, request, *args, **kwargs):  # new
           # ...
           self.service.any_business_function()
           # ...
           return Response(...)
   ```

### Description

When a view is initialized by DRF's `initial()` method, `dto` property you have implemented is used as an argument when
instantiating the service layer. DTO is already injected into the service layer as an instance variable(`self.dto`), so
you don't need to care about parameters when implementing business logic and using them. After all, you can call any
function from the service layer using `self.service` in your views.

<br>

## How to use DRF-Service-Layer in Serializer

Under Experiment...

```python
@service_layer(OrderService)
class FooSerializer(serializers.ModelSerializer):
    # ...
```

## Inspired by

- [How to implement a service layer in Django + Rest Framework](https://breadcrumbscollector.tech/how-to-implement-a-service-layer-in-django-rest-framework/)