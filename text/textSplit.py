import os
import re

bookTitle = 'SAHIH BUKHARI'
bookPrefix = 'bukhari_'
saveLocation = 'data/text/raw/hadith/'

def scan(directoryPath):
    filePaths = []
    for root, dirs, files in os.walk(directoryPath):
        for file in files:
            if file.endswith(".txt"):
                filePaths.append(os.path.join(root, file))
    return filePaths

def getSentences(filePath):
    file = open(filePath, 'r')
    fileContent = file.read();
    text_content = fileContent.split('\n')
    file.close();
    return text_content

def startingPositionOfSubString(text, subText):
    text = text.lower()
    subText = subText.lower()
    if subText not in text:
        return -1

    subTextLength = len(subText)
    index = 0
    for ch in text:
        if ch != subText[0]:
            index +=1
            continue

        if text[index:index+subTextLength] == subText:
            return index

        index += 1

    return -1

def getVolumeNumber(sentence):
    startPosition = len('VOLUME') + 1
    endPosition = startingPositionOfSubString(sentence, 'BOOK')
    number = sentence[startPosition:endPosition]
    number = re.sub(r"[\s,>]", "", number)
    return number.strip()

def getBookNumber(sentence):
    sentence = re.sub(r"VOLUME .* BOOK ", "", sentence, flags=re.IGNORECASE)
    number = re.sub(r"[,:].+", "", sentence)
    return number.strip()

def getHadithNumber(sentence):
    sentence = re.sub(r"VOLUME .* BOOK .* NUMBER", "", sentence, flags=re.IGNORECASE)
    number = re.sub(r":.+", "", sentence)
    return number.strip()

def getBookTitle(sentence):
    parts = sentence.split(":")
    if len(parts) > 1:
        return parts[1].strip()
    return ''

def extractAndSaveHadiths(previousFilePath, currentFilePath):
    global bookTitle
    sentences = getSentences(currentFilePath)
    
    if not len(sentences):
        return
    source = sentences.pop()
    item = {}
    oldItemContent = ''
    for sentence in sentences:
        if(re.search('VOLUME', sentence, re.IGNORECASE)):
            if not (re.search('BOOK', sentence, re.IGNORECASE)):
                continue
            
            if (len(item) and len(item['content'])):
                saveHadith(item)
            item['source'] = source
            item['volume'] = getVolumeNumber(sentence)
            item['book'] = getBookNumber(sentence)
            item['title'] = getBookTitle(sentence)
            item['number'] = getHadithNumber(sentence)
            item['file_name'] = bookPrefix + 'v' + item['volume'] + '_b' + item['book'] + '_n' + item['number']
            item['content'] = ''
            item['narrated'] = ''
        
            if item['title']:
                bookTitle =  item['title']
            elif bookTitle:
                item['title'] = bookTitle
        elif len(item):
            if(sentence[0:8].lower() == 'narrated'):
                item['narrated'] = sentence[9:]
                item['narrated'] = re.sub(':', '', item['narrated'])
                item['narrated'] = item['narrated'].strip()
            else:
                item['content'] += sentence
        else:
            oldItemContent += sentence

    if len(item):
        saveHadith(item)
    
    if oldItemContent != '':
        file = open(previousFilePath, 'w+')
        file.write(oldItemContent);
        file.close();
    return

def deleteFile(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)
    return

def saveHadith(item):
    saveFilePath = saveLocation + item['file_name']
    deleteFile(saveFilePath)

    file = open(saveFilePath, 'w+')
    file.write('[SOURCE]' + item['source'] + "\n");
    file.write('[VOLUME]' + item['volume'] + "\n");
    file.write('[BOOK]' + item['book'] + "\n");
    file.write('[TITLE]' + item['title'] + "\n");
    file.write('[NUMBER]' + item['number'] + "\n");
    file.write('[NARRATED]' + item['narrated'] + "\n");
    file.write('[CONTENT]' + item['content'] + "\n");
    file.close();
    return

def scanDirectoryAndSaveHadith():
    allFiles = scan("data/text/raw/bukhari")
    oldFilePath = 'data/text/raw/hadith/bukhari_init.txt'
    i = 0
    for filePath in allFiles:
        #print("------------------------------------------")
        #print(filePath)
        extractAndSaveHadiths(oldFilePath, filePath)
        oldFilePath = filePath
        print('.')
        i += 1
        if i == 2:
            break

    return


scanDirectoryAndSaveHadith()

#extractAndSaveHadiths('data/hadith/bukhari_init.txt', 'data/bukhari/96_bukhari.txt')






