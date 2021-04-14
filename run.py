import sys

class Switch(object):
    def auto(self):
        print("auto")
    def mal(self):
        print("mal")
    def default(self):
        print("default")   

if __name__ == "__main__":
    command = "auto"
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
    switch = Switch()

    # getattr(switch, command)()

    switcher = { 
        "auto": switch.auto, 
        "mal": switch.mal, 
    } 
    switcher.get(command, switch.default)()