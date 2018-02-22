Installation:
--------

1. Creating virtualenv for the project is recommended, pip is required to install dependencies
1. Install dependencies with ``pip install -e .``
1. Copy configuration file: ``cp config.ini.template config.ini``
1. Copy example data file: ``cp config.csv.template config.csv``
1. Run with ``python pulsar`` 
1. Turn off with ``CTRL+C``, but it might cause issues on Windows

Notes:
--------
- Configuration CSV file needs to be without heading row, in ``URL;Text_To_Find`` format, semicolon separator
- Script looks for given text in whole response, so it can give false positives for commented out code. For more precise checks headless browser would be needed
- Web interface page auto-refreshes in frequency depending on data refresh (more or less, tests take few seconds and it's a dumb auto-refresh)

Future development:
--------
For multiple clients in different locations, central server would be needed.

Instead of inelegant text log, database for both clients and server is preferable.
More so, additional script, responsible only for sending data to the server would be recommended.

Data sent to the server could be in json format, containing information regarding time of test, and outcome of each test, preferably for all tests conducted since last communication, with some upper limit of records that could be sent in case of longer downtime (so it would not generate too big requests).

Since geo-location of own IP address can generate false information, info about client's location should be kept in configuration file.

Because central server would not have publicly accessible API, simple user/password authentication and https connection should be enough to protect it from false data injections. 

Contact
--------
Project website: https://github.com/Boberro/pulsar