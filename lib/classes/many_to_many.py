class Article:
    all = []  
    
    def __init__(self, author, magazine, title):
        # Title validation for immutability and length constraints
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        
        self._title = title  
        self.author = author  
        self.magazine = magazine  
        Article.all.append(self)  

    @property
    def title(self):
        return self._title  

    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, new_author):
        if isinstance(new_author, Author):
            self._author = new_author
        else:
            raise TypeError("Author must be an instance of Author")
    
    @property
    def magazine(self):
        return self._magazine
    
    @magazine.setter
    def magazine(self, new_magazine):
        if isinstance(new_magazine, Magazine):
            self._magazine = new_magazine
        else:
            raise TypeError("Magazine must be an instance of Magazine")


class Author:
    def __init__(self, name):
        # Author name validation for immutability and non-empty string
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self._name = name  

    @property
    def name(self):
        return self._name

    # Prevent name change after initialization
    @name.setter
    def name(self, new_name):
        raise AttributeError("Author name is immutable and cannot be changed.")

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def articles(self):
        return [article for article in Article.all if article.author == self]
    
    def magazines(self):
        return list(set(article.magazine for article in self.articles()))
    
    def topic_areas(self):
        categories = list(set(magazine.category for magazine in self.magazines()))
        return categories if categories else None


class Magazine:
    all_magazines = []  # List to store all magazines

    def __init__(self, name, category):
        # Validate magazine name and category
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Magazine name must be a string between 2 and 16 characters.")
        
        if not isinstance(category, str) or len(category.strip()) == 0:
            raise ValueError("Magazine category must be a non-empty string.")

        self._name = name
        self._category = category
        Magazine.all_magazines.append(self)  

    @property
    def name(self):
        return self._name

    # Allow magazine name to change, but keep within length constraints
    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and 2 <= len(new_name) <= 16:
            self._name = new_name
        else:
            raise ValueError("Magazine name must be a string between 2 and 16 characters.")

    @property
    def category(self):
        return self._category  

    # Allow category to change, but prevent empty values
    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str) and len(new_category.strip()) > 0:
            self._category = new_category
        else:
            raise ValueError("Magazine category must be a non-empty string.")

    def articles(self):
        # Return all articles in this magazine
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        # Return unique list of authors who have contributed to this magazine
        return list(set(article.author for article in self.articles()))

    def article_titles(self):
        # Return a list of all article titles in the magazine
        titles = [article.title for article in self.articles()]
        return titles if titles else None
    
    def contributing_authors(self):
        # Return authors who have contributed more than 2 articles to the magazine
        author_counts = {}
        for article in self.articles():
            author_counts[article.author] = author_counts.get(article.author, 0) + 1
        result = [author for author, count in author_counts.items() if count > 2]
        return result if result else None

    @classmethod
    def get_all_magazines(cls):
        # Return all magazines
        return cls.all_magazines


# Example setup for testing
magazine = Magazine("Sensors", "Internet of Things")  
magazine.category = "Science & Technology"  

author_1 = Author("Alexander O'niel")
article_1 = author_1.add_article(magazine, "The mind of a programmer")

# Test validation and immutability
try:
    article_1.title = "Updated Title"  
except AttributeError as e:
    print(e)

try:
    author_1.name = "Alexander O'niel" 
except AttributeError as e:
    print(e)
