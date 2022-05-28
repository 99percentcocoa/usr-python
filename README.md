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
