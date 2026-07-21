#include <stdio.h>
#include <stdlib.h>

enum OS
{
    WINDOWS = 0,
    LINUX = 2,
    MACOS = 3,
    OHER = 4
};

enum OS detect_os()
{
#if defined(_WIN32) || defined(_WIN64)
    return WINDOWS;
#elif defined(__linux__)
    return LINUX;
#elif defined(__APPLE__) && defined(__MACH__)
    return MACOS;
#else
    return OHER;
#endif
}

int main(void)
{
    const enum OS current_os = detect_os();

    switch (current_os)
    {
    case WINDOWS:
        system("python --version");
        break;
    case LINUX:
        system("python3 main.py");
        break;
    case MACOS:
        system("python --version");
        break;
    default:
        printf("Detected OS: Other\n");
        break;
    }
}