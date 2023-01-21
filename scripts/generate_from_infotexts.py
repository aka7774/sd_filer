import modules.scripts as scripts
from modules.processing import Processed

from filer.generate import generate_images

class Script(scripts.Script):
    def title(self):
        return "Generate from Infotexts"

    def run(self, p):
        p.do_not_save_grid = True
        return Processed(p, generate_images(p), p.seed, "")
