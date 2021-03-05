from re import sub, search, compile, findall

def split_en_han(text):
    en = ''.join(findall("[a-zA-Z]", text))
    han_dashed = sub(en, '-', text)
    return han_dashed

def split_han_ko(text):
    regex = compile("(?<=[\u4e00-\u9FFF])[. ]{1,2}(?=[~\uac00-\ud7a3])")
    return regex.split(text)

def split_han_num(text):
    regex = compile("(?<=[\u4e00-\u9FFF])[. ]{1,2}(?=[0-9])")
    return regex.split(text)

def detect_khen(text):
    # korean
    grid = []
    if search("[\uac00-\ud7a3]", text):
        grid.append('ko')
    # chinese
    if search("[\u4e00-\u9FFF]", text):
        grid.append('han')
    # english
    if search("[a-zA-Z]", text):
        grid.append('en')
    # numbers
    if search("[0-9]", text):
        grid.append('num')
    return ('/' if len(grid) >  1 else '').join(grid)

def transfer_khen(text, language):
    transfer = ''
    new_text = text
    if language in ['ko', 'en', 'ko/en', 'ko/num']:
        transfer = new_text
        new_text = ''
    elif language == 'han/en':
        new_text = split_en_han(new_text)
    elif language in ['ko/han', 'ko/han/num']:
        [han, ko] = split_han_ko(new_text)
        transfer = ko
        new_text = han
    elif language == 'han/num':
        [han, num] = split_han_num(new_text)
        transfer = num
        new_text = han
    return [new_text, transfer]
