from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
from parser_blast import Parser_blast
from summary import Summary
p = Parser_blast(os.path.join("files",'data.xml'))
p.generate_xml_tree()
p.group_to_classes()
p.divide_to_species()
p.divide_to_species_predicted()
s = Summary(p)

config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf\\bin\wkhtmltopdf.exe')
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("t.html")
template_vars = {"all_alignments": p.return_alignment(p.main_alignments,True),
                 "summary": s.summary(),
                 "means_all": s.get_data(p.main_alignments,True),
                 "normal": p.return_norm_alignment()[0],
                 "species":p.return_norm_alignment()[1],
                 "predicted": p.return_predicted_alignment()[0],
                 "species_pred":p.return_predicted_alignment()[1],
                 "means_normal":s.get_data(p.rest,True),
                 "means_pred": s.get_data(p.predicted, True),
                 "n":len(p.species),
                 "n_pred": len(p.species_predicted)}

html_out = template.render(template_vars)
with open("report.html","w") as f:
    f.write(html_out)

pdfkit.from_file('report.html', 'out1.pdf',configuration=config)