#!/usr/bin/env python
# -*- coding: utf8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.

class Infinitupla(list):
    def __init__(self, es_numerica):
        super(Infinitupla, self).__init__()
        self.numerica = es_numerica
    def __getitem__(self, key):
        assert key != 0, "las infinituplas se indexan desde 1"
        if key >= 1:
            key -= 1
        if 0 <= key < len(self) or key < 0:
            return super(Infinitupla, self).__getitem__(key)
        else:
            if self.numerica:
                return 0
            else:
                return ""

    def __setitem__(self, key, value):
        assert key != 0, "las infinituplas se indexan desde 1"
        if key >= 1:
            key -= 1
        if 0 <= key < len(self) or key < 0:
            super(Infinitupla, self).__setitem__(key, value)
        else:
            for i in range(len(self), key):
                if self.numerica:
                    self.append(0)
                else:
                    self.append("")
            self.append(value)
    
    def __getslice__(self, i, j):
        assert i != 0 and j != 0, "las infinituplas se indexan desde 1"
        if i >= 1:
            i -= 1
        if j >= 1:
            j -= 1
        print i,j
        return super(Infinitupla, self).__getslice__(i, j)

#object.__setitem__(self, key, value)


#object.__delitem__(self, key)


#object.__iter__(self)



#object.__reversed__(self)


