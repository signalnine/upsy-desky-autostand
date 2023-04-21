# upsy-desky-autostand
a quick and dirty python script to control a standing desk

Works with the [Upsy Desky](https://github.com/tjhorner/upsy-desky)

### Why 
I wanted a script that raises and lowers my desk automatically to achieve my goal to stand at my desk a minimum amount of time with sitting breaks in between. But I find it really disruptive when this happens when I'm in a meeting so I added some functionality to only raise/lower my desk when I'm _not_ in a meeting according to my Google Calendar (supports any publicly-readable ICS format calendar).

### How
* Modify the configuration parameters in `standing.py`
* Run it in a cronjob that runs once a day at the start of your workday. Or run it manually, I'm not the boss of you.
