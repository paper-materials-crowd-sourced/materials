import json
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from panel.models import Code, Tag, Code_Answer, GHResult, CodeTags, GHResult_LastVersions
from panel.views.github._base import _checkGHUrl
from panel.views.github._helpers import _getGHReferencesFromJSON


@login_required(login_url="/admin/login")
@require_http_methods(['GET'])
def list_tags(request):
    OUT = []
    for tag in Tag.objects.all():
        OUT.append({
            "id" : tag.id,
            "name" : tag.name
        })
    return HttpResponse(json.dumps(OUT),content_type="application/json")

@login_required(login_url="/admin/login")
@csrf_exempt
@require_http_methods(['POST'])
def add_tag(request):
    # if request.is_ajax():
        try:
            if request.body.decode('utf-8'):
                tag_name = json.loads(request.body.decode('utf-8'))
                tag = Tag.objects.get_or_create(name=str(tag_name.get('tag',None)).lower())[0]
                return HttpResponse(json.dumps({
                    "id": tag.id,
                    "name": tag.name,
                }),content_type="application/json")

            return HttpResponse("failed")
        except Exception as e:
            print(e)

@login_required(login_url="/admin/login")
@require_http_methods(['GET'])
def answer_code_ids(request,answer_id):
    codes = Code.objects.filter(code_answer__answer_id=answer_id).filter(is_vulnerable=True)
    code_ids = []
    for code in codes:
        code_ids.append(code.id)
    return HttpResponse(json.dumps(code_ids))

def add_answer_id(request):
    BASE_PATH = os.path.join(settings.BASE_DIR, "code_snippets_metadata")
    try:
        # for snippet_code in [Code.objects.get(pk=336)]:
        for snippet_code in Code.objects.all():
            with open(os.path.join(BASE_PATH, "{}.json".format(snippet_code.id)), 'r') as file:
                data = json.load(file)
            answers = data.get('answers')

            for answer in answers:
                snippet_code.code_answer_set.create(
                    answer_id = answer.get('answerid',None),
                    question_id = answer.get('questionid',None),
                )
        return HttpResponse("Done")
    except Exception as e:
        print(e)
    return HttpResponse("No response")


def add(request):

    BASE_PATH = os.path.join(settings.BASE_DIR,"code_snippets_metadata")
    try:
        for order_id in range(1,2057):
            with open(os.path.join(BASE_PATH,"{}.json".format(order_id)) , 'r') as file:
                data  = json.load(file)
                snippet_code = ""
                with open(os.path.join(BASE_PATH, "{}.cpp".format(order_id)), encoding="utf8", errors='ignore', mode='r') as code:
                    snippet_code = code.read()
                filename = "{}.cpp".format(order_id)
                group_id = data.get('group_id',None)

                CODE = Code.objects.create(
                    filename = filename,
                    group_id = group_id,
                    snipped_code = snippet_code
                )
                for answer in data.get('answers', []):
                    CODE.sourl_set.create(
                        url=answer.get('sourl', None)
                    )

        return HttpResponse("Done")
    except Exception as e:
        print(e)
    return HttpResponse("No response")

def answer_downgrade(request, answer_id):
    code_answers = Code_Answer.objects.filter(answer_id=answer_id)
    for code_answer in code_answers:
        code_answer.code.is_vulnerable = True
        code_answer.code.save()
    return HttpResponse("All of Code snippet set Vulnerable")

def add_template_to_description(request):
    # code_answers = Code_Answer.objects.filter(answer_id=148766)
    code_answers = Code_Answer.objects.filter(is_done=False)
    for code_answer in code_answers:
        code_answer.code.description += "\n" \
                                        "#### Explain\n\n" \
                                        "#### Keywords\n\n" \
                                        "#### Mitigation\n\n" \
                                        "#### References\n\n"
        code_answer.code.save()
    return HttpResponse("Done")

def test(request, tgid = 0):

    gh = GHResult.objects.filter(code__codetags__tag_id=tgid)
    ghv = gh.filter(is_vulnerable=True)
    tg = Tag.objects.filter(id=tgid).first()
    return HttpResponse("{} Count : {} ({})".format(tg.name, gh.count(), ghv.count()))

    # code_snippets = Code.objects.filter(is_vulnerable=True)
    #
    # name_s = [code.filename+", " for code in code_snippets]
    # return HttpResponse(name_s)

    # print(len(_getGHReferencesFromJSON(36)))
    # # Give Number of Tags for each Answer
    # __ignored_tag_ids = [
    #     39,  # not a security vuln
    #     # 36,  # unsearchabe in github
    #     10,  # unreadable
    #     3 ,  # last version
    #     2 ,  # last version vulnerable
    # ]
    # result = CodeTags.objects\
    #     .filter(code__is_vulnerable=True)\
    #     .exclude(code__codetags__tag_id__in=__ignored_tag_ids)\
    #     .values('answer_id')\
    #     .annotate(counts=Count('answer_id'))
    #
    # return HttpResponse(result)

    # links = {
    #     840:[
    #         'https://raw.githubusercontent.com/AlexMcGilvray/FightingGameStudyLog/master/FighterInterface/Utilities.cpp',
    #         'https://raw.githubusercontent.com/perwin/imfit/master/core/utilities.cpp',
    #         '"https://raw.githubusercontent.com/trodevel/utils/master/vformat.h',
    #     ],
    # }
    # for _k in links.keys():
    #     print(_k,links[_k])
    #     for _ in links[_k]:
    #         _checkGHUrl(_,_k)
    # return HttpResponse("Done")

    # i = CodeTags.objects.filter(tag_id=37)
    # for _ in i:
    #     for __ in Code_Answer.objects.filter(code_id=_.code_id):
    #         print(__.answer_id)
    #
    # return HttpResponse(i)