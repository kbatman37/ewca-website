from pdfminer.high_level import extract_text
import scriptures
import re
import os

questionPath = '/media/data/data/Media/BSF/2020-2021/Adult Questions'
    
for filename in sorted(os.listdir(questionPath)):
    text = extract_text(f'{questionPath}/{filename}')

    p = re.compile('Lesson \d+')
    lesson = p.findall(text)[0]
    print(f'## {lesson}')

    verses = scriptures.extract(text)

    for verse in verses:
        str = scriptures.reference_to_string(verse[0],verse[1],verse[2],verse[3],verse[4])
        str = str.replace('Revelation of Jesus Christ','Revelation')
        urlStr = str.replace(' ','+').replace(':','%3A')
        url = f'https://www.biblegateway.com/passage/?search={urlStr}&version=NLT&interface=print'
        print(f'- [{str}]({url})')
