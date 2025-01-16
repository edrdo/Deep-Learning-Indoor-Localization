import os
from pathlib import Path
import random
import sys

def gen(inp_dir, out_dir, type, label, lf):
    idir = inp_dir + "/" + label
    odir = out_dir + "/" + type + "/" + label
    os.makedirs(odir, exist_ok=True)
    for f in list(lf):
        sf = os.path.abspath(idir + "/" + f)
        df = odir + "/" + f
        if os.path.islink(df):
            os.unlink(df)
        os.symlink(sf, df)

def gens(inp_dir, out_dir, label, lf):
    random.shuffle(lf)
    gen(inp_dir, out_dir, 'train', label, lf[:40])
    gen(inp_dir, out_dir, 'valid', label, lf[40:45])
    gen(inp_dir, out_dir, 'test', label, lf[45:])



inp_dir = sys.argv[1]
out_dir = sys.argv[2]


random.seed(123456789)

for d in os.listdir(inp_dir):
    pd = inp_dir + "/" + d
    if not os.path.isdir(pd):
        continue
    lf = os.listdir(pd)
    plf = sorted([ x  for x in lf if 'pixel' in x])
    xlf = sorted([ x  for x in lf if 'xiaomi' in x])
    gens(inp_dir, out_dir, d, plf)
    gens(inp_dir, out_dir, d, xlf)





