from imports.dicts_conversions import pos_conversions, anomalies_conversions
from imports.lists import khen_targets
from imports.funcs_khen import detect_khen, transfer_khen
from imports.funcs_converters import line_string_to_line_array

spacer = ''

def go_fragmentize_sanitize(line_string):
    [go_frequency, go_korean, go_pos, go_hanja, go_level] = line_string_to_line_array(line_string)
    go_pos = pos_conversions[go_pos]
    go_hanja_language = detect_khen(go_hanja)
    go_hint = spacer
    if go_hanja in anomalies_conversions:
        go_hanja = anomalies_conversions[go_hanja]
    if go_hanja and detect_khen(go_hanja) in khen_targets:
        [new_hanja, transfer] = transfer_khen(go_hanja, go_hanja_language)
        go_hanja = new_hanja
        go_hint = transfer
    return [go_frequency, go_korean, go_pos, go_hanja, go_hint, go_level, spacer]


def topik_fragmentize_sanitize(line):
    [topik_level, topik_korean, topik_hint, topik_pos] = line_string_to_line_array(line) 
    topik_pos = pos_conversions[topik_pos] 
    topik_frequency = spacer
    topik_hanja = spacer
    go_level = spacer
    if topik_hint in anomalies_conversions:
        topik_hint = anomalies_conversions[topik_hint]
    return [topik_frequency, topik_korean, topik_pos, topik_hanja, topik_hint, spacer, topik_level]