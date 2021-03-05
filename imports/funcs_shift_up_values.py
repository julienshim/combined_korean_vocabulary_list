def shift_up_values(arr):
    processed_arr = arr
    for index, line in enumerate(processed_arr):
        if index + 1 < len(processed_arr):
            [frequency, korean, pos, hanja, hint, go_level, topik_level] = line
            [frequency_next, korean_next, pos_next, hanja_next, hint_next, go_level_next, topik_level_next] = processed_arr[index+1]
            if frequency and not frequency_next and korean == korean_next and pos in pos_next.split('/'):
                pos = pos_next if pos in pos_next.split('/') else pos
                hint = hint_next if not hint else hint
                topik_level = topik_level_next if not topik_level else topik_level
                processed_arr[index] = [frequency, korean, pos, hanja, hint, go_level, topik_level]
    return processed_arr