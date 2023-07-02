import os

root = os.getcwd()
src = os.path.join(root, "src")

if not os.path.exists(src):
    root = os.path.join(root, os.path.basename(root))
    src = os.path.join(root, "src")

static = os.path.join(root, "static")

