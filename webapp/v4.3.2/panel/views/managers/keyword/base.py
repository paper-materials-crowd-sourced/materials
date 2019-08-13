from django.urls import reverse
from nltk import word_tokenize
from panel.models import GHResult_KeywordMeter, GHResult_LastVersions, Code
from panel.views.auxiliary._extractor import extract_from_description
from panel.views.github._base import _checkGHUrl
from panel.views.github._helpers import comment_remover, _get_github_reponame_from_json
from panel.views.managers.keyword.utils import delete_table, extract_tokens


def _copy_table(_all: bool = False, top: int = 3):
    # reset table
    delete_table()

    # step 1. find vulnerable code snippets
    vulnerable_code_snippets = Code.objects.filter(is_vulnerable=True)
    for code in vulnerable_code_snippets:
        # step 2. retrieve repositories of each code snippet
        gh_repositories = _get_github_reponame_from_json(code.id)

        # step 3. sort repositories by repo_name
        gh_repositories.sort(key=lambda x: x.get('repo_name'))

        # step 4. fetch top 3 repositories
        top_gh_repos = gh_repositories[0: top]

        # print(top_gh_repos)
        # step 5. add repos to GHResult_KeywordMeter
        for repo in top_gh_repos:
            GHResult_KeywordMeter.objects.create(
                answer_id=repo.get('answer_id'),
                code=code,
                ghUrl=repo.get('url'),
                repo_name=repo.get('repo_name')
            )
    '''
    ## previous algorithm
    
    # copy from just vulnerable GHResult_LastVersions to GHResult_KeywordMeter
    # if _all:
    #     vulnerable_repos = GHResult_LastVersions.objects.all()
    # else:
    #     vulnerable_repos = GHResult_LastVersions.objects.filter(is_vulnerable=True)

    # vulnerable_repos = GHResult_LastVersions.objects.filter(is_vulnerable=True).values('code_id').distinct()
    # vulnerable_repos = Code.objects.filter(is_vulnerable=True)

    # step 1. list the repositories of each code snippet

    # step 2. sort by repository name

    return
    vulnerable_repos = []
    # lazy copy
    for repo in vulnerable_repos:
        gh_repos_of_code = _get_github_reponame_from_json(repo.code_id)
        repo_name = ""
        # find ghUrl of last versions
        for ghRepo in gh_repos_of_code:
            # compare repo.url with ghResult.ghUrl
            if str(ghRepo.get('url', '')).strip() == repo.ghUrl.strip():
                repo_name = repo.get('repo_name', '')
                break

        GHResult_KeywordMeter.objects.create(
            answer_id=repo.answer_id,
            code=repo.code,
            ghUrl=repo.ghUrl,
            repo_name=repo_name
        )
    '''


def _check_repos():
    repos = GHResult_KeywordMeter.objects.filter(is_checked=False)
    for repo in repos:

        # retrieve the code snippet
        code = repo.code

        # step 0. remove comments
        text = comment_remover(code.snipped_code)

        # step 1. Tokenize the code snippet (A)
        tokens = word_tokenize(text)

        # step 2. extract the previous keywords (B)
        keywords = extract_from_description(code.description, with_space=True)

        # TODO step 3. subtract the second set from the first set (C = A - B)
        if len(keywords) == 0:
            continue
        # step 4. choose random keywords from C (to the A number)
        final_tokens = extract_tokens(tokens, len(keywords))

        print(final_tokens)

        # step 5. check repo with new keywords
        # step 6. store result in the database
        _checkGHUrl(repo, final_tokens)

    return "Done"
    # vulnerable_previous_algorithm = GHResult_LastVersions.objects.filter(is_vulnerable=True).count()
    # vulnerable_current_algorithm = GHResult_KeywordMeter.objects.filter(is_vulnerable=True).count()
    #
    # return ("Vulnerable Repositories (Previous Algorithm): {}<br>"
    #         "Vulnerable Repositories (Auto Generate Tokens): {}<br>"
    #         "Accuracy (Auto / Previous): {:.2f}%<br>"
    #         "to run again Click <a href='{}'>here</a>".format(
    #     vulnerable_previous_algorithm,
    #     vulnerable_current_algorithm,
    #     (vulnerable_current_algorithm / vulnerable_previous_algorithm) * 100,
    #     reverse(viewname='copy_gh_result_last_version_and_check')
    # ))
