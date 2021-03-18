from re import sub, findall, search, compile, match
from imports.funcs_khen import detect_khen
import csv
import os

#############################################################
# Will make DRY later after analyzing data README completed #
#############################################################

def regenerate(arr):
    new_arr = arr
    for index, line in enumerate(arr):
        [frequency,	korean, pos, hanja, hint, go_level, topik_level] = line

        koreanRegex = compile('.*다[0-9]{0,}$')
        hintRegex = compile('.*다$')
        hsRegex = compile('^[\uac00-\ud7a3]{1,}다$')

        leads = ('가', '에', '이', '을', '를', '로', '으로', '에서', '에게', '과', '께', '도', '만', '와', '의', '처럼', '이나', '까지')
        leads_regex = compile(f"^[{('|' if len(leads) > 1 else '').join(leads)}]{{1,2}} .*[다(.*)]{{1,5}}$") # '가 튼튼하다'  or '가 튼튼하다(ㅇㅇ)' 
        ends = ('에', '이', '가','를', '을', '에서', '으로', '께', '와', '처럼', '과', '에게', '하고', '쯤', '의')
        vocabulary_categories = ('병원', '방법', '방향', '행정 구역','고적', '가구', '나라', '숫자', '직업', '신체', '계절', '색깔', '과일', '채소', '가족', '동물', '곤충', '친척', '지명', '음식', '달(월)', '요일', '신체의 일부', '신체의 일부', '시간', '식물', '꽃')
        pos_categories = ('감탄사', '관형사', '줄어든 말', '의존명사', '대명사', '부사')
        ends_regex = compile(f".*[{('|' if len(leads) > 1 else '').join(ends)}]$")
        exceptions = []

        if hint: # 1. No blank hints
            if not search('[~\'&]', hint): # No hints with −
                if not (detect_khen(hint) == 'en' or detect_khen(hint) == 'ko/num'): # No english or korean / numbers
                    if not search(''.join(findall("[\uac00-\ud7a3]", korean)), hint): # No korean that can found in its hints
                        if hint not in vocabulary_categories: # No hints that are categories
                            if not any(x in pos.split('/') for x in pos_categories): # No pos that fall pos category
                                if not search(''.join(findall("[\uac00-\ud7a3]", hint)), korean): # no hints that can be found in korean
                                    if not ((match('.*다$', ''.join(findall("[\uac00-\ud7a3]", korean))) and match('.*다$', hint) and not match(leads_regex, hint))): # no 다  ends in both hint and korean
                                        if not (match(".*(?=[\uac00-\ud7a3][다])", korean) and len(match(".*(?=[\uac00-\ud7a3][다])", korean).group()) > 0 and search(match(".*(?=[\uac00-\ud7a3][다])", korean).group(), hint)):
                                            if match(leads_regex, hint) :
                                                hint = f"~{hint}"
                                                new_arr[index] = [frequency, korean, pos, hanja, hint, go_level, topik_level]
                                            elif match(ends_regex, hint) and hint not in ('애호가', '시간의 길이', '사이', '아이', '요 사이'):
                                                hint = f"{hint} ~"
                                                new_arr[index] = [frequency, korean, pos, hanja, hint, go_level, topik_level]
                                            elif not findall("[\uac00-\ud7a3]", korean)[len(findall("[\uac00-\ud7a3]", korean))-1] == hint[len(hint)-1]:
                                                if match(compile('의 .*'), hint) or hint in ['받다', '지키다']:
                                                    hint = f"~{hint}"
                                                    new_arr[index] = [frequency, korean, pos, hanja, hint, go_level, topik_level]
                                                elif hint in ('어색한', '오래', '맛'):
                                                    hint = f"{hint} ~"
                                                    new_arr[index] = [frequency, korean, pos, hanja, hint, go_level, topik_level]
    return new_arr

# experimental

def regenerate_2(candidate_arr, ref_arr):
    new_arr = []
    for index_r, r_data in enumerate(ref_arr):
        [cheese_korean, cheese_number, cheese_type, cheese_pos, cheese_origin, cheese_pronunciation, cheese_level, cheese_hint, cheese_eng_simp, cheese_eng_complex] = r_data
        if index_r % 1000 == 0:
            print(f"{round(index_r/len(ref_arr)*100, 2)}%")
        if cheese_type == '단어':
            for index, c_data in enumerate(candidate_arr):
                [go_frequency, go_korean, go_pos, go_hanja, go_hint, go_level, go_english] = c_data
                if ''.join(findall("[\uac00-\ud7a3]", go_korean)) == ''.join(findall("[\uac00-\ud7a3]", cheese_korean)) and r_data not in new_arr:
                    new_arr.append(r_data)
    return new_arr