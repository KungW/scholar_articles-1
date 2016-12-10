#coding:utf-8
"""
@file:      update_ieee_url
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-09-27 17:04
@description:
            --
"""

from db_config import DB_CONNS_POOL

cur = DB_CONNS_POOL.new_db_cursor()

cur.execute(
    "select id,resource_link from articles where resource_link like '%arnumber=IEEE%'"
)
data = cur.fetchall()
print(data)
for item in data:
    id = item[0]
    pdf_url = item[1]
    l = pdf_url.split('IEEE')
    handled_url = l[0] + l[1]
    cur.execute(
        "update articles set pdf_temp_url='{}',resource_link=null where id = {}"\
            .format(handled_url,id)
    )
    print('{} ok'.format(id))