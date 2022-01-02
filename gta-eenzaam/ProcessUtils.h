#pragma once
#include <windows.h>
#include <tlhelp32.h>

typedef LONG(NTAPI* NtSuspendProcess)(IN HANDLE ProcessHandle);
typedef LONG(NTAPI* NtResumeProcess)(IN HANDLE ProcessHandle);

DWORD getProcessId(const char* processName);
bool suspend(DWORD processId);
bool resume(DWORD processId);
