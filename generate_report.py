from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
from parser_blast import Parser_blast
p = Parser_blast(os.path.join("files",'data.xml'))
p.generate_xml_tree()

config = pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("report.html")
template_vars = {"all_alignments": p.return_all_alignment()}
# Render our file and create the PDF using our css style file
html_out = template.render(template_vars)
with open("report.html","w") as f:
    f.write(html_out)

pdfkit.from_file('report.html', 'out1.pdf',configuration=config)