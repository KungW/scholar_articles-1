#coding:utf-8
"""
@file:      run.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-10-06 20:26
@description:
            --
"""
import sys,os
up_level_N = 1
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
root_dir = SCRIPT_DIR
for i in range(up_level_N):
    root_dir = os.path.normpath(os.path.join(root_dir, '..'))
sys.path.append(root_dir)


from Journals_Task.JournalTaskManager import JournalTaskManager
from Journals_Task.GetDBJournals import MajorEntrance,PublisherEntrance
from crawl_tools.WatchDog import close_procs_by_keyword

close_procs_by_keyword('chromedriver')
close_procs_by_keyword('phantom')

JournalTaskManager(keyword = 'lww').run(
    DB_EntranceFunc=PublisherEntrance,
    journal_need_single_area_relation = False,
    journal_need_open_access = False,
    thread_cot = 16,
    internal_thread_cot = 16,
    max_count=1000,
    driver_pool_size=0,
    drvier_is_visual=True,
    volume_links_got='no limit',
    just_init = False
)


'''
JournalTaskManager(keyword = 'Artificial').run(
    DB_EntranceFunc=MajorEntrance,
    journal_need_single_area_relation = False,
    journal_need_open_access = False,
    journal_need_index_by_area = False,
    journal_need_index_by_category = True,
    drvier_is_visual=False,
    thread_cot = 32,
    driver_pool_size = 16
)
'''