from scraping.config import HtmlTags, HtmlClasses


class Headline:
    def __init__(self, soup):
        self.soup = soup

    @property
    def author(self):
        """ Extracts author of headline from the html

        @return:
        """
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.AUTHOR}).text.strip('\n -')

    @property
    def content(self):
        """ Extracts content of headline from the html

        @return:
        """
        return self.soup.find(text=True, recursive=False).strip()