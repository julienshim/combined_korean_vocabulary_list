from re import search, findall

def remove_duplciates(arr):
    tracker = []
    new_arr = []
    exceptions = []
    gy_ms = []
    for index, line in enumerate(arr):
        [frequency_prev, korean_prev, pos_prev, hanja_prev, hint_prev, go_level_prev, topik_level_prev] = arr[index-1]
        [frequency, korean, pos, hanja, hint, go_level, topik_level] = line
        if index + 1 < len(arr):
            [frequency_next, korean_next, pos_next, hanja_next, hint_next, go_level_next, topik_level_next] = arr[index+1]
            if frequency: # has no effect in filtering but just in case
                new_arr.append([frequency, korean, pos, hanja, hint, go_level, topik_level])
                tracker.append((korean,pos))
            else:
                if len(pos.split("/")) > 1:
                    pos_check = search(pos_next, pos)
                    if korean == korean_next and pos_check is None:
                        multi_compare = [(korean, x) for x in pos.split("/") if (korean, x)  in tracker]
                        if len([x for x in multi_compare if x in tracker]) == 0:
                            new_arr.append([frequency, korean, pos, hanja, hint, go_level, topik_level])
                elif korean == korean_next and search(pos_next, pos):
                    # we know this is '고궁' hint only
                    if not (korean_prev == ''.join(findall("[\uac00-\ud7a3]", korean)) and pos_prev == '고유 명사'):
                        new_arr.append([frequency, korean, pos, hanja, hint, go_level, topik_level])
                        tracker.append((korean,pos))
                        exceptions.append(korean)
                elif (korean, pos) not in tracker and korean not in exceptions:
                    if not (korean_prev == ''.join(findall("[\uac00-\ud7a3]", korean)) and pos_prev == '고유 명사'):
                        new_arr.append([frequency, korean, pos, hanja, hint, go_level, topik_level])
                        tracker.append((korean,pos))
    return new_arr
