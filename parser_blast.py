from aligment import Aligment
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from collections import defaultdict

class Parser_blast:
    def __init__(self,file_name):
        self.file = file_name

    def generate_xml_tree(self):
        title = []
        length = []
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
            self.hits_content.append(h)
        for i in self.hits_content:
                title.append(i[2].text)
                length.append(i[4].text)

        self.hit_hsps = [self.hits_content[z][5] for z in range(len(self.hits_content))]
        self.hsps = [self.hit_hsps[z][0] for z in range(len(self.hit_hsps))]
        self.hsps_content = []
        for i in self.hsps:
            h = []
            for j in i:
                h.append(j)
            self.hsps_content.append(h)
        self.procents = []
        self.identities = []
        for i, hsps in enumerate(self.hsps_content):
            procent = "{0:.2f}".format(int(hsps[10].text)/int(hsps[13].text) *100)
            procent = float(procent)
            self.procents.append(int(procent))
            self.identities.append(int(hsps[10].text))
            self.aligns.append(Aligment(title[i],length[i],hsps[1].text,procent,hsps[12].text,hsps[10].text,hsps[13].text,re.sub('\n'," ",hsps[14].text),re.sub('\n'," ",hsps[15].text),re.sub('\n'," ",hsps[16].text)))

        # for i in self.aligns:
        #     print("Title: ", i.title)
        #     print("Align_length: ",i.align_length)
        #     print("Identities: ", i.identities)
        #     print("Procent: ", i.correct_procent)
        #     print("Gap: ",i.gap)
        #     # print(i.qseq)
        #     # print(i.k)
        #     # print(i.hseq)


        self.data_dict = []

        for i in self.aligns:
            self.data_dict.append({"Title":i.title,"Gap":i.gap,"Identities":i.identities,"Bit score": i.bit_score,"Procent":i.correct_procent})

    def group_to_predicted(self):
        self.predicted = []
        self.rest = []
        self.synthetic = []
        for align in self.aligns:
            if re.search("PREDICTED:",align.title):
                self.predicted.append(align)
                #print(align)
            elif re.search("Synthetic construct",align.title):
                self.synthetic.append(align)
            else:
                print(align)
                self.rest.append(align)

    def divide_to_species(self):
        species = defaultdict(list)
        titles = []
        for i in self.rest:
            titles.append(i.title.split(" "))
        print(titles[20])
        #print(titles)
        z =0
        for i in range(len(titles)):
            for j in range(i,len(titles)):
                if titles[i][0]==titles[j][0] and titles[i][1] == titles[j][1]:
                    if " ".join(titles[i]) not in species[" ".join(titles[i][:2])].title:
                        species[" ".join(titles[i][:2])].append(self.rest[i])
                    if " ".join(titles[j]) not in species[" ".join(titles[j][:2])].title:
                        species[" ".join(titles[j][:2])].append(self.rest[j])
                    else:
                        print("aloo")
        #         if titles[i][0] == titles[j][0] and titles[i][1] == titles[j][1]:
        #             print(i, titles[i])
                    # print(titles[i][0], titles[j])
                    # if titles[i] not in species[" ".join(titles[i][:2])]:
                    #     species[" ".join(titles[i][:2])].append(" ".join(titles[i]))
                    # if titles[j] not in species[" ".join(titles[i][:2])]:
                    #     species[" ".join(titles[i][:2])].append(" ".join(titles[j]))
        print(len(species["Homo sapiens"]))
        # print(z)
        print(species.keys())



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

p = Parser_blast('data.xml')
p.generate_xml_tree()
p.group_to_predicted()
p.divide_to_species()