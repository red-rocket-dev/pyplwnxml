from unittest import TestCase

from pyplwnxml import PlwnxmlParser, PartOfSpeech, SentimentType, Qualifier, RelationType


class TestPlwnxmlParser(TestCase):
    def setUp(self):
        parser = PlwnxmlParser("test_file.xml")
        self.wordnet = parser.read_wordnet()

    def test_basic_field_rewriting(self):
        self.assertEqual(len(self.wordnet.synsets), 2)
        self.assertEqual(len(self.wordnet.lexical_units), 5)

        lemma_331 = self.wordnet.lemma_id(331)
        self.assertIsNotNone(lemma_331)
        self.assertEqual(lemma_331.id, 331)
        self.assertEqual(lemma_331.name, "jabłecznik")
        self.assertEqual(lemma_331.part_of_speech, PartOfSpeech.NOUN)
        self.assertEqual(lemma_331.tag_count, 0)
        self.assertEqual(lemma_331.description, "##K: og. apple pie")
        self.assertEqual(lemma_331.work_state, "Testing..")
        self.assertEqual(lemma_331.source, "source test")
        self.assertEqual(lemma_331.variant, "1")

    def test_lu_synset_relation(self):
        lemma_332 = self.wordnet.lemma_id(332)
        self.assertIsNotNone(lemma_332)
        self.assertEqual(lemma_332.id, 332)
        self.assertEqual(lemma_332.name, "szarlotka")
        synsets_332 = lemma_332.synsets
        self.assertEqual(len(synsets_332), 1)
        self.assertEqual(lemma_332.synsets[0].id, 111)

    def test_lu_relations(self):
        lemma_333 = self.wordnet.lemma_id(333)
        hypernyms = lemma_333.relations[RelationType.HYPERNYMS]
        self.assertEqual(len(hypernyms), 2)

        relation_ids = [relation.id for relation in hypernyms]

        self.assertIn(331, relation_ids)
        self.assertIn(332, relation_ids)

    def test_sentiment(self):
        list_wypiek = self.wordnet.lemma("wypiek")
        self.assertEqual(len(list_wypiek), 1)
        lemma_wypiek = list_wypiek[0]
        self.assertEqual(lemma_wypiek.name, "wypiek")
        self.assertIsNotNone(lemma_wypiek.sentiment)
        self.assertEqual(lemma_wypiek.sentiment.type, SentimentType.NEUTRAL)
        self.assertEqual(len(lemma_wypiek.sentiment.feelings), 0)

        list_burrito = self.wordnet.lemma("burrito")
        self.assertEqual(len(list_burrito), 1)
        lemma_burrito = list_burrito[0]
        self.assertEqual(lemma_burrito.name, "burrito")
        self.assertIsNotNone(lemma_burrito.sentiment)
        self.assertEqual(lemma_burrito.sentiment.type, SentimentType.STRONGLY_NEGATIVE)
        self.assertEqual(lemma_burrito.sentiment.feelings, {"example"})

    def test_qualifier(self):
        list_ciasto = self.wordnet.lemma("ciasto")
        self.assertEqual(len(list_ciasto), 1)
        lemma_ciasto = list_ciasto[0]
        self.assertEqual(lemma_ciasto.name, "ciasto")
        self.assertIsNotNone(lemma_ciasto.qualifier)
        self.assertEqual(lemma_ciasto.qualifier, Qualifier.GENERAL)
