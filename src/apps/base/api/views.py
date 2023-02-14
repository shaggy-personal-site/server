from rest_framework import mixins, settings
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet


class ShaggyGenericViewSet(GenericViewSet):
    """
    Permissions:
    We override get_permissions() GenericViewSet method, inherited from views.APIView.

    Serializers:
    We override get_serializer_class() GenericViewSet method
    """

    action_permissions: dict = {"default": api_settings.DEFAULT_PERMISSION_CLASSES}
    action_serializers: dict

    def get_permissions(self):
        assert (
            self.action_permissions
        ), f"{self.__class__.__name__} needs to define a `action_permissions` attribute"
        assert self.action_permissions.get(
            "default"
        ), f"{self.__class__.__name__} needs to define a `default` in 'action_permissions' attribute"
        self.permission_classes = self.action_permissions.get(
            self.action, self.action_permissions["default"]
        )

        return super().get_permissions()

    def get_serializer_class(self):
        assert (
            self.action_serializers
        ), f"{self.__class__.__name__} needs to define a `action_serializers` attribute"
        assert self.action_serializers.get(
            "default"
        ), f"{self.__class__.__name__} needs to define `default` in `action_serializers` attribute"

        self.serializer_class = self.action_serializers.get(
            self.action, self.action_serializers["default"]
        )

        return super().get_serializer_class()


class ShaggyModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    ShaggyGenericViewSet,
):
    # ModelViewSet from rest_framework.viewsets with overriden:
    #    - get_permissions
    #    - get_serializer_class

    ...
