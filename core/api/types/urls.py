from django.urls import path

from .views import (
    type_attributes,
    type_parent_entities,
)


app_name = 'types'

urlpatterns = [
    path('<int:pk>/attributes', type_attributes.TypeAttributesApiView.as_view(), name='type_attributes'),
    path('<int:pk>/entity-parents', type_parent_entities.ParentEntitiesTypeView.as_view(), name='parent_entities'),
]
