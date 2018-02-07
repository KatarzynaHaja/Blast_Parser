import unittest
from parser_blast import ParserBlast
from main_alignment import MainAlignment
import re


class TestParser(unittest.TestCase):

    def test_generate_xml_tree_good(self):
        p = ParserBlast("good_file.xml")
        p.generate_xml_tree()
        self.assertTrue(len(p.main_alignments) != 0)

    def test_generate_xml_tree_bad(self):
        p = ParserBlast("bad_file.xml")
        p.generate_xml_tree()
        self.assertRaises(IndexError)
        self.assertTrue(len(p.main_alignments) == 0)

    def test_group_to_class_all_fill(self):
        p = ParserBlast("group_to_class_all.xml")
        p.generate_xml_tree()
        p.group_to_classes()
        self.assertTrue(len(p.rest) != 0 and len(p.synthetic) != 0 and len(p.predicted) != 0 and len(p.weird) != 0)

    def test_group_to_class_synthetic_all_good(self):
        p = ParserBlast("group_to_class_all.xml")
        p.generate_xml_tree()
        p.group_to_classes()
        values = [re.search("Synthetic", i.title) for i in p.synthetic]
        self.assertNotIn(None, values)

    def test_more_hsp(self):
        p = ParserBlast("more_hsp.xml")
        p.generate_xml_tree()
        self.assertTrue(len(p.main_alignments[0].alignments) != 1)

    def test_one_hsp(self):
        p = ParserBlast("good_file.xml")
        p.generate_xml_tree()
        self.assertTrue(len(p.main_alignments[0].alignments) == 1)

    def test_group_to_class_synthetic_one_bad(self):
        p = ParserBlast("group_to_class_all.xml")
        p.generate_xml_tree()
        p.group_to_classes()
        p.synthetic.append(MainAlignment("Bad example", "123"))
        values = [re.search("Synthetic", i.title) for i in p.synthetic]
        self.assertIn(None, values)

    def test_divided_to_species_number_uniq(self):
        p = ParserBlast("divided_to_species.xml")
        p.generate_xml_tree()
        p.group_to_classes()
        p.divide_to_species()
        self.assertTrue(len(p.species) == 2)

    def test_divided_to_species_count(self):
        p = ParserBlast("divided_to_species.xml")
        p.generate_xml_tree()
        p.group_to_classes()
        p.divide_to_species()
        count = 0
        for i in p.species.keys():
            count += len(p.species[i])
        self.assertEqual(count, 3)

    def test_divided_to_species_predicted_number_uniq(self):
        p = ParserBlast("divided_to_species.xml")
        p.generate_xml_tree()
        p.group_to_classes()
        p.divide_to_species_predicted()
        self.assertTrue(len(p.species_predicted) == 3)

    def test_divided_to_species_predicted_count(self):
        p = ParserBlast("divided_to_species.xml")
        p.generate_xml_tree()
        p.group_to_classes()
        p.divide_to_species_predicted()
        count = 0
        for i in p.species_predicted.keys():
            count += len(p.species_predicted[i])
        self.assertEqual(count, 4)

    def test_divided_to_species_predicted_names(self):
        p = ParserBlast("divided_to_species.xml")
        p.generate_xml_tree()
        p.group_to_classes()
        p.divide_to_species_predicted()
        keys = sorted(['Pan troglodytes', "Pongo abelii", "Nomascus leucogenys"])
        self.assertListEqual(sorted(p.name_of_species_predicted), keys)

    def test_divided_to_species__names(self):
        p = ParserBlast("divided_to_species.xml")
        p.generate_xml_tree()
        p.group_to_classes()
        p.divide_to_species()
        keys = sorted(['Homo sapiens', "Nomascus leucogenys"])
        self.assertListEqual(sorted(p.name_of_species), keys)

if __name__ == '__main__':
    unittest.main()