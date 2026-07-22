from colorama import Fore, Back, Style, init
import os, socket, time, platform, psutil, subprocess, sys

version = "1.0.4"

init()

def get_uptime():
    try:
        return time.time() - psutil.boot_time()
    except:
        pass
        return 0

def format_uptime(seconds):
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    parts = []
    if days: parts.append(f"{days} days")
    if hours: parts.append(f"{hours} hours")
    if minutes: parts.append(f"{minutes} mins")
    return " ".join(parts)

def packages_or_programs():
    if platform.system() == "Windows" or platform.system() == "Darwin":
        return "Programs"
    elif platform.system() == "Linux":
        return "Packages"

def get_package_count():
    system = platform.system()
    try:
        if system == 'Windows':
            import winreg
            programs = []
            for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                for key_path in [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                                r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall']:
                    try:
                        key = winreg.OpenKey(hive, key_path)
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            try:
                                subkey = winreg.OpenKey(key, winreg.EnumKey(key, i))
                                name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                                programs.append(name)
                            except:
                                pass
                        return len(programs)
                    except:
                        pass
        elif system == 'Linux':
            output = subprocess.check_output(['dpkg', '-l'], text=True)
            return len([line for line in output.splitlines() if line.startswith('ii')])
    except:
        return 0

def get_shell_version():
    system = platform.system()
    try:
        if system == 'Windows':
            if 'WT_SESSION' in os.environ:
                shell_name = 'wt'
                try:
                    ver = subprocess.check_output(['wt', '--version'], text=True).split()[-1]
                except:
                    ver = platform.version()
            elif 'TERM_PROGRAM' in os.environ and os.environ['TERM_PROGRAM'] == 'vscode':
                shell_name = 'vscode'
                ver = os.environ.get('TERM_PROGRAM_VERSION', 'unknown')

            else:
                shell_name = 'cmd'
                ver = platform.version()
            return f"{shell_name} {ver}"
        
        elif system == 'Linux':
            shell = os.environ.get('SHELL', '').split('/')[-1]
            if shell == 'bash':
                output = subprocess.check_output(['bash', '--version'], text=True)
                version = output.splitlines()[0].split()[3]
            elif shell == 'zsh':
                output = subprocess.check_output(['zsh', '--version'], text=True)
                version = output.split()[1]
            else:
                version = 'unknown'
            return f"{shell} {version}"
        
        elif system == 'Darwin':
            shell = os.environ.get('SHELL', '').split('/')[-1]
            if shell == 'bash':
                output = subprocess.check_output(['bash', '--version'], text=True)
                version = output.splitlines()[0].split()[3]
            elif shell == 'zsh':
                output = subprocess.check_output(['zsh', '--version'], text=True)
                version = output.split()[1]
            else:
                version = 'unknown'
            return f"{shell} {version}"
        
        else:
            return 'unknown'
    except:
        return 'unknown'

def get_screen_resolution():
    try:
        if platform.system() == 'Windows':
            import ctypes
            user32 = ctypes.windll.user32
            return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        elif platform.system() == 'Linux':
            output = subprocess.check_output(['xrandr', '--current'], text=True)
            for line in output.splitlines():
                if ' connected' in line and '+' in line:
                    import re
                    match = re.search(r'(\d+)x(\d+)\+', line)
                    if match:
                        return int(match.group(1)), int(match.group(2))
            try:
                with open('/sys/class/graphics/fb0/virtual_size', 'r') as f:
                    w, h = f.read().strip().split(',')
                    return int(w), int(h)
            except:
                pass
        elif platform.system() == 'Darwin':
            output = subprocess.check_output(
                ['system_profiler', 'SPDisplaysDataType'],
                text=True
            )
            import re
            match = re.search(r'Resolution:\s*(\d+) x (\d+)', output)
            if match:
                return int(match.group(1)), int(match.group(2))
    except:
        pass
    return 0, 0

def get_gpu():
    try:
        if platform.system() == 'Windows':
            out = subprocess.check_output(
                'wmic path win32_VideoController get name',
                shell=True, encoding='cp866', errors='ignore'
            )
            lines = [l.strip() for l in out.split('\n') if l.strip()]
            return lines[1] if len(lines) > 1 else 'unknown'
        elif platform.system() == 'Linux':
            try:
                gpu = subprocess.run(['lspci'], capture_output=True, text=True).stdout
                for line in gpu.split('\n'):
                    if 'VGA' in line or '3D' in line:
                        return line.strip()
                return 'not found'
            except:
                return 'not found'
    except:
        return 'unknown'

def get_cpu():
    try:
        if platform.system() == 'Windows':
            output = subprocess.check_output(
                'wmic cpu get name',
                shell=True, encoding='cp866', errors='ignore'
            )
            lines = [line.strip() for line in output.split('\n') if line.strip()]
            return lines[1] if len(lines) > 1 else 'unknown'
        elif platform.system() == 'Linux':
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line:
                        return line.split(':')[1].strip()
        elif platform.system() == 'Darwin':
            output = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string'], text=True)
            return output.strip()
    except:
        return 'unknown'
    return 'unknown'

windows = f"""{Fore.CYAN}                           ....iilll
{Fore.CYAN}                 ....iilllllllllllll
{Fore.CYAN}     ....iillll  lllllllllllllllllll
{Fore.CYAN} iillllllllllll  lllllllllllllllllll
{Fore.CYAN} llllllllllllll  lllllllllllllllllll
{Fore.CYAN} llllllllllllll  lllllllllllllllllll
{Fore.CYAN} llllllllllllll  lllllllllllllllllll
{Fore.CYAN} llllllllllllll  lllllllllllllllllll
{Fore.CYAN} llllllllllllll  lllllllllllllllllll
                                    
{Fore.CYAN} llllllllllllll  lllllllllllllllllll
{Fore.CYAN} llllllllllllll  lllllllllllllllllll
{Fore.CYAN} llllllllllllll  lllllllllllllllllll
{Fore.CYAN} llllllllllllll  lllllllllllllllllll
{Fore.CYAN} llllllllllllll  lllllllllllllllllll
{Fore.CYAN} `^^^^^^lllllll  lllllllllllllllllll
{Fore.CYAN}       ````^^^^  ^^lllllllllllllllll
{Fore.CYAN}                      ````^^^^^^llll"""

windows_eleven = f"""{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}                                            
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}   lllllllllllllllllll   lllllllllllllllllll
{Fore.CYAN}
{Fore.CYAN}                                            """

linux = rf"""{Style.RESET_ALL}         _nnnn_        
{Style.RESET_ALL}        dGGGGMMb       
{Style.RESET_ALL}       @p~qp~~qMb      
{Style.RESET_ALL}       M|@||@) M|      
{Style.RESET_ALL}       @,----.JM|      
{Style.RESET_ALL}      JS^\__/  qKL     
{Style.RESET_ALL}     dZP        qKRb   
{Style.RESET_ALL}    dZP          qKKb  
{Style.RESET_ALL}   fZP            SMMb 
{Style.RESET_ALL}   HZM            MMMM 
{Style.RESET_ALL}   FqM            MMMM 
{Style.RESET_ALL} __| ".        |\dS"qML
{Style.RESET_ALL} |    `.       | `' \Zq
{Style.RESET_ALL}_)      \.___.,|     .'
{Style.RESET_ALL}\____   )MMMMMP|   .'  
{Style.RESET_ALL}     `-'       `--'    

"""

apple = rf"""                       
{Style.RESET_ALL}              ll       
{Style.RESET_ALL}           lllll       
{Style.RESET_ALL}          llllll       
{Style.RESET_ALL}   lllllllllllllllll   
{Style.RESET_ALL} lllllllllllllllllllll 
{Style.RESET_ALL}lllllllllllllllllllll  
{Style.RESET_ALL}lllllllllllllllllll    
{Style.RESET_ALL}lllllllllllllllllll    
{Style.RESET_ALL}lllllllllllllllllll    
{Style.RESET_ALL}llllllllllllllllllllll 
{Style.RESET_ALL} lllllllllllllllllllll 
{Style.RESET_ALL}  lllllllllllllllllll  
{Style.RESET_ALL}   llllllllllllllll    



"""

hashtag = rf"""                          
{Style.RESET_ALL}     ######    ######     
{Style.RESET_ALL}     #::::#    #::::#     
{Style.RESET_ALL}     #::::#    #::::#     
{Style.RESET_ALL}######::::######::::######
{Style.RESET_ALL}#::::::::::::::::::::::::#
{Style.RESET_ALL}######::::######::::######
{Style.RESET_ALL}     #::::#    #::::#     
{Style.RESET_ALL}     #::::#    #::::#     
{Style.RESET_ALL}######::::######::::######
{Style.RESET_ALL}#::::::::::::::::::::::::#
{Style.RESET_ALL}######::::######::::######
{Style.RESET_ALL}     #::::#    #::::#     
{Style.RESET_ALL}     #::::#    #::::#     
{Style.RESET_ALL}     ######    ######     
{Style.RESET_ALL}                          
{Style.RESET_ALL}                          
"""

if len(sys.argv) < 2 or not sys.argv[1]:
    if platform.system() == "Windows" and platform.version().startswith("10.0.2"):
        target = windows_eleven
    elif platform.system() == "Windows" and platform.version().startswith("10.0.26"):
        target = windows_eleven
    elif platform.system() == "Windows" and platform.version().startswith("10.0.19"):
        target = windows
    elif platform.system() == "Linux":
        target = linux
    elif platform.system() == "Darwin":
        target = apple
    else:
        target = hashtag
else:
    if sys.argv[1].lower() == "windows":
        target = windows
    if sys.argv[1].lower() == "windows10":
        target = windows
    elif sys.argv[1].lower() == "windows11":
        target = windows_eleven
    elif sys.argv[1].lower() == "linux":
        target = linux
    elif sys.argv[1].lower() == "darwin":
        target = apple
    elif sys.argv[1].lower() == "hashtag":
        target = hashtag
    else:
        if platform.system() == "Windows" and platform.version().startswith("10.0.2"):
            target = windows_eleven
        elif platform.system() == "Windows" and platform.version().startswith("10.0.1"):
            target = windows
        elif platform.system() == "Windows" and platform.version().startswith("10.0.26"):
            target = windows_eleven
        elif platform.system() == "Linux":
            target = linux
        elif platform.system().startswith("Android"):
            target = linux
        elif platform.system() == "Darwin":
            target = apple
        else:
            target = hashtag

packages = str(get_package_count())

username = os.getenv('USER') or os.getenv('USERNAME') or 'unknown'
hostname = socket.gethostname() or 'localhost'

mem = psutil.virtual_memory() or "Unknown"
operating_system = platform.platform() or "Unknown"
kernel = platform.uname().version or "Unknown"
uptime = format_uptime(get_uptime()) or "Unknown"
pkg_or_prg = packages_or_programs() or "Unknown"
shell = get_shell_version() or "Unknown"
screen = get_screen_resolution() or "Unknown"
cpu = get_cpu() or "Unknown"
cpu_count = psutil.cpu_count(logical=False) or "Unknown"
gpu = get_gpu() or "Unknown"

print(target.split('\n')[0] + "            " + Fore.RED + username + Fore.GREEN + "@" + Fore.RED + hostname)
print(target.split('\n')[1] +  "            " + Fore.WHITE + "-"*len(username + "@" + hostname))
print(target.split('\n')[2] +  "            " + Fore.RED + f"OS{Fore.GREEN}: " + operating_system)
print(target.split('\n')[3] +  "            " + Fore.RED + f"Kernel{Fore.GREEN}: " + kernel)
print(target.split('\n')[4] +  "            " + Fore.RED + f"Uptime{Fore.GREEN}: " + uptime)
print(target.split('\n')[5] +  "            " + Fore.RED + f"{pkg_or_prg}{Fore.GREEN}: " + packages)
print(target.split('\n')[6] +  "            " + Fore.RED + f"Shell{Fore.GREEN}: " + shell)
print(target.split('\n')[7] +  "            " + Fore.RED + f"Resolution{Fore.GREEN}: " + f"{screen[0]}x{screen[1]}")
print(target.split('\n')[8] +  "            " + Fore.RED + f"CPU{Fore.GREEN}: " + cpu + f"{Fore.RED}({Fore.GREEN}{cpu_count}{Fore.RED})")
print(target.split('\n')[9] +  "            " + Fore.RED + f"GPU{Fore.GREEN}: " + gpu)
print(target.split('\n')[10] +  "            " + Fore.RED + f"Memory{Fore.GREEN}: " + f"{mem.available // (1024**2)}MB / {mem.total // (1024**2)}MB")
print(target.split('\n')[11] + "            " + Fore.RED + f"TagFetch Version{Fore.GREEN}: " + version)
print(target.split('\n')[13])
print(target.split('\n')[14] + "           " + Back.BLACK + "   " + Back.RED + "   " + Back.GREEN + "   " + Back.YELLOW + "   " + Back.BLUE + "   " + Back.MAGENTA + "   " + Back.CYAN + "   " + Back.WHITE + "   " + Style.RESET_ALL)
print(target.split('\n')[15] + r"           " + Back.LIGHTBLACK_EX + "   " + Back.LIGHTRED_EX + "   " + Back.LIGHTGREEN_EX + "   " + Back.LIGHTYELLOW_EX + "   " + Back.LIGHTBLUE_EX + "   " + Back.LIGHTMAGENTA_EX + "   " + Back.LIGHTCYAN_EX + "   " + Back.LIGHTWHITE_EX + "   " + Style.RESET_ALL)
print(target.split('\n')[16])
print(target.split('\n')[17])
