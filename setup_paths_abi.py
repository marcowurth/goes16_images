
import os


base_path = '/data_fast/'
print('base_path:', base_path)

os.makedirs(base_path + 'data/additional_data/colorpalettes', exist_ok=True)
os.makedirs(base_path + 'data/additional_data/shapefiles', exist_ok=True)
os.makedirs(base_path + 'data/ABI/GOES-16/b02', exist_ok=True)
os.makedirs(base_path + 'data/ABI/GOES-16/b13', exist_ok=True)
os.makedirs(base_path + 'images/GOES-16/sandwich_vis_ir', exist_ok=True)
