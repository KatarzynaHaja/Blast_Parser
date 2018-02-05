import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
class Summary:
    def __init__(self,P):
        self.p = P
        self.procents = []
        self.identities = []
        self.length = []
        self.gaps = []
        self.score = []
        self.gaps_count = {}

    def get_data(self,from_list,to_pdf):
        for hit in from_list:
            for align in hit.alignments:
                if align.gap not in self.gaps_count.keys():
                    self.gaps_count[align.gap] = 1
                else:
                    self.gaps_count[align.gap] += 1
                self.procents.append(align.correct_procent)
                self.identities.append(int(align.identities))
                self.gaps.append(int(align.gap))
                self.length.append(int(align.length))
                self.score.append(float(align.bit_score))
        result =  [{"Mean length": str(np.mean(self.length)),
                    "Mean identities": str(np.mean(self.identities)),
                    "Mean score":str(np.mean(self.score)),
                    "Mean percent":str(np.mean(self.procents))}]
        print(result)
        df = pd.DataFrame(result,columns=["Mean length",
                                          "Mean identities",
                                          "Mean score",
                                          "Mean percent"])
        print(df)
        if to_pdf == True:
            return df.to_html(index=False)
        else:
            return df

    def summary(self, to_pdf=True):
        number_of_all = 0
        number_of_pred = 0
        number_of_normal = 0
        number_of_syntetic = 0
        number_of_weird = 0
        for hit in self.p.main_alignments:
            for _ in hit.alignments:
                number_of_all += 1
        for hit in self.p.predicted:
            for _ in hit.alignments:
                number_of_pred += 1
        for hit in self.p.rest:
            for _ in hit.alignments:
                number_of_normal += 1
        for hit in self.p.synthetic:
            for _ in hit.alignments:
                number_of_syntetic += 1
        for hit in self.p.weird:
            for _ in hit.alignments:
                number_of_weird += 1

        number_of_species_in_pred = len(self.p.name_of_species_predicted)
        number_of_species = len(self.p.name_of_species)

        result = [{"Number of all alignments": number_of_all,
                   "Number of predicted": number_of_pred,
                   "Number of normal alignments": number_of_normal,
                   "Number of syntetic": number_of_syntetic,
                   "Number of weird": number_of_weird,
                   "Number of species": number_of_species,
                   "Number of species in predicted": number_of_species_in_pred}]
        df = pd.DataFrame(result, columns=["Number of all alignments",
                                           "Number of predicted",
                                           "Number of normal alignments",
                                           "Number of syntetic",
                                           "Number of weird",
                                           "Number of species",
                                           "Number of species in predicted"])

        if to_pdf == True:
            return df.to_html(index=False)
        else:
            return df

    def generate_chart_percent(self):
        plt.hist(self.procents, bins='auto', color='yellow')
        plt.title("Histogram of percent")
        plt.show()

    def generate_chart_gaps(self):
        plt.hist(self.gaps, bins='auto', color='red')
        plt.title("Histogram of gaps")
        plt.show()

    def generate_chart_lenght(self):
        plt.hist(self.length, bins='auto', color='red')
        plt.title("Histogram of length")
        plt.show()

    def generate_chart_identities(self):
        plt.hist(self.identities, bins='auto', color='green')
        plt.title("Histogram of identities")
        plt.show()

    def generate_chart_score(self):
        plt.hist(self.score, bins='auto', color='green')
        plt.title("Histogram of score")
        plt.show()


