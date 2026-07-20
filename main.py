from colorama import Fore, Back, Style, init
import os, socket, time, platform, psutil, subprocess, sys

mem = psutil.virtual_memory()

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
            output = subprocess.check_output(['winget', 'list'], encoding='utf-8', errors='ignore')
            return len([line for line in output.splitlines() if ' ' in line and '---' not in line]) - 1
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
            elif 'VSCODE_TERM' in os.environ:
                shell_name = 'vscode'
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
            out = subprocess.check_output('lspci | grep -E "VGA|3D"', shell=True, text=True)
            return out.split(':')[1].strip() if out else 'unknown'
    except:
        pass
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


"""

if len(sys.argv) < 2 or not sys.argv[1]:
    if platform.system() == "Windows":
        target = windows
    elif platform.system() == "Linux":
        target = linux
    elif platform.system() == "Darwin":
        target = apple
    else:
        target = hashtag
else:
    if sys.argv[1] == "Windows":
        target = windows
    elif sys.argv[1] == "Linux":
        target = linux
    elif sys.argv[1] == "Darwin":
        target = apple
    elif sys.argv[1] == "Hashtag":
        target = hashtag
    else:
        if platform.system() == "Windows":
            target = windows
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

print(target.split('\n')[0] + "            " + Fore.RED + username + Fore.GREEN + "@" + Fore.RED + hostname)
print(target.split('\n')[1] +  "            " + Fore.WHITE + "-"*len(username + "@" + hostname))
print(target.split('\n')[2] +  "            " + Fore.RED + f"OS{Fore.GREEN}: " + platform.platform())
print(target.split('\n')[3] +  "            " + Fore.RED + f"Kernel{Fore.GREEN}: " + platform.uname().version)
print(target.split('\n')[4] +  "            " + Fore.RED + f"Uptime{Fore.GREEN}: " + format_uptime(get_uptime()))
print(target.split('\n')[5] +  "            " + Fore.RED + f"{packages_or_programs()}{Fore.GREEN}: " + packages)
print(target.split('\n')[6] +  "            " + Fore.RED + f"Shell{Fore.GREEN}: " + get_shell_version())
print(target.split('\n')[7] +  "            " + Fore.RED + f"Resolution{Fore.GREEN}: " + f"{get_screen_resolution()[0]}x{get_screen_resolution()[1]}")
print(target.split('\n')[8] +  "            " + Fore.RED + f"CPU{Fore.GREEN}: " + get_cpu())
print(target.split('\n')[9] +  "            " + Fore.RED + f"GPU{Fore.GREEN}: " + get_gpu())
print(target.split('\n')[10] +  "            " + Fore.RED + f"Memory{Fore.GREEN}: " + f"{mem.available // (1024**2)}MB / {mem.total // (1024**2)}MB")
print(target.split('\n')[11])
print(target.split('\n')[12] + "           " + Back.BLACK + "   " + Back.RED + "   " + Back.GREEN + "   " + Back.YELLOW + "   " + Back.BLUE + "   " + Back.MAGENTA + "   " + Back.CYAN + "   " + Back.WHITE + "   " + Style.RESET_ALL)
print(target.split('\n')[13] + r"           " + Back.LIGHTBLACK_EX + "   " + Back.LIGHTRED_EX + "   " + Back.LIGHTGREEN_EX + "   " + Back.LIGHTYELLOW_EX + "   " + Back.LIGHTBLUE_EX + "   " + Back.LIGHTMAGENTA_EX + "   " + Back.LIGHTCYAN_EX + "   " + Back.LIGHTWHITE_EX + "   " + Style.RESET_ALL)
print(target.split('\n')[14])
print(target.split('\n')[15])
print(target.split('\n')[16])
print(target.split('\n')[17])
