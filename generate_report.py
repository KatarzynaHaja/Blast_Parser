from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
from parser_blast import Parser_blast
from summary import Summary
from tkinter import filedialog

class Generate_report_pdf:
    def __init__(self,p,filename):
        self.filename = filename
        self.p = p
        self.p.generate_xml_tree()
        self.p.group_to_classes()
        self.p.divide_to_species()
        self.p.divide_to_species_predicted()
        s = Summary(self.p)
        s.get_data(self.p.main_alignments, False)
        s.generate_chart_percent()
        s.generate_chart_identities()
        s.generate_chart_gaps()
        s.generate_chart_lenght()
        s.generate_division_pie()
        self.config = pdfkit.configuration(wkhtmltopdf=os.environ.get('wkhtmltopdf'))
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("t.html")
        env.filters['print_sequence'] = self.p.print_sequence
        template_vars = {"all_alignments": self.p.return_alignment(self.p.main_alignments,True),
                     "summary": s.summary(),
                     "means_all": s.get_data(self.p.main_alignments,True),
                     "normal": self.p.return_norm_alignment()[0],
                     "species":self.p.return_norm_alignment()[1],
                     "predicted": self.p.return_predicted_alignment()[0],
                     "species_pred":self.p.return_predicted_alignment()[1],
                     "means_normal":s.get_data(self.p.rest,True),
                     "means_pred": s.get_data(self.p.predicted, True),
                     "n":len(self.p.species),
                     "n_pred": len(self.p.species_predicted),
                     "species_divided_normal":self.p.return_species()[0],
                     "species_divided_pred": self.p.return_species()[1],
                     "path_pie":os.path.abspath(os.path.join("static","pie.png")),
                     "path_percent": os.path.abspath(os.path.join("static", "percent.png")),
                     "path_length": os.path.abspath(os.path.join("static", "length.png")),
                     "path_identities": os.path.abspath(os.path.join("static", "identities.png")),
                     "path_gaps": os.path.abspath(os.path.join("static", "gaps.png"))}


        html_out = template.render(template_vars)
        with open("report.html","w") as f:
            f.write(html_out)

    
        pdfkit.from_file('report.html', self.filename,configuration=self.config,css="style.css")