import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import Length
from django.http import HttpResponse, Http404
from django.shortcuts import render
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from panel.models import Code, Code_Answer, CodeTags, GHResult_LastVersions
from panel.views.auxiliary._extractor import extract_from_description, Sections


def index(request):
    # return HttpResponseRedirect("/admin")
    return render(request, "index.html")


def show(request, id):
    code = Code.objects.filter(id=id).first()
    if code:
        return render(request, "cpp.html", {
            "filename": code.filename,
            "code": code.snipped_code
        })
    return HttpResponse("Not found")


@login_required(login_url="/admin/login")
def code_answers_list(request):
    Answers = Code_Answer.objects \
        .filter(code__is_vulnerable=True) \
        .values('answer_id', 'is_done').annotate(counts=Count('answer_id'))

    done_ = len(Code_Answer.objects \
                .filter(code__is_vulnerable=True) \
                .filter(is_done=True) \
                .values('answer_id', 'is_done').annotate(counts=Count('answer_id')))
    paginate = Paginator(Answers, 20)
    page = request.GET.get('page')

    answers = paginate.get_page(page)
    return render(request, "answers_list.html", {
        "answers": answers,
        "all_": Answers.count(),
        "done_": done_
    })


@login_required(login_url="/admin/login")
def code_answers(request, answer_id):
    codes = Code.objects.filter(code_answer__answer_id=answer_id).filter(is_vulnerable=True)
    if not codes:
        raise Http404
    return render(request, "CodesOfAnswer.html", {
        "answer_id": answer_id,
        "codes": codes,
    })


@login_required(login_url="/admin/login")
def tgs(request):
    __ignored_tag_ids = [
        39,  # not a security vuln
        # 36,  # unsearchabe in github
        10,  # unreadable
        3,  # last version
        2,  # last version vulnerable
    ]

    TagedCodes = CodeTags.objects
    if request.GET.get('result', None) != 'all':
        TagedCodes = TagedCodes.exclude(code__codetags__tag_id__in=__ignored_tag_ids)

    TagedCodes = TagedCodes.filter(code__is_vulnerable=True) \
        .values('tag_id', 'tag__name') \
        .annotate(counts=Count('tag_id'))

    ca = Code_Answer.objects \
        .filter(code__is_vulnerable=True) \
        .values('answer_id') \
        .annotate(counts=Count('answer_id'))

    # Count Number of each Tag
    __tc_count = {}
    for tc in TagedCodes:
        __tc_count[tc.get('tag_id', None)] = ca.filter(code__codetags__tag_id=tc.get('tag_id', None)).count()

    paginate = Paginator(TagedCodes, 40)
    page = request.GET.get('page')

    tags = paginate.get_page(page)
    return render(request, "tags/tag_list.html", {
        "TagedCodes": tags,
        "tag_counts": __tc_count
    })


@login_required(login_url="/admin/login")
def tg_codes(request, tag_id):
    answers = Code_Answer.objects \
        .filter(code__codetags__tag_id=tag_id) \
        .filter(code__is_vulnerable=True) \
        .values('answer_id') \
        .annotate(counts=Count('answer_id'))
    if not answers:
        raise Http404

    return render(request, "tags/answers_of_tag.html", {
        # "tag_id" : tag_id,
        "answers": answers,
    })


