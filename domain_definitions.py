
def get_image_domain(domain_name):

    if domain_name == 'Central_Europe':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 50, centerlon = 9, radius = 550)

    elif domain_name == 'Spain':
        domain = dict(lat_max = 46,
                lon_min = -10, lon_max = 4,
                      lat_min = 35.5, name = domain_name)

    elif domain_name == 'Medicane_Cassilda':
        domain = dict(lat_max = 38,
                lon_min = 14, lon_max = 22,
                      lat_min = 32, name = domain_name)

    elif domain_name == 'Ionian_Sea_W':
        domain = dict(lat_max = 40.0,
                lon_min = 13.3, lon_max = 20.5,
                      lat_min = 34.2, name = domain_name)

    elif domain_name == 'Ionian_Sea_E':
        domain = dict(lat_max = 40.0,
                lon_min = 15.1, lon_max = 22.3,
                      lat_min = 34.2, name = domain_name)

    elif domain_name == 'Ionian_Sea_E_close':
        domain = dict(lat_max = 39.5,
                lon_min = 16.5, lon_max = 21.5,
                      lat_min = 35.5, name = domain_name)

    elif domain_name == 'Athen_Southeast_far':
        domain = dict(lat_max = 37.97,
                lon_min = 23.65, lon_max = 24.25,
                      lat_min = 37.5, name = domain_name)

    elif domain_name == 'Bengal_Sea':
        domain = dict(lat_max = 25.5,
                lon_min = 79, lon_max = 95,
                      lat_min = 10, name = domain_name)

    elif domain_name == 'Argentina_Central':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -34.6, centerlon = -64.4, radius = 800)

    elif domain_name == 'Argentina_Noreste':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -30.0, centerlon = -59.0, radius = 500)

    elif domain_name == 'AMBA':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -34.6, centerlon = -58.5, radius = 100)

    elif domain_name == 'AMBA_cerca':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -34.6, centerlon = -58.5, radius = 50)

    elif domain_name == 'CABA':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -34.6, centerlon = -58.45, radius = 20)

    elif domain_name == 'Santa_Fe':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -31.7, centerlon = -60.6, radius = 300)

    elif domain_name == 'Santa_Fe_cerca':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -32.4, centerlon = -61.2, radius = 150)

    elif domain_name == 'Santa_Fe_Norte':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -29.5, centerlon = -61.5, radius = 130)

    elif domain_name == 'La_Pampa':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -37.2, centerlon = -65.7, radius = 300)

    elif domain_name == 'La_Pampa_Este':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -37.2, centerlon = -64.2, radius = 100)

    elif domain_name == 'Neuquen':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -38.5, centerlon = -70.0, radius = 300)

    elif domain_name == 'Neuquen_Norte':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -37.7, centerlon = -69.5, radius = 130)

    elif domain_name == 'Prov_BsAs':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -36.5, centerlon = -60.2, radius = 350)

    elif domain_name == 'Prov_BsAs_Oeste':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -37.0, centerlon = -62.0, radius = 150)

    elif domain_name == 'Prov_BsAs_Saladillo':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -35.7, centerlon = -59.9, radius = 150)

    elif domain_name == 'Prov_BsAs_Saladillo_cerca':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -35.8, centerlon = -59.7, radius = 50)

    elif domain_name == 'Prov_BsAs_bigger':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -36.0, centerlon = -61.0, radius = 450)

    elif domain_name == 'Prov_BsAs_Saladillo_cerca':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -35.8, centerlon = -59.7, radius = 50)

    elif domain_name == 'Entre_Rios':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -32.2, centerlon = -59.7, radius = 200)

    elif domain_name == 'Radar_Termas_de_Río_Ondo':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -27.5, centerlon = -64.93, radius = 270)

    elif domain_name == 'Rosario':
        domain = dict(lat_max = -32.5,\
                lon_min = -61.5, lon_max = -59.5,\
                      lat_min = -34, name = domain_name)

    elif domain_name == 'Humedales_Rosario':
        domain = dict(lat_max = -32.0,\
                lon_min = -61.5, lon_max = -58.5,\
                      lat_min = -34.5, name = domain_name)

    elif domain_name == 'Humedales_Rio_de_la_Plata':
        domain = dict(lat_max = -32.0,\
                lon_min = -60.0, lon_max = -57.0,\
                      lat_min = -34.5, name = domain_name)

    elif domain_name == 'Sierras_Cordobesas':
        domain = dict(lat_max = -30.0,\
                lon_min = -66.4, lon_max = -62.8,\
                      lat_min = -33.1, name = domain_name)

    elif domain_name == 'Sierras_Cordobesas2':
        domain = dict(lat_max = -30.4,\
                lon_min = -66.4, lon_max = -62.8,\
                      lat_min = -33.5, name = domain_name)

    elif domain_name == 'Sierras_Cordobesas_Norte':
        domain = dict(lat_max = -30.4,\
                lon_min = -65.4, lon_max = -63.5,\
                      lat_min = -32.0, name = domain_name)

    elif domain_name == 'Mendoza_Norte':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -33.0, centerlon = -69.0, radius = 100)

    elif domain_name == 'Mendoza_Norte2':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -33.2, centerlon = -68.5, radius = 90)

    elif domain_name == 'Mendoza_San_Rafael':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -34.6, centerlon = -68.2, radius = 200)

    elif domain_name == 'Mendoza_Suroeste':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -35.0, centerlon = -68.7, radius = 80)

    elif domain_name == 'Formosa_Sur':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -27.0, centerlon = -61.0, radius = 200)

    elif domain_name == 'San_Luis_grande':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -34.25, centerlon = -66.0, radius = 400)

    elif domain_name == 'San_Luis_Sur_Cordoba':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -34.5, centerlon = -65.5, radius = 110)

    elif domain_name == 'San_Luis_Sur_Cordoba_cerca':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -34.7, centerlon = -65.4, radius = 70)

    elif domain_name == 'Tripolis_Misrata':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 32.6, centerlon = 14.2, radius = 350)

    elif domain_name == 'Brisbane':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = -27.7, centerlon = 153.1, radius = 400)

    elif domain_name == 'Philippines_North':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 14.3, centerlon = 123.2, radius = 900)

    elif domain_name == 'Philippines_North2':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 15.2, centerlon = 121.4, radius = 900)

    elif domain_name == 'Philippines_North3':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 15.2, centerlon = 119.1, radius = 900)

    elif domain_name == 'Philippines_Sea_East':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 14.8, centerlon = 125.4, radius = 900)

    elif domain_name == 'Philippines_Sea_East2':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 13.7, centerlon = 128.1, radius = 900)

    elif domain_name == 'Philippines_Sea_East3':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 12.1, centerlon = 129.5, radius = 900)

    elif domain_name == 'Philippines_Sea_West':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 15.1, centerlon = 118.3, radius = 900)

    elif domain_name == 'TC_Iota_6':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 13.5, centerlon = -85.0, radius = 600)

    elif domain_name == 'TC_Theta_2':
        domain =   dict(name = domain_name, plot_width = 800, projection = 'Hammer', limits_type = 'radius',
                        centerlat = 32.4, centerlon = -20.0, radius = 900)

    else:
        print('domain unknown:', domain_name)
        exit()

    return domain

    #domain = dict(lat_max = 55,\
    #        lon_min = 2, lon_max = 16,\
    #              lat_min = 45, name = 'Central_Europe')

    #domain = dict(lat_max = 50,\
    #        lon_min = 8, lon_max = 13,\
    #              lat_min = 46.5, name = 'SBayern_Austria')

    #domain = dict(lat_max = 46,\
    #        lon_min = -10, lon_max = 4,\
    #              lat_min = 35.5, name = 'Spain')

    #domain = dict(lat_max = -13,\
    #        lon_min = -78, lon_max = -55,\
    #              lat_min = -57, name = 'Atacama+Argentina')

    #domain = dict(lat_max = -30,\
    #        lon_min = -70, lon_max = -55,\
    #              lat_min = -43, name = 'Argentina_Central_Este')

    #domain = dict(lat_max = -27.2,\
    #        lon_min = -59.4, lon_max = -55.5,\
    #              lat_min = -30.6, name = 'Corrientes')

    #domain = dict(lat_max = -32,\
    #        lon_min = -67, lon_max = -55,\
    #                lat_min = -40, name = 'Prov_BsAs_bigger')

    #domain = dict(lat_max = -36.0,\
    #        lon_min = -67.4, lon_max = -62.9,\
    #                lat_min = -39.6, name = 'Tormentas_La_Pampa')

    #domain = dict(lat_max = -33.1,\
    #        lon_min = -61, lon_max = -58,\
    #                lat_min = -35.6, name = 'Tormentas_BsAs')

    #domain = dict(lat_max = -35.2,\
    #        lon_min = -62, lon_max = -59,\
    #                lat_min = -37.6, name = 'Tormentas_Interior')

    #domain = dict(lat_max = -35.6,\
    #        lon_min = -58.8, lon_max = -56.8,\
    #                lat_min = -37.2, name = 'Tormentas_BsAs_Este')

    #domain = dict(lat_max = -32.6,\
    #        lon_min = -61.5, lon_max = -58.5,\
    #              lat_min = -35.1, name = 'Tormentas_BsAs_Norte')

    #domain = dict(lat_max = -32.5,\
    #        lon_min = -61.5, lon_max = -59.5,\
    #              lat_min = -34, name = 'Rosario')

    #domain = dict(lat_max = -32.0,\
    #        lon_min = -61.5, lon_max = -58.5,\
    #              lat_min = -34.5, name = 'Humedales_Rosario')

    #domain = dict(lat_max = -32.7,\
    #        lon_min = -61.0, lon_max = -60.0,\
    #              lat_min = -33.5, name = 'Rosario_cerca')

    #domain = dict(lat_max = -31.0,\
    #        lon_min = -61.5, lon_max = -59.5,\
    #              lat_min = -32.5, name = 'Santa_Fe_Capital')

    #domain = dict(lat_max = -32.0,\
    #        lon_min = -61.7, lon_max = -60.5,\
    #              lat_min = -33.5, name = 'Detalle_sur_de_Santa_Fe')

    #domain = dict(lat_max = -32.5,\
    #        lon_min = -61.4, lon_max = -59.0,\
    #                lat_min = -35.5, name = 'Noroeste_Prov_BsAs')

    #domain = dict(lat_max = -33.4,\
    #        lon_min = -61.3, lon_max = -59.8,\
    #                 lat_min = -34.6, name = 'Pergamino')

    #domain = dict(lat_max = -30.0,\
    #        lon_min = -66.4, lon_max = -62.8,\
    #              lat_min = -33.1, name = 'Sierras_Cordobesas')

    #domain = dict(lat_max = -30.4,\
    #        lon_min = -65.4, lon_max = -63.5,\
    #              lat_min = -32.0, name = 'Sierras_Cordobesas_Norte')

    #domain = dict(lat_max = -34.3,\
    #        lon_min = -67.5, lon_max = -64.8,\
    #              lat_min = -36.5, name = 'Sur_San_Luis')

    #domain = dict(lat_max = -34.3,\
    #        lon_min = -67.0, lon_max = -65.5,\
    #              lat_min = -35.1, name = 'Central_San_Luis')

    #domain = dict(lat_max = -26,\
    #        lon_min = -76, lon_max = -64,\
    #              lat_min = -36.5, name = 'Argentina_Central_Oeste')

    #domain = dict(lat_max = -35.0,\
    #        lon_min = -71.0, lon_max = -70.0,\
    #              lat_min = -36.0, name = 'Cordillera_Detalle')

    #domain = dict(lat_max = 25.5,
    #           lon_min = 79, lon_max = 95,
    #                 lat_min = 10, name = 'Bengal_Sea')

    #domain = dict(lat_max = 20.5,
    #           lon_min = 82.5, lon_max = 91,
    #                 lat_min = 12.5, name = 'Cyclone_Amphan')

    #domain = dict(lat_max = 24.5,
    #           lon_min = 83, lon_max = 91.5,
    #                 lat_min = 16.5, name = 'Cyclone_Amphan')
