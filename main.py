from __future__ import unicode_literals
import logging
from isc_parser import Parser
from wxconv import WXC
import requests
import json
import re
# use multithreading in the future
# import threading

# setting up debug
logging.basicConfig(level=logging.WARNING)

con = WXC(order="utf2wx")

parser = Parser(lang='hin')

input = u"सूर्यास्त के बाद आकाश को देखना कितना अच्छा लगता है।"

morphURL = "https://ssmt.iiit.ac.in/samparkuniverse"

conceptDictFile = "H_concept-to-mrs-rels.dat"
tamDictFile = "TAM-num-per-details.tsv.wx"

# returns wx string
def toWx(inputString):
    logging.debug("converting to wx.")

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
    with open(conceptDictFile, 'r') as fp:
        for l_no, line in enumerate(fp):
            if key in line:
                return True
    return False

# search iteratively in tam, return first column if found, else return None
def search_TAM(key):
    temp = key
    removed = ''
    with open(tamDictFile, 'r') as fp:
        lines = fp.readlines()
        while (len(temp) > 0):
            for line in lines:
                if bool(re.search(f'\s{temp}\s', line)):
                    logging.debug(f'{temp} match line found: {line}')
                    return removed + '_1-' + line.split('	')[0]
            # logging.debug(f'match not found for {temp}')
            removed = removed + temp[0]
            temp = temp[1:]
            # logging.debug(f'new temp: {temp}')
            # logging.debug(f'removed: {removed}')
        return None
            

def main(inputString):

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

    # words not found in dictionary
    dictWarnings = []

    # line 1 - original sentence
    line1String = f"# {inputString}"

    # - - - - - - - - - -

    # line 2 - concepts

    # starting with string for easy appending, will later split into array
    line2 = ''

    logging.debug(parserOutput)

    # array containing the indices of final row 2 words, in wxArray.
    line2index = []

    # iterate through wx array, using while and counter
    count = 0

    while count < len(wxArray):
        val = wxArray[count]
        logging.debug(f'at word {val}.')
        logging.debug(f'Parser output for {val}: {parserOutput[count]}')
        # skip if lwg__psp
        if (parserOutput[count][7] == 'lwg__psp'):
            logging.debug(f'{val}: lwg__psp. Skipping.')
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
            logging.debug(f'VM found: {val}')
            # scan ahead to get the entire verb group
            # append to line2index of not preceeded by + or -
            if (line2[-1] not in ('+', '-')):
                line2index.append(count)
            verbGroup = ''
            verbCount = count
            while (parserOutput[verbCount][3] in ('VM', 'VAUX', 'VAUX_CONT')):
                verbGroup = ' '.join((verbGroup, wxArray[verbCount])).strip()
                verbCount += 1
            logging.debug(f'Searching {verbGroup} in TAM.')
            searchTAM = search_TAM(verbGroup)
            if (bool(searchTAM)):
                line2 = ''.join((line2, searchTAM, ','))
            else:
                line2 = ''.join((line2, val, '_1,'))
            logging.debug(f'line2: {line2}')
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
        line3Array.append(index+1)
    
    line3String = ",".join(str(x) for x in line3Array)

    # - - - - - - - - - -

    # line 4 - semantic category of nouns

    line4Array = []
    for index, value in enumerate(line2Array):
        line4Array.append('')
    
    line4String = ",".join(str(x) for x in line4Array)

    # - - - - - - - - - -

    # line 5 - GNP info

    line5Array = []
    for index, value in enumerate(line2Array):
        line5Array.append('')
    
    line5String = ",".join(str(x) for x in line5Array)

    # - - - - - - - - - -

    # line 6 - dependency relations

    line6Array = []
    for index, value in enumerate(line2Array):
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
    for index, value in enumerate(line2Array):
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
    if (wxString[-1] == '?'):
        line10 = 'interrogative'
    elif (wxString[-1] in ("|", "।", ".")):
        line10 = 'affirmative'
    # print(line10)

    returnDict = {
        'line1': line1String,
        'line2': line2Array,
        'line3': line3Array,
        'line4': line4Array,
        'line5': line5Array,
        'line6': line6Array,
        'line7': line7Array,
        'line8': line8Array,
        'line9': line9Array,
        'line10': line10
    }

    return returnDict

if __name__ == "__main__":
    print(main(input))