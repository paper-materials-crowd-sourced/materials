import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from panel.models import Code, CodeTags, Tag, Code_Answer


@login_required(login_url="/admin/login")
@csrf_exempt
@require_http_methods(['GET'])
def code_tags(request, code_id):
    codeTags = CodeTags.objects.filter(code_id=code_id)
    OUT = []
    for tag in codeTags:
        OUT.append(tag.tag.id)

    return HttpResponse(json.dumps(OUT),content_type="application/json")


@login_required(login_url="/admin/login")
@csrf_exempt
@require_http_methods(['POST'])
def update_vuln(request, code_id):
    if request.is_ajax():
        code = get_object_or_404(Code,pk=code_id)
        is_vuln = json.loads(request.POST.get('is_vulnerable',None))
        if (is_vuln is None) or (not isinstance(is_vuln,bool)):
            return HttpResponse('not changed',status=400)
        code.is_vulnerable = is_vuln
        code.save()
        return HttpResponse("Changed",status=200)

@login_required(login_url="/admin/login")
@csrf_exempt
@require_http_methods(['POST'])
def update_des(request, code_id):
    code = get_object_or_404(Code,pk=code_id)
    if request.body.decode('utf-8'):
        data = json.loads(request.body.decode('utf-8'))

        # description
        newDescription = (data.get('description',code.description))
        code.description = newDescription
        code.save()

        # tags
        # delete before tags !
        CodeTags.objects.filter(code_id=code_id).delete()

        # add new tags
        tag_ids = data.get('tag_ids',[])
        for tag_id in tag_ids:
            code.codetags_set.create(
                tag_id=tag_id
            )

        return HttpResponse(json.dumps({
            "message":"success"
        }),status=200,content_type="application/json")

@login_required(login_url="/admin/login")
@csrf_exempt
@require_http_methods(['POST'])
def answer_done(request, answer_id):
    if request.is_ajax():
        # crazy method !
        code_answers = (Code_Answer.objects.filter(answer_id = answer_id))
        is_done = json.loads(request.POST.get('is_done',None))
        if (is_done is None) or (not isinstance(is_done,bool)):
            return HttpResponse('not changed',status=400)
        for code_answer in code_answers:
            code_answer.is_done= is_done
            code_answer.save()
        return HttpResponse("Changed",status=200)