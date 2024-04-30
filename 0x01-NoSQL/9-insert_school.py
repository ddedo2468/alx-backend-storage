#!/usr/bin/env python3
"""task 9"""


def insert_school(mongo_collection, **kwargs):
    """
    insert to collection
    """
    return mongo_collection.insert_one(kwargs).inserted_id
