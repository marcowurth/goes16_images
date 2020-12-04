
import os
import time
import datetime
import fnmatch

import boto3
import numpy as np
import netCDF4 as nc
import dask


def main():
    #distributed_exec = True
    distributed_exec = False

    if distributed_exec:
        num_max_tasks = 48
        client = dask.distributed.Client(
                  dask.distributed.LocalCluster(
                    n_workers = 1,
                    processes = True,
                    threads_per_worker = num_max_tasks))
        print(client)
    else:
        num_max_tasks = None
        client = None


    channels = [13]
    #channels = [15]
    #channels = [13,15]
    #channels = [1,7,13]

    year = 2020
    month = 12
    days = [2]
    #days = list(range(1,31))
    hours = [23]
    #hours = list(range(18,21))
    #hours = list(range(24))
    #minutes = list(range(0, 60, 10))
    minutes = [0]

    download_abi_files(distributed_exec, num_max_tasks, client, channels, year, month, days, hours, minutes)

    return

############################################################################
############################################################################
############################################################################

def download_abi_files(distributed_exec, num_max_tasks, client, channels, year, month, days, hours, minutes):

    if distributed_exec:
        for day in days:
            date_channels = []
            for hour in hours:
                for minute in minutes:
                    for channel in channels:
                        date_channels.append([datetime.datetime(year, month, day, hour, minute), channel])
            #date_channels = [[datetime.datetime(2019, 8, 8, 9, 30), 7]]
            #print(len(date_channels))

            sub_date_channels = []
            if num_max_tasks > len(date_channels):
                num_max_tasks = len(date_channels)
            for i in range(len(date_channels) // num_max_tasks):
                sub_date_channels.append(date_channels[i * num_max_tasks : (i + 1) * num_max_tasks])
            if len(date_channels) % num_max_tasks > 0:
                sub_date_channels.append(date_channels[-1 * (len(date_channels) % num_max_tasks) : ])

            all_tasks = []
            for sub_date_channel in sub_date_channels:
                futures = []
                for date_channel in sub_date_channel:
                    futures.append(client.submit(download_file, date_channel[0], date_channel[1], retries = 3))
                dask.distributed.wait(futures)
                all_tasks += futures

            print('------------------------------------------')
            try:
                #print('all downloaded files:')
                #for f in all_tasks:
                #    print(f.result())

                testlist = [f.result()[-9:] for f in all_tasks]
                if testlist.count('subset.nc') == len(testlist):
                    print('                        #             ')
                    print('                     #                ')
                    print('                  #                   ')
                    print('     #         #                      ')
                    print('       #    #                         ')
                    print('         #                            ')
            except:
                    print('            #           #             ')
                    print('              #       #               ')
                    print('                #   #                 ')
                    print('                  #                   ')
                    print('                #   #                 ')
                    print('              #       #               ')
                    print('            #           #             ')

            client.restart()
            print('client restarted')

        client.close()
    else:
        for day in days:
            date_channels = []
            for hour in hours:
                for minute in minutes:
                    for channel in channels:
                        download_file(datetime.datetime(year, month, day, hour, minute), channel)


    return

############################################################################
############################################################################
############################################################################

def download_file(date, channel):

    with open('/data_slow/base_path.txt', 'r') as f:
        base_path = f.readlines()[0][:-1]
    path = dict(base = base_path,
                data = 'data/ABI/GOES-16/',)

    dayofyear = (date-datetime.datetime(date.year,1,1)).days + 1

    subfolder = 'ABI-L2-CMIPF/{:4d}/{:03d}/{:02d}'.format(\
                    date.year, dayofyear, date.hour)

    match_string = '*C{:02d}_G16_s{:4d}{:03d}{:02d}{:02d}*'.format(\
                    channel, date.year, dayofyear, date.hour, date.minute)

    #time.sleep(.5)
    s3 = boto3.resource('s3')
    noaa_bucket = s3.Bucket('noaa-goes16')
    file_list = []
    for object in noaa_bucket.objects.filter(Prefix=subfolder):
        file_list.append(object.key)
    
    filename = fnmatch.filter(file_list, match_string)[0]

    #print('matched filename')

    obj = noaa_bucket.Object(filename)
    filename = filename[28:]
    with open(path['base'] + path['data'] + filename, 'wb') as file:
        obj.download_fileobj(file)

    filename_subset = reduce_file_to_subset(path, filename, channel)
    os.remove(path['base'] + path['data'] + filename)

    print('downloaded goes-16 abi b{:02d}, {:02d}.{:02d}.{:02d}, {:02d}:{:02d}UTC'.format(\
            channel, date.day, date.month, date.year, date.hour, date.minute))

    #filename_subset = create_fillValue_image(path, filename)

    #return  'bla'
    return filename_subset

############################################################################
############################################################################
############################################################################

def reduce_file_to_subset(path, filename_full, channel):

    # open files #

    channel_subfolder = 'b{:02d}/'.format(channel)
    filename_subset = filename_full[:-3] + '_subset.nc'
    abi_file_full = nc.Dataset(path['base'] + path['data'] + filename_full, 'r')
    abi_file_subset = nc.Dataset(path['base'] + path['data'] + channel_subfolder + filename_subset, 'w')


    # copy global attributes #

    for name in abi_file_full.ncattrs():
        abi_file_subset.setncattr(name, abi_file_full.getncattr(name))
    print(abi_file_full.getncattr(name))


    # create new subset dimensions #

    if channel >= 7:
        f_res = 1
    elif channel == 1:
        f_res = 2
    elif channel == 2:
        f_res = 4

    abi_file_subset.createDimension('x_subset', 1300*f_res)
    abi_file_subset.createDimension('y_subset', 1900*f_res)


    # create variables CMI/DQF/goes_imager_projection and copy attributes #

    for var_name in ['CMI','DQF']:
        var_full = abi_file_full.variables[var_name]
        var_subset = abi_file_subset.createVariable(var_name, var_full.datatype, ('y_subset','x_subset'),
                                                    zlib = True, complevel = 4, fill_value = var_full._FillValue)

        for name in var_full.ncattrs():
            if name == '_FillValue':
                continue
            var_subset.setncattr(name, var_full.getncattr(name))

    for var_name in ['goes_imager_projection']:
        var_full = abi_file_full.variables[var_name]
        var_subset = abi_file_subset.createVariable(var_name, var_full.datatype)

        for name in var_full.ncattrs():
            var_subset.setncattr(name, var_full.getncattr(name))


    # create variable y and copy attributes #

    var_full = abi_file_full.variables['y']
    var_subset = abi_file_subset.createVariable('y_subset', var_full.datatype, ('y_subset'),
                                                zlib = True, complevel = 4)

    for name in var_full.ncattrs():
        var_subset.setncattr(name, var_full.getncattr(name))
    var_subset.setncattr('description', 'Rectangular domain around southern South America')


    # create variable x and copy attributes #

    var_full = abi_file_full.variables['x']
    var_subset = abi_file_subset.createVariable('x_subset', var_full.datatype, ('x_subset'),
                                                zlib = True, complevel = 4)

    for name in var_full.ncattrs():
        var_subset.setncattr(name, var_full.getncattr(name))
    var_subset.setncattr('description', 'Rectangular domain around southern South America')


    # copy variable entries #

    abi_file_subset.variables['CMI'][:] = abi_file_full.variables['CMI'][3300*f_res:5200*f_res, 2500*f_res:3800*f_res]
    abi_file_subset.variables['DQF'][:] = abi_file_full.variables['DQF'][3300*f_res:5200*f_res, 2500*f_res:3800*f_res]
    abi_file_subset.variables['y_subset'][:] = abi_file_full.variables['y'][3300*f_res:5200*f_res]
    abi_file_subset.variables['x_subset'][:] = abi_file_full.variables['x'][2500*f_res:3800*f_res]


    # close and write to files #

    abi_file_full.close()
    abi_file_subset.close()


    '''print('size full:  {:.1f}MB'.format(\
            os.path.getsize(path['base'] + path['data'] + filename_full) / 1e6))
    print('size subset: {:.1f}MB ({:.1f}%)'.format(
            os.path.getsize(path['base'] + path['data'] + channel_subfolder + filename_subset) / 1e6,\
            os.path.getsize(path['base'] + path['data'] + channel_subfolder + filename_subset)\
             / os.path.getsize(path['base'] + path['data'] + filename_full) * 100))'''

    return filename_subset


############################################################################
############################################################################
############################################################################

def create_fillValue_image(path, filename_full):

    # open files #

    filename_subset = 'empty_image.nc'
    abi_file_full = nc.Dataset(path['base'] + path['data'] + filename_full, 'r')
    abi_file_subset = nc.Dataset(path['base'] + path['data'] + filename_subset, 'w')


    # copy global attributes #

    for name in abi_file_full.ncattrs():
        abi_file_subset.setncattr(name, abi_file_full.getncattr(name))


    # create new subset dimensions #

    abi_file_subset.createDimension('x_subset', 1300)
    abi_file_subset.createDimension('y_subset', 1900)


    # create variables CMI/DQF/goes_imager_projection and copy attributes #

    for var_name in ['CMI','DQF','goes_imager_projection']:
        var_full = abi_file_full.variables[var_name]
        var_subset = abi_file_subset.createVariable(var_name, var_full.datatype, ('y_subset','x_subset'),\
                                                     zlib = True, complevel = 4)

        for name in var_full.ncattrs():
            var_subset.setncattr(name, var_full.getncattr(name))


    # create variable y and copy attributes #

    var_full = abi_file_full.variables['y']
    var_subset = abi_file_subset.createVariable('y_subset', var_full.datatype, ('y_subset'),\
                                                     zlib = True, complevel = 4)

    for name in var_full.ncattrs():
        var_subset.setncattr(name, var_full.getncattr(name))


    # create variable x and copy attributes #

    var_full = abi_file_full.variables['x']
    var_subset = abi_file_subset.createVariable('x_subset', var_full.datatype, ('x_subset'),\
                                                     zlib = True, complevel = 4)

    for name in var_full.ncattrs():
        var_subset.setncattr(name, var_full.getncattr(name))


    # copy variable entries #

    fillValue = 130
    cmi_fillValue = np.zeros((1900, 1300)) + fillValue
    dqf_fillValue = np.zeros((1900, 1300))
    print(cmi_fillValue.shape)
    print(dqf_fillValue.shape)
    abi_file_subset.variables['CMI'][:] = cmi_fillValue
    abi_file_subset.variables['DQF'][:] = dqf_fillValue
    abi_file_subset.variables['y_subset'][:] = abi_file_full.variables['y'][3300:5200]
    abi_file_subset.variables['x_subset'][:] = abi_file_full.variables['x'][2500:3800]


    # close and write to files #

    abi_file_full.close()
    abi_file_subset.close()

    return filename_subset

############################################################################
############################################################################
############################################################################

def delete_all_abi_files():

    delete_paths = []
    delete_paths.append('/data_slow/data/ABI/GOES-16/')
    delete_paths.append('/data_slow/data/ABI/GOES-16/b02/')
    delete_paths.append('/data_slow/data/ABI/GOES-16/b13/')

    for delete_path in delete_paths:
        for filename in os.listdir(delete_path):
            os.remove(delete_path + filename)

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
