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
                article.metadata[category] = slugs

                for slug in slugs:
                    # Check for valid slug.
                    if slug not in articles:
                      continue

                    # Default to an empty list.
                    if 'referenced_by' not in articles[slug].metadata:
                        articles[slug].metadata['referenced_by'] = []

                    articles[slug].metadata['referenced_by'].append(article)

def register():
    signals.article_generator_finalized.connect(add_references)
