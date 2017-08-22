Welcome to project SiqNAL
================

This project aims to provide a reliable open-sourced cubesats tracking following different
mechanisms and protocols for transmitting signals that too using very low end receiver i.e
Software Defined Radio (SDR) and under limited computation power. As an input it takes output file
of sdr (both .dat or .wav) plots waterfall displaying of the signal file showing signal present in different
bands of frequency. Further, it applies bandpass filtering to remove undesired frequency and based
upon the transmission mechanism used by the transponder on the satellite it follows appropriate tracking
pipeline. Right now transponders following Automatic Packet Reporting System (APRS), Beacons or
Automatic Picture Transmission (APT) is supported.

Our future goal is to make this project more universal by tracking signals using correlation of signal
received from different ground stations but, it will require us to know the preamble part of signal in
advance as well as synchronized signals from multiple sources since simple signal correlation gives 
ambiguous results due to colored gaussian noise.

This project is part of Google Summer of Code 2017 under [Aerospaceresearch](http://aerospaceresearch.net/) written by [Jay Krishna](https://github.com/jay-krishna) with [Andreas Hornig](https://github.com/hornig) as mentor.

Installation
========

This project requires

    Python-3.x
    Numpy >= 1.12.0
    Matplotlib >= 2.0.0
    Scipy >= 0.18.1
    PyQt4

Make sure you have ``python3.x`` and ``pip`` installeted on your machine then except for PyQt4 rest of the
dependencies can be installed using requirements.txt provided. Open terminal in SiqNAL folder and type

	pip3 install -r requirements.txt

**Note:** Above command may require administrative permissions.

Installation of PyQt4 is system dependent, for some major distributions steps are below.

1. **Ubuntu**
    
		sudo apt-get install python-qt4

2. **Windows**

	Run installer after downloading from [here](https://goo.gl/LgVh2).

3. **Mac OSX**

      	brew install qt
      	brew install sip
      	brew install cartr/qt4/pyqt
        
External Links
=========

For more details you can check this project's [documentation](https://goo.gl/8dddPf).