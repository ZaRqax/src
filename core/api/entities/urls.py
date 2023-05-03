from django.urls import path

from .views import (
    entities,
    entity_children,
    entity_types,
)


app_name = 'entities'

urlpatterns = [
    path('', entities.EntityViewSet.as_view({'post': 'create', 'get': 'list'}), name='entities'),
    path('<int:pk>', entities.EntityViewSet.as_view({'get': 'retrieve', 'delete': 'delete'}), name='entity-detail'),
    path('types', entity_types.EntityTypesApiView.as_view(), name='get_types'),
    path('<int:pk>/children', entity_children.EntityChildrenApiView.as_view(), name='entity_children'),
]
