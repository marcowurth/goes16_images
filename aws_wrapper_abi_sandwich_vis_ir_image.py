
import datetime

import dask

from download_abi import download_abi_files
from domain_definitions import get_image_domain
from plot_abi_sandwich_vis_ir_image import plot_image


def main():
    distributed_exec = True
    #distributed_exec = False

    if distributed_exec:
        num_max_tasks = 2
        client = dask.distributed.Client(
                  dask.distributed.LocalCluster(
                    n_workers = 1,
                    processes = True,
                    threads_per_worker = num_max_tasks))
        print(client)
    else:
        num_max_tasks = None
        client = None

    channels = [2,13]
    #channels = [15]
    #channels = [13,15]
    #channels = [1,7,13]

    year = 2020
    month = 12
    days = [2]
    #days = list(range(1,31))
    hours = [18]
    #hours = list(range(18,21))
    #hours = list(range(24))
    #minutes = list(range(0, 60, 10))
    minutes = [0]

    domain_names = []
    '''domain_names.append('La_Pampa')
    domain_names.append('Neuquen')
    domain_names.append('Prov_BsAs')
    domain_names.append('Entre_Rios')
    domain_names.append('Santa_Fe')
    domain_names.append('AMBA')
    domain_names.append('San_Luis_Sur_Cordoba')
    domain_names.append('Formosa_Sur')
    domain_names.append('Mendoza_San_Rafael')
    domain_names.append('Radar_Termas_de_Río_Ondo')'''

    max_percentile = 99.9
    #gamma = 1.0
    #gamma = 0.8
    gamma = 0.5

    download_abi_files(distributed_exec, num_max_tasks, client, channels, year, month, days, hours, minutes)

    for domain_name in domain_names:
        domain = get_image_domain(domain_name)
        for day in days:
            for hour in hours:
                for minute in minutes:
                    plot_image(datetime.datetime(year, month, day, hour, minute), domain, max_percentile, gamma)

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