@login_required(login_url="/admin/login")
def FindCategoreis(request):
    '''
        Find 3 Categories:
         1. Vulnerabelity in (LastVersion and History)
         2. Vulnerabelity Just in (LastVersion)
         3. Vulnerabelity Just in (History)
    :param request:
    :return: Array of IDs [[Categorie 1], [Categorie 2], [Categorie 3]]
    '''

    _LAST_VERSION_TAG_ID = 2
    # 2 (LastVersion)
    JustLastVersion = Code_Answer.objects \
        .filter(code__is_vulnerable=True) \
        .filter(code__codetags__tag_id=_LAST_VERSION_TAG_ID) \
        .values('answer_id') \
        .annotate(counts=Count('answer_id'))

    _justLastVersion = []
    for _ in JustLastVersion:
        code_answers = Code_Answer.objects.filter(answer_id=_['answer_id']).filter(code__is_vulnerable=True)
        print(code_answers)
        _l, _h = False, False
        # check lastversion
        for code in code_answers:
            if Code.objects. \
                    filter(id=code.code_id). \
                    filter(codetags__tag_id=_LAST_VERSION_TAG_ID). \
                    exists():
                _l = True
            # check others
            __ignored_tag_ids = [
                39,  # not a security vuln
                36,  # unsearchabe in github
                10,  # unreadable
                3,  # last version
                2,  # last version vulnerable
            ]
            for code in code_answers:
                if Code.objects. \
                        filter(id=code.code_id). \
                        exclude(codetags__tag_id__in=__ignored_tag_ids). \
                        exists():
                    _h = True

        if _l and not _h:
            _justLastVersion.append(_['answer_id'])

    print(_justLastVersion)

    # 3 (Histroy)
    JustHistory = Code_Answer.objects \
        .exclude(code__codetags__tag_id=_LAST_VERSION_TAG_ID) \
        .filter(code__is_vulnerable=True) \
        .values('answer_id') \
        .annotate(counts=Count('answer_id'))
    _justHistory = []
    for _ in JustHistory:
        code_answers = Code_Answer.objects.filter(answer_id=_['answer_id']).filter(code__is_vulnerable=True)
        # print(code_answers)
        _h = True
        # check others
        __ignored_tag_ids = [
            39,  # not a security vuln
            36,  # unsearchabe in github
            10,  # unreadable
            3,  # last version
            2,  # last version vulnerable
        ]
        for code in code_answers:
            if Code.objects. \
                    filter(id=code.code_id). \
                    filter(codetags__tag_id__in=__ignored_tag_ids). \
                    exists():
                _h = False

        if _h:
            _justHistory.append(_['answer_id'])

    # print(_justHistory)

    # 1 (History and LastVersion)
    Both = Code_Answer.objects \
        .filter(code__is_vulnerable=True) \
        .values('answer_id') \
        .annotate(counts=Count('answer_id'))

    _both = []
    for _ in Both:
        if _['counts'] >= 2:

            code_answers = Code_Answer.objects.filter(answer_id=_['answer_id']).filter(code__is_vulnerable=True)

            l, h = False, False
            # check lastversion
            for code in code_answers:
                if Code.objects. \
                        filter(id=code.code_id). \
                        filter(codetags__tag_id=_LAST_VERSION_TAG_ID). \
                        exists():
                    l = True
            # check others
            __ignored_tag_ids = [
                39,  # not a security vuln
                36,  # unsearchabe in github
                10,  # unreadable
                3,  # last version
                2,  # last version vulnerable
            ]
            for code in code_answers:
                if Code.objects. \
                        filter(id=code.code_id). \
                        exclude(codetags__tag_id__in=__ignored_tag_ids). \
                        exists():
                    h = True

            if l and h:
                _both.append(_['answer_id'])

    finded = "64166, 236180, 236803, 478960, 900035, 1056424, 1911863, 3301284, 3520427, 4049562, 4119881, 4156038, 4505166, 5097100, 6925201, 6943003, 7413516, 7725289, 8098080, 8362718, 8545389, 8969776, 9212542, 9676623, 9764508, 10050258, 11093644, 11417774, 12468109, 16358264, 16859693, 19102250, 20447331, 21653558, 21767578, 25360996, 27928463, 28471421, 34571089, 35585744, 41031865, 46050762, 265978, 446327, 447307, 933996, 2466264, 4654718, 5056797, 5665377, 6089413, 6930407, 17708801, 27652012, 28172162, 28413370, 29988626, 42341811, 69911, 440240, 2654860, 3487062, 4152881, 5989676, 6417908, 8391601, 12413298, 40577390"
    finded = finded.replace(" ", "").strip().split(",")

    ca = Code_Answer.objects \
        .filter(code__is_vulnerable=True) \
        .values('answer_id') \
        .annotate(counts=Count('answer_id'))

    for i in ca:
        if str(i['answer_id']) not in finded:
            print(i['answer_id'])

    return render(request, '3Categories.html', {
        'LastVersions': _justLastVersion,
        'Histories': _justHistory,
        'Both': _both
    })


def CodeSnippetsWithDescriptionHigherThan50Chars(request, min: str):
    if not min.isdigit():
        return HttpResponse(":|")
    min = int(min)
    if min < 0:
        return HttpResponse(":|:|")

    code_s = Code.objects \
        .filter(is_vulnerable=False) \
        .annotate(text_len=Length('description')) \
        .filter(text_len__gt=min)

    return render(request, "CheckAnswersHigherThan50/CodesOfAnswer.html", {
        "codes": code_s,
    })


class IssueResult(View):

    def extract_section(self, code: Code, section):
        return '\n'.join(extract_from_description(code.description, section=section, with_space=True))

    def generate_response(self, gh: GHResult_LastVersions):
        return {
            'id': gh.id,
            'repo_name': gh.repo_name,
            'github_link': gh.ghUrl,
            'so_link': [so_url.url for so_url in gh.code.sourl_set.all()],
            'vulndetails': {
                'description': self.extract_section(gh.code, section=Sections.DESCRIPTION),
                'mitigations': self.extract_section(gh.code, section=Sections.MITIGATION),
                'references': self.extract_section(gh.code, section=Sections.REFERENCES)
            }
        }

    @method_decorator(login_required)
    def get(self, request):
        response = []

        # step 1. get github results
        github_results = GHResult_LastVersions.objects.filter(is_vulnerable=True)

        # step 2. create response
        for idx, github in enumerate(github_results):
            response.append(self.generate_response(github))
            if len(self.extract_section(github.code, section=Sections.REFERENCES)) > 0:
                print(idx)
        return HttpResponse(json.dumps(response), content_type='application/json')

