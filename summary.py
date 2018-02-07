import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
from tkinter import *


class Summary:
    def __init__(self, p):
        """
        :param p: ParserBlast object
        """
        self.p = p
        self.procents = []
        self.identities = []
        self.length = []
        self.gaps = []
        self.score = []
        self.gaps_count = {}
        self.number_of_all = 0
        self.number_of_pred = 0
        self.number_of_normal = 0
        self.number_of_syntetic = 0
        self.number_of_weird = 0

    def get_data(self, from_list, to_pdf):
        """
        This function makes statistic about alignment such as mean
        :param from_list: from which list we want to make statistic
        :param to_pdf: if save to pdf or not
        :return: dataFrame or html
        """
        self.procents = []
        self.identities = []
        self.length = []
        self.gaps = []
        self.score = []
        for hit in from_list:
            for align in hit.alignments:
                if align.gap not in self.gaps_count.keys():
                    self.gaps_count[align.gap] = 1
                else:
                    self.gaps_count[align.gap] += 1
                self.procents.append(align.correct_procent)
                self.identities.append(int(align.identities))
                self.gaps.append(int(align.gap))
                self.length.append(int(align.align_length))
                self.score.append(float(align.bit_score))
        if len(self.procents) == 0:
            result = [{"Mean length": 0,
                       "Mean identities": 0,
                       "Mean score": 0,
                       "Mean percent": 0}]
        else:

            result = [{"Mean length": str(np.mean(self.length)),
                       "Mean identities": str(np.mean(self.identities)),
                       "Mean score": str(np.mean(self.score)),
                       "Mean percent": str(np.mean(self.procents))}]
        df = pd.DataFrame(result, columns=["Mean length",
                                           "Mean identities",
                                           "Mean score",
                                           "Mean percent"])
        if to_pdf:
            return df.to_html(index=False)
        else:
            return df

    def summary(self, to_pdf=True):
        """
        Make a summary of number of alignemnts in each group
        :param to_pdf: if it will be save to pdf
        :return: dataFrame or html
        """
        self.number_of_all = 0
        self.number_of_pred = 0
        self.number_of_normal = 0
        self.number_of_syntetic = 0
        self.number_of_weird = 0
        for hit in self.p.main_alignments:
            for _ in hit.alignments:
                self.number_of_all += 1
        for hit in self.p.predicted:
            for _ in hit.alignments:
                self.number_of_pred += 1
        for hit in self.p.rest:
            for _ in hit.alignments:
                self.number_of_normal += 1
        for hit in self.p.synthetic:
            for _ in hit.alignments:
                self.number_of_syntetic += 1
        for hit in self.p.weird:
            for _ in hit.alignments:
                self.number_of_weird += 1

        number_of_species_in_pred = len(self.p.name_of_species_predicted)
        number_of_species = len(self.p.name_of_species)

        result = [{"Number of all alignments": self.number_of_all,
                   "Number of predicted": self.number_of_pred,
                   "Number of normal alignments": self.number_of_normal,
                   "Number of syntetic": self.number_of_syntetic,
                   "Number of weird": self.number_of_weird,
                   "Number of species": number_of_species,
                   "Number of species in predicted": number_of_species_in_pred}]
        df = pd.DataFrame(result, columns=["Number of all alignments",
                                           "Number of predicted",
                                           "Number of normal alignments",
                                           "Number of syntetic",
                                           "Number of weird",
                                           "Number of species",
                                           "Number of species in predicted"])

        if to_pdf:
            return df.to_html(index=False)
        else:
            return df

    def generate_chart_percent(self):
        """
        Generate and save in file percent chart
        """
        plt.hist(self.procents, bins='auto', color='yellow')
        plt.title("Histogram of percent")
        plt.savefig(os.path.join("static", 'percent.png'), dpi=100)
        plt.close()

    def generate_chart_gaps(self):
        """
        Generate and save in file gaps chart
        """
        plt.hist(self.gaps, bins='auto', color='red')
        plt.title("Histogram of gaps")
        plt.savefig(os.path.join("static", 'gaps.png'), dpi=100)
        plt.close()

    def generate_chart_lenght(self):
        """
        Generate and save in file length chart
        """
        plt.hist(self.length, bins='auto', color='red')
        plt.title("Histogram of length")
        plt.savefig(os.path.join("static", 'length.png'), dpi=100)
        plt.close()

    def generate_chart_identities(self):
        """
        Generate and save in file identities chart
        """
        plt.hist(self.identities, bins='auto', color='green')
        plt.title("Histogram of identities")
        plt.savefig(os.path.join("static", 'identities.png'), dpi=100)
        plt.close()

    def generate_chart_score(self):
        """
        Generate and save in file percent chart
        """
        plt.hist(self.score, bins='auto', color='green')
        plt.title("Histogram of score")
        plt.savefig(os.path.join("static", 'score.png'), dpi=100)
        plt.close()

    def generate_division_pie(self):
        """
        Generate and save in file division to group pie
        """
        self.summary()
        labels = 'Predicted', 'Normal', 'Syntetic', 'Weird'
        sizes = [self.number_of_pred, self.number_of_normal, self.number_of_syntetic, self.number_of_weird]
        explode = (0, 0, 0, 0.3)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        fig1.savefig(os.path.join("static", 'pie.png'), dpi=100)

    def export_to_excel(self):
        """
        Export data to excel
        """
        self.p.group_to_classes()
        self.p.divide_to_species()
        self.p.divide_to_species_predicted()
        filename = filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))

        if filename == '':
            return ''
        else:
            if re.search("xlsx", filename) is None:
                filename = filename + ".xlsx"
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')
            self.p.return_alignment(self.p.main_alignments, False).to_excel(writer, sheet_name='All data', index=False)
            self.p.return_alignment(self.p.rest, False).to_excel(writer, sheet_name='Normal', index=False)
            self.p.return_alignment(self.p.synthetic, False).to_excel(writer, sheet_name='Synethic', index=False)
            self.p.return_alignment(self.p.predicted, False).to_excel(writer, sheet_name='Predicted', index=False)
            self.summary(False).to_excel(writer, sheet_name="Summary", index=False)
            for i in writer.sheets:
                if i != "Summary":
                    writer.sheets[i].set_column('A:A', 100)
                else:
                    writer.sheets[i].set_column('A:G', 30)
            writer.save()
