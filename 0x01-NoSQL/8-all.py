#!/usr/bin/env python3
"""find all"""


def list_all(mongo_collection):
    """
    get all docs in collection
    """

    return mongo_collection.find()
