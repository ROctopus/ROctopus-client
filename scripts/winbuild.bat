%PYINSTALLER% ^
    --noconfirm --log-level=INFO ^
    --onefile --windowed ^
    --name="rocto-client" ^
    --icon=rocto_client\Qt\ui\source\icons\rocto_icon.ico ^
    rocto_client\__main__.py
