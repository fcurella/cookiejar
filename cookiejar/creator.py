from cookiecutter.main import cookiecutter


class PackageCreator(object):
    blacklist = ('.template.cfg', '.DS_Store', 'cookiecutter.json')

    def __init__(self, settings):
        self.settings = settings
        super(PackageCreator, self).__init__()

    def create(self, template_name, context=None):
        source = None

        for Loader in self.settings['template-loaders']:
            loader = Loader(self.settings, template_name)
            if loader.template_exists():
                source = loader.template_path()
                self.copy_skeleton(source, context=context)
                loader.cleanup()
                break

        if source is None:
            print("Template '%s' not found." % template_name)

    def copy_skeleton(self, source, context):
        cookiecutter(source, parameters=context)
