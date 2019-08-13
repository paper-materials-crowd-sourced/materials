from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from keyword_meter.models import GHResultKeywordMeter, KeywordMeterStatus
from keyword_meter.views.base import import_to_table_from_files, rollback, check_a_repo_by_random_algorithm, check_a_repo_by_our_algorithm


@login_required
def import_to_database(request, number=3):
    # clean the table
    GHResultKeywordMeter.objects.all().delete()

    # import to database
    import_to_table_from_files(number)

    return HttpResponse("Done")


def rollback_response(request):
    rollback()

    return HttpResponse("Rollback Done")


@login_required
def check_database_with_each_algorithm(request):
    github_repos = GHResultKeywordMeter.objects.exclude(status=KeywordMeterStatus.checked_by_both)
    for repo in github_repos:

        # Run Our Algorithm
        check_a_repo_by_our_algorithm(repo)

        # Run Random Algorithm
        check_a_repo_by_random_algorithm(repo)

        # update repo status
        repo.status = KeywordMeterStatus.checked_by_both
        repo.save()

    return HttpResponseRedirect('/admin/keyword_meter/ghresultkeywordmeter/')


def reset_all(request, number=3):
    # reset
    GHResultKeywordMeter.objects.all().delete()

    # import to database
    import_to_table_from_files(number)

    # Run
    github_repos = GHResultKeywordMeter.objects.exclude(status=KeywordMeterStatus.checked_by_both)
    for repo in github_repos:
        # Run Our Algorithm
        check_a_repo_by_our_algorithm(repo)

        # Run Random Algorithm
        check_a_repo_by_random_algorithm(repo, shuffle=True)

        # update repo status
        repo.status = KeywordMeterStatus.checked_by_both
        repo.save()

    return HttpResponseRedirect('/admin/keyword_meter/ghresultkeywordmeter/')