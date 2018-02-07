from alignment import Alignment
from main_alignment import MainAlignment
import xml.etree.ElementTree as et
import pandas as pd
import re
from collections import defaultdict
from operator import itemgetter
from colorama import Fore, Style


class ParserBlast:
    def __init__(self, file_name):
        """
        :param file_name: file name from program takes data
        """
        self.file = file_name
        self.gaps = []
        self.main_alignments = []
        self.aligns = []
        self.hits = []
        self.root = []
        self.blast_output = []
        self.iteration = []
        self.iteration_hit = []
        self.hits_content = []
        self.gaps_count = {}
        self.aligns = []
        self.predicted = []
        self.rest = []
        self.synthetic = []
        self.weird = []
        self.name_of_species = []
        self.species = defaultdict(list)
        self.count_species = {}
        self.name_of_species_predicted = []
        self.species_predicted = defaultdict(list)
        self.count_species_predicted = {}

    def generate_xml_tree(self):
        """
        Try to parse xml, generate tree with xml tags and then cast it to mainAligment object and Alignment
        :return: exception when file has't got correct content
        """
        try:
            tree = et.parse(self.file)
            self.root = tree.getroot()
            self.blast_output = self.root[8]
            self.iteration = self.blast_output[0]
            self.iteration_hit = self.iteration[4]

            for i in self.iteration_hit:
                self.hits.append(i)

            for i in self.hits:
                h = []
                for j in i:
                    h.append(j)

                for hsp in h[5]:
                    procent = "{0:.2f}".format(int(hsp[10].text) / int(hsp[13].text) * 100)
                    procent = float(procent)
                    self.aligns.append(Alignment(h[2].text,
                                                 hsp[1].text,
                                                 procent,
                                                 hsp[12].text,
                                                 hsp[10].text,
                                                 hsp[13].text,
                                                 hsp[14].text,
                                                 hsp[15].text,
                                                 hsp[16].text))
                self.main_alignments.append(MainAlignment(i[2].text,
                                                          self.aligns))
                self.aligns = []
        except IndexError:
            "Bad file."
            raise

    def group_to_classes(self):
        """
        Function divided all alignemnts into groups:
        - normal group ( example: Homo sapiens breast and ovarian cancer susceptibility (BRCA1) mRNA, complete cds)
        - predicted group (they start with "predicted" word)
        - synthetic group (they start with "synthetic" word)
        - weird group (this group contain alignments which are "weird" it has non regular content)
        """
        for hit in self.main_alignments:
                if re.search("PREDICTED:", hit.title):
                    hit.predicted = "True"
                    self.predicted.append(hit)
                elif re.search("Synthetic construct", hit.title):
                    hit.synthetic = "True"
                    self.synthetic.append(hit)
                elif re.match(re.compile(r'\b[A-Z].*\b'), hit.title):
                    self.rest.append(hit)
                else:
                    self.weird.append(hit)

    def divide_to_species(self):
        """
        Function divide all normal alignments to species
        Algorithm:
         - in biology names of species consist 2 words
         - if 2 names are the same on first and second place it belong to one species
        """
        titles = []
        for i in self.rest:
            titles.append(i.title.split(" "))
        for i in range(len(titles)):
            for j in range(i, len(titles)):
                if titles[i][0] == titles[j][0] and titles[i][1] == titles[j][1]:
                    if " ".join(titles[i]) not in [z.title for z in self.species[" ".join(titles[i][:2])]]:
                        self.rest[i].species = " ".join(titles[i])
                        self.species[" ".join(titles[i][:2])].append(self.rest[i])
                    if " ".join(titles[j]) not in [z.title for z in self.species[" ".join(titles[j][:2])]]:
                        self.rest[j].species = " ".join(titles[j])
                        self.species[" ".join(titles[j][:2])].append(self.rest[j])

        self.name_of_species = list(self.species.keys())

        for i in self.species.keys():
            self.count_species[i] = len(self.species[i])

    def divide_to_species_predicted(self):
        """
           Function divide all predicted alignments to species
           Algorithm:
            - in biology names of species consist 2 words
            - if 2 names are the same on first and second place it belong to one species
       """
        titles = []
        for i in self.predicted:
            titles.append(i.title.split(" "))
        for i in range(len(titles)):
            for j in range(i, len(titles)):
                if titles[i][1] == titles[j][1] and titles[i][2] == titles[j][2]:
                    if " ".join(titles[i]) not in [z.title for z in self.species_predicted[" ".join(titles[i][1:3])]]:
                        self.predicted[i].species = " ".join(titles[i])
                        self.species_predicted[" ".join(titles[i][1:3])].append(self.predicted[i])
                    if " ".join(titles[j]) not in [z.title for z in self.species_predicted[" ".join(titles[j][1:3])]]:
                        self.predicted[j].species = " ".join(titles[j])
                        self.species_predicted[" ".join(titles[j][1:3])].append(self.predicted[j])

        for i in self.species_predicted.keys():
            self.count_species_predicted[i] = len(self.species_predicted[i])

        self.name_of_species_predicted = list(self.species_predicted.keys())

    def return_species(self):
        """
        This function return 2 dataFrames which consist name of species and number of alignments belong to them
        :return: dataFrames
        """
        r = pd.DataFrame([self.count_species]).T
        t = pd.DataFrame([self.count_species_predicted]).T

        return r.to_html(), t.to_html()

    def return_predicted_alignment(self):
        """
        Make dataFrames with information about predicted aligments, with divided to species
        :return: dataFrame and list of names od species
        """
        data_frames = []
        pred = defaultdict(list)
        for s, k in self.species_predicted.items():
            for i in k:
                for t in i.alignments:
                    pred[s].append({"Title": t.title,
                                    "Percent": t.correct_procent,
                                    "Gap": t.gap,
                                    "Score": t.bit_score,
                                    "Length": t.align_length,
                                    "Identities": t.identities})

        for i in pred.keys():
            pred[i] = sorted(pred[i], key=itemgetter('Percent'), reverse=True)
            df = pd.DataFrame(pred[i], columns=["Title",
                                                "Percent",
                                                "Score",
                                                "Length",
                                                "Gap",
                                                "Identities"])
            data_frames.append(df.to_html(index=False))
        return [data_frames, list(pred.keys())]

    def return_norm_alignment(self):
        """
         Make dataFrames with information about normal aligments, with divided to species
        :return: dataFrames and list of name of species
        """
        data_frames = []
        norm = defaultdict(list)
        for s, k in self.species.items():
            for i in k:
                for t in i.alignments:
                    norm[s].append({"Title": t.title,
                                    "Percent": t.correct_procent,
                                    "Gap": t.gap,
                                    "Score": t.bit_score,
                                    "Length": t.align_length,
                                    "Identities": t.identities})

        for i in norm.keys():
            norm[i] = sorted(norm[i], key=itemgetter('Percent'), reverse=True)
            df = pd.DataFrame(norm[i], columns=["Title",
                                                "Percent",
                                                "Score",
                                                "Length",
                                                "Gap",
                                                "Identities"])
            data_frames.append(df.to_html(index=False))

        return [data_frames, list(norm.keys())]

    @staticmethod
    def return_alignment(from_list, to_pdf):
        """
        :param from_list: from which file
        :param to_pdf: if result will be save as pdf
        :return: DataFrames
        """
        norm = []
        for hit in from_list:
            for align in hit.alignments:
                norm.append({"Title": align.title,
                             "Percent": align.correct_procent,
                             "Gap": align.gap,
                             "Score": align.bit_score,
                             "Length": align.align_length,
                             "Identities": align.identities})
        pd.set_option('display.max_colwidth', -1)
        if to_pdf:
            norm = sorted(norm, key=itemgetter('Percent'), reverse=True)
            df = pd.DataFrame(norm, columns=["Title",
                                             "Percent",
                                             "Score",
                                             "Length",
                                             "Gap",
                                             "Identities"])
            return df.to_html(index=False)
        else:
            norm = sorted(norm, key=itemgetter('Title'))
            df = pd.DataFrame(norm, columns=["Title",
                                             "Percent",
                                             "Score",
                                             "Length",
                                             "Gap",
                                             "Identities"])
            return df

    def print_sequence(self):
        """
        Printing all sequences
        """
        first = []
        second = []
        third = []
        for hit in self.main_alignments:
            for align in hit.alignments:
                print()
                print(Fore.GREEN + hit.title)
                print()
                print(Style.RESET_ALL)
                first = [align.qseq[i:i + 200] for i in range(0, len(align.qseq), 200)]
                second = [align.k[i:i + 200] for i in range(0, len(align.k), 200)]
                third = [align.hseq[i:i + 200] for i in range(0, len(align.hseq), 200)]

                for i in range(len(first)):
                        print(first[i])
                        print(second[i])
                        print(third[i])
