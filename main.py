from classes import *
ir=inlineraise
args=sys.argv
if not "-i" in args:
    wifi_interfaces=get_interfaces()
    for i,interface in enumerate(wifi_interfaces):
        print(f"[{i}] - {interface[0]} ({interface[1]})")
    ans = input("Please select the number of the interface you would like to use\n>")
interface=Interface((wifi_interfaces[int(ans if ans.isdigit() else 0 if ans == "" else ir("Answer must be an integer!"))][0])if "-i" not in args else args[args.index("-i")+1])
interface.start()
interface.stop()