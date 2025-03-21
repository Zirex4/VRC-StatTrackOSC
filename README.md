![ProductShowcase](https://github.com/Zirex4/VRC-StatTrackOSC/blob/main/Tutorial/Product.png )

# VRC-StatTrackOSC Installation Guide

This project allows you to track in-game stats via OSC when tilting your head back in VRChat. Follow the instructions below to add it to your avatar.

---

## Prerequisites

- [VRChat Creator Companion](https://vrchat.com/home/download)  
- [VRCFury](https://github.com/orels1/VRCFury) (installed and imported into your VRChat Creator Companion avatar project)

---

## Installation

1. **Import the Unity package**  
   Drag the `VRC-StatTrackOSC.unitypackage` into your Unity project.

2. **Add to your avatar**  
   - Locate the newly imported prefab(s) or objects.  
   - Attach or parent them to your avatar in the appropriate spot (e.g., near the head, or wherever it’s meant to track).
![Adding to the avatar](https://github.com/Zirex4/VRC-StatTrackOSC/blob/main/Tutorial/1.png  )

3. **Adjust colliders**  
   - Find the collider objects included with the stattrack system.  
   - Position them so that they make contact when your avatar’s head is tilted back in VRChat.
![Adjusting the colliders](https://github.com/Zirex4/VRC-StatTrackOSC/blob/main/Tutorial/2.png  )
   

4. **Resize and reposition**  
   - Adjust the size and position of the stattrack visual or logic to match your avatar’s proportions.
![Resizing Stattrack](https://github.com/Zirex4/VRC-StatTrackOSC/blob/main/Tutorial/3.png  )

5. **Upload your avatar**  
   - Use the standard VRChat Creator Companion / Unity upload process once everything is set up.
  
6. **Test it ingame**
   - Use the Collider view overlay under Options>Avatar to check for the desired angle to trigger the StatTrack
![Not Colliding](https://github.com/Zirex4/VRC-StatTrackOSC/blob/main/Tutorial/Test_1.png  )
![Colliding](https://github.com/Zirex4/VRC-StatTrackOSC/blob/main/Tutorial/Test_2.png  )

---

## Running in VRChat

1. **Enable OSC in VRChat**  
   - In VRChat, open your settings and ensure “OSC” is enabled.

2. **Launch the OSC server**  
   - Run `OSCserver.exe`.  
   - This will start listening for your avatar’s OSC signals.

3. **Enter VRChat**  
   - Load your newly uploaded avatar.  
   - Once in-game, tilt your head back to trigger the collider and send data via OSC.

---

## Information

Number of Materials: 2
- Counter material
- Mesh material
  
Number of Triangles: 988

---

## Troubleshooting

- If the OSC server does not receive data, double-check that:
  - Your avatar has OSC enabled.
  - The colliders are properly placed.
  - The server is running and not blocked by a firewall.

---

**Enjoy your new stattracking setup!**
**Drink responsibly!**
