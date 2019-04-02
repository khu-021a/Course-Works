import os
import shutil
import numpy as np

source_path = 'inputs/'
target_path = 'targets/'

ts = np.random.permutation(159705).reshape((5, 31941))
print ts
ts = np.random.permutation(ts.T).T
print ts

a = []
for x in range(5):
    a.append(np.random.permutation(np.concatenate((np.zeros(1941), np.ones(30000)))))
j = np.array(a, dtype=int)

print j

m = (ts + 1) * j
n = m[m > 0].reshape((10, 15000))

b = []
for y in range(10):
    b.append(np.random.permutation(np.concatenate((np.zeros(5000), np.ones(10000)))))
k = np.array(b, dtype=int)

p = k * n
q = p[p > 0].reshape((10, 10000)) - 1

files = os.listdir(source_path)

for h in range(q.shape[0]):
    for i in range(q.shape[1]):
        shutil.move(source_path + files[q[h][i]], target_path + str(h) + '/' + files[q[h][i]])
