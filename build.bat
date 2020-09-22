rm ./dist/*

python setup.py build sdist bdist_wheel

python setup.py install

python -m twine upload dist/*

pause
