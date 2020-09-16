from pdfminer.high_level import extract_text
import scriptures
import re
import os

questionPath = '/media/data/data/Media/BSF/2020-2021/Adult Questions'

def GetLink(passage: str, version: str):
    urlStr = passage.replace(' ','+')
    urlStr = urlStr.replace(':','%3A')
    return f'https://www.biblegateway.com/passage/?search={urlStr}&version={version}&interface=print'

def GetVerseString(verse):
    str = scriptures.reference_to_string(verse[0],verse[1],verse[2],verse[3],verse[4])
    return str.replace('Revelation of Jesus Christ','Revelation')

def GetVerseMarkdown(verse):
    str = GetVerseString(verse)
    esvLink = GetLink(str,'ESV')
    nltLink = GetLink(str,'NLT')
    nivLink = GetLink(str,'NIV')
    nirvLink = GetLink(str,'NIRV')
    allLink = GetLink(str,'NLT,ESV,NIV,NIRV')
    return f'{str} <small>[[NLT]({nltLink}) / [ESV]({esvLink}) / [NIV]({nivLink}) / [NIRV]({nirvLink}) / [All]({allLink})]</small>'

def GetVerseCount(verse):
    count = 0
    for ch in range(verse[1],verse[3]+1):
        if ch == verse[1] and ch == verse[3]:
            for v in range(verse[2],verse[4]+1):
                if scriptures.is_valid_reference(verse[0],ch,v):
                    count = count + 1
                else:
                    continue
        elif ch == verse[1]:
            for v in range(verse[2],500):
                if scriptures.is_valid_reference(verse[0],ch,v):
                    count = count + 1
                else:
                    continue
        elif ch == verse[3]:
            for v in range(1,verse[4]+1):
                if scriptures.is_valid_reference(verse[0],ch,v):
                    count = count + 1
                else:
                    continue
        else:
            for v in range(1,500):
                if scriptures.is_valid_reference(verse[0],ch,v):
                    count = count + 1
                else:
                    continue
    return count

def RemoveDupicates(verses):
    output = []
    for x in verses:
        if x not in output:
            output.append(x)
    return output

def GetAllVerseCount(verses):
    t = 0
    for v in RemoveDupicates(verses):
        t = t + GetVerseCount(v)
    return t



# text = 'Genesis 8:15-22;Genesis 8:15-22;John 12:27-33;Romans 3:25-26;I Peter 2:21-24;Proverbs 21:3;Hosea 6:6;Micah 6:8;John 15:13;Romans 12:1-2;Hebrews 13:15-16'
# text='Genesis 10;Genesis 9;Genesis 11;Acts 17:26-27;Revelation 7:9'
# verses = scriptures.extract(text)
# total = 0
# for v in RemoveDupicates(verses):
#     t = GetVerseCount(v)
#     print(f'\t{t} \t{v[0]}\t\t{v[1]}\t{v[2]}\t{v[3]}\t{v[4]}')
#     total = total + t
# print(total)
# exit()


print('# 2020-2021 BSF')

for filename in sorted(os.listdir(questionPath)):
    text = extract_text(f'{questionPath}/{filename}')
    text = text.replace('\n','~~~')
    lessonLine = re.match(r".*Lesson (\d+)\s*~~~Adult Questions\s*~~~(.*?)\s*~~~.*", text)
    text = re.sub(r"Lesson (\d+)\s*~~~Adult Questions\s*~~~(.*?)\s*~~~",'', text)
    text = text.replace('~~~','')
    text = re.sub('([A-Z]+ DAY)',r'\n\1', text)
    text = re.sub('(Focus Verse)',r'\n\1', text)

    daySeen = False

    if(lessonLine):
        lessonNumber = lessonLine.group(1)
        lessonVerses = scriptures.extract(lessonLine.group(2))

        print(f'\n\n## Lesson {lessonNumber}')
        print(f'**Scripture**')
        for verse in RemoveDupicates(lessonVerses):
            print(f'- {GetVerseMarkdown(verse)}\n')
    
    for line in text.splitlines():
        if re.match('[A-Z]+ DAY',line):
            section = re.match('[A-Z]+ DAY',line)
            if section:
                if not daySeen:
                    daySeen = True
                    print(f'**Days**')
                verses = scriptures.extract(line)
                print(f'- {section.group(0)} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  *({GetAllVerseCount(verses)} verses)* ')
                for verse in RemoveDupicates(verses):
                    print(f'    - {GetVerseMarkdown(verse)}')

        elif re.match('Focus Verse',line):
            print(f'**Focus Verse**')
            verses = scriptures.extract(line)
            for verse in RemoveDupicates(verses):
                print(f'- {GetVerseMarkdown(verse)}\n')

