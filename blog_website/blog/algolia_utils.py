# blog/algolia_utils.py
from algoliasearch.search_client import SearchClient
from django.conf import settings

client = SearchClient.create(settings.ALGOLIA_APP_ID, settings.ALGOLIA_API_KEY)
index = client.init_index(settings.ALGOLIA_INDEX_NAME)

def index_post(post):
    record = {
        'objectID': post.id,
        'title': post.title,
        'slug': post.slug,
        'category': post.category,
    }
    index.save_object(record)

def delete_post(post):
    index.delete_object(post.id)
