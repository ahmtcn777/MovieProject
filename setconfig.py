import os
from pathlib import Path
from shutil import copy
import os
import asyncio
import subprocess
from tkinter import messagebox
import ctypes

configs = ["WebUI\\LocalHostAuth=true", "WebUI\\Address=*",
           "WebUI\\Enabled=false"]
errorMsg = "Uygulamayı kullanabilmeniz için qBittorrent yüklü olmalıdır."


def setConfiguration():
    path = str(Path.home())+'\\AppData\\Roaming\\qBittorrent\\qBittorrent.ini'
    file = open(path, 'r')
    content = file.read()
    if configs[0] in content:
        content.replace(configs[0], "WebUI\\LocalHostAuth=false")
    if configs[1] in content:
        content.replace(configs[1], "WebUI\\Address=127.0.0.1")
    if configs[2] in content:
        content.replace(configs[2], "WebUI\\Enabled=true")
    file.close()
    file = open(path, "w")
    file.write(content)
    file.close()


def setConf():
    asyncio.run(closeExe())
    path = os.getcwd()+'\\qBittorrent\\'
    copyPath = str(Path.home())+'\\AppData\\Roaming\\qBittorrent'
    copy(path+'qBittorrent-data.ini', copyPath)
    copy(path+'qBittorrent.ini', copyPath)
    try:
        subprocess.Popen(path+'qBittorrent.exe',  stderr=subprocess.PIPE)
    except OSError:
        ctypes.windll.user32.MessageBoxW(None, errorMsg, "Hata", 0x40 | 0x0)


async def closeExe():
    os.system("TASKKILL /F /IM qbittorrent.exe")


if __name__ == "__main__":
    setConf()
