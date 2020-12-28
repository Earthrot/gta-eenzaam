import os
import time
import ctypes
from ctypes.wintypes import HANDLE, LONG, ULONG
from ctypes import c_long, c_int, c_uint, c_char, c_ubyte, c_char_p, c_void_p
from ctypes import windll
from ctypes import Structure
from ctypes import sizeof, POINTER, pointer, cast

TH32CS_SNAPPROCESS = 2
STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)

class PROCESSENTRY32(Structure):
  _fields_ = [('dwSize', c_uint), 
              ('cntUsage', c_uint),
              ('th32ProcessID', c_uint),
              ('th32DefaultHeapID', c_uint),
              ('th32ModuleID', c_uint),
              ('cntThreads', c_uint),
              ('th32ParentProcessID', c_uint),
              ('pcPriClassBase', c_long),
              ('dwFlags', c_uint),
              ('szExeFile', c_char * 260), 
              ('th32MemoryBase', c_long),
              ('th32AccessKey', c_long)]

CreateToolhelp32Snapshot= windll.kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.reltype = c_long
CreateToolhelp32Snapshot.argtypes = [c_int, c_int]
Process32First = windll.kernel32.Process32First
Process32First.argtypes = [c_void_p, POINTER(PROCESSENTRY32)]
Process32First.rettype = c_int
Process32Next = windll.kernel32.Process32Next
Process32Next.argtypes = [c_void_p, POINTER(PROCESSENTRY32)]
Process32Next.rettype = c_int
OpenProcess = windll.kernel32.OpenProcess
OpenProcess.argtypes = [c_void_p, c_int, c_long]
OpenProcess.rettype = c_long
CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [c_void_p]
CloseHandle.rettype = c_int

RtlNtStatusToDosError = windll.ntdll.RtlNtStatusToDosError
NtSuspendProcess = windll.ntdll.NtSuspendProcess
NtResumeProcess = windll.ntdll.NtResumeProcess

def errcheck_ntstatus(status, *etc):
  if status < 0: raise ctypes.WinError(RtlNtStatusToDosError(status))
  return status

RtlNtStatusToDosError.argtypes = (LONG,)
RtlNtStatusToDosError.restype = ULONG

NtSuspendProcess.argtypes = (HANDLE,)
NtSuspendProcess.restype = LONG
NtSuspendProcess.errcheck = errcheck_ntstatus

NtResumeProcess.argtypes = (HANDLE,)
NtResumeProcess.restype = LONG
NtResumeProcess.errcheck = errcheck_ntstatus

def GetProcessIdFromName(ProcessName):
  hProcessSnap = c_void_p(0)
  hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

  pe32 = PROCESSENTRY32()
  pe32.dwSize = sizeof(PROCESSENTRY32)
  ret = Process32First(hProcessSnap, pointer(pe32))

  while ret:
    if pe32.szExeFile.decode() == ProcessName:
      return pe32.th32ProcessID
    ret = Process32Next(hProcessSnap, pointer(pe32))
  
  return None

def SuspendProcess(pId):
  hProcess = OpenProcess(PROCESS_ALL_ACCESS, 0, pId)
  NtSuspendProcess(hProcess)
  CloseHandle(hProcess)

def ResumeProcess(pId):
  hProcess = OpenProcess(PROCESS_ALL_ACCESS, 0, pId)
  NtResumeProcess(hProcess)
  CloseHandle(hProcess)