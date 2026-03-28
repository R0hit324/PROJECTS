=========================================================
           PYTHON BACKGROUND SENDER & LISTENER
=========================================================

Description:
-------------
This project demonstrates a simple client-server setup using Python.
The sender runs in the background on Windows and sends log output 
to a listener (server) running on another system every 2 seconds.

---------------------------------------------------------
FILES INCLUDED
---------------------------------------------------------
1. log.py   -> Client-side script (sends log data)
2. listen.py    -> Server-side script (receives data)
3. README.txt      -> Instructions and usage guide

---------------------------------------------------------
REQUIREMENTS
---------------------------------------------------------
- Python 3.8 or newer
- Works on Windows (sender) and Windows/Linux (listener)
- Install dependencies using pip:

    pip install pyinstaller pynput

---------------------------------------------------------
HOW IT WORKS
---------------------------------------------------------
- The sender reads or generates log output every 2 seconds.
- It connects to the listener over TCP and sends the output.
- The listener displays the incoming data in real time.

---------------------------------------------------------
STEP 1: SETTING UP THE LISTENER (SERVER)
---------------------------------------------------------
1. Open listener_server.py in any text editor.
2. Set the IP and port if needed:
       HOST = "0.0.0.0"
       PORT = 5555
3. Run the script on the machine that will receive the data:
       python listen.py
4. The console will show:
       [LISTENER] Listening on 0.0.0.0:5555
       [LISTENER] Connection from 192.168.0.xx
       [LISTENER] Received: example log message...

---------------------------------------------------------
STEP 2: SETTING UP THE SENDER (CLIENT)
---------------------------------------------------------
1. Open sender_background.py in a text editor.
2. Set the server IP and port to match your listener:
       SERVER_HOST = "192.168.0.100"   # Replace with listener IP
       SERVER_PORT = 5555
3. Run the script directly for testing:
       python log.py
4. You should see messages arriving at the listener.

---------------------------------------------------------
STEP 3: BUILDING THE EXECUTABLE (.EXE)
---------------------------------------------------------
You can package the sender into a single Windows executable file 
that runs silently in the background.

OPTION 1: Using Virtual Environment (Recommended)
---------------------------------------------------------
    cd C:\Users\akhil\myproject
    python -m venv venv
    .\venv\Scripts\activate
    pip install --upgrade pip
    pip install pyinstaller pynput
    .\venv\Scripts\pyinstaller.exe --onefile --noconsole --clean --collect-all ^
      . log.py

OPTION 2: Using Global PyInstaller Installation
---------------------------------------------------------
    pyinstaller --onefile --noconsole --clean --collect-all ^
      . log.py

After building, your executable will appear in:
    dist\log.exe

---------------------------------------------------------
STEP 4: CLEANING UP
---------------------------------------------------------
After building, remove unnecessary build files:
    rmdir /s /q build
    del log.spec

Keep only:
    dist\log.exe
    listen.py
    README.txt

---------------------------------------------------------
TROUBLESHOOTING
---------------------------------------------------------
- If the exe does nothing, rebuild without --noconsole to view errors.
- Add extra --hidden-import flags if modules are missing.
- Make sure your firewall allows communication on the chosen port.

---------------------------------------------------------
NOTES
---------------------------------------------------------
- Use this only in a safe, isolated, and controlled environment.
- Do not use this script to collect data from any unauthorized system.
- Intended strictly for testing and educational projects.

---------------------------------------------------------
AUTHOR
---------------------------------------------------------
Created by: Akhil Tripathi
Purpose: Educational / Project testing in virtual environment
License: MIT License (Free to modify and use for learning)

=========================================================
