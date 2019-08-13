import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from markdown import markdown

from panel.models import GHResult, Code, GHResult_LastVersions, Code_Answer
from panel.views.github._base import _goCheckRepos, _COPY_FROM_GHRESULT_TO_GURESULT_LASTVERSIONS, _goCheckLastVersions
from panel.views.github._helpers import _importVulnerableAnswersWithGHUrlToDB, _get_github_reponame_from_json


@login_required(login_url="/admin/login")
def _importVulnerableAnswersWithGHUrlToDB_Response(request):
    result,msg = _importVulnerableAnswersWithGHUrlToDB()
    return HttpResponse(msg)


@login_required(login_url="/admin/login")
def _goCheckRepos_Response(request):
    _goCheckRepos()
    return HttpResponseRedirect("/admin/panel/ghresult/")


@login_required(login_url="/admin/login")
def _goResetRepos_Respone(requst):
    _goCheckRepos()
    return HttpResponse("Reset Done")


@login_required(login_url="/admin/login")
def _reset_importGHUrlsOfVulnerableTODB_CheckRepos_Response(request):

    # delete all ghUrls
    GHResult.objects.all().delete()

    # import from json to db
    importGH_Vulnes_TO_DB , msg = _importVulnerableAnswersWithGHUrlToDB()
    if not importGH_Vulnes_TO_DB:
        return HttpResponse(msg)

    # check repos
    _goCheckRepos()

    return HttpResponseRedirect("/admin/panel/ghresult/")


@login_required(login_url="/admin/login")
def LastVersion_On_GHRepos(request):
    # delete all
    GHResult_LastVersions.objects.all().delete()

    # copy all last versions
    _COPY_FROM_GHRESULT_TO_GURESULT_LASTVERSIONS()

    # Last step
    _goCheckLastVersions()

    return HttpResponseRedirect("/admin/panel/ghresult_lastversions/")


@login_required(login_url="/admin/login")
def set_reponame_of_last_version_github_repositories(request):

    # get all vulnerabilities repos
    last_version_vulnerable = GHResult_LastVersions.objects.filter(is_vulnerable=True)

    # run this procedural for each vulnerable github repo
    for ghResult in last_version_vulnerable:
        # load all github repositories of this code snippet
        github_repos_info = _get_github_reponame_from_json(ghResult.code_id)

        # find ghUrl of last versions
        for repo in github_repos_info:

            # compare repo.url with ghResult.ghUrl
            if str(repo.get('url', '')).strip() == ghResult.ghUrl.strip():
                ghResult.repo_name = repo.get('repo_name', '')
                ghResult.save()

    return HttpResponse("Done")


@login_required(login_url='/admin/login')
def export_for_extension_markdown_to_html(request):
    export_file_name = "export_markdown_to_html.json"

    is_markdown = False
    if request.GET.get('markdown', None):
        is_markdown = True

    # find all vulnerable github repositories
    vulnerable_github_repos = GHResult_LastVersions.objects.filter(is_vulnerable=True)

    vulnerabilities = []
    for github_repo in vulnerable_github_repos:
        # convert markdown description of
        if is_markdown:
            converted_description = github_repo.code.description
        else:
            converted_description = markdown(github_repo.code.description)

        # generate template
        instance = {
            'full_repo_name': github_repo.repo_name,
            'issue_title': 'Auto Title Generator',
            'issue_body': converted_description,
        }

        # add instance to vulnerabilities array
        vulnerabilities.append(instance)

    # add vulnerabilities to base template
    final_result = {
        "created_timestamp": timezone.now().timestamp(),
        "vulnerabilities": vulnerabilities
    }

    # write to file
    # with open(export_file_name, 'w') as file:
    #     json.dump(final_result, file)

    return HttpResponse(
        json.dumps(final_result),
        content_type='application/json'
    )


@login_required(login_url='/admin/login')
def export_for_extension_template(request):
    export_file_name = "export_extension_template.json"

    is_markdown = False
    if request.GET.get('markdown', None):
        is_markdown = True

    # find all vulnerable github repositories
    vulnerable_github_repos = GHResult_LastVersions.objects.filter(is_vulnerable=True)

    question_with_answers = dict()
    for github_repo in vulnerable_github_repos:
        # convert markdown description of
        if is_markdown:
            converted_description = github_repo.code.description
        else:
            converted_description = markdown(github_repo.code.description)

        # generate template
        question_id = Code_Answer.objects.filter(answer_id=github_repo.answer_id).first().question_id
        answers_with_content = dict()
        for answer in Code_Answer.objects.filter(question_id=question_id):
            if answer.code.is_vulnerable:
                answers_with_content[answer.answer_id] = converted_description

        # add instance to vulnerabilities array
        question_with_answers[question_id] = answers_with_content

    return HttpResponse(
        json.dumps(question_with_answers),
        content_type='application/json'
    )


@login_required(login_url='/admin/login')
def export_for_extension_vulnerable_repos(request):

    # find all vulnerable github repositories
    vulnerable_github_repos = GHResult_LastVersions.objects.filter(is_vulnerable=True)

    data = []
    for ghResult in vulnerable_github_repos:
        instance = {
            "github": {
                "id": ghResult.id,
                "url": ghResult.ghUrl,
                "repo_name": ghResult.repo_name
            },
            "code_snippet": {
                "id": ghResult.code_id,
                "content": ghResult.code.snipped_code
            }
        }

        data.append(instance)

    return HttpResponse(
        json.dumps(data),
        content_type='application/json'
    )
