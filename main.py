from __future__ import unicode_literals
import logging
from isc_parser import Parser
from wxconv import WXC
import requests, json
import threading

# setting up debug
logging.basicConfig(level=logging.DEBUG)

con = WXC(order="utf2wx")

parser = Parser(lang='hin')

input = u"सूर्यास्त के बाद आकाश को देखना कितना अच्छा लगता है ।"
morphURL = "https://ssmt.iiit.ac.in/samparkuniverse"

def toWx(inputString):
    logging.debug("converting to wx.")

    # returns wx STRING
    return con.convert(inputString)

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

def main():
    # print(toWx(input))
    # print(getMorph(input)["morphOut"])
    # print(parse(input))

    # line 1 - original sentence
    print(f"# {input}")
    # line 2 - concepts
    # line 3 - concepts index
    # line 4 - semantic category of nouns
    # line 5 - GNP info
    # line 6 - dependency relations
    # line 7 - discourse elements
    # line 8 - speaker's view points
    # line 9 - scope
    # line 10 - sentence type

if __name__ == "__main__":
    main()