# -*- coding: utf-8 -*-
# This file is part of S-Sigma.
# This code was written by Pablo Ventura in 2013, and is covered by the GPLv3.

class Infinitupla(list):
    """Estado s⃗ (numéricas) o σ⃗ (palabras). Índice desde 1."""
    def __init__(self, es_numerica):
        super(Infinitupla, self).__init__()
        self.numerica = es_numerica

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            if start is not None and start != 0:
                start = start - 1 if start >= 1 else start
            if stop is not None and stop != 0:
                stop = stop - 1 if stop >= 1 else stop
            return super(Infinitupla, self).__getitem__(slice(start, stop, step))
        assert key != 0, "las infinituplas se indexan desde 1"
        if key >= 1:
            key -= 1
        if 0 <= key < len(self) or key < 0:
            return super(Infinitupla, self).__getitem__(key)
        return 0 if self.numerica else ""

    def __setitem__(self, key, value):
        assert not isinstance(key, slice), "asignación por rebanado no soportada"
        assert key != 0, "las infinituplas se indexan desde 1"
        if key >= 1:
            key -= 1
        if 0 <= key < len(self) or key < 0:
            super(Infinitupla, self).__setitem__(key, value)
        else:
            for _ in range(len(self), key):
                self.append(0 if self.numerica else "")
            self.append(value)
