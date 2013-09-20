from __future__ import absolute_import
import pager


class OptionsPrompt(object):
    options = {
        pager.ESC_: 'quit',
        pager.CTRL_C_: 'quit',
        'q': 'quit',
        'Q': 'quit',
    }

    def get_options(self):
        return self.options

    def get_prompt(self, pagenum):
        return "Page -%s-. Press any key to continue . . . " % pagenum

    def quit(self, ch):
        return False

    def __call__(self, pagenum):
        prompt = self.get_prompt(pagenum)
        pager.echo(prompt)

        options = self.get_options()
        ch = pager.getch()
        if ch in options:
            return getattr(self, options[ch])(ch)
        pager.echo('\r' + ' '*(len(prompt)-1) + '\r')


class Pager(object):
    def page(self, content, pagecallback=None, always_page=False):
        rows = pager.getheight()

        if always_page is False:
            if len(content) < rows:
                for line in content:
                    print(line)
                return

        if pagecallback is None:
            pagecallback = OptionsPrompt()

        pager.page(iter(content), pagecallback=pagecallback)

    def echo(self, content):
        pager.echo(content)
