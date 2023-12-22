# WiFuck (❌)
A more robust version of [wifidos](https://github.com/killgriff22/wifidos)
## This is in active development!
Pleae be patient with releases.  
this readme outlines the features and usages that I plan to implement as I work on this project.  
a ❌ means a feature does not exist :(  
a ✅ means a feature is fully working!  
a ⚠️ means that the feature is semi-functional, but broken.  
a 🚧 means that a feature is development!
# Features
* [*Single MAC Deauth*](#Single-MAC) (❌)  
* [*Multi-MAC Deauth*](#Multi-MAC) (❌)  
* [*MAC Scanning*](#Scanning) (❌)  
* [*Target Specific Deauth*](#Targeting) (❌)  
* [*Command Line Arguments*](#Args) (❌)  
## Multi-MAC Deauth (❌)
## Single MAC Deauth (❌)
## Scanning (❌)
## Targeting (❌)
## Args (❌)
***ALL COMMAND-LINE ARGUMENTS ARE FORCED LOWERCASE (i.e. -s is the same as -S)***  
* -i or --interface  
* -s or --scan  
* -b or --bssid  
* -c or --channel  
* -t or --target  
* -f or --file  
There are three parts to this argument.  
  1. This argument can be passed multiple times. (*i.e. -f b bssids.txt*)
  2. The first section after the flag stated the information stored inside the file  
    -> *b or bssid*: there are bssids stored in the file.  
    -> *t or target*: there are target MACs stored insise the file.  
    -> *None or both*: assumes both are present. this will only apply in the event a .csv file is passed.  
  3. The second section is for the name of the file. The program will decide how to decode it based on the file extension. you will be asked for the format of the file. the formatting rules are as follows: *b or bssid,c or channel,t or target,n or name*  
❌✅