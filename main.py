from classes import *
if not "-i" in args:
    wifi_interfaces=get_interfaces()
    for i,interface in enumerate(wifi_interfaces):
        print(f"[{i}] - {interface[0]} ({interface[1]})")
    ans = input("Please select the number of the interface you would like to use\n>")
interface=Interface((wifi_interfaces[int(ans if ans.isdigit() else 0 if ans == "" else ir("Answer must be an integer!"))][0])if "-i" not in args else args[args.index("-i")+1])
if not any(["-s","--scan"]) in args:
    ans = input("would you like to scan for BSSIDs? (Y/n)\n>")
if ans.lower() in ["y","yes",""] or any(["-s","--scan"]) in args:
    list_of_BSSIDs=interface.scan_for_MACs()
else:
    list_of_BSSIDs=[]