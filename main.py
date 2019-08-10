import os
import json
import markdown
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict


CONFIG_JSON = 'config.json'
STATIC_DIR = 'static/html/'
DIR_ARTICLES = 'articles/'
TEMPLATES_DIR = 'templates/'
TEMPLATES_ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)
TEMPLATE_ARTICLES = 'articles.html'
TEMPLATE_INDEX = 'index.html'


def main():
    config = load_json(CONFIG_JSON)
    topics = config['topics']
    articles = config['articles']
    convert_articles_to_html(articles)
    render_index_to_template(topics, articles)


def convert_articles_to_html(articles):
    for article in articles:
        text = load_file(DIR_ARTICLES + article['source'])
        raw_html = convert_md_to_html(text)
        html = render_article_to_template(article, raw_html)
        filepath = replace_extension_to_html(article['source'])
        save_to_static(filepath, html)


def render_index_to_template(topics, articles):
    html = TEMPLATES_ENV.get_template(TEMPLATE_INDEX).render(
                        grouped_topics=group_items_in_array(topics),
                        articles=normalize_articles(articles))
    save_to_static(TEMPLATE_INDEX, html)


def load_json(jsonpath):
    with open(jsonpath, 'r') as jsonfile:
        return json.load(jsonfile)


def load_file(filepath):
    with open(filepath, 'r') as filename:
        return filename.read()


def convert_md_to_html(md):
    extensions = ['codehilite', 'fenced_code']
    return markdown.markdown(md, extensions=extensions)


def render_article_to_template(article, html):
    return TEMPLATES_ENV.get_template(TEMPLATE_ARTICLES).render(html=html, title=article['title'])


def save_to_static(path, content):
    dirname = STATIC_DIR + os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    with open(STATIC_DIR + path, 'w') as file_obj:
        file_obj.write(content)


def replace_extension_to_html(path):
    filename, extension = os.path.splitext(path)
    return filename + '.html'


def group_items_in_array(array, group_volume=3):
    grouped_items = []
    for start_index_group in range(0, len(array), group_volume):
        grouped_items.append(array[start_index_group:start_index_group+group_volume])
    return grouped_items


def normalize_articles(articles):
    grouped_articles = defaultdict(list)
    for article in articles:
        article['source'] = replace_extension_to_html(article['source'])
        grouped_articles[article['topic']].append(article)
    return grouped_articles


if __name__ == "__main__":
    main()
