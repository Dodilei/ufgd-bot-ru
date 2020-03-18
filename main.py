#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 08:26:53 2020

@author: mauricio
"""

#%% Initialize
print("Starting")

from bs4 import BeautifulSoup
from bs4 import element
import requests as rq

import datetime as dt

import pandas as pd

today = dt.datetime.utcnow() + dt.timedelta(hours = -4)

year = {1:"Janeiro",
       2:"Fevereiro",
       3:"Março",
       4:"Abril",
       5:"Maio",
       6:"Junho",
       7:"Julho",
       8:"Agosto",
       9:"Setembro",
       10:"Outubro",
       11:"Novembro",
       12:"Dezembro"}

week = {0:"Segunda- feira",
        1:"Terça- feira",
        2:"Quarta- feira",
        3:"Quinta- feira",
        4:"Sexta- feira",
        5:"Sábado"}

classes = ["Salada 1", "Salada 2", "Prato Principal 1", "Prato Principal 2", "Guarnição 1", "Guarnição 2", "Vegetariano", "Suco", "Sobremesa"]

weekday = week[today.weekday()]

month = year[today.month]

menu = pd.DataFrame(columns = week.values())


#%% Scraping
print("Getting data...")

pg = rq.get("https://portal.ufgd.edu.br/secao/restaurante-universitario-proae/cardapio", verify = "chain.pem")

soup = BeautifulSoup(pg.content, features = "lxml")

if not month in soup.table.tbody.tr.td.string: print("Warning, wrong month")

table = soup.table.tbody

clean = [c for c in table.contents if type(c) == element.Tag][2:]

for name, row in zip(classes, clean):
    
    if row.td.string != name: print("Warning, wrong row")
    
    row = [v for v in row.contents if type(v) == element.Tag][1:]
    
    values = [value.string if value.string != None else value.p.string for value in row]
    
    data_row = pd.Series(data = values, name = name, index = week.values())

    menu = menu.append(data_row)


#%% Assembly thread
print("Preparing text...")

menu_today = menu[weekday]

tweets = []

tweets.append(
    "Apresento-lhes o cardápio de hoje, dia {d} de {m}, {w}:".format(
                            d = today.day,
                            m = month,
                            w = weekday.lower().replace(" ", "")) + "\n\n" +
    "Prato principal: " +
    menu_today["Prato Principal 1"] + " ou " +
    menu_today["Prato Principal 2"] + "\n" +
    "Opção vegetariana: " + menu_today["Vegetariano"] + "\n\n" +
    "Salada: " +
    menu_today["Salada 1"] + ", " + menu_today["Salada 2"] + "\n\n" +
    "Guarnições: " +
    menu_today["Guarnição 1"] + " e " + menu_today["Guarnição 2"]
    )

tweets.append(
    "Hoje teremos suco de {sc}, e {s} de sobremesa.".format(
                                                    sc = menu_today["Suco"],
                                                    s = menu_today["Sobremesa"]
                                                    )
    )

tweets.append("Bom apetite! \\o/")


#%% Initialize TwitterAPI
print("Building tweeting powers...")

from TwitterAPI import TwitterAPI

tokens = open("token.txt", "r").read().split("\n")

api = TwitterAPI(*tokens)

tweet_ids = [None]

#%% Tweet
print("Tweeting...")

for tweet in tweets:
    
    params = {"status": tweet}
    
    last_id = tweet_ids[-1]
    if last_id:
        params["in_reply_to_status_id"] = last_id
        
    t = api.request("statuses/update", params)
    
    tweet_ids.append(t.json()["id"])
    print(tweet)