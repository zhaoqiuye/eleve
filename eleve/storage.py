from eleve.memory import MemoryTrie
from eleve.leveldb import LevelTrie
import math

# -*- coding:utf8 -*-
""" Storage interface for LM
"""

class MemoryStorage:
    order = None

    def __init__(self, order):
        assert order > 0 and isinstance(order, int)
        self.order = order

        self.bwd = MemoryTrie(order)
        self.fwd = MemoryTrie(order)

    def add_sentence(self, sentence, freq=1):
        if not sentence:
            return

        token_list = ['^'] + sentence + ['$']
        for i in range(len(token_list) - 1):
            self.fwd.add_ngram(token_list[i:i+self.order], freq)
        token_list = token_list[::-1]
        for i in range(len(token_list) - 1):
            self.bwd.add_ngram(token_list[i:i+self.order], freq)

    def clear(self):
        self.bwd.clear()
        self.fwd.clear()

    def update_stats(self):
        self.bwd.update_stats()
        self.fwd.update_stats()

    def query_autonomy(self, ngram):
        result_fwd = self.fwd.query_autonomy(ngram)
        result_bwd = self.bwd.query_autonomy(ngram[::-1])
        if math.isnan(result_fwd) or math.isnan(result_bwd):
            return float('nan')
        return (result_fwd + result_bwd) / 2
     
    def query_ev(self, ngram):
        result_fwd = self.fwd.query_ev(ngram)
        result_bwd = self.bwd.query_ev(ngram[::-1])
        if math.isnan(result_fwd) or math.isnan(result_bwd):
            return float('nan')
        return (result_fwd + result_bwd) / 2

    def query_count(self, ngram):
        count_fwd = self.fwd.query_count(ngram)
        count_bwd = self.bwd.query_count(ngram[::-1])
        return (count_fwd + count_bwd) / 2

    def query_entropy(self, ngram):
        entropy_fwd = self.fwd.query_entropy(ngram)
        entropy_bwd = self.bwd.query_entropy(ngram[::-1])
        if math.isnan(entropy_fwd) or math.isnan(entropy_bwd):
            return float('nan')
        return (entropy_fwd + entropy_bwd) / 2

class LevelStorage(MemoryStorage):

    def __init__(self, order, path=None):
        assert order > 0 and isinstance(order, int)
        self.order = order

        if path is None:
            path = '/tmp/level_storage'

        self.bwd = LevelTrie(path=(path + '_bwd'))
        self.fwd = LevelTrie(path=(path + '_fwd'))
