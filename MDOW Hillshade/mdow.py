from __future__ import absolute_import, division, print_function
from functools import reduce
from concurrent import futures
import numpy as np
import scipy.signal as spsg
import rasterio
import click
import os

def horn_gradient(dem):
    x_kernel = np.array([
        [-1/8, 0, 1/8], 
        [-1/4, 0, 1/4], 
        [-1/8, 0, 1/8]])
    y_kernel = np.array([
        [-1/8, -1/4, -1/8],
        [0, 0, 0],
        [1/8, 1/4, 1/8]])
    dx = spsg.convolve2d(dem, x_kernel)
    dy = spsg.convolve2d(dem, y_kernel)
    return dx, dy

def slope(dem):
    dx, dy = horn_gradient(dem)
    dem_slope = np.arctan(np.sqrt(np.square(dx) + np.square(dy)))
    return dem_slope

def aspect(dem):
    dx, dy = horn_gradient(dem)
    direction = np.arctan2(dy, -dx)
    dem_aspect = np.where(direction > np.pi/2, np.pi*5/2 - direction, np.pi/2 - direction)
    return dem_aspect

def hillshade(dem, azimuth, altitude):
    azimuth_rad = np.deg2rad(azimuth)
    altitude_rad = np.deg2rad(altitude)
    dem_slope = slope(dem)
    dem_aspect = aspect(dem)
    dem_hillshade = 255 * (np.cos(np.pi/2 - altitude_rad) * np.cos(dem_slope) + np.sin(np.pi/2 - altitude_rad) * np.sin(dem_slope) * np.cos(azimuth_rad - dem_aspect))
    return dem_hillshade

def mdow_hillshade(dem, azimuth, altitude):
    azimuth_rad = np.deg2rad(azimuth)
    altitude_rad = np.deg2rad(altitude)
    init_slope = slope(dem)
    init_aspect = aspect(dem)
    init_hillshade = hillshade(dem, azimuth, altitude)
    secondary_azimuths = [np.deg2rad(180+90*(n+1)) for n in range(4)]
    workers = futures.ThreadPoolExecutor(max_workers=os.cpu_count())
    hs_task = lambda az: hillshade(dem, az, altitude)
    w_var_task = lambda az: (np.cos(init_aspect - az) + 1)
    weight_task = lambda w: (w / np.sqrt(2 * w_total))
    secondary_hillshades = list(workers.map(hs_task, secondary_azimuths))
    secondary_w_vars = list(workers.map(w_var_task, secondary_azimuths))
    w_total = reduce(lambda x, y: x + y, secondary_w_vars)
    secondary_weights = list(workers.map(weight_task, secondary_w_vars))
    md_hillshade = reduce(lambda x, y: x + y, [m * n for m, n in zip(secondary_hillshades, secondary_weights)])
    merge_weight = np.square(np.sin(np.sin(altitude_rad) * np.cos(init_slope) + np.sin(init_slope) * np.cos(altitude_rad) * np.cos(init_aspect - azimuth_rad)))
    hs_final = merge_weight * md_hillshade + (1 - merge_weight) * init_hillshade
    mdow = np.min(init_hillshade) + (hs_final - np.min(hs_final)) / (np.max(hs_final) - np.min(hs_final)) * (np.max(init_hillshade) - np.min(init_hillshade))
    return mdow

def read_dem(dem_file):
    src = rasterio.open(dem_file)
    band = src.read(1)
    meta = {
        'height': band.shape[0],
        'width': band.shape[1],
        'count': src.count,
        'dtype': band.dtype,
        'crs': src.crs,
        'transform': src.transform,
        'nodata': src.nodata
    }
    src.close()
    return band, meta

def write_hillshade(file_path, hs, metadata):
    with rasterio.open(file_path, 'w', driver='GTiff', height=metadata['height'], width=metadata['width'], count=metadata['count'], dtype=metadata['dtype'], crs=metadata['crs'], transform=metadata['transform'], nodata=metadata['nodata']) as dst:
        dst.write(hs.astype(metadata['dtype']), 1)

def run(in_path, out_path, azimuth, altitude):
    arr, meta = read_dem(in_path)
    md = mdow_hillshade(arr, azimuth, altitude)
    write_hillshade(out_path, md, meta)

def validate_azimuth(ctx, param, value):
    if 0 <= value <= 360:
        return value
    else:
        raise click.BadParameter('Azimuth should be between 0 and 360.')

def validate_altitude(ctx, param, value):
    if 0 <= value <= 90:
        return value
    else:
        raise click.BadParameter('Altitude should be between 0 and 90.')

@click.command()
@click.option('-i', '--in', 'in_path', help='Input DEM path.', required=True, type=str)
@click.option('-o', '--out', 'out_path', help='Output hillshade path.', required=True, type=str)
@click.option('--azimuth', 'azimuth', help='Hillshade azimuth in degree.', required=True, type=float, callback=validate_azimuth)
@click.option('--altitude', 'altitude', help='Hillshade altitude in degree.', required=True, type=float, callback=validate_altitude)
def cmd(in_path, out_path, azimuth, altitude):
    """MDOW Hillshade Generator."""
    run(in_path, out_path, azimuth, altitude)

if __name__ == '__main__':
    cmd()
