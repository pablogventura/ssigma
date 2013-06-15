#!/usr/bin/env python
# -*- coding: utf8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.

from parser import *

p=Parser()

h=p.programa_desde_archivo("devuelveunoconh.code")
e=Ejecucion(h)
f=e.orquilla_numerica(0,1)
f("g")

