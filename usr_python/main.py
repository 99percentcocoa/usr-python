from __future__ import unicode_literals
import logging
from isc_parser import Parser
from wxconv import WXC
import requests
import json
import re

from importlib import resources
import io

# setting up logging
logging.basicConfig(level=logging.WARNING)

con = WXC(order="utf2wx")

parser = Parser(lang='hin')

input = u"""सूर्यास्त के बाद आकाश को देखना कितना अच्छा लगता है।
आप उनकी गणना नहीं कर सकते।
इनमें से कुछ टिमटिमाते प्रतीत होते हैं।
ये बिना किसी टिमटिमाहट के चंद्रमा के समान चमकते हैं।"""

morphURL = "https://ssmt.iiit.ac.in/samparkuniverse"

conceptDictFile = "H_concept-to-mrs-rels.dat"
tamDictFile = "TAM-num-per-details.tsv.wx"

# returns wx string
def toWx(inputString):
    # logging.debug("converting to wx.")

    wx_str = con.convert(inputString)
    return wx_str.strip()

def getMorph(inputString):
    reqData = {"text": input.strip(), "source_language": "hin", "target_language": "urd", "start": 1, "end": 9}
    header = {"Content-Type": "application/json;charset=UTF-8"}
    res = requests.post(morphURL, data=json.dumps(reqData), headers=header)
    morphOutput = json.loads(res.text)
    # logging.debug(morphOutput)
    # returns a DICT containing morphOut, pruneOut and nerOut
    return {
        "morphOut": morphOutput["modular_outputs"]["morph-3"], 
        "pruneOut": morphOutput["modular_outputs"]["pickonemorph-6"],
        "nerOut": morphOutput["modular_outputs"]["ner-9"]
    }

def parse(inputString):
    return parser.parse(inputString.split())

# returns true or false, whether term present in concept dict
def search_concept(key):


    # with open(conceptDictFile, 'r') as fp:
    with resources.open_text('usr_python', conceptDictFile) as fp:
        for l_no, line in enumerate(fp):
            if key in line:
                return True
    return False

# search iteratively in tam, return first column if found, else return None
def search_TAM(key):
    temp = key
    removed = ''
    with resources.open_text('usr_python', tamDictFile) as fp:
        lines = fp.readlines()
        while (len(temp) > 0):
            for line in lines:
                if bool(re.search(f'\s{temp}\s', line)):
                    # logging.debug(f'{temp} match line found: {line}')
                    return removed + '_1-' + line.split('	')[0]
            # logging.debug(f'match not found for {temp}')
            removed = removed + temp[0]
            temp = temp[1:]
            # logging.debug(f'new temp: {temp}')
            # logging.debug(f'removed: {removed}')
        return None
            

