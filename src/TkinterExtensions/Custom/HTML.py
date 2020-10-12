"""
tkinter HTML text widgets
"""

import sys

from tk_html_widgets import html_parser

from TkinterExtensions.Widgets.Widgets import ScrolledText




__all__ = [
        'HTMLScrolledText', 'HTMLText', 'HTMLLabel'
        ]

class HTMLScrolledText(ScrolledText):
    """ HTML scrolled text widget """
    def __init__(self, *args, html=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._w_init(kwargs)
        self.html_parser = html_parser.HTMLTextParser()
        if isinstance(html, str):
            self.set_html(html)
    def _w_init(self, kwargs):
        if not 'wrap' in kwargs.keys():
            self.config(wrap='word')
        if not 'background' in kwargs.keys():
            if sys.platform.startswith('win'):
                self.config(background='SystemWindow')
            else:
                self.config(background='white')
    def fit_height(self):
        # ------------------------------------------------------------------------------------------
        """
        Fit widget height to wrapped lines
        """
        for h in range(1, 4):
            self.config(height=h)
            self.master.update()
            if self.text.yview()[1] >= 1:
                break
        else:
            self.config(height=0.5 + 3 / self.text.yview()[1])
    def set_html(self, html, strip=True):
        # ------------------------------------------------------------------------------------------
        """
        Set HTML widget text. If strip is enabled (default) it ignores spaces and new lines.

        """
        prev_state = self.cget('state')
        self.Enable()
        self.text.Clear()
        self.text.tag_delete(self.text.tag_names)
        self.html_parser.w_set_html(self.text, html, strip=strip)
        self.Enable(state=prev_state)


    @property
    def txt(self) -> str: return self.text.txt
    @txt.setter
    def txt(self, value: str): self.set_html(value)



class HTMLText(HTMLScrolledText):
    """ HTML text widget """
    def _w_init(self, kwargs):
        # ------------------------------------------------------------------------------------------
        super()._w_init(kwargs)
        self.vbar.hide()

    def fit_height(self):
        # ------------------------------------------------------------------------------------------
        super().fit_height()
        # self.master.update()
        self.vbar.hide()


class HTMLLabel(HTMLText):
    """ HTML label widget """
    def _w_init(self, kwargs):
        # ------------------------------------------------------------------------------------------
        super()._w_init(kwargs)
        if not 'background' in kwargs.keys():
            if sys.platform.startswith('win'):
                self.config(background='SystemButtonFace')
            else:
                self.config(background='#d9d9d9')

        if not 'borderwidth' in kwargs.keys():
            self.config(borderwidth=0)

        if not 'padx' in kwargs.keys():
            self.config(padx=3)

    def set_html(self, *args, **kwargs):
        # ------------------------------------------------------------------------------------------
        super().set_html(*args, **kwargs)
        self.Disable()
