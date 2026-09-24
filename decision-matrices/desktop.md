# Desktop GIS Decision Matrix

## Candidates
Qt/PySide/PyQt, QGIS plugin architecture, Electron, Tauri, .NET desktop, other native/cross-platform frameworks.

## Rules
- Deep native GIS processing/offline workflows: evaluate Qt/PySide or QGIS plugin architecture.
- Existing QGIS environment and extension requirement: prefer QGIS plugin architecture when the requirement fits.
- Web technology reuse with desktop packaging: evaluate Tauri/Electron, with native GIS processing isolated behind services/workers.
- Windows/.NET enterprise requirement: evaluate .NET desktop.

## Checks
Native GIS library access, map canvas, file handling, offline behavior, worker architecture, packaging, updates, memory, OS support, licensing.
