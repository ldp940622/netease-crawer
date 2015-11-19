from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager


app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/test'
db = SQLAlchemy(app)
mysession = db.session()
restless = APIManager(app, flask_sqlalchemy_db=db)


class News(db.Model):

    """
    News
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(
        db.String(255), unique=True, nullable=False, autoincrement=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    keywords = db.Column(db.String(255), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    images = db.Column(db.TEXT, nullable=False)

    @classmethod  # 类方法
    def get_all_news(cls):
        query = mysession.query(News)
        all_news = query.all()
        news_set = set()
        for news in all_news:
            news_set.add(news.url)
        return news_set

    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self.__parse__()

    def __parse__(self):
        # self.title = self.soup.title.string
        self.title = self.__get_title__(self.soup)
        self.keywords = self.soup.find(
            'meta', attrs={'name': 'keywords'})['content']
        self.content = self.__get_content__(self.soup)

    def __get_title__(self, soup):
        return soup.title.string[0:len(soup.title.string) - 7]

    def __get_source__(self, soup):
        pass

    def __get_content__(self, soup):
        # return soup.find('div', id='endText')
        content_div = soup.find('div', 'end-text')
        content_p = content_div.find_all('p')
        # for content_string in content_p:
        #     content += str(content_string)
        # return content
        # image_arrar = []
        index = 0
        content = ''
        images = ''
        for element in content_p:
            if element.string:
                content += element.string + "\\n\\t"
            elif element.img:
                content += '[IMG-' + str(index) + "]\\n\\t"
                index = index + 1
        # image_arrar.append(element.img['src'])
                images += element.img['src'] + ','
        self.images = images
        return content

    def __get_description__(self, content):
        pass

    def add(self):
        mysession.add(self)
        mysession.commit()
        # News.session.close()

restless.create_api(
    News, methods=['GET'], results_per_page=10)

db.create_all()
