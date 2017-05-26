# Roctopus-client
This is a minimal working example of a client for Roctopus. Currently has severe drawbacks.

# Urgent to-do:
* Pack the dependencies: PyQt5 and socketIO-client. (Done for Windows executable.)
* Implement task requesting and ~~running~~ function~~s~~ in threads.
* Profile the start-up.

# How to use?
First you will need to install dependencies:

* Python 3.6
* [PyQt5](https://pypi.python.org/pypi/PyQt5)
* [socketIO-client](https://pypi.python.org/pypi/socketIO-client)

Then open up a command line in the root folder of the project and run
`python ROctopus_client/Qt/gui.py`.

# How to compile?
* Check the `buildcommand.txt` file and adjust the command for your system.
* Run the build command **in the root folder of the project.**
