import subprocess
import platform
import os
import threading
import sys
import fnmatch
import winreg  # Windows专属库，用于操作注册表
import pyautogui
import time
import keyboard

#############################################文件查找(out!)########################################
"""
library=[]
def simple_find(app_name):###########浅查找##########################
    common_paths = [
        r"C:/Program Files (x86)/tencent/QQMusic/QQMusic.exe",
        r"C:/Program Files/tencent/QQMusic/QQMusic.exe",
        r"D:/Program Files (x86)/tencent/QQMusic/QQMusic.exe",
        r"D:/Program Files/tencent/QQMusic/QQMusic.exe",
        r"C:/Program Files (x86)/CloudMusic/cloudmusic.exe",
        r"C:/Program Files/CloudMusic/cloudmusic.exe",
        r"D:/Program Files (x86)/CloudMusic/cloudmusic.exe",
        r"D:/Program Files/CloudMusic/cloudmusic.exe",
        r"D:/CloudMusic/cloudmusic.exe"
    ]
    for path in common_paths:
        if os.path.exists(path) and app_name in path:
            return path
    return None
def advance_search(app_name):#############cmd查询？？有点不理解为什么失效~#####################
    try:
        result = subprocess.aim_output(f"where {app_name}.exe", shell=True, text=True)
        return result.strip().split('\n')[0]
    except:
        return None
def easy_find(app):###############方法整合##############
    path= simple_find(app)
    if path:
        return path
    else:
        return advance_search(app)
"""
#################################################路径获取#####################################################
def registry_search(app_name):
    # 定义注册表路径：64位系统和32位软件的注册表位置不同
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",  # 64位程序
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"  # 32位程序
    ]
    for reg_path in reg_paths:
        try:
            # 打开注册表键（类似打开文件夹）
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            # 遍历该键下的所有子项（类似查看文件夹里的文件）
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                # 打开子项
                with winreg.OpenKey(key, subkey_name) as subkey:
                    try:
                        # 读取软件名称（类似查看文件名）
                        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        if app_name.lower() in display_name.lower():
                            # 读取安装路径（类似查看文件内容）
                            install_path = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                            exe_path = os.path.join(install_path, f"{app_name}.exe")
                            if os.path.exists(exe_path):
                                return exe_path
                    except FileNotFoundError:
                        continue
        except Exception as e:
            pass
    return None
def deep_search(app_name,system_type,max_depth=3):#max_depth限制递归数量级
    if system_type == "Windows":
        targets = f"{app_name}.exe"
        common_dirs = [
            r"C:\CloudMusic",
            r"D:\CloudMusic",
            r"C:\QQMusic",
            r"D:\QQMusic",
            os.environ.get("PROGRAMFILES", ""),
            os.environ.get("PROGRAMFILES(X86)", ""),
            os.environ.get("LOCALAPPDATA", "")
        ]
    else:
        targets = app_name
        common_dirs = [
            "/Applications",  # Mac
            os.path.expanduser("~/.local/bin"),  # Linux
            "/usr/bin"
        ]
    for dir_path in common_dirs:
        if not os.path.exists(dir_path):
            continue
        for root,dirs,files in os.walk(dir_path):
            depth=root.count(os.sep)-dir_path.count(os.sep)
            if depth>max_depth:
                del dirs[:]####重点~！！停止递归子链
                continue#######重点~！！同级目录下一文件

            for file in fnmatch.filter(files, targets):  ###检测是否具有存在性
                full_path = os.path.join(root, file)  ###路径整合
                if os.path.isfile(full_path):
                    if system_type == "Windows" or os.access(full_path, os.X_OK):
                        return full_path
    return None
################################################启动软件##################################################
def run_it(app_path, system_type):
    if system_type == 'Windows':
        try:
            subprocess.Popen(
                ["start", "", app_path],
                shell=True,
                creationflags=subprocess.DETACHED_PROCESS
            )
        except PermissionError:
            import ctypes
            ctypes.windll.shell32.ShellExecuteW(None, "open", app_path, None, None, 1)
    elif system_type == 'Darwin':
        subprocess.Popen(
            ["open", "-n", app_path],
            start_new_session=True
        )
    elif system_type == 'Linux':
        try:
            subprocess.Popen(
                ["nohup", app_path, "&"],
                start_new_session=True
            )
        except FileNotFoundError:
            subprocess.run(['gio', 'open', app_path])
########################################################整合封装###########################################
def get_path(app_name, system_type):
    """路径获取主函数"""
    # Windows优先使用注册表查询
    if system_type == "Windows":
        path = registry_search(app_name)
        if path:
            return path

    # 深度搜索
    path = deep_search(app_name, system_type)
    if path:
        return path

    # 图形化选择
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title=f"请选择 {app_name}",
        filetypes=[("可执行文件", "*.exe")] if system_type == "Windows" else [("所有文件", "*.*")]
    )
###########################################识别##################
def recognise(pictures, match=0.8):
    key = pyautogui.locateOnScreen(pictures[0], confidence=match)
    if key:
        for sequent in range(1, len(pictures)):
            try:
                location = pyautogui.locateOnScreen(pictures[sequent], confidence=match)
                if sequent==3:##设置延时启动
                    time.sleep(8)
                if location:
                    print(f"⭕{pictures[sequent]}")
                    heart_x, heart_y = pyautogui.center(location)
                    pyautogui.moveTo(heart_x, heart_y, duration=0.3)
                    pyautogui.click()
                    if sequent==4:###检测最终完成情况
                        return False
                else:
                    print(f"❌{pictures[sequent]}")
                    return False
            except Exception as e:
                print(f"‼️{e}‼️")
                return False



# 主程序
def main():

    system = platform.system()
    apps = ["cloudmusic", "QQMusic"]
    confidence = 0.8
    lib = ['heart_template.png', 'cloudmusic.png', 'search.png', 'add.png', 'in.png']
    pause = False
    threads = []

    for app in apps:
        path = get_path(app, system)
        if not path:
            print(f"❌ 未找到 {app}")
            continue

        thread = threading.Thread(target=run_it, args=(path, system))
        thread.start()
        threads.append(thread)
        print(f"✅ 成功启动：{path}")

    for thread in threads:
        thread.join()
    print("🎉 所有程序启动完成！")

    time.sleep(10)

    while True:
        if keyboard.is_pressed('q'):
            print('🚫')
            break
        elif keyboard.is_pressed('ctrl+p'):
            pause = True
        elif keyboard.is_pressed('ctrl+r'):
            pause = False
        if not pause:
            recognise(lib, confidence)
            time.sleep(5)



if __name__ == "__main__":
    main()

