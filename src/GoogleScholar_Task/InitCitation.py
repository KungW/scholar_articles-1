#coding:utf-8
"""
@file:      InitCitation
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-11-17 13:51
@description:
            本模块为生成初始化文章的引用关系，以及与年份的关系
"""
from db_config import DB_CONNS_POOL

class CitationGenerator:
    def __init__(self):
        pass

    def save_relation(self,cite_google_id,cited_google_id):
        cur = DB_CONNS_POOL.new_db_cursor()
        cur.execute(
            'INSERT INTO citation_relation(cite_google_id,cited_google_id)'
            'VALUES(%s, %s)',
            (cite_google_id,cited_google_id)
        )

    def get_uninitialized_article_items(self,limit):
        cur = DB_CONNS_POOL.new_db_cursor()
        sql = (
            'SELECT * FROM articles '
            'WHERE citations_init_ok = FALSE LIMIT {}'
        ).format(limit)
        cur.execute(sql)
        return cur.fetchall()

    def add_article_citations(self,article_item):



if __name__=="__main__":
    sql = (
            'SELECT * FROM articles '
            'WHERE citations_init_ok = FALSE'
        )
    print(sql)