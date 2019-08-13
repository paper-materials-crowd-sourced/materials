from django.contrib import admin
# Register your models here.
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from panel.forms import CodeForm, GHResultForm, GHResultLastVersionsForm
from panel.models import Code, Tag, GHResult, GHResult_LastVersions


# Code Model
@admin.register(GHResult)
class GHResultAdmin(admin.ModelAdmin):
    form = GHResultForm

    list_filter = [
        'is_checked',
        'is_error',
        'is_vulnerable'
    ]
    search_fields = ['ghUrl', 'answer_id']
    list_per_page = 12
    list_display = [
        'id',
        'answer_id',
        'code_id',
        'ghUrl',
        'is_checked',
        'is_vulnerable',
        'is_error',
        'report',
    ]
    list_editable = [
        'is_error',
        'is_vulnerable',
    ]


# Code Model
@admin.register(GHResult_LastVersions)
class GHResultLastVersionAdmin(admin.ModelAdmin):
    form = GHResultLastVersionsForm

    list_filter = [
        'is_checked',
        'is_error',
        'is_vulnerable'
    ]
    search_fields = ['ghUrl', 'answer_id', 'id']
    list_per_page = 12
    list_display = [
        'id',
        'answer_id',
        'code_id',
        'ghUrl',
        'repo_name',
        'is_checked',
        'is_vulnerable',
        'is_error',
        'report',
    ]
    list_editable = [
        'is_error',
        'is_vulnerable',
    ]

# # Code Model
# @admin.register(GHResult_KeywordMeter)
# class GHResultKeywordMeterAdmin(admin.ModelAdmin):
#     form = GHResultKeywordMeterForm
#
#     list_filter = [
#         'is_checked',
#         'is_error',
#         'is_vulnerable'
#     ]
#     search_fields = ['ghUrl', 'answer_id', 'id']
#     list_per_page = 12
#     list_display = [
#         'id',
#         'answer_id',
#         'code_id',
#         'ghUrl',
#         'repo_name',
#         'is_checked',
#         'is_vulnerable',
#         'is_error',
#         'report',
#     ]
#     list_editable = [
#         'is_error',
#         'is_vulnerable',
#     ]


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.13.1/highlight.min.js',
            'js/custom.js',
        )
        css = {
            'all' : ('//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.13.1/styles/default.min.css',)
        }
    form = CodeForm
    search_fields = [
        'filename',
        'snipped_code',
    ]
    list_filter = [
        'reviewed',
        'is_vulnerable'
    ]

    list_per_page = 5
    list_display = [
        'link',
        'filename',
        'group_id',
        'reviewed',
        'is_vulnerable',
        'so_urls',
        'show'
    ]
    list_editable = [
        'reviewed',
        'is_vulnerable'
    ]
    readonly_fields = [
        'filename',
        'group_id',
        # 'snipped_code',
        'code_',
        'so_urls'
    ]
    exclude = [
        'snipped_code'
    ]

    list_display_links = ['filename']

    def so_urls(self,obj):
        urls = obj.sourl_set.all()
        out = ""
        for url in urls :
            out += "<a href='{0}'>{0}</a> <br>".format(url.url)

        return mark_safe(out)

    def link(self,obj):
        return mark_safe('<a href="/code/{ID}">{ID}</a>'.format(ID=obj.id))
    link.short_description = "link to code"

    def code_(self,obj):

        data = '''
    <pre>
    <code class="cpp">
    {code}
    </code>
    </pre>
        '''
        return format_html(data,code=obj.snipped_code.strip())

    def show(self,obj):

        data = '''
    <pre>
    <code class="cpp">
    {code}
    </code>
    </pre>
        '''
        return format_html(data,code=obj.snipped_code.strip())

    # def attached(self,obj):
    #     if not obj.file:
    #         return None
    #     return mark_safe('<a href="{MEDIA_URL}{url}">Attached</a>'.format(
    #                 MEDIA_URL=settings.MEDIA_URL,
    #                 url=obj.file
    #             )
    #         )


# Tag Model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name'
    ]
    list_display_links = ['id', 'name']