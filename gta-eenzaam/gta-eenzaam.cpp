#include <windows.h>
#include <iostream>
#include <conio.h>
#include "ProcessUtils.h"

int main()
{
	try {
		DWORD pid = getProcessId("GTA5.exe");

		if (pid > 0)
		{
			std::cout << "GTA slaapje laten doen";

			suspend(pid);

			for (int i = 0; i < 10; i++)
			{
				Sleep(1000);
				std::cout << ".";
			}
			std::cout << std::endl;

			std::cout << "GTA weer wakker rammelen" << std::endl;

			resume(pid);

			std::cout << "ALL GOOD RATTY!" << std::endl;
		}
		else
		{
			std::cout << "GTA niet actief" << std::endl;
		}
	}
	catch (...)
	{
		std::cout << "Oeps, iets fout gegaan!" << std::endl;
		Sleep(3000);
	}

	Sleep(3000);
}

