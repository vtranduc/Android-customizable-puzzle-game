# Android-customizable-puzzle-game
The game is available on Goolge Play!

https://play.google.com/store/apps/details?id=ca.ualberta.customizableanimeartpuzzle&amp;hl=en

To run this code on Windows 10, 64 bits (Which is the environment in which it was developed), please install proper version of Python and Kivy. At the time this is written, the developer had done the following:

1) Download and install Python 3.6.4, 32 bits for Windows 10.
2) Change the environment variables as following:
a) In PATH for both user variables for (username) and System variables, add
C:\...\Python36-32
C:\...\Python36-32\Lib
C:\...\Python36-32\Scripts
C:\...\Python36-32\DLLs
Note: Either put these on the top or delete the path to microsoft store. Otherwise, typing "python" in the terminal might open the store, and "python ..." might just show blank space.
If PYTHONPATH does not exist, create one. In it, add the path to all four above.
3) Open cmd terminal as admin and run the following:
python -m pip install --upgrade pip wheel setuptools
python -m pip install pygame
python -m pip install cython
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.angle
python -m pip install kivy
4) Now the kivy is ready. To run the app, open IDLE or Python 3.6.4 Shell, then open main.py file from it. Simply hit f5 to run the app.
5) Enjoy!

To reset the data, simply delete all .json files in the folder.
All json files need to be deleted before compiling into apk file.
