This program logs into the Canvas learning management system for all classes (PPS specific currently).
Since the PPS school district uses Canvas login to detect attendance, this program can automatically fulfill that.
The program requires that the user has a Chrome browser on his/her machine.

To setup the program, put your Canvas username and password into the "login.txt" file like below:
Username
Password

To specify times, enter them in the "times.txt" file like below:
01:15
12:15
16:50

The system uses 24-hour time, and single digit numbers (from 1-9 AM) must have a 0 at the start.
The file is currently set to PPS asynchronous class times (Pacififc Time).

Making a shortcut to the executable (which can be found in the EXE folder) and putting it in the startup folder is recommended.
The "quiet" program version will not display any information, and this is likely the best version to use.
>> Right click on the EXE file and click create shortcut.
>> Copy to the start folder.  On Windows, the start folder is: C:\Users\{your username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

Check the history.log file to make sure the program is running correctly for a given session.
The firewall may also block the program on it's first login attempt.  If this happens, just allow it access.

Enjoy :)