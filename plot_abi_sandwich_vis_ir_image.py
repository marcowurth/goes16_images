
import os
import datetime
import fnmatch

import numpy as np
import xarray as xr
import pyproj
import Ngl
import Nio
from PIL import Image

from domain_definitions import get_image_domain
from cut_abi_image import cut_data


def main():

    max_percentile = 99.9
    #gamma = 1.0
    #gamma = 0.8
    gamma = 0.5

    year = 2020
    month = 11
    days = [22]
    #days = list(range(1,31))
    hours = [21]
    #hours = list(range(18,21))
    #hours = list(range(24))
    #minutes = list(range(0, 60, 10))
    minutes = [30]

    #domain_name = 'Argentina_Central'
    domain_name = 'La_Pampa'


    domain = get_image_domain(domain_name)
    for day in days:
        for hour in hours:
            for minute in minutes:
                plot_image(datetime.datetime(year, month, day, hour, minute), domain, max_percentile, gamma)

    return

############################################################################
############################################################################
############################################################################

def plot_image(date, domain, max_percentile, gamma):

    with open('/data_slow/base_path.txt', 'r') as f:
        base_path = f.readlines()[0][:-1]
    path = dict(base = base_path,
                data = 'data/ABI/GOES-16/',
                image = 'images/GOES-16/sandwich_vis_ir/',
                colorpalette = 'data/additional_data/colorpalettes/',
                shapefiles = 'data/additional_data/shapefiles/')


    # search and open goes-16 file

    dayofyear = (date - datetime.datetime(date.year,1,1)).days + 1
    match_string_b13 = '*C13_G16_s{:4d}{:03d}{:02d}{:02d}*'.format(\
                        date.year, dayofyear, date.hour, date.minute)
    files_list_b13 = os.listdir(path['base'] + path['data'] + 'b13/')

    filename_b13 = None
    for file in files_list_b13:
        if fnmatch.fnmatch(file, match_string_b13):
            filename_b13 = file
    if filename_b13 == None:
        print('----- abi file not found -----')
        print('----- match_string: {} -----'.format(match_string_b13))
        return

    match_string_b02 = '*C02_G16_s{:4d}{:03d}{:02d}{:02d}*'.format(\
                        date.year, dayofyear, date.hour, date.minute)
    files_list_b02 = os.listdir(path['base'] + path['data'] + 'b02/')

    filename_b02 = None
    for file in files_list_b02:
        if fnmatch.fnmatch(file, match_string_b02):
            filename_b02 = file
    if filename_b02 == None:
        print('----- abi file not found -----')
        print('----- match_string: {} -----'.format(match_string_b02))
        return

    goes_dataset_b13 = xr.open_dataset(path['base'] + path['data'] + 'b13/' + filename_b13)
    image_array_b13 = goes_dataset_b13['CMI'].values - 273.15
    goes_dataset_b02 = xr.open_dataset(path['base'] + path['data'] + 'b02/' + filename_b02)
    image_array_b02 = goes_dataset_b02['CMI'].values
    #print(goes_dataset_b13)
    #print(goes_dataset_b02)


    # calculate geographical coordinates

    x = goes_dataset_b13['x_subset'].values
    y = goes_dataset_b13['y_subset'].values
    sat_h = goes_dataset_b13['goes_imager_projection'].perspective_point_height
    sat_lon = goes_dataset_b13['goes_imager_projection'].longitude_of_projection_origin
    sat_sweep = goes_dataset_b13['goes_imager_projection'].sweep_angle_axis

    p = pyproj.Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep, ellps='GRS80')
    xx, yy = np.meshgrid(x * sat_h, y * sat_h)
    lons_b13, lats_b13 = p(xx, yy, inverse=True)

    lats_b13 = np.ma.masked_outside(lats_b13, -90.0, 90.0)
    lons_b13 = np.ma.masked_outside(lons_b13, -180.0, 180.0)
    lats_b13.fill_value = 1000
    lons_b13.fill_value = 1000

    del x, y, p, xx, yy
    goes_dataset_b13.close()

    x = goes_dataset_b02['x_subset'].values
    y = goes_dataset_b02['y_subset'].values
    sat_h = goes_dataset_b02['goes_imager_projection'].perspective_point_height
    sat_lon = goes_dataset_b02['goes_imager_projection'].longitude_of_projection_origin
    sat_sweep = goes_dataset_b02['goes_imager_projection'].sweep_angle_axis

    p = pyproj.Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep, ellps='GRS80')
    xx, yy = np.meshgrid(x * sat_h, y * sat_h)
    lons_b02, lats_b02 = p(xx, yy, inverse=True)

    lats_b02 = np.ma.masked_outside(lats_b02, -90.0, 90.0)
    lons_b02 = np.ma.masked_outside(lons_b02, -180.0, 180.0)
    lats_b02.fill_value = 1000
    lons_b02.fill_value = 1000

    del x, y, p, xx, yy
    goes_dataset_b02.close()


    #margin_deg = 1.0
    margin_deg = 0.5
    index_x_first, index_x_last, index_y_first, index_y_last = cut_data(image_array_b13, lats_b13, lons_b13, domain,
                                                                        margin_deg, False)
    image_array_b13 = image_array_b13[index_y_first:index_y_last+1, index_x_first:index_x_last+1]
    lats_b13 = lats_b13[index_y_first:index_y_last+1, index_x_first:index_x_last+1]
    lons_b13 = lons_b13[index_y_first:index_y_last+1, index_x_first:index_x_last+1]

    index_x_first, index_x_last, index_y_first, index_y_last = cut_data(image_array_b02, lats_b02, lons_b02, domain,
                                                                        margin_deg, False)
    image_array_b02 = image_array_b02[index_y_first:index_y_last+1, index_x_first:index_x_last+1]
    lats_b02 = lats_b02[index_y_first:index_y_last+1, index_x_first:index_x_last+1]
    lons_b02 = lons_b02[index_y_first:index_y_last+1, index_x_first:index_x_last+1]

    min_bt = np.nanmin(image_array_b13)
    #print('min BT: {:.1f} °C'.format(min_bt))
    image_array_b13 = np.where(image_array_b13 > -20, 99, image_array_b13)

    ########################################################################
    ########################################################################

    custom_palette_map = np.array([[0, 0, 0],[0, 0, 0],[0, 0, 0]])

    filename_colorpalette = 'rainbowIRsummer.txt'
    with open(path['base'] + path['colorpalette'] + filename_colorpalette, 'r') as f:
        lines = f.readlines()
    rgb_colors_b13 = []
    #rgb_colors_b13.append([1, 1, 1])
    rgb_colors_b13.append([1, 1, 1])
    rgb_colors_b13.append([float(lines[70][:10]), float(lines[70][11:21]), float(lines[70][22:32])])
    for i, line in enumerate(lines):
        if i % 14 == 0 and i > 70:
            rgb_colors_b13.append([float(line[:10]), float(line[11:21]), float(line[22:32])])
    #rgb_colors_b13.append([0, 0, 0])
    custom_palette_b13 = np.array(rgb_colors_b13)
    clevels_b13 = list(range(-90,-20+1,1))


    range_min = 0.0
    range_max = np.percentile(np.concatenate(image_array_b02), max_percentile)
    image_array_b02 = (image_array_b02 - range_min) / (range_max - range_min)
    image_array_b02 = np.where(image_array_b02 < 0.0, 0.0, image_array_b02)
    image_array_b02 = np.where(image_array_b02 > 1.0, 1.0, image_array_b02)
    image_array_b02 = image_array_b02 ** (1.0 / gamma)
    clevels_b02 = np.linspace(0.0, 1.0, 251)

    rgb_colors_b02 = []
    for refl_value in np.linspace(0, 1, 255):
        rgb_colors_b02.append([refl_value, refl_value, refl_value])
    custom_palette_b02 = np.array(rgb_colors_b02)

    #print('custom_palette_b13 shape:', custom_palette_b13.shape)
    #print('custom_palette_b02 shape:', custom_palette_b02.shape)


    opacity_b13 = 0.4
    opacity_b02 = 1.0
    resolution = 800

    date += datetime.timedelta(minutes = 8)    # time shift of actual sensor time for Central Argentina

    imagename = 'ABI_Sandwich_VIS-IR_GOES-16_{}_{:4d}{:02d}{:02d}_{:02d}:{:02d}UTC_{:d}px'.format(
                 domain['name'], date.year, date.month, date.day, date.hour, date.minute, resolution)
    print('plot {}...'.format(imagename))

    wks_res             = Ngl.Resources()
    wks_res.wkWidth     = resolution
    wks_res.wkHeight    = resolution
    wks_res.wkColorMap  = custom_palette_map
    wks_type  = 'png'
    wks = Ngl.open_wks(wks_type, path['base'] + path['image'] + imagename, wks_res)

    ########################################################################
    ########################################################################

    resources = Ngl.Resources()
    resources.nglDraw  = False
    resources.nglFrame = False

    resources.mpProjection = domain['projection']

    if domain['limits_type'] == 'radius':
        resources.mpLimitMode  = 'LatLon'
        resources.mpCenterLonF = domain['centerlon']
        resources.mpCenterLatF = domain['centerlat']
        cutout_plot = dict(
                            lat_min = float(np.where(domain['centerlat'] - domain['radius'] / 111.2 < -90,
                                               -90, domain['centerlat'] - domain['radius'] / 111.2)),
                            lat_max = float(np.where(domain['centerlat'] + domain['radius'] / 111.2 > 90,
                                               90, domain['centerlat'] + domain['radius'] / 111.2)),
                           )
        cutout_plot['lon_min'] = float(np.where(cutout_plot['lat_min'] <= -90 or cutout_plot['lat_max'] >= 90,
                                       0,
                                       domain['centerlon'] - domain['radius'] \
                                        / (111.2 * np.cos(domain['centerlat']*np.pi/180))))
        cutout_plot['lon_max'] = float(np.where(cutout_plot['lat_min'] <= -90 or cutout_plot['lat_max'] >= 90,
                                       360,
                                       domain['centerlon'] + domain['radius'] \
                                        / (111.2 * np.cos(domain['centerlat']*np.pi/180))))
        resources.mpMinLonF     = cutout_plot['lon_min']
        resources.mpMaxLonF     = cutout_plot['lon_max']
        resources.mpMinLatF     = cutout_plot['lat_min']
        resources.mpMaxLatF     = cutout_plot['lat_max']

    resources.vpXF          = 0.001
    resources.vpYF          = 1.00
    resources.vpWidthF      = 0.88
    resources.vpHeightF     = 1.00

    #resources.mpProjection  = 'Hammer'
    #resources.mpCenterLonF  = (domain['lon_max'] + domain['lon_min']) / 2
    #resources.mpCenterLatF  = (domain['lat_max'] + domain['lat_min']) / 2

    '''resources.mpProjection      = 'Satellite'
    resources.mpSatelliteDistF  = 5.62
    resources.mpCenterLonF      = -75.0
    resources.mpCenterLatF      = 0.0'''

    #resources.mpLimitMode   = 'latlon'
    #resources.mpMinLonF     = domain['lon_min']
    #resources.mpMaxLonF     = domain['lon_max']
    #resources.mpMinLatF     = domain['lat_min']
    #resources.mpMaxLatF     = domain['lat_max']
    resources.mpPerimOn             = True
    resources.mpPerimLineColor      = 'black'
    resources.mpPerimLineThicknessF = 8.0 * resolution / 1000

    resources.nglMaximize   = False
    #resources.vpXF          = 0.02
    #resources.vpYF          = 0.96
    #resources.vpWidthF      = 0.96
    #resources.vpHeightF     = 0.94
    #resources.mpShapeMode = 'freeAspect'

    resources.tmXBOn = False
    resources.tmXTOn = False
    resources.tmYLOn = False
    resources.tmYROn = False

    ########################################################################

    resources.mpGridAndLimbOn           = False

    #resources.mpDataBaseVersion             = 'HighRes'
    #resources.mpDataResolution              = 'Finest'
    #resources.mpGeophysicalLineThicknessF   = 3.0
    #resources.mpGeophysicalLineColor    = 'black'
    resources.mpOutlineOn               = False
    #resources.mpOutlineOn               = True

    resources.mpDataBaseVersion         = 'MediumRes'
    resources.mpDataSetName             = 'Earth..4'
    resources.mpOutlineBoundarySets     = 'national'
    resources.mpGeophysicalLineColor        = 'black'
    resources.mpGeophysicalLineThicknessF   = 1.5 *  resolution / 1000
    resources.mpNationalLineColor           = 'black'
    resources.mpNationalLineThicknessF      = 1.5 *  resolution / 1000

    image_map = Ngl.map(wks, resources)
    del resources

    shp_filenames = []
    #shp_filenames.append(['gadm36_DEU_0.shp', 3.0])
    #shp_filenames.append(['gadm36_DEU_1.shp', 3.0])
    #shp_filenames.append(['gadm36_AUT_0.shp', 3.0])
    #shp_filenames.append(['gadm36_CHE_0.shp', 3.0])
    #shp_filenames.append(['gadm36_ITA_0.shp', 3.0])
    #shp_filenames.append(['gadm36_GRC_0.shp', 3.0])
    #shp_filenames.append(['gadm36_CZE_0.shp', 3.0])
    #shp_filenames.append(['gadm36_DEU_2.shp', 3.0])
    #shp_filenames.append(['gadm36_ESP_0.shp', 3.0])
    #shp_filenames.append(['gadm36_PRT_0.shp', 3.0])
    #shp_filenames.append(['gadm36_FRA_0.shp', 3.0])

    shp_filenames.append(['gadm36_ARG_0.shp', 0.5])
    shp_filenames.append(['gadm36_BRA_0.shp', 0.5])
    shp_filenames.append(['gadm36_CHL_0.shp', 0.5])
    shp_filenames.append(['gadm36_URY_0.shp', 0.5])
    shp_filenames.append(['gadm36_ARG_1.shp', 0.5])
    shp_filenames.append(['gadm36_BRA_1.shp', 0.5])
    shp_filenames.append(['gadm36_CHL_1.shp', 0.5])
    shp_filenames.append(['gadm36_URY_1.shp', 0.2])
    shp_filenames.append(['gadm36_ARG_2.shp', 0.2])

    '''shp_filenames.append(['gadm36_ARG_0.shp', 0.5])
    shp_filenames.append(['gadm36_BRA_0.shp', 0.5])
    shp_filenames.append(['gadm36_CHL_0.shp', 0.5])
    shp_filenames.append(['gadm36_URY_0.shp', 0.5])
    shp_filenames.append(['gadm36_ARG_1.shp', 0.2])
    shp_filenames.append(['gadm36_BRA_1.shp', 0.2])
    shp_filenames.append(['gadm36_CHL_1.shp', 0.2])'''

    for shp_filename, lineThickness in shp_filenames:
        shpf = Nio.open_file(path['base'] + path['shapefiles'] + shp_filename, 'r')
        shpf_lon = np.ravel(shpf.variables['x'][:])
        shpf_lat = np.ravel(shpf.variables['y'][:])
        shpf_segments = shpf.variables['segments'][:, 0]
        #sf = shapefile.Reader(path['base'] + path['shapefiles'] + shp_filename)
        #shapes = sf.shapes()
        #shpf_lon = [point[0] for point in shapes[0].points]
        #shpf_lat = [point[1] for point in shapes[0].points]

        plres = Ngl.Resources()
        plres.gsLineColor = 'white'
        plres.gsLineThicknessF = lineThickness
        plres.gsSegments = shpf_segments
        Ngl.add_polyline(wks, image_map, shpf_lon, shpf_lat, plres)
        del shpf, shpf_lat, shpf_lon, shpf_segments

    ########################################################################
    ########################################################################

    resources = Ngl.Resources()
    resources.nglDraw  = False
    resources.nglFrame = False

    resources.sfXArray        = lons_b13.filled()
    resources.sfYArray        = lats_b13.filled()
    resources.sfMissingValueV = 99

    ########################################################################

    #resources.trGridType            = 'TriangularMesh'
    resources.cnFillOn              = True
    resources.cnFillMode            = 'RasterFill'
    resources.cnFillOpacityF        = opacity_b13
    resources.cnMissingValFillColor = 'transparent'
    resources.cnLevelSelectionMode  = 'ExplicitLevels'
    resources.cnLevels              = clevels_b13
    resources.cnFillColors          = custom_palette_b13
    resources.cnConstFLabelOn       = False
    resources.cnNoDataLabelOn       = False

    resources.cnLinesOn             = False
    resources.cnLineLabelsOn        = False
    #resources.lbLabelBarOn          = False
    #resources.lbLabelStride         = 14
    #resources.lbLabelFontHeightF    = 0.016

    resources.lbLabelBarOn          = True
    resources.lbAutoManage          = False
    resources.lbOrientation         = 'vertical'
    resources.lbLabelOffsetF        = 0.04      # minor axis fraction: the distance between colorbar and numbers
    resources.lbBoxMinorExtentF     = 0.20      # minor axis fraction: width of the color boxes when labelbar down
    resources.lbTopMarginF          = 0.2       # make a little more space at top for the unit label
    resources.lbRightMarginF        = 0.0
    resources.lbBottomMarginF       = 0.05
    resources.lbLeftMarginF         = -0.35

    resources.cnLabelBarEndStyle    = 'ExcludeOuterBoxes'
    resources.pmLabelBarWidthF      = 0.10
    resources.lbLabelFontHeightF    = 0.010
    resources.lbBoxSeparatorLinesOn = False
    resources.lbBoxLineThicknessF   = 4
    resources.lbLabelAlignment      = 'ExternalEdges'
    resources.lbLabelStride = 10

    image_b13 = Ngl.contour(wks, image_array_b13, resources)

    del resources

    ########################################################################
    ########################################################################

    resources = Ngl.Resources()
    resources.nglDraw  = False
    resources.nglFrame = False

    resources.sfXArray        = lons_b02.filled()
    resources.sfYArray        = lats_b02.filled()
    resources.sfMissingValueV = lats_b02.fill_value

    ########################################################################

    #resources.trGridType            = 'TriangularMesh'
    resources.cnFillOn              = True
    resources.cnFillMode            = 'RasterFill'
    resources.cnFillOpacityF        = opacity_b02
    resources.cnMissingValFillColor = 'black'
    resources.cnLevelSelectionMode  = 'ExplicitLevels'
    resources.cnLevels              = clevels_b02
    resources.cnFillColors          = custom_palette_b02
    resources.cnConstFLabelOn       = False
    resources.cnNoDataLabelOn       = False

    resources.cnLinesOn             = False
    resources.cnLineLabelsOn        = False
    resources.lbLabelBarOn          = False

    image_b02 = Ngl.contour(wks, image_array_b02, resources)

    ########################################################################

    # plot unit #

    text_str = '  ~S~o~N~C'
    text_res_1 = Ngl.Resources()
    text_res_1.txFontColor   = 'black'
    text_res_1.txFontHeightF = 0.013
    text_x = 0.97
    if domain['name'] == 'La_Pampa'\
     or domain['name'] == 'Mendoza_San_Luis'\
     or domain['name'] == 'Uruguay'\
     or domain['name'] == 'Prov_BsAs':
        text_y = 0.920
    elif domain['name'] == 'Neuquen_Bio_Bio'\
     or domain['name'] == 'Rio_Negro_Este_Golfo_San_Matias':
        text_y = 0.915
    elif domain['name'] == 'Argentina_Central':
        text_y = 0.905
    else:
        text_y = 0.925

    # calulate and plot image description #

    res_text_descr = Ngl.Resources()
    res_text_descr.txJust           = 'CenterLeft'
    res_text_descr.txFontHeightF    = 0.015
    res_text_descr.txFontColor      = 'black'
    res_text_descr.txBackgroundFillColor = 'white'
    res_text_descr.txPerimOn = True
    res_text_descr.txPerimColor = 'black'

    date -= datetime.timedelta(hours=3)
    comp_descr = 'Sandwich IR VIS 10.3~F33~m~F21~m 0.64~F33~m~F21~m'
    text_descr_str = 'GOES-16/ABI: {}   {:02d}.{:02d}.{:4d}, {:02d}:{:02d}UTC-3'.format(
                      comp_descr, date.day, date.month, date.year,
                      date.hour, date.minute)
    text_descr_x = 0.02
    text_descr_y = text_y - 0.015

    ########################################################################

    Ngl.overlay(image_map, image_b02)
    Ngl.overlay(image_map, image_b13)
    Ngl.draw(image_map)
    Ngl.text_ndc(wks, text_descr_str, text_descr_x, text_descr_y, res_text_descr)
    Ngl.text_ndc(wks, text_str, text_x, text_y, text_res_1)
    Ngl.frame(wks)

    Ngl.destroy(wks)
    del image_array_b13, lats_b13, lons_b13, image_array_b02, lats_b02, lons_b02
    del image_map, image_b13, image_b02, wks_res

    ########################################################################

    # cut top and bottom whitespace of plot #

    im = Image.open(path['base'] + path['image'] + imagename + '.png')
    image_array = np.asarray(im.convert('L'))
    image_array = np.where(image_array < 255, 1, 0)
    image_filter = np.amax(image_array, axis=1)
    vmargins = [np.nonzero(image_filter)[0][0]+1, np.nonzero(image_filter[::-1])[0][0]+1]
    #print(vmargins)
    #print(im.size)

    im_cropped = Image.new('RGB',(im.size[0], im.size[1] - vmargins[0] - vmargins[1]), (255,255,255))
    im_cropped.paste(im.crop((0, vmargins[0], im.size[0], im.size[1] - vmargins[1])), (0, 0))
    #print(im_cropped.size)
    im.close()
    im_cropped.save(path['base'] + path['image'] + imagename + '.png', 'png')
    im_cropped.close()

    return

############################################################################
############################################################################
############################################################################

if __name__ == '__main__':
    import time
    t1 = time.time()
    main()
    t2 = time.time()
    delta_t = t2-t1
    if delta_t < 60:
        print('total script time:  {:.1f}s'.format(delta_t))
    elif 60 <= delta_t <= 3600:
        print('total script time:  {:.0f}min{:.0f}s'.format(delta_t//60, delta_t-delta_t//60*60))
    else:
        print('total script time:  {:.0f}h{:.0f}min'.format(delta_t//3600, (delta_t-delta_t//3600*3600)/60))
