import re


def split_text(text, split_types):
    patterns = {
        "hanja": r"[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF]+",
        "english": r"[a-zA-Z]+",
        "korean": r"[\uAC00-\uD7A3\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uD7B0-\uD7FF]+",
    }

    combined_pattern = "|".join(f"(?P<{type}>{patterns[type]})" for type in split_types)

    matches = re.finditer(combined_pattern, text)
    result = {type: "" for type in split_types}

    for match in matches:
        for type in split_types:
            if match.group(type):
                result[type] += match.group(type)

    return result


import re


def detect_languages(text, languages_to_detect):
    patterns = {
        "hanja": r"[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF]",
        "english": r"[a-zA-Z]",
        "korean": r"[\uAC00-\uD7A3\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uD7B0-\uD7FF]",
    }

    result = {}
    for lang in languages_to_detect:
        if lang in patterns:
            result[lang] = bool(re.search(patterns[lang], text))
        else:
            result[lang] = False  # Language not supported

    return result
