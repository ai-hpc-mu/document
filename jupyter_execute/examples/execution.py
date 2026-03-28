#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng()
data = rng.standard_normal((3, 100))
fig, ax = plt.subplots()
ax.scatter(data[0], data[1], c=data[2], s=3)

