# AI-Driven 3D Weather Visualization (ParaView)

A high-resolution 3D scientific visualization project that models and visualizes weather data using volumetric rendering and vector fields.



## Features

- 🧊 3D volumetric data modeling (temperature field)
- 🌀 Vector field simulation (wind flow)
- 🎨 Volume rendering using ParaView
- 🌈 Color mapping + opacity control
- 🎥 Automated camera rotation (animation generation)
- ⚙️ Fully automated pipeline using pvpython


## Tech Stack

- Python
- ParaView (pvpython)
- VTK
- NumPy


## Demo

![demo](demo.gif)

> Rotating 3D volumetric visualization with color-mapped scalar field.


## Run
```bash
pvpython scripts/generate_3d_weather_vti.py
pvpython scripts/render_animation.py
python GIF.py


