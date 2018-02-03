from alignment import Alignment
from main_alignment import Main_alignment
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from collections import defaultdict
import os

class Parser_blast:
    def __init__(self,file_name):
        self.file = file_name

    def generate_xml_tree(self):
        try:
            title = []
            length = []
            self.main_alignments = []
            self.aligns = []
            tree = ET.parse(self.file)
            self.root = tree.getroot()
            self.blast_output = self.root[8]
            self.iteration = self.blast_output[0]
            self.iteration_hit = self.iteration[4]
            self.hits = []
            for i in self.iteration_hit:
                self.hits.append(i)
            self.hits_content = []
            for i in self.hits:
                h = []
                for j in i :
                    h.append(j)

                for hsp in h[5]:
                    procent = "{0:.2f}".format(int(hsp[10].text) / int(hsp[13].text) * 100)
                    procent = float(procent)
                    self.aligns.append(
                        Alignment(h[2].text, h[4].text, hsp[1].text, procent, hsp[12].text, hsp[10].text, hsp[13].text,
                                  re.sub('\n', " ", hsp[14].text), re.sub('\n', " ", hsp[15].text),
                                  re.sub('\n', " ", hsp[16].text)))
                self.main_alignments.append(Main_alignment(i[1].text, i[2].text,self.aligns))
                self.aligns = []

            print(len(self.main_alignments[0].alignments))
        except IndexError:
            "Bad file."

            self.data_dict = []


        # for i in self.aligns:
        #     self.data_dict.append({"Title":i.title,"Gap":i.gap,"Identities":i.identities,"Bit score": i.bit_score,"Procent":i.correct_procent})

    def get_data(self):
        self.procents = []
        self.identities = []
        for i in self.main_alignments:
            for j in i:
                self.procents.append(j.correct_procent)
                self.identities.append(j.identities)

    def group_to_classes(self):
        self.predicted = []
        self.rest = []
        self.synthetic = []
        self.weird = []
        for hit in self.main_alignments:
                if re.search("PREDICTED:",hit.title):
                    self.predicted.append(hit)
                elif re.search("Synthetic construct",hit.title):
                    self.synthetic.append(hit)
                elif re.match(re.compile(r'\b[A-Z]{1}.*\b'),hit.title):
                    self.rest.append(hit)
                else:
                    self.weird.append(hit)

    def divide_to_species(self):
        self.name_of_species = []
        self.species = defaultdict(list)
        titles = []
        for i in self.rest:
            titles.append(i.title.split(" "))
        z =0
        for i in range(len(titles)):
            for j in range(i,len(titles)):
                if titles[i][0]==titles[j][0] and titles[i][1] == titles[j][1]:
                    if " ".join(titles[i]) not in [z.title for z in self.species[" ".join(titles[i][:2])]]:
                        self.species[" ".join(titles[i][:2])].append(self.rest[i])
                    if " ".join(titles[j]) not in [z.title for z in self.species[" ".join(titles[j][:2])]]:
                        self.species[" ".join(titles[j][:2])].append(self.rest[j])

        # for s,k in self.species.items():
        #     print()
        #     print(s)
        #     for i in k:
        #         print(i.title, len(i.alignments))
        #         for t in i.alignments:
        #             print(t)
        #             print(t.print_sequence())
        self.name_of_species = list(self.species.keys())
        print("Diffrent species", len(self.name_of_species))
        print("Statistic")

    def divide_to_species_predicted(self):
        self.name_of_species_predicted = []
        self.species_predicted = defaultdict(list)
        titles = []
        for i in self.predicted:
            titles.append(i.title.split(" "))
        print(len(titles))
        for i in range(len(titles)):
            for j in range(i, len(titles)):
                if titles[i][1] == titles[j][1] and titles[i][2] == titles[j][2]:
                    if " ".join(titles[i]) not in [z.title for z in self.species_predicted[" ".join(titles[i][1:3])]]:
                        self.species_predicted[" ".join(titles[i][1:3])].append(self.predicted[i])
                    if " ".join(titles[j]) not in [z.title for z in self.species_predicted[" ".join(titles[j][1:3])]]:
                        self.species_predicted[" ".join(titles[j][1:3])].append(self.predicted[j])



        # for s,k in self.species_predicted.items():
        #     print()
        #     print(s)
        #     for i in k:
        #         print(i.title, len(i.alignments))
        #         for t in i.alignments:
        #                 print(t)
        #                 print(t.print_sequence())
        self.name_of_species_predicted = list(self.species_predicted.keys())
        print(len(self.name_of_species_predicted))

    def print_synthetic(self):
        for i in self.synthetic:
            print(i.title)
            for j in i.alignments:
                print(j)
                print(j.print_sequence())

    def print_weird(self):
        for i in self.weird:
            print(i.title)
            for j in i.alignments:
                print(j.print_sequence())



    def export_to_excel(self):

        df = pd.DataFrame(self.data_dict)
        writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()

    def generate_chart_percent(self):
        print(self.procents)
        plt.hist(self.procents, bins='auto',color='yellow')
        plt.title("Histogram of percent")
        plt.show()

    def generate_chart_identities(self):
        plt.hist(self.identities, bins='auto', color='yellow')
        plt.title("Histogram of identities")
        plt.show()

    def generate_plot_identities(self):
        plt.plot(np.arange(len(self.identities)),self.identities)
        plt.title("Identities")
        plt.show()

    def generate_plot_percent(self):
        plt.plot(np.arange(len(self.procents)), self.procents)
        plt.title("Identities")
        plt.show()

# p = Parser_blast(os.path.join("files",'data.xml'))
# p.generate_xml_tree()
# p.group_to_classes()
# print("Divided to species")
# p.divide_to_species()
# print("____________________________________________________________________")
# print("Divided to species when predicted")
# p.divide_to_species_predicted()
# print("_______________________________________________________________________")
# print("Synthetic")
# p.print_synthetic()
# print("__________________________________________________________________________")
# print("Rest")
# p.print_weird()