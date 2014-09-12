# -*- coding: utf8 -*-
__author__ = 'Antol'

import csv
import numpy as np

def d_print(a):
    if is_debug: print(a)

is_debug = 1

# чтение csv-файла
print('---------------- чтение csv-файла ----------------')
# fname = 'res-with-limit.csv'
fname = 'train_data-Kasan.csv'
print(fname)
tr_data = []
with open(fname, 'r') as csvfile:
    csvlines = csv.reader(csvfile, delimiter=';')
    # csvfile.close()
    for row in csvlines:
        tr_data.append(row)
    csvfile.close()
    del tr_data[0]

d_print(tr_data)
x = np.array(tr_data[:])
d_print('x:')
d_print(x[:,(1,2,3,4)])

# одномерный массив
x1 = np.array(map(int, x[:, (6)]))
d_print(x1)

# nmer-мерный массив
nmer = 2
x2 = np.zeros((0, nmer), dtype=int)
d_print(x2)
s = 0
for i in x[:, range(1, nmer + 1)]:
    # d_print(i)
    x2 = np.append(x2, [map(int, i)], axis=0)
    s += 1
    # d_print(map(int, i))
d_print(x2)
print('Всего строк в файле: s = '+ str(s))
print('------------------ конец чтения ------------------')