cd D:\WorkSpace\PyDebug> 

Get-ChildItem -Path "./dist" -Include *.* -File -Recurse | foreach { $_.Delete()}
Get-ChildItem -Path "./build" -Include *.* -File -Recurse | foreach { $_.Delete()}


python setup.py build sdist

python -m twine upload dist/*

pause
