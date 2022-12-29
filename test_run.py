from hip_flask import *


class PageBase(Widget):
    root = ClassNode('DocType')
    html = ClassNode('html')
    html_block = ClassNode('block', 'html')
    head = ClassNode('head')
    head_block = ClassNode('block', 'head')
    title = ClassNode('title')
    title_block = ClassNode('block', 'title')
    body = ClassNode('body')
    body_block = ClassNode('block', 'body')

    def __init__(self, title, *args, **kwargs):
        self.root = self.html
        self.html = self.html_block
        self.html_block = self.head, self.body
        self.head = self.head_block
        self.head_block = self.title
        self.title = self.title_block
        self.title_block = title
        self.body = self.body_block
        super().__init__(*args, **kwargs)


class NavBar(Widget):
    root = ClassNode('nav')
    ul = ClassNode('ul')

    def __init__(self, register = False, **kwargs):
        self.root = self.ul
        self.ul = (
                Node('li', _class = 'nav-item').append(Node('a', href = link, _class = 'nav-link').append(text))
                for text, link in kwargs.items()
        )
        super().__init__(register = register)


class Footer(Widget):
    root = ClassNode('footer')
    div = ClassNode('div', _class = 'container')
    p = ClassNode('p', _class = 'text-muted')

    def __init__(self, text, register = False):
        self.root = self.div
        self.div = self.p
        self.p = text
        super().__init__(register = register)


class Card(Widget):
    root = ClassNode('div', _class = 'card')
    img = ClassNode('img', _class = 'card-img img-fluid')
    body = ClassNode('div', _class = 'card-body')
    title = ClassNode('h5', _class = 'card-title')
    text = ClassNode('p', _class = 'card-text')
    link = ClassNode('a', _class = 'btn btn-primary')

    def __init__(self, title, text, link, img, register = False):
        self.root = self.img, self.body
        self.img = img
        self.body = self.title, self.text, self.link
        self.title = title
        self.text = text
        self.link = link
        super().__init__(register = register)


class Page(PageBase):
    def __init__(self, title, nav_bar, footer, content, register = False):
        self.body_block = nav_bar, content, footer
        super().__init__(title, register = register)


def main():
    page = Page(
            title = 'Test Page',
            nav_bar = NavBar(
                    Home = '/',
                    About = '/about',
                    Contact = '/contact',
            ),
            footer = Footer(
                    'This is a footer',
            ),
            content = (
                    Card(
                            title = 'Card 1',
                            text = 'This is a card',
                            link = 'https://www.google.com',
                            img = 'https://via.placeholder.com/150',
                    ),
                    Card(
                            title = 'Card 2',
                            text = 'This is a card',
                            link = 'https://www.google.com',
                            img = 'https://via.placeholder.com/150',
                    ),
                    Card(
                            title = 'Card 3',
                            text = 'This is a card',
                            link = 'https://www.google.com',
                            img = 'https://via.placeholder.com/150',
                    )
            ),
    )
    print(page)


if __name__ == '__main__':
    main()
