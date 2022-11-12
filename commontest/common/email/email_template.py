import jinja2
from jinja2 import Environment, PackageLoader, select_autoescape
from common.util.logging_helper import get_logger
from common.util.utility_functions import utils_get_email_template_dir

# -------------------------------------------------------------
# Class Email Template
# -------------------------------------------------------------
class EmailTemplate:
    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self):
        self.glogger = get_logger("emailtemplate")
        template_dir = utils_get_email_template_dir()
        self.glogger.info("Setting Template Directory=%s", template_dir)
        template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
        self._env = Environment(loader=template_loader,autoescape=select_autoescape(['html', 'xml']))

    # ---------------------------------------------
    # Build html file
    # ---------------------------------------------
    def build_html(self, templatefilename : str, context : str) -> str:
        try:
            self.glogger.info("Building an HTML file based on template=%s contect=%s", templatefilename, context)
            template = self._get_template(templatefilename)
            html = template.render(context)
            self.glogger.debug("The HTML for %s: %s", templatefilename, html)
            return html
        except Exception as err:
            self.glogger.error("Failed to create html from the tamplate=%s. err=%s", templatefilename, err)
            return None

    # ---------------------------------------------
    # Get the template of a specific subject
    # ---------------------------------------------
    def _get_template(self, templatefilename : str):
        try:
            template = self._env.get_template(templatefilename)
            return template
        except Exception as err:
            self.glogger.error("Failed to get template from the file=%s. err=%s", templatefilename, err)
            return None

