from django.contrib import admin
from .models import RecentIpActivity, RequestRecord, Ban, VerifyCode
from DjiStudio.utils import get_model_field_names, MyAdmin


class BanAdmin(MyAdmin):
    list_display = get_model_field_names(model=Ban)


class RequestRecordAdmin(MyAdmin):
    list_display = get_model_field_names(model=RequestRecord)
    
    def get_list_filter(self, request):
        res = super(RequestRecordAdmin, self).get_list_filter(request)
        if "method" not in res:
            res.append("method")
        return res


class RecentIpActivityAdmin(MyAdmin):
    list_display = get_model_field_names(model=RecentIpActivity)
    

class VerifyCodeAdmin(MyAdmin):
    list_display = get_model_field_names(model=VerifyCode)


admin.site.register(RequestRecord, RequestRecordAdmin)
admin.site.register(RecentIpActivity, RecentIpActivityAdmin)
admin.site.register(Ban, BanAdmin)
admin.site.register(VerifyCode, VerifyCodeAdmin)
