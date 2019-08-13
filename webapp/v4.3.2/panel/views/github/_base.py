import requests

from panel.models import Code, GHResult, GHResult_LastVersions
from panel.views.auxiliary._extractor import extract_from_description
from panel.views.github._helpers import find_all, findnth, comment_remover, _importVulnerableAnswersWithGHUrlToDB


def contain_keywords(content_text, keywords, offset=0, keyword_index=0):
    or_keyword = False

    if keyword_index >= len(keywords) or offset >= len(content_text):
        return True

    for loop_keyword_index, keyword in enumerate(keywords[keyword_index:]):
        keyword = keyword.lstrip()
        if keyword.startswith("@!"):
            reg = keyword[2:]
            # Don't look whole file, just search it in at last 10 lines:
            # If you want to search all over the file, remove these 3 lines (including pos_of_tens_line at location ...)
            pos_of_tens_line = findnth(content_text[offset:], '\n', 10)
            if pos_of_tens_line == -1:
                pos_of_tens_line = len(content_text)

            location = content_text.find(reg, offset, offset + pos_of_tens_line)

            if location != -1:
                return False
            return contain_keywords(content_text, keywords, offset=offset,
                                    keyword_index=keyword_index + loop_keyword_index + 1)
        elif keyword.startswith("!"):
            reg = keyword[1:].strip()

            for keyword_positions in list(find_all(content_text[offset:], reg)):
                valid_pattern = contain_keywords(content_text, keywords,
                                                 offset=(offset + keyword_positions + len(reg)),
                                                 keyword_index=(keyword_index + loop_keyword_index + 1))
                if valid_pattern:
                    return True
            return False
        elif keyword.startswith('|!'):
            or_keyword = True
            break

    if or_keyword:
        for keyword in keywords:
            if keyword.startswith('|!'):
                if keyword[2:] in content_text:
                    return True
    return False


# def _checkGHUrl(url: str, code_id: int, answer_id: int = 0):
#     _gh,_ = GHResult.objects.get_or_create(
#         answer_id=answer_id,
#         ghUrl=url
#     )
def _checkGHUrl(gResult, keywords: list = None):
    try:
        # load content
        req = requests.get(gResult.ghUrl)
        # remove comments from content
        content = comment_remover(req.text.replace(" ", ""))
        #print(content)

        # load keywords
        if keywords is None:
            code = Code.objects.filter(id=gResult.code_id).first()
            keywords = extract_from_description(code.description)

        # check keywords for file
        if contain_keywords(content, keywords):
            print("YESS", gResult.id, gResult.code_id, gResult.answer_id)
            # save it to the DB
            gResult.is_vulnerable = True
            gResult.is_checked    = True
            gResult.save()
        else:
            print("NOOO", gResult.code_id, gResult.answer_id)
            gResult.is_vulnerable = False
            gResult.is_checked = True
            gResult.save()
        return True
    except Exception as e:
        # open('/home/ali/error_connection_report','a').write("Exception: {}\n"
        #                                                     "Answer Link: {}\n"
        #                                                     "CodeID: {}\n\n".format(e,answer_id,code_id))
        gResult.is_error = True
        gResult.report = "{}".format(e)
        gResult.save()
        return False

def _goCheckRepos():
    __denied_tags = [36, 40, 39]
    _VALID_EXTENSIONS = ['.cpp', '.hpp', '.cc', '.h', '.cu', '.re2c']
    _all = GHResult.objects.exclude(code__codetags__tag_id__in=__denied_tags).filter(is_checked=False)
    for gh in _all:
        for extension in _VALID_EXTENSIONS:
            if gh.ghUrl.lower().endswith(extension):
                with_same_answer_id = GHResult.objects\
                    .filter(answer_id=gh.answer_id)\
                    .filter(ghUrl=gh.ghUrl)
                # check to has a vulnerable with this answer_id or not
                _ = with_same_answer_id.filter(is_vulnerable=True)
                if _.count() == 0:
                    _checkGHUrl(gh)
                else:
                    with_same_answer_id.filter(is_vulnerable=False).update(report="Refer to AnswerID ({}) with ID : {}".format(_.first().answer_id,_.first().id))

                break
    return True # =)

def _goResetRepos():
    _all = GHResult.objects.all().update(
        is_checked = False,
        is_vulnerable = False,
        is_error = False,
        report = "",
    )
    return True # =)

def _COPY_FROM_GHRESULT_TO_GURESULT_LASTVERSIONS():
    __tags = [
        2 , # last version vulnerable
    ]
    _VALID_EXTENSIONS = ['.cpp','.hpp','.cc','.h','.cu','.re2c']
    _ = GHResult.objects.all()
    for ghU in _:
        if Code.objects.filter(id=ghU.code.id).filter(codetags__tag_id__in=__tags).exists():
            # Just valid extensions added to list
            for extension in _VALID_EXTENSIONS:
                if ghU.ghUrl.lower().endswith(extension):
                    # add to GHResult_LastVersions
                    GHResult_LastVersions.objects.create(
                        answer_id=ghU.answer_id,
                        code=ghU.code,
                        ghUrl=ghU.ghUrl
                    )
                    break
    return True # =)

def _goCheckLastVersions():
    _all = GHResult_LastVersions.objects.all()
    for gh in  _all:
        _checkGHUrl(gh)
    return True # =)