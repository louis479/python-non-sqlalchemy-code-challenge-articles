class Article:
    all = []  # Maintain a class-level list to track all articles

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        if not isinstance(author, Author):
            raise TypeError("Author must be of type Author.")
        if not isinstance(magazine, Magazine):
            raise TypeError("Magazine must be of type Magazine.")

        self._title = title  # Now mutable
        self.author = author
        self.magazine = magazine

        author._articles.append(self)
        magazine._articles.append(self)
        Article.all.append(self)  # Track all articles

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string.")
        if not (5 <= len(value) <= 50):
            raise ValueError("Title must be between 5 and 50 characters.")
        self._title = value  # Allow reassignment

class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name  # Name is immutable

    @name.setter
    def name(self, value):
        raise AttributeError("Author name is immutable and cannot be changed.")

    def articles(self):
        from classes.many_to_many import Article
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list(set(article.magazine for article in self.articles()))

    def add_article(self, magazine, title):
        from classes.many_to_many import Article
        return Article(self, magazine, title)

    def topic_areas(self):
        topics = list(set(magazine.category for magazine in self.magazines()))
        return topics if topics else None

class Magazine:
    def __init__(self, name, category):
        self._name = None
        self._category = None
        self.name = name
        self.category = category
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
    
    def articles(self):
        return self._articles

    def add_article(self, article):
        if isinstance(article, Article):
            self._articles.append(article)

    def contributors(self):
        return list(set(article.author for article in self._articles))

    def article_titles(self):
        return [article.title for article in self._articles] if self._articles else None

    def contributing_authors(self):
        author_count = {}
        for article in self._articles:
            author_count[article.author] = author_count.get(article.author, 0) + 1
        
        top_authors = [author for author, count in author_count.items() if count > 2]
        return top_authors if top_authors else None


