#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 22:03:48 2020

@author: shwetabhat
"""
# ====================Import libraries.====================================================================================
import functools
import operator
import re
import math
from itertools import groupby

import pandas as pd
from operator import itemgetter
import functools
import operator
from sklearn import preprocessing

# ====================Defining Paths.======================================================================================
##SET TRUE to ECHO.
ECHO = False
PATH_SUPPORT_FILE = r"C:/Users/Admin/Desktop/javaNegFIN/Support_bigData_NegFin.txt"
PATH_ITEMS_LIST_FILE = r"C:/Users/Admin/Desktop/javaNegFIN/output_bigData_NegFin.txt"
PATH_STATS_FILE = r"C:/Users/Admin/Desktop/javaNegFIN/Stats_bigData_recordLink.csv"
SUP = "#SUP:"
# =========================================================================================================================
# ====================Hash MAP Object Creation to store item and support. and other Variables.==========================================================
# =========================================================================================================================
new_dict = dict()
ANTECEDENTS = []
CONSEQUENTS = []
all_CONFIDENCE = []
COSINE = []
KULCZYNSKI = []
LIFT = []
SUPP = []
CONFIDENCE = []
RULES = []
tot_trans = 0
strings = list()
strings1 = list()

# =========================================================================================================================
# =========================================================================================================================
##Store item and support resp. in Hash Map.=============================================================================
# =========================================================================================================================
with open(PATH_SUPPORT_FILE, "r") as f:
    line = f.readline()
    tot_trans = float(line)
    # print(line)
    while True:
        line = f.readline()
        if not line:
            break
        item = re.sub("\s+", r" ", line).split(" ")[0]
        sup = re.sub("\s+", r" ", line).split(" ")[1]
        if ECHO:
            print(item, ":", sup)
        new_dict[item] = sup


f.close()
print(new_dict)


# =========================================================================================================================
##Defining methods to compute the Measures..=============================================================================
def token_sentence(text):
    x = sorted([int(s) for s in text.split(",")])
    return "".join(str(x).rstrip().lstrip())


def find_supersets(strings):
    superstrings = set()
    set_to_string = dict(zip([frozenset(s.split(",")) for s in strings], strings))
    for s in set_to_string.keys():
        for sup in superstrings.copy():
            if s <= sup:
                # print('{s!r} <= {sup!r}'.format(s = s, sup = sup))
                break
            elif sup < s:
                # print('{sup!r} <= {s!r}'.format(s = s, sup = sup))
                superstrings.remove(sup)
        else:
            superstrings.add(s)
    return [set_to_string[sup] for sup in superstrings]


def cal_lift(antecedent, sup, conseq):
    global new_dict
    if ECHO:
        print("=============LIFT==================================================")
        print("Antecedent:", antecedent)
        print("Conseq:", conseq)

    a = antecedent + ','
    a = a + conseq
    new_dict[a] = sup
    den = 1
    num = float(sup)
    sup_A = new_dict.get(antecedent)
    sup_C = new_dict.get(conseq)
    den *= float(sup_A) * float(sup_C)
    if ECHO:
        print("Sup_", antecedent, ":", sup_A, "Den:", den)
    lift = (num / den)
    if ECHO:
        print("Num:", num, "LIFT:", lift)
        print("=============LIFT==================================================")

    return lift


def cal_all_CONFIDENCE(antecedent, sup, conseq):
    global new_dict
    if ECHO:
        print("=============ALL CONFIDENCE==================================================")
        print("Antecedent:", antecedent)
        print("Conseq:", conseq)

    den = 0
    num = float(sup)
    sup_A = new_dict.get(antecedent)
    sup_C = new_dict.get(conseq)

    den = max(float(sup_C), float(sup_A))
    if ECHO:
        print("max{", sup_A, ",", sup_C, "}:", den)
        print("Sup_", antecedent, ":", sup_A, "Den:", den)
    conf = (num / den)
    if ECHO:
        print("Num:", num, "all_CONFIDENCE:", conf)
        print("=============ALL CONFIDENCE==================================================")

    return conf


def cal_CONF(antecedent, sup, conseq):
    global new_dict
    if ECHO:
        print("=============LIFT==================================================")
        print("Antecedent:", antecedent)
        print("Conseq:", conseq)

    a = antecedent + ','
    a = a + conseq
    new_dict[a] = sup
    sup_A = new_dict.get(antecedent)
    sup_C = new_dict.get(conseq)
    if ECHO:
        print("Sup_", antecedent, ":", sup_A, "Den:", sup_C)
    conf = float(sup_A) / float(sup_C)
    if ECHO:
        print("CONF:", conf)
        print("=============LIFT==================================================")
    return conf


def cal_KULCZYNSKI(antecedent, sup, conseq):
    global new_dict
    if ECHO:
        print("=============KULCZYNSKI==================================================")
        print("Antecedent:", antecedent)
        print("Conseq:", conseq)

    K = 0
    num = float(sup)
    sup_A = float(new_dict.get(antecedent))
    sup_C = float(new_dict.get(conseq))

    K += (num / sup_A) + (num / sup_C)
    if ECHO:
        print("Sup_", antecedent, ":", sup_A, "Ratio_", antecedent, ":", (num / sup_A))
        print("Sup_", conseq, ":", sup_C, "Ratio_", conseq, ":", (num / sup_C), "K:", K)

    K = 1 / 2 * K
    if ECHO:
        print("Num:", num, "KULCZYNSKI:", K)
        print("=============KULCZYNSKI==================================================")

    return K


def cal_COSINE(antecedent, sup, conseq):
    global new_dict
    if ECHO:
        print("=============COSINE==================================================")
        print("Antecedent:", antecedent)
        print("Conseq:", conseq)

    sup_A = new_dict.get(antecedent)
    sup_C = new_dict.get(conseq)

    den = 1
    num = float(sup)
    den = float(sup_A) * float(sup_C)
    if ECHO:
        print("Sup_", antecedent, ":", sup_A, "Sup_", conseq, ":", sup_C, "Den:", den)
    den = math.sqrt(den)
    cosine = (num / den)
    if ECHO:
        print("Num:", num, "COSINE:", cosine)
        print("=============COSINE==================================================")
    return cosine


# ==============Pre-processing the Frequent Items List file.===============================================================
##Pre-Processing:Finding antecedant and consequent.#======================================================================
# =========================================================================================================================
def preprocessing():
    with open(PATH_ITEMS_LIST_FILE, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            # print(line.split("#SUP:"))
            temp = re.sub("\s+", r" ", line).split(SUP)
            if ECHO and temp[0] != ' ':
                print("===============================================================")
            if temp[0] != ' ':
                antecedent = temp[0]
                sup = temp[1]
                antecedent = re.sub("\s+", r",", antecedent)
                antecedent = antecedent[:len(antecedent) - 1]
                coseq = antecedent.split(",")
                if len(coseq) != 1:
                    coseq = coseq[len(coseq) - 1]
                    strings1.append([antecedent, int(sup)])
                    strings.append(antecedent)
                    antecedent = ",".join(antecedent.split(",")[:-1])
                    lift = cal_lift(antecedent, sup, coseq)
                    all_conf = cal_all_CONFIDENCE(antecedent, sup, coseq)
                    K = cal_KULCZYNSKI(antecedent, sup, coseq)
                    cosine = cal_COSINE(antecedent, sup, coseq)
                    conf = cal_CONF(antecedent, sup, coseq)
                    ANTECEDENTS.append(antecedent)
                    CONSEQUENTS.append(coseq)
                    all_CONFIDENCE.append(all_conf)
                    COSINE.append(cosine)
                    KULCZYNSKI.append(K)
                    LIFT.append(lift)
                    SUPP.append(int(sup))
                    CONFIDENCE.append(conf)
                    if ECHO:
                        print("{", antecedent, "}->", "{", coseq, "}", "Sup:", sup)
                        print("LIFT:", lift, "all_CONFIDENCE:", conf, "KULCZYNSKI:", K, "COSINE:", cosine)
                        print("===============================================================")
        f.close()


# =========================================================================================================================
# =========================================================================================================================
##Calling method to print all the measures for respective Frequent Items.==================================================
# =========================================================================================================================
preprocessing()

# x=pd.DataFrame({"Strings":strings})
# x['Strings']=x['Strings'].apply(token_sentence)
# SuperSets=find_supersets(x['Strings'].to_list())

# indexesSuperSets=sorted([allSets.index(item) for item in SuperSets])

lst = strings1 #rule + support
t = [[x[0] for x in g] for k, g in groupby(lst, key=lambda x: x[1])]
#grouped based on support value
sets = list()
addIndices = 0
SuperSets = []

for i, strings in enumerate(t):
    x = pd.DataFrame({"Strings": strings})
    x['Strings'] = x['Strings'].apply(token_sentence)
    if (len(sets)):
        if ECHO:
            print(len(sets))
        addIndices += len(t[i - 1])
    else:
        if ECHO:
            print("NULL")
        addIndices = 0
    sets = find_supersets(x['Strings'].to_list())
    x = x['Strings'].to_list()
    sets = sorted([x.index(item) for item in sets])
    if (addIndices != 0):
        sets = list(map(lambda x: x + addIndices, sets))
    SuperSets.append(sets)

indexesSuperSets = functools.reduce(operator.concat, SuperSets)

del SuperSets, strings, strings1

ANTECEDENTS = list(itemgetter(*indexesSuperSets)(ANTECEDENTS))
CONSEQUENTS = list(itemgetter(*indexesSuperSets)(CONSEQUENTS))
SUPP = list(itemgetter(*indexesSuperSets)(SUPP))
CONFIDENCE = list(itemgetter(*indexesSuperSets)(CONFIDENCE))
LIFT = list(itemgetter(*indexesSuperSets)(LIFT))
all_CONFIDENCE = list(itemgetter(*indexesSuperSets)(all_CONFIDENCE))
COSINE = list(itemgetter(*indexesSuperSets)(COSINE))
KULCZYNSKI = list(itemgetter(*indexesSuperSets)(KULCZYNSKI))

ANTECEDENTS.append("AVERAGE:")
CONSEQUENTS.append(" ")
SUPP = list(map(lambda x: x / tot_trans, SUPP))
SUPP.append(sum(SUPP) / tot_trans)
CONFIDENCE.append(sum(CONFIDENCE) / len(CONFIDENCE))
LIFT.append(sum(LIFT) / len(LIFT))
all_CONFIDENCE.append(sum(all_CONFIDENCE) / len(all_CONFIDENCE))
COSINE.append(sum(COSINE) / len(COSINE))
KULCZYNSKI.append(sum(KULCZYNSKI) / len(KULCZYNSKI))
# =========================================================================================================================
##Printing the Statistical measures values and items list to file .==================================================
# =========================================================================================================================
df = pd.DataFrame(
    {"ANTECEDANTS": ANTECEDENTS, "CONSEQUENTS": CONSEQUENTS, "SUPPORT": SUPP, "CONFIDENCE": CONFIDENCE, "LIFT": LIFT,
     "all_CONFIDENCE": all_CONFIDENCE, "KULCZYNSKI": KULCZYNSKI, "COSINE": COSINE})
df.to_csv(PATH_STATS_FILE, header=True, index=False)
print("---- after file write step ----")
print(new_dict)
# =========================================================================================================================
# ================References:=========================================================================================================
# =========================================================================================================================
# https://michael.hahsler.net/research/association_rules/measures.html#cosine
# https://stackoverflow.com/questions/40313483/pythonic-way-to-group-list-by-key
# https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
# https://stackoverflow.com/questions/14363016/finding-superstrings-in-a-set-of-strings-in-python
# =========================================================================================================================