from random import randint, shuffle
from panel.models import GHResult_KeywordMeter

CPP_KEYWORD_RESERVED = [
'alignas',
'alignof',
'and',
'and_eq',
'asm',
'atomic_cancel',
'atomic_commit',
'atomic_noexcept',
'auto',
'bitand',
'bitor',
'bool',
'break',
'case',
'catch',
'char',
'char8_t',
'char16_t',
'char32_t',
'class',
'compl',
'concept',
'const',
'consteval',
'constexpr',
'const_cast',
'continue',
'co_await',
'co_return',
'co_yield',
'decltype',
'default',
'delete',
'do',
'double',
'dynamic_cast',
'else',
'enum',
'explicit',
'export',
'extern',
'false',
'float',
'for',
'friend',
'goto',
'if',
'inline',
'int',
'long',
'mutable',
'namespace',
'new',
'noexcept',
'not',
'not_eq',
'nullptr',
'operator',
'or',
'or_eq',
'private',
'protected',
'public',
'reflexpr',
'register',
'reinterpret_cast',
'requires',
'return',
'short',
'signed',
'sizeof',
'static',
'static_assert',
'static_cast',
'struct',
'switch',
'synchronized',
'template',
'this',
'thread_local',
'throw',
'true',
'try',
'typedef',
'typeid',
'typename',
'union',
'unsigned',
'using',
'virtual',
'void',
'volatile',
'wchar_t',
'while',
'xor',
'xor_eq ',
'override',
'final',
'audit',
'axiom',
'import',
'module',
'transaction_safe',
'transaction_safe_dynamic ',
'if',
'elif',
'else',
'endif',
'ifdef',
'ifndef',
'define',
'undef',
'include',
'line',
'error',
'pragma',
'defined',
'__has_include',
'__has_cpp_attribute ',
'_Pragma',
'string',
'std',
]


def delete_table():
    GHResult_KeywordMeter.objects.all().delete()


def extract_tokens(tokens: list, size: int, min_len: int = 3, shuffling: bool = False):
    temporary_tokens = []

    # clean tokens
    for token in tokens:
        if len(token) >= min_len:
            temporary_tokens.append(token)

    # random choices
    final_tokens, counter = {}, 0
    while True:
        # choice a number
        random_number = randint(0, len(temporary_tokens) - 1)

        # check the token is a keyword reserved in c++ or not
        token = temporary_tokens[random_number]
        if token in CPP_KEYWORD_RESERVED:
            continue

        choose_token = "!{}".format(token)
        if choose_token not in final_tokens:
            counter += 1
            final_tokens[random_number] = choose_token

        if counter == size:
            break

    # ordering tokens
    keys = list(final_tokens.keys())
    keys.sort()

    # generate output

    final_output = [final_tokens[key] for key in keys]

    if shuffling:
        shuffle(final_output)

    return final_output
