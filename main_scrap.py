#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 08:26:53 2020

@author: mauricio
"""


from bs4 import BeautifulSoup
from bs4 import element
import requests as rq

import datetime as dt

import pandas as pd

import re



today = dt.datetime.utcnow() + dt.timedelta(hours = -4)

year = {"Janeiro":1,
       "Fevereiro":2,
       "Março":3,
       "Abril":4,
       "Maio":5,
       "Junho":6,
       "Julho":7,
       "Agosto":8,
       "Setembro":9,
       "Outubro":10,
       "Novembro":11,
       "Dezembro":12}

week = {"Segunda- feira":1,
        "Terça- feira":2,
        "Quarta- feira":3,
        "Quinta- feira":4,
        "Sexta- feira":5,
        "Sábado":6}

classes = ["Salada 1", "Salada 2", "Prato Principal 1", "Prato Principal 2", "Guarnição 1", "Guarnição 2", "Vegetariano", "Suco", "Sobremesa"]

pg = rq.get("https://portal.ufgd.edu.br/secao/restaurante-universitario-proae/cardapio", verify = "chain.pem")

soup = BeautifulSoup(pg.content, features = "lxml")

month = [m for m in year if m in soup.table.tbody.tr.td.string][0]

menu = pd.DataFrame(columns = week.keys())

table = soup.table.tbody

clean = [c for c in table.contents if type(c) == element.Tag][2:]

for name, row in zip(classes, clean):
    
    print(name)
    
    if row.td.string != name: print("Warning")
    
    row = [v for v in row.contents if type(v) == element.Tag][1:]
    
    values = [value.string if value.string != None else value.p.string for value in row]
    
    data_row = pd.Series(data = values, name = name, index = week.keys())
    print(data_row)
    
    menu = menu.append(data_row)

        