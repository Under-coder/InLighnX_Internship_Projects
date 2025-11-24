📌 **Port Scanner Using Python**
-------------------------------------

This repository contains two versions of a Python-based port scanner.
The base version provides the basic TCP port-scanning functionality, while Port Scanner 2.0 introduces additional features in a modular structure.

-----------------------------
**1. Base Version — scanner.py**

The file scanner.py represents the original implementation, focusing on:
- Multithreaded TCP port scanning
- Service detection using getservbyport
- Banner grabbing where available
- Simple console progress updates
- Clean terminal output formatting

This file serves as the foundational port scanner on which the enhanced version is built.

------------------------------------

**2. Enhanced Version — Port Scanner 2.0**

The folder Port Scanner 2.0 contains a more structured and feature-rich version of the tool.
The original scanning logic remains same, but additional capabilities are implemented as separate modules, making the project scalable and maintainable.

Modules inside the folder:
- scanner2.py
  - The basic program for scanning ports.

- udp_scanner.py
  - Provides UDP port scanning support.
   - Handles open, closed, and open | filtered cases.

- os_detect.py
  - Implements basic OS fingerprinting using TTL analysis from ICMP responses.

- gui.py
  - Adds a Tkinter-based graphical interface offering:
       - Input fields for target and port range
       - Options for TCP scan, UDP scan, and OS detection
       - A progress bar
       - A tabular result view

- main.py
  - Acts as the entry point for the enhanced version.
  - Allows choosing between command-line mode and GUI mode.
