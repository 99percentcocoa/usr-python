from __future__ import unicode_literals
import logging
from isc_parser import Parser
from wxconv import WXC
import requests, json
import re
from itertools import islice
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
            

def main():

    # add space before final punctuation mark if none, using regex matching
    if (bool(re.search(r'(?<=[^ ])[।?]', input[-2:]))):
        inputFinalSeparated = input[:-1] + ' ' + input[-1:]
    else:
        inputFinalSeparated = input
    
    wxString = toWx(inputFinalSeparated)
    # logging.debug(wxString)

    wxArray = wxString.split(' ')
   #  logging.debug(wxArray)

    # parser run on inputFinalSeparated, not raw input
    # note, parser index corresponds to wxArray index
    parserOutput = parse(inputFinalSeparated)
    # logging.debug(parserOutput)

    # words not found in dictionary
    dictWarnings = []

    # line 1 - original sentence
    print(f"# {input}")

    # - - - - - - - - - -

    # line 2 - concepts

    # starting with string for easy appending, will later split into array
    line2 = ''

    logging.debug(parserOutput)

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
            count += 1
        # if symbol, don't append to line2
        elif (parserOutput[count][3] == 'SYM'):
            # line2 = line2 + val
            count += 1
        # if verb group then search entire verb group in TAM
        elif (parserOutput[count][3] == 'VM'):
            logging.debug(f'VM found: {val}')
            # scan ahead to get the entire verb group
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
            line2 = ''.join((line2, val, '_1,'))
            if (search_concept(val + "_1") == False):
                 dictWarnings.append(''.join((val, "_1")))
            count += 1
    
    # remove final comma
    if line2[-1] == ',':
        line2 = line2[:-1]
    
    line2Array = line2.split(',')
    print(line2Array)
    logging.debug(f'dict warnings: warnings: {dictWarnings}')

    # - - - - - - - - - -

    # line 3 - concepts index

    line3Array = []

    for index, value in enumerate(line2Array):
        line3Array.append(index+1)
    
    print(line3Array)

    # - - - - - - - - - -

    # line 4 - semantic category of nouns

    

    # - - - - - - - - - -

    # line 5 - GNP info

    # - - - - - - - - - -

    # line 6 - dependency relations

    # - - - - - - - - - -

    # line 7 - discourse elements

    # - - - - - - - - - -

    # line 8 - speaker's view points

    # - - - - - - - - - -

    # line 9 - scope

    # - - - - - - - - - -

    # line 10 - sentence type

if __name__ == "__main__":
    main()