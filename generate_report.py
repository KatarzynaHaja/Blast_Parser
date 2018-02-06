from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
from parser_blast import Parser_blast
from summary import Summary

class Generate_report_pdf:
    def __init__(self,p):
        self.p = p
        p.generate_xml_tree()
        p.group_to_classes()
        p.divide_to_species()
        p.divide_to_species_predicted()
        s = Summary(p)
        s.get_data(p.main_alignments, False)
        s.generate_chart_percent()
        s.generate_chart_identities()
        s.generate_chart_gaps()
        s.generate_chart_lenght()
        s.generate_division_pie()
        config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf\\bin\wkhtmltopdf.exe")
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("t.html")
        env.filters['print_sequence'] = p.print_sequence
        template_vars   = {"all_alignments": p.return_alignment(p.main_alignments,True),
                     "summary": s.summary(),
                     "means_all": s.get_data(p.main_alignments,True),
                     "normal": p.return_norm_alignment()[0],
                     "species":p.return_norm_alignment()[1],
                     "predicted": p.return_predicted_alignment()[0],
                     "species_pred":p.return_predicted_alignment()[1],
                     "means_normal":s.get_data(p.rest,True),
                     "means_pred": s.get_data(p.predicted, True),
                     "n":len(p.species),
                     "n_pred": len(p.species_predicted),
                     "species_divided_normal":p.return_species()[0],
                     "species_divided_pred": p.return_species()[1],
                     "path_pie":os.path.abspath(os.path.join("static","pie.png")),
                     "path_percent": os.path.abspath(os.path.join("static", "percent.png")),
                     "path_length": os.path.abspath(os.path.join("static", "length.png")),
                     "path_identities": os.path.abspath(os.path.join("static", "identities.png")),
                     "path_gaps": os.path.abspath(os.path.join("static", "gaps.png"))}


        html_out = template.render(template_vars)
        with open("report.html","w") as f:
            f.write(html_out)

        pdfkit.from_file('report.html', 'out1.pdf',configuration=config,css="style.css")