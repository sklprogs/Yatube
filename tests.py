#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import model as md


def time():
    itime = md.Time()
    itime.set_date(DaysDelta=0)
    print('Current time:')
    print('Year:',itime._year)
    print('Month:',itime._month)
    print('Day:',itime._day)
    itime.set_date(DaysDelta=7)
    print()
    print('A week ago:')
    print('Year:',itime._year)
    print('Month:',itime._month)
    print('Day:',itime._day)
    
def constants():
    cs = md.Constants()
    print('Countries:')
    print(cs.countries())
    print()
    print('Trending:')
    print(cs.trending())
    
def delimiter():
    input('Press Return')
    print('--------------------------------------------')
    
def lists():
    lists = md.Lists()
    lists.load()
    print('Subscribe to authors:')
    print(lists._subsc_auth)
    print('URLs:')
    print(lists._subsc_urls)
    print('Block authors:')
    print(lists._block_auth)
    print('URLs:')
    print(lists._block_urls)
    
def all():
    print('Run all tests')
    time()
    delimiter()
    constants()
    delimiter()


if __name__ == '__main__':
    lists()
