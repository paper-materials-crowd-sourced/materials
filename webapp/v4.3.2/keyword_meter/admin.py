from django.contrib import admin

# Register your models here.
# Code Model
from keyword_meter.forms import GHResultKeywordMeterForm
from keyword_meter.models import GHResultKeywordMeter, KeywordMeterStatus, CHECK_STATUS


@admin.register(GHResultKeywordMeter)
class GHResultKeywordMeterAdmin(admin.ModelAdmin):
    form = GHResultKeywordMeterForm

    list_filter = [
        'is_vulnerable_our_algorithm',
        'is_error',
        'is_vulnerable_random_algorithm',
        'status'
    ]
    search_fields = ['ghUrl', 'answer_id', 'id']
    list_per_page = 12
    list_display = [
        'id',
        'answer_id',
        'code_id',
        'ghUrl',
        'repo_name',
        'is_vulnerable_our_algorithm',
        'is_vulnerable_random_algorithm',
        'is_error',
        'check_status',
        'report',
    ]
    list_editable = [
        'is_error',
        'is_vulnerable_our_algorithm',
        'is_vulnerable_random_algorithm',
    ]

    def check_status(self, obj):
        return CHECK_STATUS[int(obj.status)][1]
