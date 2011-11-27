from selenium.webdriver.remote.webelement import WebElement as _WebElement
from webdriverplus.selectors import SelectorMixin
from webdriverplus.wrappers import Style, Attributes, Size


class WebElement(SelectorMixin, _WebElement):
    # Traversal
    @property
    def parent(self):
        """
        Note: We're overriding the default WebElement.parent behaviour here.
        (Normally .parent is a property that returns the WebDriver object.)
        """
        return self.find(xpath='..')

    @property
    def children(self):
        return self.find_all(xpath='./*')

    @property
    def descendants(self):
        return self.find_all(xpath='./descendant::*')

    @property
    def next(self):
        return self.find(xpath='./following-sibling::*[1]')

    @property
    def prev(self):
        return self.find(xpath='./preceding-sibling::*[1]')

    @property
    def next_all(self):
        return self.find_all(xpath='./following-sibling::*')

    @property
    def prev_all(self):
        return self.find_all(xpath='./preceding-sibling::*')

    @property
    def siblings(self):
        return self.prev_all | self.next_all

    # Inspection & Manipulation
    @property
    def value(self):
        return self.get_attribute('value')

    @property
    def inner_html(self):
        return self.get_attribute('innerHTML')

    @property
    def html(self):
        # http://stackoverflow.com/questions/1763479/how-to-get-the-html-for-a-dom-element-in-javascript
        script = """
            var container = document.createElement("div");
            container.appendChild(arguments[0].cloneNode(true));
            return container.innerHTML;
        """
        return self._parent.execute_script(script, self)

    @property
    def index(self):
        return len(self.prev_all)

    @property
    def style(self):
        return Style(self)

    @property
    def size(self):
        val = super(WebElement, self).size
        return Size(val['width'], val['height'])

    @property
    def location(self):
        val = super(WebElement, self).size
        return Size(val['width'], val['height'])

    @property
    def attributes(self):
        return Attributes(self)

    def javascript(self, script):
        script = "return arguments[0].%s;" % script
        return  self._parent.execute_script(script, self)

    def jquery(self, script):
        script = "return $(arguments[0]).%s;" % script
        return  self._parent.execute_script(script, self)

    def __repr__(self):
        return "<%s>" % self.tag_name

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return self._id == other._id