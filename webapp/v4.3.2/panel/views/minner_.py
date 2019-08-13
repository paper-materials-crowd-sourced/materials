from django.http import HttpResponse
from panel.models import Code
from panel.views.auxiliary._extractor import extract_from_description


def _extract_from_code(request, id, extract_type):
    vulnerable_code = Code.objects.filter(is_vulnerable=True).filter(id=id).first()

    if vulnerable_code is None:
        return HttpResponse("", status=404)

    result = extract_from_description(vulnerable_code.description, extract_type)
    if result is None:
        return HttpResponse(
            "'{}' type not exists. (valid types: explain, keywords, mitigation, references)".format(extract_type),
            status=406)

    return HttpResponse(result)
