from collections import defaultdict

from pyplwnxml.enums import Domain, PartOfSpeech, Qualifier, SentimentType


class BasicUnit:
    """
    class consisting of fields common for lexical unit and
    """

    def __init__(self, id, description):
        """
        constructor
        :param id: id
        :param description: description
        """
        self.id = id
        self.description = description
        self.relations = defaultdict(list)


class Sentiment:
    """
    sentiment information extracted from lexical unit's description
    """

    def __init__(self, feelings: set, type: SentimentType):
        """
        constructor
        :param feelings: all feelings listed in description of lexical unit
        :param type: sentiment type
        """
        self.feelings = feelings
        self.type = type

    def __repr__(self) -> str:
        return "<{} - sentiment_type:{} feelings:{}>".format(self.__class__.__name__, self.type,
                                                             self.feelings)

    def __str__(self) -> str:
        return self.type.value


class LexicalUnit(BasicUnit):
    """
    information about lexical unit
    """

    def __init__(self, id: int, name: str, part_of_speech: PartOfSpeech, qualifier: Qualifier, sentiment: Sentiment,
                 tag_count: int, domain: Domain, description: str, work_state: str, source: str, variant: int) -> None:
        """
        constructor
        :param id: lu's id
        :param name: name
        :param description: description
        :param part_of_speech: part of speech of lu
        :param qualifier: qualifier
        :param sentiment: sentiment
        :param tag_count: tag count
        :param domain: domain
        :param work_state: workstate
        :param source: source
        :param variant: variant
        """
        super().__init__(id, description)
        self.name = name
        self.part_of_speech = part_of_speech
        self.tag_count = tag_count
        self.domain = domain
        self.work_state = work_state
        self.source = source
        self.variant = variant
        self.qualifier = qualifier
        self.sentiment = sentiment
        self.synsets = []

    def __repr__(self) -> str:
        return "<{} - id:{},name:{},pos:{},domain:{},sentiment:{}>" \
            .format(self.__class__.__name__,
                    self.id, self.name,
                    self.part_of_speech, self.domain,
                    self.sentiment.type if self.sentiment else None)


class Synset(BasicUnit):
    """
    information about synset
    """

    def __init__(self, id: int, work_state: str, split: int, definition: str, description: str, abstract: bool) -> None:
        """
        constructor
        :param id:  id
        :param work_state: work state
        :param split: value of split field
        :param definition: definition
        :param description: description
        :param abstract: abstract
        """
        super().__init__(id, description)
        self.work_state = work_state
        self.split = split
        self.definition = definition
        self.abstract = abstract
        self.lexical_units = []

    def __repr__(self):
        return "<{} - id:{},lexical_units:{}>" \
            .format(self.__class__.__name__, self.id,
                    ",".join(["'{}'".format(unit.name) for unit in self.lexical_units]))


class Wordnet:
    def __init__(self, lexical_units: dict, synsets: dict) -> None:
        """
        constructor
        :param lexical_units: lexical units
        :param synsets: synsets
        """
        self.__lexical_units_by_file_id = lexical_units
        self.__lexical_units_by_name = defaultdict(list)
        for lex_id, lexical_unit in lexical_units.items():
            self.__lexical_units_by_name[lexical_unit.name].append(lexical_unit)
        self.__synsets_by_id = synsets

    @property
    def lexical_units(self) -> list:
        """
        returns all lexical units
        :return: lexical units
        """
        return list(self.__lexical_units_by_file_id.values())

    @property
    def synsets(self) -> list:
        """
        Returns all synsets
        :return: synsets
        """
        return list(self.__synsets_by_id.values())

    def lemma(self, name: str) -> dict:
        """
        selects lexical unit by name
        :param name: lexical unit's name
        :return:
        """
        return self.__lexical_units_by_name[name]

    def lemma_id(self, lu_id: str) -> LexicalUnit:
        """
        selects lemma by lexical unit's id
        :param lu_id:
        :return: lexical unit of given id
        """
        return self.__lexical_units_by_file_id[lu_id]

    def synset(self, synset_id: int):
        """
        selects synset by synset's id
        :param synset_id:
        :return: synset of given id
        """
        return self.__synsets_by_id[synset_id]

    def synset_count(self):
        """
        returns amount of synsets
        :return: amount of synsets
        """
        return len(self.__synsets_by_id)
