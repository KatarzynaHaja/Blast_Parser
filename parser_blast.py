from alignment import Alignment
from main_alignment import Main_alignment
import xml.etree.ElementTree as ET
import pandas as pd

import numpy as np
import re
from collections import defaultdict
import os
from operator import itemgetter
from summary import Summary


class Parser_blast:
    def __init__(self,file_name):
        self.file = file_name

    def generate_xml_tree(self):
        try:
            self.gaps = []
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
            self.gaps_count = {}
            for i in self.hits:
                h = []
                for j in i:
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


        except IndexError:
            "Bad file."



    def group_to_classes(self):
        self.predicted = []
        self.rest = []
        self.synthetic = []
        self.weird = []
        for hit in self.main_alignments:
                if re.search("PREDICTED:", hit.title):
                    hit.predicted = "True"
                    self.predicted.append(hit)
                elif re.search("Synthetic construct",hit.title):
                    hit.synthetic = "True"
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
                        self.rest[i].species =  " ".join(titles[i])
                        self.species[" ".join(titles[i][:2])].append(self.rest[i])
                    if " ".join(titles[j]) not in [z.title for z in self.species[" ".join(titles[j][:2])]]:
                        self.rest[j].species = " ".join(titles[j])
                        self.species[" ".join(titles[j][:2])].append(self.rest[j])

        self.name_of_species = list(self.species.keys())

    def divide_to_species_predicted(self):
        self.name_of_species_predicted = []
        self.species_predicted = defaultdict(list)
        titles = []
        for i in self.predicted:
            titles.append(i.title.split(" "))
        # print(len(titles))
        for i in range(len(titles)):
            for j in range(i, len(titles)):
                if titles[i][1] == titles[j][1] and titles[i][2] == titles[j][2]:
                    if " ".join(titles[i]) not in [z.title for z in self.species_predicted[" ".join(titles[i][1:3])]]:
                        self.predicted[i].species = " ".join(titles[i])
                        self.species_predicted[" ".join(titles[i][1:3])].append(self.predicted[i])
                    if " ".join(titles[j]) not in [z.title for z in self.species_predicted[" ".join(titles[j][1:3])]]:
                        self.predicted[j].species = " ".join(titles[j])
                        self.species_predicted[" ".join(titles[j][1:3])].append(self.predicted[j])



        # for s,k in self.species_predicted.items():
        #     print()
        #     print(s)
        #     for i in k:
        #         print(i.title, len(i.alignments))
        #         for t in i.alignments:
        #                 print(t)

        self.name_of_species_predicted = list(self.species_predicted.keys())




    def return_predicted_alignment(self):
        data_frames = []
        pred = defaultdict(list)
        for s, k in self.species_predicted.items():
            for i in k:
                for t in i.alignments:
                    pred[s].append({"Title": t.title, "Percent": t.correct_procent, "Gap": t.gap})

        for i in pred.keys():
            pred[i] = sorted(pred[i], key=itemgetter('Percent'), reverse=True)
            data_frames.append(pd.DataFrame(pred[i]).to_html(index=False))
        return [data_frames, list(pred.keys())]


    def return_norm_alignment(self):
        data_frames = []
        norm = defaultdict(list)
        for s, k in self.species.items():
            for i in k:
                for t in i.alignments:
                    norm[s].append({"Title": t.title, "Percent": t.correct_procent, "Gap": t.gap})

        for i in norm.keys():
            norm[i] = sorted(norm[i], key=itemgetter('Percent'), reverse=True)
            data_frames.append(pd.DataFrame(norm[i]).to_html(index=False))
        print(norm.keys())
        return [data_frames, list(norm.keys())]

    def return_alignment(self,from_list, to_pdf):
        norm = []
        for hit in from_list:
            for align in hit.alignments:
                norm.append({"Title": align.title,
                             "Percent": align.correct_procent,
                             "Gap": align.gap,
                             "Score":align.bit_score})

        norm = sorted(norm, key=itemgetter('Percent'), reverse=True)
        pd.set_option('display.max_colwidth', -1)
        df = pd.DataFrame(norm)
        if to_pdf == True:
            return df.to_html(index=False)
        else:
            return df

    def print_sequence(self,align):
        first = [align.qseq[i:i + 200] for i in range(0, len(align.qseq), 200)]
        second = [align.k[i:i + 200] for i in range(0, len(align.k), 200)]
        third = [align.hseq[i:i + 200] for i in range(0, len(align.hseq), 200)]
        return [first, second, third]

    def export_to_excel(self):
        self.group_to_classes()
        self.divide_to_species()
        self.divide_to_species_predicted()
        s = Summary(self)
        writer = pd.ExcelWriter(os.path.join("xlsx","report.xlsx"), engine='xlsxwriter')
        self.return_alignment().to_excel(writer, sheet_name='All data')
        pred = self.return_predicted_alignment()
        index = 0
        for i in pred.keys():
            print(index)
            df = pd.DataFrame(pred[i])
            df.to_excel(writer, sheet_name="Predicted",startrow=index+2, startcol=0,index=False)
            worksheet = writer.sheets['Predicted']
            worksheet.write(index,0, i)
            index += len(pred[i]) + 2
        self.return_alignment(self.rest,False).to_excel(writer, sheet_name='Normal',index=False)
        self.return_alignment(self.synthetic,False).to_excel(writer, sheet_name='Synethic',index=False)
        s.summary(False).to_excel(writer,sheet_name="Summary",index=False)
        for i in writer.sheets:
            writer.sheets[i].set_column('D:D', 100)
        writer.save()


p = Parser_blast(os.path.join("files",'data.xml'))
p.generate_xml_tree()
p.group_to_classes()
p.divide_to_species()
# print("____________________________________________________________________")
# print("Divided to species when predicted")
p.divide_to_species_predicted()

# print("_______________________________________________________________________")
# print("Synthetic")
# p.print_synthetic()
# print("__________________________________________________________________________")
# print("Rest")
# p.print_weird()