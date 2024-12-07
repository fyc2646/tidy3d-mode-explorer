# Tidy3D Mode Explorer

A simplistic graphical user interface for exploring optical waveguide modes using Tidy3D's waveguide plugin and mode solver. It provides two mode solve options: local mode solve and server mode solve. Local mode solve runs on your local machine, which doesn't require a tidy3d account and is totally free. Local mode solve does not implement the subpixel averaging scheme so the accuracy of the mode data is not guaranteed. Server mode solve sends the mode solve request to a Flexcompute server, which requires a tidy3d account and a small amount of FlexCredits. When more accurate mode data is needed, server mode solve is recommended.

![Demo Interface](demo.png)

## Description

This tool provides an interactive interface for quicklyanalyzing and visualizing optical waveguide modes using the Tidy3D electromagnetic simulation framework. The GUI supports:

### Waveguide Types
- Strip waveguide
- Rib waveguide
- Slot waveguide

### Key Features
- Interactive parameter adjustment for each waveguide type
- Real-time visualization of waveguide geometry
- Support for both straight and bent waveguides
- Configurable material properties (core, cladding, and box layer indices). Currently only limit to lossless materials.
- Adjustable simulation parameters:
  - Wavelength
  - Grid resolution (minimum steps per wavelength)
  - Number of modes to solve
  - Target effective index (optional)
  - Bend radius (optional)
  - PML (Perfectly Matched Layer) boundaries (optional)

### Parameters
- **Geometric Parameters**:
  - Core width and thickness
  - Sidewall angle
  - Slab thickness (for rib waveguides)
  - Slot gap (for slot waveguides)
  - Cladding and box layer thicknesses

- **Material Parameters**:
  - Core refractive index
  - Cladding refractive index
  - Box layer refractive index

- **Simulation Settings**:
  - Grid resolution
  - Number of modes
  - Target effective index
  - Bend radius
  - PML boundaries

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/tidy3d-mode-explorer.git
cd tidy3d-mode-explorer
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the GUI application:
```bash
python waveguide_gui.py
```

## License

This project is licensed under the MIT License.
