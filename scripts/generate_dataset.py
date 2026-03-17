#!/usr/bin/env python3
"""Generate a dummy dataset of shape (1000, 11) at data/dataset.csv"""

import pandas as pd
import numpy as np
import os

os.makedirs('data', exist_ok=True)
np.random.seed(42)
df = pd.DataFrame(np.random.rand(1000, 10), columns=[f'feature_{i}' for i in range(10)])
df['target'] = np.random.randint(0, 2, 1000)
df.to_csv('data/dataset.csv', index=False)
print('dataset.csv generated successfully!')
