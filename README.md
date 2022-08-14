# Picasso-Cup

## Features
- Rename .igc files automatically (aircraft, date, takeofftime, etc.)
- Draw flightpath as HTML file
- Associate .igc file with pilot via Vereinsflieger

## Requirements
- Python packages (aerofiles, geopy, numpy)
- [osmsm CLI](https://github.com/jperelli/osm-static-maps "osm-static-maps")

## How to use

1. Put .igc files in a folder in "raw_files" folder
2. ```
    python3 ./main.py ./raw_files/{your folder}/ 
    ```