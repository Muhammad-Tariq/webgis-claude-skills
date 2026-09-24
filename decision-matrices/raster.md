# Raster Decision Matrix

## Candidates
COG/GDAL, object storage, STAC, PostGIS raster, raster services, cloud processing, or local processing.

## Rules
- Large read-mostly raster: evaluate Cloud Optimized GeoTIFF + object storage.
- Large catalogs/time series: evaluate STAC metadata/catalog patterns.
- Local scientific processing: evaluate GDAL/rasterio and local/cloud hybrid workflows.
- Use PostGIS raster only when database integration materially benefits the workload.
- Use processing platforms such as GEE when their datasets/computation model materially reduce complexity and requirements permit.

## Checks
Raster size, access windows, update frequency, tiling, overviews, nodata, CRS, resolution, provenance, egress/compute cost.
