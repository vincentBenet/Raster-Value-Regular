from scipy.interpolate import RegularGridInterpolator
import rasterio
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt


def load_tif(file_name):
    
    with rasterio.open(file_name) as src:
         band1 = src.read(1)
         height = band1.shape[0]
         width = band1.shape[1]
         cols, rows = np.meshgrid(np.arange(width), np.arange(height))
         xs, ys = rasterio.transform.xy(src.transform, rows, cols)
         lons= np.array(xs)
         lats = np.array(ys)

    data = np.flip(band1, 0)
    data_temp = data.copy()
    data_temp[data_temp==0] = np.nan
    data_temp[~np.isnan(data_temp)] = 1
    
    mask = data_temp

    x_arr = lons[0, :]
    y_arr=lats[:, 0][::-1]
    
    points = np.c_[lons.ravel(), lats.ravel()]
    alt_1d = data.ravel()
    
    
    return x_arr, y_arr, data, mask, points, alt_1d

# %%

path_map_ground = r"map_ground__ef90f84c.tiff"
x_arr, y_arr, data, mask, coord_map_ground, alt_map_ground = load_tif(path_map_ground)
   
path_pipe = r"smooth_0.gpkg"
pipe_df = gpd.read_file(path_pipe)
pipe_xy = np.c_[pipe_df.geometry.x, pipe_df.geometry.y]

fig, ax = plt.subplots()
im = plt.contourf(x_arr, y_arr, data*mask , 30, cmap='jet')
ax.plot(pipe_xy[:, 0], pipe_xy[:, 1], 'w-o')

alt_ground_pipe_nearest = np.zeros(len(pipe_xy))
alt_ground_pipe_Regular = np.zeros(len(pipe_xy))

mask_1d_bool = ~np.isnan(mask.ravel())


Interpolator_Regular = RegularGridInterpolator((x_arr, y_arr), data.T)


for mm in range(len(pipe_xy)):
    alt_ground_pipe_Regular[mm] = Interpolator_Regular(pipe_xy[mm])[0]
    


qgis_df = gpd.read_file(r"result_de_Qgis.gpkg")
alt_qgis = qgis_df.geometry.z.values

plt.figure()
plt.plot(alt_ground_pipe_Regular, 'r', label="Regular")
plt.plot(alt_qgis, 'k', label="Qgis")
plt.legend()












