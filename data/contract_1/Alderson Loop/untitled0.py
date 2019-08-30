# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:20:00 2019

@author: Sina
"""

import spacy

nlp = spacy.load("en_core_web_sm")

doc =nlp( open('Alderson loop - Modified.txt').read())

for token in doc:
    print(token.text, token.pos_, token.dep_)