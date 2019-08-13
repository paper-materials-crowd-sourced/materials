from django.urls import path, include

from panel.views.ajax import update_vuln, update_des, code_tags, answer_done
from panel.views.github.Responses import _reset_importGHUrlsOfVulnerableTODB_CheckRepos_Response, _goResetRepos_Respone, \
    _goCheckRepos_Response, _importVulnerableAnswersWithGHUrlToDB_Response, LastVersion_On_GHRepos, \
    set_reponame_of_last_version_github_repositories, export_for_extension_markdown_to_html, \
    export_for_extension_vulnerable_repos, export_for_extension_template
from panel.views.helper import add_answer_id, add, list_tags, add_tag, answer_code_ids, answer_downgrade, \
    add_template_to_description, test
from panel.views.managers.keyword.responses import copy_table, check_repos, copy_all_table, copy_and_check, \
    copy_all_and_check, reset_and_check
from panel.views.minner_ import _extract_from_code
from panel.views.views import show, index, code_answers_list, code_answers, tgs, tg_codes, FindCategoreis, \
    CodeSnippetsWithDescriptionHigherThan50Chars, IssueResult

urlpatterns = [
    path('', index),

    # AJAX ROUTES
    path('updateVuln/<code_id>/', update_vuln),
    path('updateDes/<code_id>/', update_des),
    path('code/<code_id>/tags/', code_tags),

    # HELPER ROUTES
    # path('add/', add),
    # path('answer/', add_answer_id),
    path('tags/',list_tags),
    path('tags/add/',add_tag),
    #path('answers/template/', add_template_to_description, name="add_template_to_description"),

    # WEB ROUTES
    path('answers/', code_answers_list , name="code_answers_list"),
    path('answers/<answer_id>/', code_answers , name="code_answers"),
    path('answers/<answer_id>/done/', answer_done , name="answer_done"),
    path('answers/<answer_id>/codes/', answer_code_ids, name="answer_code_ids"),
    path('answers/<answer_id>/downgrade/', answer_downgrade, name="answer_downgrade"),

    # Code
    path('code/<id>/', show , name="show_code"),
    # extract types: explain, keywords, mitigation, references
    path('code/<id>/<extract_type>/', _extract_from_code, name="extract_code_keywords"),

    # Additional Code Manipulations
    path('cs/<min>/', CodeSnippetsWithDescriptionHigherThan50Chars, name="CodeSnippetsWithDescriptionHigherThan50Chars"),

    # Code with Tags
    path('tg/', tgs, name="tag_list"),
    path('tg/<tag_id>/', tg_codes, name="tags_with_codes"),

    # Github
    path('gh/import/', _importVulnerableAnswersWithGHUrlToDB_Response, name="importVulnerableAnswersWithGHUrlToDB"),
    path('gh/check/', _goCheckRepos_Response, name="goCheckRepos"),
    path('gh/check/reset/', _goResetRepos_Respone, name="goResetRepos"),
    path('gh/check/reset/all/', _reset_importGHUrlsOfVulnerableTODB_CheckRepos_Response, name="reset_importGHUrlsOfVulnerableTODB_CheckRepos_Response"),
    path('gh/check/lastversion/', LastVersion_On_GHRepos, name="LastVersion_On_GHRepos"),
    path('gh/set/reponame/', set_reponame_of_last_version_github_repositories, name="set_reponame_of_last_version_github_repositories"),
    path('gh/export/vulnerable_repos_extension.json', export_for_extension_markdown_to_html, name='export_for_extension_markdown_to_html'),
    path('gh/export/extension_template.json', export_for_extension_template, name='export_for_extension_template'),
    path('gh/export/vulnerable_repos_code_snippet.json', export_for_extension_vulnerable_repos, name='export_for_extension_vulnerable_repos'),


    # Keyword Metric
    # path('keyword/copy/', copy_table, name='copy_gh_result_last_version_table'),
    # path('keyword/copy/all/', copy_all_table, name='copy_all_gh_result_last_version_table'),
    # path('keyword/copy/all/check/', copy_all_and_check, name='copy_all_gh_result_last_version_and_check'),
    # path('keyword/copy/check/', copy_and_check, name='copy_gh_result_last_version_and_check'),
    # path('keyword/reset/check/', reset_and_check, name='reset_and_check'),
    # path('keyword/check/', check_repos, name='check_gh_result_keyword_meter'),
    path('keyword/', include('keyword_meter.urls')),
    # Categories
    path('categories/', FindCategoreis, name='FindCategoreis'),

    # Issue Manipulations
    path('issue/result/', IssueResult.as_view(), name='IssueResult'),

    path('test/<tgid>', test, name="test"),
]


