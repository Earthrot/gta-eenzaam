import time
import procfreeze

ProcessName = "GTA5.exe"
#ProcessName = "notepad.exe"

try:
  pid = procfreeze.GetProcessIdFromName(ProcessName)
  if pid:

    print("GTA slaapje laten doen", end = "", flush = True)
    procfreeze.SuspendProcess(pid)

    for i in range(1, 10):
      print(".", end = "", flush = True)
      time.sleep(1)

    print(" ")

    print("GTA weer wakker rammelen")
    procfreeze.ResumeProcess(pid)

    print("ALL GOOD RATTY!")
    
  else:
    print("GTA niet actief")
except:
  print("Oeps, iets fout gegaan!")
  time.sleep(3)
  
time.sleep(2)