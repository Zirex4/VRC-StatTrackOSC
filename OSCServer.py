import threading
from pythonosc import udp_client, dispatcher, osc_server
import os
import time
import json
 
# Globals
CurrentCounterDisplay = 0 # 0 = Session 1 = All Time 2 = Session Max Score

CurrentSessionH = -1.0
CurrentSessionL = -1.0

AllTimeH = -1.0
AllTimeL = -1.0
 
Loop = False
Loop_aux = True

Time_speed = 1 # Seconds to sleep while triggering the collider
 
# OSC client setup for sending messages to VRChat on port 9000
client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
 
def set_float_from_x(x):
    return -1.0 + 2.0 * (x / 255.0)
 
def get_n(CurrentSessionH, CurrentSessionL):
    x1 = round((CurrentSessionH + 1.0) / 2.0 * 255)
    x2 = round((CurrentSessionL + 1.0) / 2.0 * 255)
    return 256 * x1 + x2
 
def increment():
    global CurrentSessionH, CurrentSessionL, AllTimeH, AllTimeL
    x2 = round((CurrentSessionL + 1.0) / 2.0 * 255)
    x1 = round((CurrentSessionH + 1.0) / 2.0 * 255)
    if x2 < 255:
        x2 += 1
    else:
        x2 = 0
        if x1 < 255:
            x1 += 1
        else:
            x1 = 0
    CurrentSessionH = set_float_from_x(x1)
    CurrentSessionL = set_float_from_x(x2)

    if CurrentSessionH > AllTimeH:
        AllTimeH = CurrentSessionH

    if CurrentSessionL > AllTimeL:
        AllTimeL = CurrentSessionL
 
    # Save the current state to a file
    save_state()
 
def send_osc():
    global CurrentSessionH, CurrentSessionL, AllTimeH, AllTimeL, CurrentCounterDisplay
    messageHigh = "/avatar/parameters/High"
    messageLow = "/avatar/parameters/Low"

    if CurrentCounterDisplay == 0:
        client.send_message(messageHigh, float(CurrentSessionH))
        client.send_message(messageLow, float(CurrentSessionL))
    elif CurrentCounterDisplay == 1:
        client.send_message(messageHigh, float(AllTimeH))
        client.send_message(messageLow, float(AllTimeL))

    print(f"Sent OSC message with high: {CurrentSessionH}, low: {CurrentSessionL}, combined: {get_n(CurrentSessionH, CurrentSessionL)}")
 
def handle_signal(unused_addr, *args):
    print(f"Received OSC signal {unused_addr}: {args}")
 
def handle_statrack_add(unused_addr, args):
    global CurrentSessionH, CurrentSessionL, Loop
    print(f"Received add request with args: {args}")
    Loop = args
    if Loop == True:
        loop()

def handle_statrack_alltime(unused_addr, args):
    global CurrentSessionH, CurrentSessionL, CurrentCounterDisplay
    print(f"Received add request with args: {args}")
    if args == True:
        CurrentCounterDisplay = 1 if CurrentCounterDisplay == 0 else 0
        send_osc()
 
def start_osc_listener():
    disp = dispatcher.Dispatcher()
    disp.map("/avatar/parameters/High", handle_signal)
    disp.map("/avatar/parameters/Low", handle_signal)
    disp.map("/avatar/parameters/statrack_add", handle_statrack_add)
   #disp.map("/avatar/parameters/statrack_alltime", handle_statrack_alltime)
    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9001), disp)
    print("Starting OSC server on port 9001...")
    server.serve_forever()
 
def loop():
    global Loop, Time_speed
    while Loop:
            try:
                increment()
                send_osc()
                time.sleep(Time_speed)
            except (ValueError, TypeError, IndexError) as e:
                print(f"Error processing incoming data: {e}")
 
def load_state():
    """Load the state from the counter_state.txt file if it exists."""
    global CurrentSessionH, CurrentSessionL, AllTimeH, AllTimeL
    if os.path.exists("counter_state.txt"):
        try:
            with open("counter_state.txt", "r") as file:
                data = json.load(file)
                #CurrentSessionH = data.get("CurrentSessionH", -1.0)
                #CurrentSessionL = data.get("CurrentSessionL", -1.0)

                AllTimeH = data.get("AllTimeH")
                AllTimeL = data.get("AllTimeL")

                print(f"Loaded state: CurrentSessionH = {CurrentSessionH}, CurrentSessionL = {CurrentSessionL} AllTimeH = {AllTimeH}, AllTimeL = {AllTimeL}")
        except Exception as e:
            print(f"Error loading state: {e}")
 
def save_state():
    global CurrentSessionH, CurrentSessionL, AllTimeH, AllTimeL
    """Save the current state (CurrentSessionH, CurrentSessionL) to the counter_state.txt file in JSON format."""
    try:
        with open("counter_state.txt", "w") as file:
            json.dump({"CurrentSessionH": CurrentSessionH, "CurrentSessionL": CurrentSessionL, "AllTimeH": AllTimeH, "AllTimeL": AllTimeL}, file)
        print(f"State saved: CurrentSessionH = {CurrentSessionH}, CurrentSessionL = {CurrentSessionL} AllTimeH = {AllTimeH}, AllTimeL = {AllTimeL}")
    except Exception as e:
        print(f"Error saving state: {e}")
 
if __name__ == "__main__":
    load_state()  # Load the last saved state before starting
    osc_thread = threading.Thread(target=start_osc_listener)
    osc_thread.start()