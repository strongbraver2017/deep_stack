from .models import RequestRecord
from DjiStudio.utils import MyModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework import permissions


class RequestRecordSerializer(ModelSerializer):
    class Meta:
        model = RequestRecord
        fields = ("__all__")


class RequestRecordViewSet(MyModelViewSet):
    queryset = RequestRecord.objects.all()
    serializer_class = RequestRecordSerializer
    permission_classes_by_action = {
        "list": [permissions.IsAuthenticated, ],
        "default": [permissions.IsAdminUser, ]
    }

    class Meta:
        model = RequestRecord

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        else:
            return RequestRecord.objects.filter(user=self.request.user)

