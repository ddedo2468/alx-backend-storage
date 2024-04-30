#!/usr/bin/env python3
"""some updates in ono"""


def update_topics(mongo_collection, name, topics):
    """
    updating a collection
    """
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
