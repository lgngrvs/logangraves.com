# A custom extension for python-markdown that disables markdown
# rendering italics as _underscores_ because I never use it
# and it frequently breaks LaTeX

from markdown.extensions import Extension

class NoUnderscoresItalics(Extension): 
    def extendMarkdown(self, md): 
        md.inlinePatterns.deregister('em_strong2')