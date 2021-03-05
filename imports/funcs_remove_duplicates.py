def remove_duplciates(arr):
    tracker = []
    new_arr = []
    for index, line in enumerate(arr):
        [frequency, korean, pos, hanja, hint, go_level, topik_level] = line
        if (korean, pos) not in tracker:
            new_arr.append([frequency, korean, pos, hanja, hint, go_level, topik_level])
            tracker.append((korean,pos))
    return new_arr