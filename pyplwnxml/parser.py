import re
import xml.etree.ElementTree as ET

from pyplwnxml.enums import Domain, RelationType, PartOfSpeech, Qualifier, SentimentType
from pyplwnxml.utils import regex_escaped_joined_enum_values
from pyplwnxml.wordnet import LexicalUnit, Synset, Wordnet, Sentiment


class PlwnxmlParser:
    __LEXICAL_RELATIONS = 'lexicalrelations'
    __SYNSET_RELATIONS = 'synsetrelations'
    __SYNSET = 'synset'
    __LEXICAL_UNIT = 'lexical-unit'

    __FEELINGS_SPLIT_PATTERN = re.compile("[,;]")
    __QUALIFIER_PATTERN = re.compile("##K: ({})".format(regex_escaped_joined_enum_values(Qualifier)))
    __POSSIBLE_ENUM_SENTIMENT_VALUES = regex_escaped_joined_enum_values(SentimentType)
    __SENTIMENT_PATTERN = \
        re.compile(".*?##A\d\:\ {0,1}[{]{0,1}(?P<feelings>.*?)[}\)]{0,1}" +
                   " (?P<sentiment_type>{poss_sentiments})".format(poss_sentiments = __POSSIBLE_ENUM_SENTIMENT_VALUES), re.DOTALL)

    def __init__(self, input_path: str) -> None:
        self.__input_path = input_path

    def _process_lexical_units(self, lus_tags: list):
        lus = {}
        for lexical_unit_tag in lus_tags:
            lu_id = int(lexical_unit_tag.get('id'))
            lu_name = lexical_unit_tag.get('name')
            lu_domain = Domain(lexical_unit_tag.get('domain'))
            pos = PartOfSpeech(lexical_unit_tag.get('pos'))

            desc = lexical_unit_tag.get('desc')
            qualifier = self._extract_qualifier(desc)
            sentiment = self._extract_sentiment(desc)

            tag_count = int(lexical_unit_tag.get('tagcount'))
            lu = LexicalUnit(id=lu_id,
                             name=lu_name,
                             part_of_speech=pos,
                             qualifier=qualifier,
                             sentiment=sentiment,
                             tag_count=tag_count,
                             domain=lu_domain,
                             description=desc,
                             work_state=lexical_unit_tag.get('workstate'),
                             source=lexical_unit_tag.get('source'),
                             variant=lexical_unit_tag.get('variant'))
            lus[lu_id] = lu
        return lus

    def _extract_sentiment(self, desc):
        sentiment_finds = PlwnxmlParser.__SENTIMENT_PATTERN.finditer(desc)
        if not sentiment_finds:
            return None
        all_feelings = set()
        found = False
        for find in sentiment_finds:
            found = True
            sentiment_type_str = find['sentiment_type']
            feelings_find_str = find['feelings']
            feelings_find = {item.strip() for item in PlwnxmlParser.__FEELINGS_SPLIT_PATTERN.split(feelings_find_str) if item != ''}
            all_feelings |= feelings_find
        if not found:
            return None
        sentiment_type = SentimentType(sentiment_type_str)
        return Sentiment(all_feelings, sentiment_type)

    def _extract_qualifier(self, desc):
        qualifier_groups = PlwnxmlParser.__QUALIFIER_PATTERN.match(desc)
        if qualifier_groups is not None:
            qualifier_str = qualifier_groups.group(1)
            qualifier = Qualifier(qualifier_str)
        else:
            qualifier = None
        return qualifier

    def _process_synsets(self, synsets_tags: list, lus):
        synsets = {}
        for synset_tag in synsets_tags:
            synset_id = int(synset_tag.get("id"))
            synset_lus_ids = [int(unit.text) for unit in synset_tag.getchildren()]
            synsets[synset_id] = Synset(
                int(synset_tag.get("id")),
                synset_tag.get("workstate"),
                synset_tag.get("split"),
                synset_tag.get("definition"),
                synset_tag.get("desc"),
                synset_tag.get("abstract") == 'true')

            self._make_lu_synset_rels(synset_id, synset_lus_ids, synsets, lus)
        return synsets

    def _make_lu_synset_rels(self, synset_id, synset_lus_ids, synsets, lus):
        for lu_id in synset_lus_ids:
            lus[lu_id].synsets.append(synsets[synset_id])
            synsets[synset_id].lexical_units.append(lus[lu_id])

    def _process_relations(self, relations_tags, units_dict):
        for relation_tag in relations_tags:
            parent_id = int(relation_tag.get('parent'))
            child_id = int(relation_tag.get('child'))
            relation_type_id = int(relation_tag.get('relation'))
            relation_type = RelationType(relation_type_id)
            units_dict[child_id].relations[relation_type].append(units_dict[parent_id])

    def read_wordnet(self):
        tree_root = ET.parse(self.__input_path).getroot()

        lus_tags = tree_root.findall(PlwnxmlParser.__LEXICAL_UNIT)
        synsets_tags = tree_root.findall(PlwnxmlParser.__SYNSET)
        lexical_relations_tags = tree_root.findall(PlwnxmlParser.__LEXICAL_RELATIONS)
        synset_relations_tags = tree_root.findall(PlwnxmlParser.__SYNSET_RELATIONS)

        lus = self._process_lexical_units(lus_tags)
        synsets = self._process_synsets(synsets_tags, lus)
        self._process_relations(lexical_relations_tags, lus)
        self._process_relations(synset_relations_tags, synsets)

        return Wordnet(lus, synsets)
