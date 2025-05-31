# Removing extraneous characters from font files to save memory

## Font Forge

To save memory, use FontForge to remove all but the basic ASCII characters per  https://learn.adafruit.com/custom-fonts
-for-pyportal-circuitpython-display/conversion.

## Technical Issues
- `.pcf` is a fast, compact binary file format which is our target
- Due to compatability issues, we use `.bdf` as an intermediate file format
  - While FontForge can read .pcf files, that will lose metadata which `bdftopcf` requires
    and FontForge maintainers do not emit (optional per the spec)
  - FontForge cannot write .pcf binary files.   Use `bdftopcf` to convert


## Process
- Convert the `.pcf` file to `.bdf` using `pcf2bdf`:
  - ```pcf2bdf PTSans-NarrowBold-40.pcf -o PTSans-NarrowBold-40.bdf```
- Open `PTSans-NarrowBold-40.bdf` in FontForge.
- Follow the step for "Optimize File Size" at https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/conversion.  Note: `Element→Regenerate Bitmap` does not seem to be enabled or needed.
- Convert the `.bdf` file back to `.pcf` using `bdftopcf`:
  - ```bdftopcf PTSans-NarrowBold-40.bdf -o PTSans-NarrowBold-40.pcf```
