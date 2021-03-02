# Vocabulary List for Korean Learning

A programatically-combined vocabulary list for learning Korean via Python 3, outputting in TSV (tab-serparated values) format for future database purposes.

## Original Sources

국립국어원 - The National Institute of the Korean Language
* [한국어 학습용 어휘 목록.xls (2003)](https://www.korean.go.kr/front/etcData/etcDataView.do?mn_id=46&etc_seq=71)

TOPIK 한국어능력시험 - Test of Proficiency in Korean
* [토픽 어휘 목록_공개 목록.xlsx (2015)](https://www.topik.go.kr/usr/cmm/subLocation.do?menuSeq=2110503&boardSeq=64217)

## Keys

* GO - The National Institute of the Korean Language, due to the site being run by the Korean government.
* en - English
* ko - Korean
* han - Hanja
* &일 - Korean term dervied from 일본어 (Japanese language)
* &프 - Korean term dervied from 프랑스어 (French language)
* &독 - Korean term derived from 독일어 (German language)
* &중 - Korean term derived from 중국어 (Chinese language)
* &이 - Korean term dericed from 이탈리아어 (Italian language)

## Decisions

### Headers

GO headers:
* `순위` (ranking) - in terms of frequency
* `단어` (word)	- Korean vocabulary word
* `품사` (part of speech)
* `풀이` (explanation) - hints
* `등급` (level) - A, B, C (basic to advanced)

TOPIK headers:
* `수준` (level) - TOPIK has two examination levels. TOPIK I, marked as `초급` on the spreadsheet, for the basic level, and TOPIK II, marked as `중급` on the spread sheet, which can be more accurately described as "from intermediate and on" since this examination combins the intermediate and advanced levels.
* `어휘` (vocabulary) - Korean vocabulary word
* `길잡이말` (guide words) - hints
* `품사` (part of speech)

Combined headers
* `frequency` - usage frequency rank
* `korean` - Korean vocabulary word
* `pos` - part of speech
* `hanja` - Hanja only
* `hint` - Korean and/or English ok
* `go_level` - chose to separate for future database purposes
* `topik_level` - chose to separate for future database purposes

### Format
 Convert to TSV prior to reading files

### Hanja (traditional Chinese characters), Korean, English

Type 1: <ampersand><ko><en>\
Example: `&일ramen`\
Decision: Move from the `hanja` column to the `hints` column.

| Hanja      | Hint |
| ----------- | ----------- |
|       | `&일ramen`       |


Type 2: <en><han> or <han><en>\
Examples: `golf場`, `市內bus`\
Decision: The `en` porition doesn't provide any value. Replace the `en` portion with a `-`.

| Hanja      | Hint |
| ----------- | ----------- |
| `-場`      |        |
| `市內-`   |         |

Type 3: <han><period><ko>
Example: `間. 서울과 부산`, \
Decision: Split at `. `. Move the `num` portion to the `hints` column.

| Hanja      | Hint |
| ----------- | ----------- |
| `間`      | `서울과 부산`       |

Type 4: <han><period><num>
Example: `等. 1~`
Decision: Split at `. `. Move the `num` portion to the `hints` column.

| Hanja      | Hint |
| ----------- | ----------- |
| `等`      | `1~`       |


### Part of Speech Conversion

GO part of speech will be used as 'reference', unless TOPIK provides better language. TOPIK part of speech will be used if more descriptive. For example:

- In GO, `일곱` part of speech is `수사`.
- In TOPIK, `일곱`, part of speech is `수사/관형사/명사`, which is more preferred as it provides more option in future database purposes, and to recognize the different nuances in various usage cases.

``` GO part of speech conversion
'감': '감탄사',
'고': '고유 명사',
'관': '관형사',
'대': '대명사',
'동': '동사',
'명': '명사',
'보': '보조 용언',
'부': '부사',
'불': '줄어든 말', # changed from original '분석 불능'
'수': '수사',
'의': '의존명사', # changed from original '의존 명사'
'형': '형용사',
```

Reasoning: `의존명사` I found to be more common than the spaced `의존명사`. It's confusing that GO has a page titled `의존명사` but writes `의존 명사` in the body. `줄어든 말` better describes the Korean words marked as `분석 불능`.

``` TOPIK part of speeech conversion
'감탄사': '감탄사',
'관형사': '관형사',
'관형사/수사': '관형사/수사',
'관형사·명사': '관형사/명사',
'대명사': '대명사',
'대명사/관형사': '대명사/관형사',
'동사': '동사',
'동사/형용사': '동사/형용사',
'명사': '명사',
'명사/관형사': '명사/관형사',
'명사/대명사': '명사/대명사',
'명사/부사': '명사/부사',
'명사/의존명사': '명사/의존명사',
'부사': '부사',
'부사/감탄사': '부사/감탄사',
'부사/관형사·명사': '부사/관형사/명사',
'부사/명사': '부사/명사',
'수사': '수사',
'수사/명사': '수사/명사',
'수사·관형사': '수사/관형사',
'수사·관형사/명사': '수사/관형사/명사',
'의존명사': '의존명사',
'의존명사/명사': '의존명사/명사',
'접사': '접사',
'줄어든 말': '줄어든 말',
'형용사': '형용사',
'형용사/동사': '형용사/동사',
```
Reasoning: With the exception of `줄어든 말`, I found that TOPIK uses spaces for 'or' rather than being consistent with the use of forward slashes. I've opted for forward slashes for easier string splits, and fore future database purposes.

## Anomalies 

Issue #1: `金medal`\
The `金` in `金medal` from the GO vocabulary list is not recognized as hanja. `en` is returned when running `khe_ditect('金medal')`.

``` tests
'金' === '金'
false

`金medal` == `金medal`
false
```
Resolution: Check for `金medal` and set go_hanja to `金-` during `re_arrange_go()`.

Issue #2: `를 g다`

In the TOPIK vocabulary list, the guide words for `필기` are `를 g다`. 

Resolution: Given the common use case for `필기` and that the `g` key corresponds with `ㅎ`. I will assume that intended guidewords are `를 하다`.

Issue #3: The Difficult Ones

| frequency      | word | pos | hanja | hint | go | topik |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| ``      | `간단하다02`       | `형용사`       | ``       | ``       | `초급`       |
| ``      | `간절하다`       | `형용사`       | ``       | ``       | `중급`       |
| ``      | `갑작스럽다`       | `형용사`       | ``       | ``       | `중급`       |
| ``      | `값싸다`       | `형용사`       | ``       | ``       | `중급`       |
| ``      | `고통스럽다`       | `형용사`       | ``       | ``       | `중급`       |
| ``      | `공손하다`       | `형용사`       | ``       | ``       | `중급`       |
| ``      | `귀중하다01`       | `형용사`       | ``       | ``       | `중급`       |
| ``      | `다03`       | `부사/명사`       | ``       | ``       | `초급`       |
| `3980`      | `달다05`       | `동사`       | ``       | ``       | ``       |
| `861`      | `달다05`       | `보조 용언`       | ``       | ``       | ``       |
| `3866`      | `만만하다01`       | `형용사`       | ``       | ``       | ``       |
| ``      | `못나다`       | `형용사`       | ``       | ``       | ``       |
| ``      | `별다르다`       | `형용사`       | ``       | ``       | ``       |
| ``      | `비롯하다`       | `동사`       | ``       | ``       | ``       |
| ``      | `상관없다`       | `형용사`       | ``       | ``       | ``       |
| ``      | `수많다`       | `형용사`       | ``       | ``       | ``       |
| ``      | `씩씩하다02`       | `형용사`       | ``       | ``       | ``       |
| ``      | `아무렇다`       | `형용사`       | ``       | ``       | ``       |
| ``      | `잘살다`       | `동사`       | ``       | ``       | ``       |
| ``      | `진정하다01`       | `형용사`       | ``       | ``       | ``       |
| ``      | `초보자`       | `명사`       | ``       | ``       | ``       |
| ``      | `캐나다`       | `명사`       | ``       | ``       | ``       |






frequency	word	pos	hanja	hint	go	topik
				간단한 설명		
				간절한 기도		
				갑작스러운 일		
				값싼 물건		
				고통스러운 표정		
				공손한 태도		
				귀중한 보석		
				모두		
				돈을 다오	B	중급
				빌려 다오	C	
				대적할 만함	C	중급
				못난 얼굴		중급
				별다른 방법		중급
				비롯한 일		중급
				상관없는 문제		중급
				수많은 사람		중급
				씩씩한 사람		중급
				미래가 아무렇든		중급
				잘사는 나라		중급
				진정한 친구		중급
				수영 초보다		중급
				나라		