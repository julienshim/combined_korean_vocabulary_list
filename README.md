# Vocabulary List for Korean Learning

A programmatically-combined vocabulary list for learning Korean via Python 3, outputting in TSV (tab-serparated values) format for future database purposes.

A programm

## Original Sources

```국립국어원 - The National Institute of the Korean Language```
* [한국어 학습용 어휘 목록.xls (2003)](https://www.korean.go.kr/front/etcData/etcDataView.do?mn_id=46&etc_seq=71)

```TOPIK 한국어능력시험 - Test of Proficiency in Korean```
* [토픽 어휘 목록_공개 목록.xlsx (2015)](https://www.topik.go.kr/usr/cmm/subLocation.do?menuSeq=2110503&boardSeq=64217)

## Keys

* `GO` - The National Institute of the Korean Language (go.kr)
* `en` - English
* `ko` - Korean
* `han` - Hanja
* `&일` - Korean term dervied from 일본어 (Japanese language)
* `&프` - Korean term dervied from 프랑스어 (French language)
* `&독` - Korean term derived from 독일어 (German language)
* `&중` - Korean term derived from 중국어 (Chinese language)
* `&이` - Korean term dericed from 이탈리아어 (Italian language)

## Decisions

### **`Determinging Combined headers`**

> **Original GO headers**

| 순위 (ranking) | 단어 (word) | 품사 (part of speech) | 풀이 (explanation) | 등급 (level) |
|--------------|-----------|---------------------|------------------|------------|
|              |           |                     |                  |            |

`순위` is in terms of usage. `등급` are as follows:
* `A` (beginner)
* `B` (intermediate)
* `C` (advanced)


> **Original TOPIK headers**

| 수준 (level) | 어휘 (vocabulary) | 길잡이말 (guide words) | 품사 (part of speech) |
|--------------|-----------|---------------------|------------------|
|              |           |                     |                  |

TOPIK has two examination levels: TOPIK I covers the basic level. TOPIK II combines the intermediate and advanced levels. Under `수준`, they would be marked as follows.
* TOPIK I - `초급` (beginner)
* TOPIK II - `중급` (intermediate), but more accurately 'from intermediate on'.

> **Combined headers**

| frequency | korean | pos | hanja | hint | go_level | topik_level |
|-----------|--------|-----|-------|------|----------|-------------|
|           |        |     |       |      |          |             |


### **`Handling GO 풀이 to Combined hanja and hint conversion`**

GO `풀이` is a combination of Korean, Hanja, English and Number explainations. Below are the found types:

> **Type 1: `<ampersand><ko><en>`**

*Example*: `&일ramen`\
Decision: Move from the `hanja` column to the `hints` column. 

| Hanja      | Hint |
| ----------- | ----------- |
|       | `&일ramen`       |
|       |        |

> **Type 2: `<en><han>` or `<han><en>`**

*Examples*: `golf場`, `市內bus`\
Decision: The `en` porition doesn't provide any value. Replace the `en` portion with a `-`.

| Hanja      | Hint |
| ----------- | ----------- |
| `-場`      |        |
| `市內-`   |         |

> **Type 3: `<han><period><ko>`**

*Example*: `間. 서울과 부산`, \
Decision: Split at `. `. Move the `num` portion to the `hints` column.

| Hanja      | Hint |
| ----------- | ----------- |
| `間`      | `서울과 부산`       |

> **Type 4: `<han><period><num>`**
Example: `等. 1~`
Decision: Split at `. `. Move the `num` portion to the `hints` column.

| Hanja      | Hint |
| ----------- | ----------- |
| `等`      | `1~`       |

> **Issue - false detection**

The following due to false language detection, must be changed manually during the process.

| Correction            | Issue                                 |
|-----------------------|---------------------------------------|
| '金medal' -> '金-'      | Detected as 'en' rather than 'han/en' |
|                       |                                       |

### **`Handling Combined hint conversions`**

GO provides better hints in Korean than TOPIK due to their consistent use of tildes (~), indicating where the Korean vocabulary word should be placed in the hints, seen below. Having consistent use of tildes where appropriate under the `hint` column may be benefitial to Korean learners not yet confident in Korean grammar and sentence structure patterns in determining the meaning of a Korean vocabulary word.

| GO hint    | TOPIK hint   |
|-------|---------|
| ~ 차다  | 단지 ~만으로 |
| 색깔이 ~ | 를 조성하다  |
| 바위가 ~ | 이 심하다   |
|       |         |

> Sifting system strategy in identifying hints to modify with tildes

Sifting systems supplies various sieves with openings varying in microns. The upper sieve will prevent particles too large from coming through, and an optional lower sieve will let anything too fine will pass through to the bottom portion. The middle sieve catches the ideal size and anything between the middle and the upper, as well as the middle and the lower sieve will be acceptable.

Tackling a large dataset requires a similar method. It starts with isolating, confirming, then hiding away data types we don't want to target, taking note of issues, until we can clearly see the data types we want to modify. We can then start isolating, confirming, then hiding away the datatypes we want to modify, taking note of issues. We continue the process until we're sure everything we want to modify is accounted for.

> Examples of distracting untargeted data types

Distracting untargeted data types will have hints that do not require a tilde to indicate where the Korean vocabulary word should be placed as there is not grammatic relation between the Korean word and hint.

1. **Empty hint  values**

| korean            | hint                                 |
|-----------------------|---------------------------------------|
| 가득히      |                         |
|  |                         |


2. **Hint values with tildes (correct format)**

| korean            | hint                                 |
|-----------------------|---------------------------------------|
| 가방  | ~을 메다 |
|  |                         |

3. **Hint values with apostrophes (')**

| korean            | hint                                 |
|-----------------------|---------------------------------------|
| 걸리다01  | '걸다'의 피동사 |
|  |                         |

4. **Hint values with ampersands (&)**

| korean            | hint                                 |
|-----------------------|---------------------------------------|
| 발레  | &프ballet |
|  |                         |

5. **Hint values in English**

| korean            | hint                                 |
|-----------------------|---------------------------------------|
| 배드민턴  | badminton |
|  |                         |

5. **Hint values in Korean with numbers**

| korean            | hint                                 |
|-----------------------|---------------------------------------|
| 분08  | 10시 20~ |
|  |                         |


5. **Topic based hints (examples)**

* 병원 
* 방법 
* 방향 
* 행정 구역 
* 고적 
* 가구 
* 나라 
* 숫자 
* 직업 
* 신체 
* 계절 
* 색깔 
* 과일 
* 채소 
* 가족 
* 동물 
* 곤충 
* 친척 
* 지명 
* 음식 
* 달(월) 
* 요일 
* 신체의 일부 
* 신체의 일부 
* 시간 
* 식물 
* 꽃


6. **Select part of speech**

* 감탄사
* 관형사
* 줄어든 말
* 의존명사
* 대명사
* 부사


7. **Hints that are not in Korean**

8. **-다 ending in both the Korean and hint columns**

Finding the -다 ending in both the Korean and columns usually indicates one of the following:

| korean            | hint                                 |
|-----------------------|---------------------------------------|
| 갖다  | 가지다 | contraction 
| 꼼꼼하다  | 꼼꼼하게 살펴보다 | example sentence 
| 바치다  | 드리다 | synonyms 


Exceptions to look out for where a tilde is needed in the hint:

| korean            | hint                                 |                                  |
|-----------------------|-----------------------|-----------------------|
| 사이다  | 를 마시다 | 를 마시다 -> ~를 마시다 -> 사이다를 마시다 |
| 베란다  | 로 나가다 | 로 나가다 -> ~로 나가다 -> 베란다로 나가다 |


### **`Issues`** 


> Issue: Errors found

| Correction            | Issue                                 |
|-----------------------|---------------------------------------|
| '를 g다' -> '를 하다'      | Should be '하다'                        |
| '에서 연습핟' -> '에서 연습하다' | Should be '하다'                        |
| '경찰 수가' -> '경찰 수사'    | Should be '-사'                        |
| '대적할 만함' -> '대적할 만한'  | Should be '-한'                        |
|                       |                                       |


> Issue: Exceptions

| frequency | korean | pos | hanja | hint   | go_level | topik_level |
|-----------|--------|-----|-------|--------|----------|-------------|
| 5992      | 팬01    | 명사  |       | 애호가    | B        |             |
| 214       | 동안01   | 명사  |       | 시간의 길이 | A        |             |
| 3117      | 새01    | 명사  |       | 사이     | C        |             |
| 315       | 애02    | 명사  |       | 아이     | B        |             |
|           | 요새01   | 명사  |       | 요 사이   |          | 중급          |
|           |        |     |       |        |          |             |

> Issue: `The Leftovers`

| frequency | korean | pos | hanja | hint | go_level | topik_level |
|-----------|--------|-----|-------|------|----------|-------------|
|           | 적용     | 명사  |       | 받다   |          | 중급          |
|           | 분위기    | 명사  |       | 어색한  |          | 초급          |
|           | 아동02   | 명사  |       | 의 성장 |          | 중급          |
|           | 아랫사람   | 명사  |       | 의 도리 |          | 중급          |
|           | 우연02   | 명사  |       | 의 일치 |          | 중급          |
|           | 재생01   | 명사  |       | 의 기회 |          | 중급          |
|           | 차례01   | 명사  |       | 지키다  |          | 초급          |
|           | 차례01   | 동사  |       | 오래   |          | 초급          |
| 4881      | 달다07   | 형용사 |       | 맛    | A        |             |
|           |        |     |       |      |          |             |



### **`Handling Part of Speech Conversions`**

GO part of speech will be used as 'reference'. TOPIK part of speech will be used if more descriptive, which is prefered for future database purposes to recognize the different nuances in vocabulary. See the example below:

| Korean    | GO hint   | TOPIK hint   |
|-------|---------|---------|
| 일곱  | 수사 | 수사/관형사/명사 | 
|   |  |  | 

> GO Part Of Speech

`의존명사` I found to be more common than the spaced `의존 명사`. It's confusing that GO has a page titled `의존명사` but writes `의존 명사` in the body. `줄어든 말` better describes the Korean words marked as `분석 불능`.

```
    '감': '감탄사',
    '고': '고유 명사',
    '관': '관형사',
    '대': '대명사',
    '동': '동사',
    '명': '명사',
    '보': '보조 용언',
    '부': '부사',
    '불': '줄어든 말', # changed from '분석 불능'
    '수': '수사',
    '의': '의존명사', # changed from '의존 명사'
    '형': '형용사',
```

> TOPIK Part Of Speech

With the exception of `줄어든 말`, I found that TOPIK uses spaces for 'or' rather than being consistent with the use of forward slashes. I've opted for forward slashes for easier string splits, and fore future database purposes.

```
    '감탄사': '감탄사',
    '관형사': '관형사',
    '관형사/수사': '관형사/수사',
    '관형사·명사': '관형사/명사',
    '관형사/대명사': '관형사/대명사',
    '대명사': '대명사',
    '대명사/부사': '대명사/부사',
    '대명사/관형사': '대명사/관형사',
    '대명사/명사': '대명사/명사',
    '대명사/감탄사': '대명사/감탄사',
    '동사': '동사',
    '동사/형용사': '동사/형용사',
    '명사': '명사',
    '명사/관형사': '명사/관형사',
    '명사/대명사': '명사/대명사',
    '명사/부사': '명사/부사',
    '명사/의존명사': '명사/의존명사',
    '명사/감탄사': '명사/감탄사',
    '부사': '부사',
    '부사/감탄사': '부사/감탄사',
    '부사/관형사·명사': '부사/관형사/명사',
    '부사/명사': '부사/명사',
    '수사': '수사',
    '수사/명사': '수사/명사',
    '수사·관형사': '수사/관형사',
    '수사/관형사': '수사/관형사',
    '수사·관형사/명사': '수사/관형사/명사',
    '수사·관형사/명사/부사': '수사/관형사/명사/부사',
    '의존명사': '의존명사',
    '의존명사/명사': '의존명사/명사',
    '접사': '접사',
    '줄어든 말': '줄어든 말',
    '형용사': '형용사',
    '형용사/동사': '형용사/동사',
    '조사': '조사',
```
