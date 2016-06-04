from controller import application #admin, terminal, nmap, db
import os
projectName = "Nmap"
softwarePurpose = "To scan a network for device types and names in certain segments"
message_of_the_day = "Here we go"

# Application directory
direct_path = os.path.dirname(os.path.abspath(__file__))

# Let's begin the journey of a thousand lines of code
THub = application.HubStation()
THub.engine(message_of_the_day, direct_path)
