### What is a PID (Process Identification Number):

- **Definition:** A PID, or Process Identification Number, is a unique numerical identifier assigned to each running process on a Unix-like operating system.
  
- **Example:** If you run the command `ps` in the terminal, it will display a list of processes along with their PIDs. For instance, you might see a line like `1234 bash`, where `1234` is the PID of the running Bash shell process.

### What is a Process:

- **Definition:** A process is a running instance of a program in an operating system. It contains the program code and its current activity, including variables, memory, and system resources.

- **Example:** If you open a web browser, each tab or instance of the browser is a separate process. So, if you have multiple tabs open, each has its own PID and runs independently.

### How to Find a Process' PID:

- **Method:** The `ps` command is commonly used to find the PIDs of running processes. For example, `ps aux` will display detailed information about all processes, including their PIDs.

- **Example:** Running `ps aux | grep firefox` will show you the PID of the Firefox browser process.

### How to Kill a Process:

- **Method:** The `kill` command is used to terminate a process. You need to provide the PID of the process you want to kill. The signal `SIGTERM` (15) is commonly used for a graceful termination.

- **Example:** `kill -15 1234` will attempt to gracefully terminate the process with PID 1234.

### What is a Signal:

- **Definition:** A signal is a software interrupt delivered to a process to notify it that a specific event has occurred. Signals can be used to communicate between processes and to control or interrupt the execution of a process.

- **Example:** `SIGTERM` is a signal sent to request termination, while `SIGKILL` is a signal sent to forcefully kill a process.

### Two Signals that Cannot Be Ignored:

1. **SIGKILL (9):**
   - **Purpose:** Used to forcefully terminate a process.
   - **Example:** `kill -9 1234` will immediately terminate the process with PID 1234.

2. **SIGSTOP (19 or 20):**
   - **Purpose:** Pauses (stops) a process.
   - **Example:** `kill -19 1234` will pause the process with PID 1234.
