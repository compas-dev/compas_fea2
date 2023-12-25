# import pandas as pd
from jinja2 import Environment, FileSystemLoader
# import pdfkit  # Make sure wkhtmltopdf is installed in your system
import os

class Report:
    def __init__(self, model, **kwargs):
        self.model = model
        self.env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__))))
        self.template = self.env.get_template('report_template.html')

    def generate_html(self, output_file='report.html'):
        summary_stats = self.model.name
        html_out = self.template.render(
            title="Structural Analysis Report",
            summary_stats=summary_stats
        )
        with open(output_file, 'w') as f:
            f.write(html_out)
        print(f"HTML report generated: {output_file}")

    # def generate_pdf(self, output_file='report.pdf'):
    #     # Generate the HTML report first
    #     html_report = 'temp_report.html'
    #     self.generate_html(html_report)

    #     # Convert HTML to PDF
    #     pdfkit.from_file(html_report, output_file)
    #     print(f"PDF report generated: {output_file}")

