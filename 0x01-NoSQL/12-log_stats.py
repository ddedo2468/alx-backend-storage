#!/usr/bin/env python3
""" Nginx logs  """
from pymongo import MongoClient


def main():
    """ Nginx logs """
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_c = client.logs.nginx

    n_logs = nginx_c.count_documents({})
    print(f"{n_logs} logs")
    methods: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for m in methods:
        c: int = nginx_c.count_documents({"method": m})
        print(f"\tmethod {m}: {c}")

    st_c: int = nginx_c.count_documents({"method": "GET", "path": "/status"})
    print(f"{st_c} status check")


if __name__ == "__main__":
    main()
