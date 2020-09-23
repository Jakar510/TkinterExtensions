@echo off

rmdir /Q /S dist
mkdir dist

python setup.py build sdist bdist_wheel

python -m twine upload dist/*

