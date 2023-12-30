from classes import *
if not "-i" in args:
    wifi_interfaces=get_interfaces()
    for i,interface in enumerate(wifi_interfaces):
        print(f"[{i}] - {interface[0]} ({interface[1]})")
    ans = input("Please select the number of the interface you would like to use\n>")
interface=Interface((wifi_interfaces[int(ans if ans.isdigit() else 0 if ans == "" else ir("Answer must be an integer!"))][0])if "-i" not in args else args[args.index("-i")+1])
if not any(arg in args for arg in ["-s","--scan","-f","---file","-b","--bssid"]):
    ans = input("would you like to scan for BSSIDs? (Y/n)\n>")
if ans.lower() in ["y","yes",""] or (any(arg in args for arg in ["-s","--scan"]) and not any(arg in args for arg in ["-f","--file","-b","--bssid"])):
    Networks=interface.scan_for_MACs()
else:
    ans="None"
    if not any(arg in args for arg in ["-f","--file"]):
        ans = input("would you like to load the networks from a file? (y/N)")
    if ans.lower() in ['n','no',''] or any(arg in args for arg in ["-f","--file"]):
        warn("🚧 Feature not yet implemented! 🚧")
        interface.stop()
        exit()