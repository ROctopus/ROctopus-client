pyuic5 source/aboutdialog.ui -o aboutdialog.py
pyuic5 source/mainwindow.ui -o mainwindow.py
pyuic5 source/preferencesdialog.ui -o preferencesdialog.py
pyrcc5 source/qtresources.rcc -o qtresources.py
echo 'All .ui files converted to .py!'
