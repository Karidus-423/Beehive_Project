# Datalogger Version 2
___

### File Structure
- **enclosure**, here you'll find all of the 3D models for the datalogger enclosure.
- **pcb**, schemas, pcb schemas and drill files will be found here.
- **resources**, libraries that are used in making the schemas and pcbs.
- **script**, where the arduino scripts for the datalogger are saved.


## Schematic and PCB Design

At the moment there are 5 main components that are required for the circuit to work.

- Programming Board
- Sensors
- Battery
- Real Time Clock (RTC)
- SD Card Moudule

The main idea is to have the <u>Programming Board</u>, to be connected to a large
battery. The battery must be able to be charged quickly or be swapped quickly. The
sensors need to be configured in a way that the user is able to unplug them relatively
easily try to look for **Audio Jacks** with 3 pins. I have a 3D model of the overall
idea of what it should look like. The parts are already placed on the schematic.

Then the RTC and the SDCard are going to be rather simple as there are some modules
that are able to just connect directly to the feather boards that where ordered.
**Feather Footprint** is a standarized layout of a microcontroller that makes it
easier to get parts for it no matter the brand. The Sparkfun microcontroller and
the adalogger can just be mounted on each other for them to work correctly.

The **Sparkfun Microcontroller** is able to charge whatever battery is connected
to it at a rate of 500mAh. So that takes care of the chargin part. What I remains
are just the design of the PCB to be printed and piecing everything together. The
3D Printers at the university will also work. I will leave two models already printed
at the lab for them to be used as examples or as the enclosure itself.
