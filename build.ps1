cd D:\WorkSpace\PyDebug> 

Get-ChildItem -Path "./dist" -Include *.* -File -Recurse | foreach { $_.Delete()}
Get-ChildItem -Path "./build" -Include *.* -File -Recurse | foreach { $_.Delete()}


python setup.py build sdist

python setup.py install

python -m twine upload dist/*

pause
