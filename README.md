# Korean Vocabulary Database Seed (Version 2025.03.01)

Using Python 3 to programmatically combine vocabulary lists from the National Institute of the Korean Language and TOPIK, outputting to TSV for future database seeding.

## Original Sources

`국립국어원 - The National Institute of the Korean Language`
* [한국어 학습용 어휘 목록.xls (2003)](https://www.korean.go.kr/front/etcData/etcDataView.do?mn_id=46&etc_seq=71)

`TOPIK 한국어능력시험 - Test of Proficiency in Korean`
* [토픽 어휘 목록_공개 목록.xlsx (2015)](https://www.topik.go.kr/usr/cmm/subLocation.do?menuSeq=2110503&boardSeq=64217)


## Output File

[Combined NIKL/TOPIK Vocabulary List (.tsv)](https://github.com/julienshim/combined_korean_vocabulary_list/blob/master/results.tsv)

## Keys

* `NIKL` - The National Institute of the Korean Language
* `TOPIK` - Test of Proficiency in Korean
* `Combined` - NIKL and TOPIK vocabulary lists combined
* `en` - English
* `ko` - Korean
* `han` - Hanja
* `&일` - Korean term dervied from 일본어 (Japanese language)
* `&프` - Korean term dervied from 프랑스어 (French language)
* `&독` - Korean term derived from 독일어 (German language)
* `&중` - Korean term derived from 중국어 (Chinese language)
* `&이` - Korean term dericed from 이탈리아어 (Italian language)

## Decisions

### **`Converting NIKL and TOPIK part of speech before creating Combined vocabulary list`**

It's worth noting that TOPIK often provides more detailed part of speech information for Korean words compared to NIKL. For instance, while NIKL might list a single part of speech for a word, TOPIK may indicate multiple grammatical functions. An example of this is the word '일곱':

| Korean    | NIKL part_of_speech   | TOPIK part_of_speech   |
|-------|---------|---------|
| 일곱  | 수사 | 수사/관형사/명사 | 
|   |  |  | 

As shown, TOPIK identifies '일곱' as potentially functioning as a numeral (수사), determiner (관형사), or noun (명사), whereas NIKL categorizes it solely as a numeral (수사)."

> NIKL Part Of Speech

I found the part of speech term 의존명사 to be more common than the spaced version 의존 명사. It's noteworthy that NIKL has a page titled 의존명사 but uses 의존 명사 in the body text, which can be confusing. Additionally, 줄어든 말 (shortened words) more accurately describes the Korean words marked as 분석 불능.

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

I found that TOPIK generally uses spaces to separate alternative parts of speech, with the exception of 줄어든 말. However, for consistency and to facilitate easier string splitting and future database operations, I've opted to use forward slashes instead of spaces.

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

### **`Explanation/Hanja splitting strategy`**

1. Handle explnation values containing hanja
- 1A. If the value contains a period (.), split it into two parts:
    - Move the hanja portion into the hanja column.
    - Keep the remaining portion as the new explanation value.

    `Example: 間. 서울과 부산 ~`

2. Check for English in explanation values without hanja
- If the explanation contains English, check if it also includes missed hanja values:
    - Split the hanja portion into the hanja column.
    - Move the English portion into the explanation column.

    `Example: golf場`

3. Handle pure hanja values without periods
- If the value contains no English and no period, assume it is pure hanja:
    -Set it to the hanja column.
    -Leave the explanation column empty.

4. Default case for all other values
- For all other values:
    - Keep the original value in the explanation column.
    -Leave the hanja column empty.

### **`Combining NIKL and TOPIK explanation`**

After reorganizing the data by splitting hanja into its own category and mapping entries by word and part of speech, I realized that the matching explanations are largely identical and can be merged. This simplification is beneficial for streamlining the information.

Additionally, I noticed that NIKL provides more effective hints for Korean vocabulary by consistently using tildes (~) to indicate where words should be placed in example sentences. Adopting this consistent use of tildes in the hint column could be advantageous for Korean learners who are still developing their understanding of Korean grammar and sentence structure patterns. This approach helps learners better determine the meaning of Korean vocabulary words.

| NIKL explanation    | TOPIK explanation   | TOPIK explanation   |
|-------|---------|---------|
| game  | 컴퓨터 게임 | game; 컴퓨터 게임 |
| ~를 돌리다 |  를 들다  | ~를 돌리다; 를 들다 |
| bus | 를 타다   | bus; 를 타다 |

### **`Determining Combined headers`**

> **Original NIKL headers**

| 순위 (rank) | 단어 (word) | 품사 (part of speech) | 풀이 (definition or explanation) | 등급 (grade or level) |
|--------------|-----------|---------------------|------------------|------------|
|              |           |                     |                  |            |

`등급` are as follows:
* `A` (beginner or elementary)
* `B` (intermediate)
* `C` (advanced)


> **Original TOPIK headers**

| 수준 (level) | 어휘 (vocabulary) | 길잡이말 (guide words) | 품사 (part of speech) |
|--------------|-----------|---------------------|------------------|
|              |           |                     |                  |

TOPIK has two examination levels: TOPIK I covers the basic level, while TOPIK II combines the intermediate and advanced levels. Under 수준, they would be marked as follows:

* TOPIK I - A (beginner)
* TOPIK II - B (intermediate), but more accurately 'from intermediate on'.

There is no 'C' to correspond to advanced vocabulary, as the 'B' category encompasses both intermediate and advanced levels. This means that while TOPIK II includes advanced proficiency, it is not distinguished by a separate 'C' classification.

> **Combined headers**

| rank | word | part_of_speech | hanja | explanation | nikl_level | topik_level |
|-----------|--------|-----|-------|------|----------|----------|
|           |        |     |       |      |          |          |




## **`Notable explanations`**

During my review of the NIKL and TOPIK vocabulary lists, I noticed several explanation terms that are categorized by topic. These terms may be particularly useful for Korean learners as they provide a structured way to understand and organize vocabulary. Here are some examples:

**Topic based explanations**

* 병원 (hospital)
* 방법 (method)
* 방향  (direction)
* 행정 구역 (administrative district)
* 고적 (historical sites)
* 가구 (furniture)
* 나라 (country)
* 숫자 (number)
* 직업 (occupation)
* 신체 (body)
* 계절 (season)
* 색깔 (color)
* 과일 (fruit)
* 채소 (vegetable)
* 가족 (family)
* 동물 (animal)
* 곤충 (insect)
* 친척 (relatives)
* 지명 (name of a place)
* 음식 (food)
* 달(월) (month)
* 요일 (day of the week)
* 신체의 일부 (part of body)
* 시간 (time)
* 식물 (plant)
* 꽃 (flower)

### **`Issues`** 

> Issue: Errors found

During the data filtering process, several errors were identified and manually corrected before combining the NIKL and TOPIK vocabulary lists.

| Correction            | Issue                                 |
|-----------------------|---------------------------------------|
| '를 g다' -> '를 하다'      | Should be '하다'                        |
| '에서 연습핟' -> '에서 연습하다' | Should be '하다'                        |
| '경찰 수가' -> '경찰 수사'    | Should be '-사'                        |
| '대적할 만함' -> '대적할 만한'  | Should be '-한'                        |
|                       |                                       |


### **`Changelog - 2025.03.01`** 

**Major Changes**

1. Complete Codebase Restructure
    - Started from scratch with a new architecture
    - Introduced DataManager class for data cleaning
    - Created MergeManager class for data merging operations
2. Enhanced Data Processing
    - Implemented updated regex patterns for improved data parsing
    - Focused on splitting hanja from explanation column into a dedicated hanja column
    - Developed a simpler method for merging matching NIKL and TOPIK entry values
3. Code Optimization
    - Streamlined data cleaning and merging processes
    - Improved efficiency in handling large datasets