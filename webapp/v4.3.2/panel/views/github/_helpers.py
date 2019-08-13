import json
import os
import sys
import re

from django.conf import settings
from django.http import HttpResponse

from panel.models import Code_Answer, GHResult

sys.setrecursionlimit(10000)


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


def findnth(haystack, needle, n):
    parts = haystack.split(needle, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)


def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "  # note: a space and not an empty string
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


def _getGHReferencesFromJSON(file_id: int):
    BASE_PATH = os.path.join(settings.BASE_DIR, "code_snippets_metadata")
    try:
        with open(os.path.join(BASE_PATH, "{}.json".format(file_id)), 'r') as file:
            data = json.load(file)
            github_refernces = []
            for answer in data.get('answers', []):
                for _gh in answer.get('github_references', []):
                    _link = _gh.get('ghurl', None)
                    if _link:
                        github_refernces.append(_link)
            file.close()

        return github_refernces
    except Exception as e:
        print(e)
    return None


def getAllGHLinks():
    _all = {}
    for order_id in range(1, 2057):
        _all[order_id] = _getGHReferencesFromJSON(order_id)
    return _all


def _importVulnerableAnswersWithGHUrlToDB():
    answers_code = Code_Answer.objects.filter(code__is_vulnerable=True)
    counter = 0
    Inner_counter = 0
    link = ""
    try:
        for ac in answers_code:
            Inner_counter = 0
            counter = ac.code_id
            _ghs = _getGHReferencesFromJSON(ac.code_id)
            for gh in _ghs:
                Inner_counter += 1
                link = gh
                GHResult.objects.get_or_create(
                    code=ac.code,
                    answer_id=ac.answer_id,
                    ghUrl=gh
                )
        return [True, 'Done']
    except Exception as e:
        return [False, "Counter: {} - InnerCounter: {}<br>{}<br>{}".format(counter, Inner_counter, link, e)]


def _get_github_reponame_from_json(file_id: int):
    base_path = os.path.join(settings.BASE_DIR, "code_snippets_metadata")
    try:
        with open(os.path.join(base_path, "{}.json".format(file_id)), 'r') as file:
            data = json.load(file)
            github_references = []
            for answer in data.get('answers', []):
                _answer_id = answer.get('answerid', 0)
                for _gh in answer.get('github_references', []):
                    _link = _gh.get('ghurl', None)
                    _repo_name = _gh.get('reponame', '')
                    if _link:
                        github_references.append({
                            "answer_id": _answer_id,
                            "url": _link,
                            "repo_name": _repo_name,
                        })
            file.close()

        return github_references
    except Exception as e:
        print(e)
    return None
