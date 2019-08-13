from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from panel.models import GHResult_KeywordMeter, GHResult_LastVersions
from panel.views.managers.keyword.base import _copy_table, _check_repos


def copy_table(request):
    # Target: find top 3 Repositories of each code snippets
    # step 1.
    _copy_table()

    return HttpResponse("Done")


def copy_all_table(request):
    _copy_table(_all=True)

    return HttpResponse("Done")


def check_repos(request):
    count_all = GHResult_KeywordMeter.objects.all().count()
    count_checked = GHResult_KeywordMeter.objects.filter(is_checked=True).count()

    print(count_all, count_checked)
    result = _check_repos()

    # if count_all != count_checked:
    #     pass
    # else:
    #     vulnerable_previous_algorithm = GHResult_LastVersions.objects.filter(is_vulnerable=True).count()
    #     vulnerable_current_algorithm = GHResult_KeywordMeter.objects.filter(is_vulnerable=True).count()
    #     result = "" \
    #              "Vulnerable Repositories (Previous Algorithm): {}<br>" \
    #              "Vulnerable Repositories (Auto Generate Tokens): {}<br>" \
    #              "Accuracy (Auto / Previous): {:.2f}%<br>" \
    #              "to run again Click <a href='{}'>here</a>".format(
    #         vulnerable_previous_algorithm,
    #         vulnerable_current_algorithm,
    #         (vulnerable_current_algorithm / vulnerable_previous_algorithm) * 100,
    #         reverse(viewname='copy_gh_result_last_version_and_check')
    #     )

    return HttpResponse(result)


def copy_and_check(request):
    _copy_table()

    return HttpResponseRedirect(reverse(viewname='check_gh_result_keyword_meter'))


def copy_all_and_check(request):
    _copy_table(_all=True)

    return HttpResponseRedirect(reverse(viewname='check_gh_result_keyword_meter'))


def reset_and_check(request):
    repos = GHResult_KeywordMeter.objects.all()
    for repo in repos:
        repo.is_checked = False
        repo.is_vulnerable = False
        repo.is_error = False
        repo.report = ""
        repo.save()

    return HttpResponseRedirect(reverse(viewname='check_gh_result_keyword_meter'))