def getSentenceUSR(inputString):

    # add space before final punctuation mark if none, using regex matching
    if (bool(re.search(r'(?<=[^ ])[।?]', inputString[-2:]))):
        inputStringFinalSeparated = inputString[:-1] + ' ' + inputString[-1:]
    else:
        inputStringFinalSeparated = inputString
    
    wxString = toWx(inputStringFinalSeparated)
    # logging.debug(wxString)

    wxArray = wxString.split(' ')
    #  logging.debug(wxArray)

    # parser run on inputStringFinalSeparated, not raw inputString
    # note, parser index corresponds to wxArray index
    parserOutput = parse(inputStringFinalSeparated)
    # logging.debug(parserOutput)

    morphOutput = getMorph(inputStringFinalSeparated)
    # slice to remove <sentence id> lines at the beginning and end
    NERarray = morphOutput['nerOut'].split('\n')[1:-1]
    pruneArray = morphOutput['pruneOut'].split('\n')[1:-1]

    # words not found in dictionary
    dictWarnings = []

    # line 1 - original sentence
    line1String = f"# {inputString}"

    # - - - - - - - - - -

    # line 2 - concepts

    # starting with string for easy appending, will later split into array
    line2 = ''

    # logging.debug(parserOutput)

    # array containing the indices of final row 2 words, in wxArray.
    line2index = []

    # iterate through wx array, using while and counter
    count = 0

    while count < len(wxArray):
        val = wxArray[count]
        # logging.debug(f'at word {val}.')
        # logging.debug(f'Parser output for {val}: {parserOutput[count]}')
        # skip if lwg__psp
        if (parserOutput[count][7] == 'lwg__psp'):
            # logging.debug(f'{val}: lwg__psp. Skipping.')
            count += 1
        # if pof, append to line2 with plus, followed by next
        elif (parserOutput[count][7] == 'pof'):
            line2 = line2 + val + '+'
            line2index.append(count)
            count += 1
        # if symbol, don't append to line2 and move on
        elif (parserOutput[count][3] == 'SYM'):
            # line2 = line2 + val
            count += 1
        # if verb group then search entire verb group in TAM
        elif (parserOutput[count][3] == 'VM'):
            # logging.debug(f'VM found: {val}')
            # scan ahead to get the entire verb group
            # append to line2index of not preceeded by + or -
            if (line2[-1] not in ('+', '-')):
                line2index.append(count)
            verbGroup = ''
            verbCount = count
            while (parserOutput[verbCount][3] in ('VM', 'VAUX', 'VAUX_CONT')):
                verbGroup = ' '.join((verbGroup, wxArray[verbCount])).strip()
                verbCount += 1
            # logging.debug(f'Searching {verbGroup} in TAM.')
            searchTAM = search_TAM(verbGroup)
            if (bool(searchTAM)):
                line2 = ''.join((line2, searchTAM, ','))
            else:
                line2 = ''.join((line2, val, '_1,'))
            # logging.debug(f'line2: {line2}')
            count = verbCount
        # append to line2, search in dictionary, warning if not found in dictionary
        else:
            line2index.append(count)
            line2 = ''.join((line2, val, '_1,'))
            if (search_concept(val + "_1") == False):
                 dictWarnings.append(''.join((val, "_1")))
            count += 1
    
    # remove final comma
    if line2[-1] == ',':
        line2 = line2[:-1]
    
    line2Array = line2.split(',')
    line2String = ",".join(str(x) for x in line2Array)
    logging.debug(f'dict warnings: warnings: {dictWarnings}')

    # logging.warning(f'line2index: {line2index}')
    # logging.warning(f'wxArray: {wxArray}')

    # - - - - - - - - - -

    # line 3 - concepts index

    line3Array = []

    for index, value in enumerate(line2Array):
        line3Array.append(f'{index+1}')
    
    line3String = ",".join(str(x) for x in line3Array)

    # - - - - - - - - - -

    # line 4 - semantic category of nouns

    # last word in NER entries if there, else not there
    
    # logging.debug(f'NERarray: {NERarray}')

    line4Array = []

    # iterate over values of line2index
    # logging.debug(f'line2index: {line2index}')
    for val in line2index:
        lineArray = NERarray[val].split('\t')
        # logging.debug(f'current line: {NERarray[val]}')
        if (len(lineArray) > 3):
            lastWord = lineArray[-1]
            if lastWord == "person":
                line4Array.append('per')
            elif lastWord == "location":
                line4Array.append('loc')
            elif lastWord == 'organization':
                line4Array.append('org')
            else:
                line4Array.append('')
        else:
            # logging.debug(f'No semantic value found.')
            line4Array.append('')
    
    line4String = ",".join(str(x) for x in line4Array)

    # - - - - - - - - - -

    # line 5 - GNP info

    # if conditions are met, then get GNP from prune output

    # logging.debug(f'pruneArray: {pruneArray}')

    line5Array = []
    
    for val in line2index:
        if (parserOutput[val][7] in ('r6', 'k7', 'k1', 'k2', 'k7p', 'ras-k1', 'k2p', 'r6-k2', 'k5', 'rt')):
            gnpArray = pruneArray[val].split('\t')[3].split(',')[2:5]
            if gnpArray[2] == '1':
                gnpArray[2] = 'u'
            elif gnpArray[2] == '2':
                gnpArray[2] = 'm'
            elif gnpArray[2] == '3':
                gnpArray[2] = 'a'
            elif gnpArray[2] == 'any':
                gnpArray[2] = '-'
            # logging.debug(f'gnpArray for {wxArray[val]}: {gnpArray}')
            line5Array.append(f"[{' '.join(str(x) for x in gnpArray)}]")
        else:
            line5Array.append('')
        # logging.debug(f'line5: {line5Array}')

    
    line5String = ",".join(str(x) for x in line5Array)

    # - - - - - - - - - -

    # line 6 - dependency relations

    line6Array = []

    # list of indices of main verbs in wxArray/parserOutput
    VMArray = []
    for index, value in enumerate(parserOutput):
        if (value[3] == 'VM'):
            VMArray.append(index)
    logging.debug(f'VMArray: {VMArray}')

    for index, val in enumerate(line2index):
        if (parserOutput[val][7] in ('nmod__adj', 'adv', 'pof__cn', 'jjmod__intf', 'r6')):
            if (parserOutput[val][3] == 'QC'):
                line6Array.append(f'{val}:card')
            elif (parserOutput[val][3] == 'QO'):
                line6Array.append(f'{val}:ord')
            elif (parserOutput[val][7] == 'adv'):
                line6Array.append(f'{val}:kr_vn')
            elif (parserOutput[val][7] == 'nmod__adj'):
                line6Array.append(f'{val}:mod')
            elif (parserOutput[val][7] == 'pof__cn'):
                line6Array.append(f'{val}.{val+1}/{val}.{line2index[index+1]-1}:pof__cn')
            else:
                line6Array.append(f'{val}:{parserOutput[val][7]}')
        elif ((int(parserOutput[val][6])-1 in VMArray) and (parserOutput[val][3] != 'VM') and (parserOutput[val][7] not in ('pof', 'rysm', 'lwg__vaux', 'lwg__vaux_cont', 'lwg__psp'))):
            if ((parserOutput[val][7] == 'k1') and (parserOutput[val+1][7] == 'k1s') and (parserOutput[val][6] == parserOutput[val+1][6])):
                line6Array.append('samAnAXi,samAnAXi')
            elif (parserOutput[val][7] == 'k1s'):
                line6Array.append('')
            else:
                line6Array.append(f'{val}:{parserOutput[val][7]}')
        else:
            line6Array.append('')

    
    line6String = ",".join(str(x) for x in line6Array)

    # - - - - - - - - - -

    # line 7 - discourse elements

    line7Array = []
    for index, value in enumerate(line2Array):
        line7Array.append('')
    
    line7String = ",".join(str(x) for x in line7Array)

    # - - - - - - - - - -

    # line 8 - speaker's view points

    line8Array = []
    for val in line2index:
        if (parserOutput[val][7] in ('lwg__rp', 'lwg__neg')):
            if (parserOutput[val][7] == 'lwg__neg'):
                line8Array.append(f'{val}:neg')
            else:
                line8Array.append(f'{val}:{wxArray[val]}')
        else:
            line8Array.append('')
    
    line8String = ",".join(str(x) for x in line8Array)

    # - - - - - - - - - -

    # line 9 - scope

    line9Array = []
    for index, value in enumerate(line2Array):
        line9Array.append('')
    
    line9String = ",".join(str(x) for x in line9Array)

    # - - - - - - - - - -

    # line 10 - sentence type

    line10 = ''
    # scan whole string for नही or नहीं
    if len(re.findall('(nahIM)|(nahI)', wxString)) > 0:
        line10 = 'negative'
    else:
        if (wxString[-1] == '?'):
            line10 = 'interrogative'
        elif (wxString[-1] in ("|", "।", ".")):
            line10 = 'affirmative'
    
    # print(line10)

    returnDict = {
        'original': line1String,
        'concepts': line2Array,
        'concepts_index': line3Array,
        'semantic': line4Array,
        'gnp': line5Array,
        'dependency': line6Array,
        'discourse': line7Array,
        'speaker_viewpoints': line8Array,
        'scope': line9Array,
        'sentence_type': line10
    }

    return returnDict

# wrapper for main function, allows passing of multi-line sentences
def getUSR(inputString):
    lines = inputString.split('\n')
    returnDict = {}

    for num, line in enumerate(lines):
        indexstr = '_'.join(('sentence', str(num+1)))
        returnDict[indexstr] = getSentenceUSR(line)
    
    return returnDict

# if __name__ == "__main__":
#     object = json.dumps(getUSR(input), indent=4)
#     print(object)
#     # print(main(input))