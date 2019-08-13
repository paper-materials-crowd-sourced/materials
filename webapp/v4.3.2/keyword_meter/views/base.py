from random import randint

import requests
from django.db.models import Q
from nltk import word_tokenize

from keyword_meter.models import GHResultKeywordMeter, KeywordMeterStatus
from panel.models import Code
from panel.views.auxiliary._extractor import extract_from_description
from panel.views.github._base import contain_keywords
from panel.views.github._helpers import _get_github_reponame_from_json, comment_remover
from panel.views.managers.keyword.utils import extract_tokens


class CHECKING_TYPE:
    OUR_ALGORITHM = 1
    RANDOM_ALGORITHM = 2


def _choose_random(array: list, number: int = 3) -> list:

    if len(array) < number:
        return array

    feedback = []
    while True:
        index = randint(0, len(array) - 1)
        if index in feedback:
            continue

        feedback.append(index)
        if len(feedback) == number:
            break

    return [array[element] for element in feedback]


def rollback():
    # reset all
    GHResultKeywordMeter.objects.filter(Q(is_vulnerable_our_algorithm=True) |
                                        Q(is_vulnerable_random_algorithm=True)) \
        .update(
        is_vulnerable_our_algorithm=False,
        is_vulnerable_random_algorithm=False,
        is_error=False,
        report=''
    )
    return True


def import_to_table_from_files(number):
    _VALID_EXTENSIONS = ['.cpp', '.hpp', '.cc', '.h', '.cu', '.re2c']

    # step 1. list vulnerable code snippets
    codes = Code.objects.filter(is_vulnerable=True)

    for code in codes:
        # step 2. get github repos of each code
        github_repos = _get_github_reponame_from_json(code.id)

        # step 2.1. validate file extensions
        valid_repos = []
        for repo in github_repos:
            for extension in _VALID_EXTENSIONS:
                if repo.get('url').lower().endswith(extension):
                    valid_repos.append(repo)
                    break

        # step 3. choose github repos randomly (same as MAX_REPO)
        repos = _choose_random(valid_repos, number)

        # step 4. import to the table (GHResultKeywordMeter)
        for repo in repos:
            GHResultKeywordMeter.objects.create(
                answer_id=repo.get('answer_id'),
                ghUrl=repo.get('url'),
                repo_name=repo.get('repo_name'),
                code=code
            )

    return True


def check_github_repo_with_keywords(gResult, checking_type: int, keywords: list = None):
    try:
        # load content
        req = requests.get(gResult.ghUrl)
        # remove comments from content
        content = comment_remover(req.text.replace(" ", ""))

        # load keywords
        if keywords is None:
            code = Code.objects.filter(id=gResult.code_id).first()
            keywords = extract_from_description(code.description)

        # check keywords for file
        if contain_keywords(content, keywords):
            print("YESS", gResult.id, gResult.code_id, gResult.answer_id)
            # save it to the DB
            if checking_type == CHECKING_TYPE.OUR_ALGORITHM:
                gResult.is_vulnerable_our_algorithm = True
                gResult.status = KeywordMeterStatus.checked_by_our_algorithm
            elif checking_type == CHECKING_TYPE.RANDOM_ALGORITHM:
                gResult.is_vulnerable_random_algorithm = True
                gResult.status = KeywordMeterStatus.checked_by_random_algorithm

            gResult.save()
        else:
            print("NOOO", gResult.code_id, gResult.answer_id)
            if checking_type == CHECKING_TYPE.OUR_ALGORITHM:
                gResult.is_vulnerable_our_algorithm = False
                gResult.status = KeywordMeterStatus.checked_by_our_algorithm
            elif checking_type == CHECKING_TYPE.RANDOM_ALGORITHM:
                gResult.is_vulnerable_random_algorithm = False
                gResult.status = KeywordMeterStatus.checked_by_random_algorithm
            gResult.save()
        return True
    except Exception as e:
        gResult.is_error = True
        gResult.report = "{}".format(e)
        gResult.save()
        return False


def check_a_repo_by_our_algorithm(repo):
    return check_github_repo_with_keywords(repo, checking_type=CHECKING_TYPE.OUR_ALGORITHM)


def check_a_repo_by_random_algorithm(repo, shuffle: bool = False):
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
        return False

    # step 4. choose random keywords from C (to the A number)
    final_tokens = extract_tokens(tokens, len(keywords), min_len=3, shuffling=shuffle)

    print(final_tokens)

    # step 5. check repo with new keywords
    # step 6. store result in the database
    check_github_repo_with_keywords(repo, checking_type=CHECKING_TYPE.RANDOM_ALGORITHM, keywords=final_tokens)

    return True


