🛡️ KEYLOGGER DETECTION & DEFENSE GUIDE
--------------------------------------

TOOLS USED
-----------
- netstat – View active network connections
- capa – Analyze binary behavior (by Mandiant)

--------------------------------------

STEPS TO DETECT
----------------

1. CHECK ACTIVE CONNECTIONS
   Command:
   netstat -ano
   → Look for unfamiliar connections or ports.
   → Note the PID (Process ID) of suspicious activity.

2. VERIFY THE PROCESS
   Command:
   tasklist | findstr <PID>
   → Identify which executable file is using that PID.

3. ANALYZE THE FILE
   Command:
   capa suspicious.exe
   → Review capa output for suspicious actions like:
     - Keystroke logging
     - Persistence mechanisms
     - Network communications

4. REMOVE OR QUARANTINE
   Command:
   taskkill /PID <PID> /F
   → Stop the process and safely move or delete the file.

--------------------------------------

PREVENTION TIPS
----------------
- Avoid running unknown .exe files.
- Use virtual machines for testing.
- Regularly monitor network activity with netstat.
- Keep Windows Defender or antivirus active and updated.

--------------------------------------

This guide helps you detect and safely handle suspicious executables while keeping your system secure.
