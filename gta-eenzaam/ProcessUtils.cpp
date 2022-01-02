#include "ProcessUtils.h"
#include <windows.h>
#include <tlhelp32.h>

DWORD getProcessId(const char* processName)
{
	PROCESSENTRY32 entry;
	entry.dwSize = sizeof(PROCESSENTRY32);

	HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, NULL);

	if (Process32First(snapshot, &entry) == TRUE)
	{
		while (Process32Next(snapshot, &entry) == TRUE)
		{
			if (_stricmp(entry.szExeFile, processName) == 0)
			{
				return entry.th32ProcessID;
			}
		}
	}

	CloseHandle(snapshot);

	return 0;
}

bool suspend(DWORD processId)
{
	HANDLE processHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processId);

	HMODULE ntdll = GetModuleHandle("ntdll");

	if (ntdll != NULL)
	{
		NtSuspendProcess pfnNtSuspendProcess = (NtSuspendProcess)GetProcAddress(ntdll, "NtSuspendProcess");

		pfnNtSuspendProcess(processHandle);
		CloseHandle(processHandle);
		return true;
	}
	else
	{
		return false;
	}
}

bool resume(DWORD processId)
{
	HANDLE processHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processId);

	HMODULE ntdll = GetModuleHandle("ntdll");

	if (ntdll != NULL)
	{
		NtResumeProcess pfnNtResumeProcess = (NtResumeProcess)GetProcAddress(ntdll, "NtResumeProcess");
		pfnNtResumeProcess(processHandle);
		CloseHandle(processHandle);
		return true;
	}

	return false;
}