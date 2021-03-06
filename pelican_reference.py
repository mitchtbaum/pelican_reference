# -*- coding: utf-8 -*-

"""
Reference field for Pelican
================================

Adds references variable to article's context
"""

import pelican.signals as signals

def add_references(generator):
    categories = []
    articles = {}

    # Find all category names.
    for category in generator.categories:
        if category not in categories:
            categories.append(category[0].name)

    # It would be nice if generator.articles was already keyed by slug.
    for article in generator.articles:
        articles[article.slug] = article

    for article in generator.articles:
        for category, slugs in article.metadata.items():
            if category in categories:
                slugs = slugs.replace(' ', '').split(',')

                referenced_articles = []

                for slug in slugs:
                    # Check for valid slug.
                    if slug not in articles:
                      continue

                    referenced_articles.append(articles[slug])

                    # Default to an empty list.
                    if not hasattr(articles[slug], 'referenced_by'):
                        articles[slug].referenced_by = []

                    articles[slug].referenced_by.append(article)

                setattr(article, category, referenced_articles)

def register():
    signals.article_generator_finalized.connect(add_references)
