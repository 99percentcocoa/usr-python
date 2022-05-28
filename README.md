# Installation

Install iscnlp-tagger, and then iscnlp-parser:
Follow the instructions in the following links:

[iscnlp / pos-tagger](https://bitbucket.org/iscnlp/pos-tagger/src/master/)

[iscnlp / parser](https://bitbucket.org/iscnlp/parser/src/master/)

Install the following packages:

Flask: ```pip install flask```

Requests: ```pip install requests```

wxconv: ```pip install wxconv```

# Usage

With the `main.py` file in your project directory, import it in the required file using

```import main```

The USR function can then be called by `main.getUSR[input]`, where `input` is the Hindi string whose USR is to be generated.

Output will be a python dictionary containing the sentence's USR representation.

- - -

## Example output:

Input:

```"सूर्यास्त के बाद आकाश को देखना कितना अच्छा लगता है।
आप उनकी गणना नहीं कर सकते।
इनमें से कुछ टिमटिमाते प्रतीत होते हैं।
ये बिना किसी टिमटिमाहट के चंद्रमा के समान चमकते हैं।"```

Output:

```{
    "sentence_1": {
        "original": "# सूर्यास्त के बाद आकाश को देखना कितना अच्छा लगता है।",
        "concepts": [
            "sUryAswa_1",
            "AkASa_1",
            "xeKa_1-nA_cAhawA_hE_1",
            "kiwanA_1",
            "acCA+laga_1-wA_hE_1"
        ],
        "concepts_index": [
            "1",
            "2",
            "3",
            "4",
            "5"
        ],
        "semantic": [
            "",
            "",
            "",
            "",
            ""
        ],
        "gnp": [
            "",
            "[m sg a]",
            "[m sg -]",
            "",
            ""
        ],
        "dependency": [
            "0:k7t",
            "3:k2",
            "",
            "6:mod",
            ""
        ],
        "discourse": [
            "",
            "",
            "",
            "",
            ""
        ],
        "speaker_viewpoints": [
            "",
            "",
            "",
            "",
            ""
        ],
        "scope": [
            "",
            "",
            "",
            "",
            ""
        ],
        "sentence_type": "affirmative"
    },
    "sentence_2": {
        "original": "# आप उनकी गणना नहीं कर सकते।",
        "concepts": [
            "Apa_1",
            "unakI_1",
            "gaNanA+nahIM_1",
            "kara _1-0_sakawA_hE_1"
        ],
        "concepts_index": [
            "1",
            "2",
            "3",
            "4"
        ],
        "semantic": [
            "",
            "",
            "",
            "",
            ""
        ],
        "gnp": [
            "[m sg a]",
            "[m sg ]",
            "",
            "",
            ""
        ],
        "dependency": [
            "0:k1",
            "",
            "",
            "3:lwg__neg",
            ""
        ],
        "discourse": [
            "",
            "",
            "",
            ""
        ],
        "speaker_viewpoints": [
            "",
            "",
            "",
            "3:neg",
            ""
        ],
        "scope": [
            "",
            "",
            "",
            ""
        ],
        "sentence_type": "negative"
    },
    "sentence_3": {
        "original": "# इनमें से कुछ टिमटिमाते प्रतीत होते हैं।",
        "concepts": [
            "inameM_1",
            "kuCa_1",
            "timatimA_1-wA_hE_1",
            "prawIwa+ho_1-wA_hE_1"
        ],
        "concepts_index": [
            "1",
            "2",
            "3",
            "4"
        ],
        "semantic": [
            "",
            "",
            "",
            ""
        ],
        "gnp": [
            "[m sg a]",
            "[  ]",
            "[m sg a]",
            ""
        ],
        "dependency": [
            "0:k5",
            "2:k2",
            "",
            ""
        ],
        "discourse": [
            "",
            "",
            "",
            ""
        ],
        "speaker_viewpoints": [
            "",
            "",
            "",
            ""
        ],
        "scope": [
            "",
            "",
            "",
            ""
        ],
        "sentence_type": "affirmative"
    },
    "sentence_4": {
        "original": "# ये बिना किसी टिमटिमाहट के चंद्रमा के समान चमकते हैं।",
        "concepts": [
            "ye_1",
            "binA_1",
            "kisI_1",
            "timatimAhata_1",
            "caMxramA_1",
            "samAna+camaka_1-wA_hE_1"
        ],
        "concepts_index": [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6"
        ],
        "semantic": [
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "gnp": [
            "",
            "",
            "",
            "[m sg a]",
            "[m sg -]",
            ""
        ],
        "dependency": [
            "0:mod",
            "",
            "",
            "3:r6",
            "5:r6",
            ""
        ],
        "discourse": [
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "speaker_viewpoints": [
            "",
            "1:binA",
            "",
            "",
            "",
            ""
        ],
        "scope": [
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "sentence_type": "affirmative"
    }
}```
