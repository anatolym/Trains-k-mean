# -*- coding: utf8 -*-
__author__ = 'Antol'

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import numpy as np
import matplotlib
import pylab
pylab.close()
import test3_read_from_file as csv_data #чтение данных из csv

def d_print(a):
    if is_debug: print(a)

# incoming data
is_debug = 0
k = 3                       # количество кластеров
n = csv_data.s  # = 100     # количество строк в массиве (поезда)
nmer = csv_data.nmer        # количество типов вагонов в композиции, nmer-ный массив
m = csv_data.x2             # m = np.random.random(n) * 1000 - testing

cl_o = np.zeros((1, n), dtype=np.int)
it_o = 0
y_out = np.zeros(((1, k, nmer)))

def a_kmeans():
    print('------ расчёт ' + str(nmer) + '-мерной задачи кластеризации ------')
    # заполняем одномерный массив m данными о вместимости составов из csv-файла
    # вынесено из функции a_kmeans
    a = np.random.random(k)

    a.sort()
    d_print('m:')
    d_print(m)
    d_print(a)
    pn = 12 #макс. кол-во плацк. вагонов
    kn = 14 #макс. кол-во куп. вагонов

    chk = -1
    it = 0
    while chk != 0:
        d_print('---------------- ' + str(it) + ' ----------------')

        if it == 0:
            # определяем первоначальные центроиды (выбраны случайно из диапазона значений m)
            y = np.zeros(((1, k, nmer)))
            # y[it, :] = [(m.max() - m.min()) * a[i] for i in range(k)]
            # y[it, :] = [m[round(n * 0.5, 0) + k] for i in range(k)] # случайная точка из центра выборки
            # y[it, :] = [m[round(n * (1 - a[i]), 0)] for i in range(k)] # случайная точка
            y[it, :] = [(a[i]*pn, (1 - a[i])*kn) for i in range(k)] # псевдослучайная точка для конкретной двумерной выборки поездов
            # y[it, :] = [[4, 11], [7, 8], [10, 5]] # вычисленные центроиды кластеров
            d_print('y0:')
            d_print(y)
            r = np.zeros(((1, n, k)))
            cl = np.zeros((1, n), dtype=np.int)
        else:
            r = np.append(r, [[[0 for i in range(k)] for j in range(n)]], axis=0)
            cl = np.append(cl, [[0 for i in range(n)]], axis=0)
 
        # вычисляем длины векторов r = |ym| - трёхмерный массив
        for i in range(n):
            for j in range(k):
                r[it, i, j] = np.sqrt(sum([(y[it, j, t] - m[i, t])**2 for t in range(nmer)]))
        d_print('r:')
        d_print(r)
        d_print(r[0,0,:].min())

        # вычисляем минимальное растояние до центроидов и проставляем кластеры
        for i in range(n):
            r_min = r[it, i, :].min()
            for j in range(k):
                if r[it, i, j] == r_min:
                    cl[it, i] = j
            # d_print(m[i, :], cl[it, i], r[it, i, :])
        d_print(cl)

        # пересчитываем центроиды, записываем в следующую итерацию
        y = np.append(y, [[[0 for i in range(nmer)] for j in range(k)]], axis=0)
        d_print('y:'+str(it))
        d_print(y)
        for j in range(k):
            j1 = int(0)
            s1 = np.zeros(nmer) #s1 = [0 for t in range(nmer)]
            for i in range(n):
                if cl[it, i] == j:
                    for t in range(nmer):
                        s1[t] += m[i, t]
                    j1 += 1
            if j1 != 0:
                y[it + 1, j, :] = [s1[t]/j1 for t in range(nmer)]

        d_print('y+1:'+str(it))
        d_print(y)

        it += 1
        # проверка завершения смещения центроидов
        chk = 0
        for j in range(k):
            for t in range(nmer):
                chk += abs(y[it, j, t] - y[it - 1, j, t])
        d_print(chk)
        if it >= 100:
            chk = 0
    it -= 1
    print('Решено за ' + str(it) + ' итерации(й).')
    print('----------------- конец расчёта ------------------')
    return y[it]

# program
max_attmps = 600
for it1 in range(max_attmps):
    if it1 == 0:
        y_out[0] = a_kmeans()
    else:
        y_out = np.append(y_out, [a_kmeans()], axis=0)
print('Центроиды y по ' + str(max_attmps) + ' итерации(ям):')
print(y_out)
y_out_res = np.zeros(((1, k, nmer)))
for i in range(k):
    x_res = sum(y_out[j, i, 0] for j in range(max_attmps)) / max_attmps
    y_res = sum(y_out[j, i, 1] for j in range(max_attmps)) / max_attmps
    y_out_res[0, i, :] = (x_res, y_res)
    print('Координаты кластера ' + str(i) + ': ' + str(x_res) + ', ' + str(y_res) + ' = ' + str(x_res + y_res))
print(y_out_res)
colors_y = np.zeros((max_attmps * k, 3))
k1 = 0
for i in range(max_attmps * k):
    colors_y[i, :] = ([1,0,0],[0,1,0],[0,0,1],[1,1,1])[k1] # Red Green Blue White
    if k1 >= k - 1:
        k1 = 0
    else:
        k1 += 1
pylab.scatter(y_out[:,:,0], y_out[:,:,1], s=20*2+9, c=colors_y, marker='o')
pylab.scatter(y_out_res[:,:,0], y_out_res[:,:,1], s=90*2+9, c=colors_y, marker='^') # вывод суперцентроидов
pylab.savefig('clust.png')
plt.show()