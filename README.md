# Instrumented Adder firmware

* [blog post](https://www.zerotoasiccourse.com/post/instrumenting-hardware-adders/)
* [results work in progress](https://docs.google.com/spreadsheets/d/1Bbo3fCbdY8g8DCxA7gg_Ctp8o8-8-lEE8ZSWUY6hakA/edit#gid=0)
* [design source](https://github.com/mattvenn/instrumented_adder)

# Serial control

Getting serial out via FTDI is annoying because it involves setting a hardware jumper that has to be changed to update the firmware.
Instead, connect a 3.3v USB serial converter to pins 5 (rx) and 6 (tx)

I used an Arduino nano 3.3v and leonardo with a firwmare that just echos forwards and backwards (see in serial test directory)
To start interaction:

    make monitor

Use [test.py](test.py) to run automated tests.
