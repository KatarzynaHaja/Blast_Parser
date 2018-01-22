from aligment import Aligment
import xml.etree.ElementTree as ET
import pandas as pd

class Parser_blast:
    def __init__(self,file_name):
        print("jestem w init")
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

        for i, hsps in enumerate(self.hsps_content):
            procent = int(hsps[10].text)/int(hsps[13].text)
            self.aligns.append(Aligment(title[i],length[i],hsps[1].text,procent,hsps[12].text,hsps[10].text,hsps[13].text,hsps[14].text,hsps[15].text))
        print(self.aligns)

        self.data_dict = []

        for i in self.aligns:
            self.data_dict.append({"Title":i.title,"Gap":i.gap,"Identities":i.identities,"Bit score": i.bit_score,"Procent":i.correct_procent})



    def export_to_excel(self):

        df = pd.DataFrame(self.data_dict)
        writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()


# p = Parser('data.xml')
# p.generate_xml_tree()
# p.find_tags()