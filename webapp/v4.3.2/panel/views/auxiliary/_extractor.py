
EXTRACT_TYPES = [
    ['explain'],
    ['keywords', 'keyword'],
    ['mitigation'],
    ['references'],
]
SECTION_SIGN = "####"


class Sections:
    EXPLAIN = DESCRIPTION = EXTRACT_TYPES[0][0]
    KEYWORDS = EXTRACT_TYPES[1][0]
    MITIGATION = EXTRACT_TYPES[2][0]
    REFERENCES = EXTRACT_TYPES[3][0]


def __exists_type(type: str):
    _ = 0
    for a_type in EXTRACT_TYPES:
        if type in a_type:
            return [True, _]
        _ += 1
    return [False, -1]


def extract_from_description(content: str, section: str = 'keywords', with_space: bool = False):
    _find = __exists_type(section.lower())
    if not _find[0]:
        return None

    cont = content
    # split by line
    lines = cont.split('\n')
    result = []
    _yes = False
    for line in lines:
        if SECTION_SIGN in line:
            _yes = False
            section = line.split(SECTION_SIGN)[-1].lower().strip()
            if section in EXTRACT_TYPES[_find[1]]:
                _yes = True
        else:
            if _yes and len(line.strip()) > 0:
                if with_space:
                    result.append(line.strip())
                else:
                    result.append(line.strip().replace(" ", ""))
    return result