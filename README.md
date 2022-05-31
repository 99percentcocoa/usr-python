# Installation

Install iscnlp-tagger, and then iscnlp-parser:
Follow the instructions in the following links:

[iscnlp / pos-tagger](https://bitbucket.org/iscnlp/pos-tagger/src/master/)

[iscnlp / parser](https://bitbucket.org/iscnlp/parser/src/master/)

Clone the project:

```git clone https://github.com/99percentcocoa/usr_python.git```

```cd usr_python```

```sudo pip install -r requirements.txt```

```sudo pip install .```

# Usage

Import the package in your project using

```from usr_python import main```

The USR function can then be called by `main.getUSR(input)`, where `input` is the Hindi string whose USR is to be generated.

Output will be a python dictionary containing the sentence's USR representation.

- - -

## Example output:

Input:

```
"सूर्यास्त के बाद आकाश को देखना कितना अच्छा लगता है।"
```

Output:

```
{
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
}
```