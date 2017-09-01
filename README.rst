pyplwnxml
=============================

Parser for plwnxml (format of polish wordnet, słowosieć, http://nlp.pwr.wroc.pl/plwordnet/download/).

-----

Usage example
----------------------------
::

    from pyplwnxml import PlwnxmlParser

    WORDNET_LOCATION = "plwordnet-3.0.xml"

    if __name__ == "__main__":
        wordnet = PlwnxmlParser(WORDNET_LOCATION).read_wordnet()
        for lu in wordnet.lemma("zły")[0].synsets[0].lexical_units:
            print(lu.name)

Will print::

    zły
    niedobry
Installation
----------------------------
::
pip install 
-----
Tested with Słowosieć 3.0 and Python 3.6.1
