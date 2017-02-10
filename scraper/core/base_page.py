
class BasePage(object):

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self._goto_page(self.url)

    def _goto_page(self, url):
        print('Loading {}...'.format(url))
        self.driver.get(url)
        print('Loading {}... OK'.format(url))
