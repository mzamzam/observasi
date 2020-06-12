# -*- coding: utf-8 -*-
# diadaptasi dari obsplan.py

import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astroplan import Observer,FixedTarget
from datetime import datetime, timedelta
import pandas as pd
from pytz import timezone
from astroplan.plots import plot_sky
x= datetime.now()
def wita(time_value): #time_value: str '2020-05-10 12:00:00.000'
    time_datetime = datetime.strptime(time_value,'%Y-%m-%d %H:%M:%S.%f')
    time = (time_datetime + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S') #WITA
    return time

longitude = '123d54m35.3160s'   #pusat sains tilong
latitude = '-10d3m53.0784s'     #pusat sains tilong
elevation = 100 * u.m
location = EarthLocation.from_geodetic(longitude, latitude, elevation)
lokasi = Observer(name='Tilong',location=location,timezone=timezone('Asia/Makassar')) # lokasi pengamat

time = Time('2020-06-21') #UTC
midnight = Time(lokasi.midnight(time).iso)
delta_md = np.linspace(-5,5,22) *u.hour
win_time = midnight+delta_md
night = win_time
day = (midnight - 12*u.hour) + delta_md
op = pd.read_csv('op.csv',index_col='nama')
ra = op.ra
dec = op.dec

def objek(nama,ra,dec):
    op = SkyCoord(ra,dec,frame='icrs',unit='deg')
    op_name = FixedTarget(coord=op,name=nama)
    # betelgeus = SkyCoord.from_name('betelgeuse')
    # altaz_frame = lokasi.altaz(time)  # ubah lokasi pengamat ke altaz frame
    # betelgeus_altaz = betelgeus.transform_to(altaz_frame)  # ubah target ke altaz
    altaz = lokasi.altaz(win_time,op)
    terbit = lokasi.target_rise_time(win_time,op)
    transit = lokasi.target_meridian_transit_time(win_time,op)
    terbenam = lokasi.target_set_time(win_time,op)
    return op_name,altaz,terbit,transit,terbenam

# altair = objek('altair',ra.altair,dec.altair)
# deneb = objek('deneb',ra.deneb,dec.deneb)
# vega = objek('vega',ra.vega,dec.vega)
# mirzam = objek('mirzam',ra.mirzam,dec.mirzam)
# castor = objek('castor',ra.castor,dec.castor)
# spica = objek('spica',ra.spica,dec.spica)
# aldebaran = objek('aldebaran',ra.aldebaran,dec.aldebaran)
# alcen = objek('alcen',ra.alcen,dec.alcen)
# betelgeus = objek('betelgeus',ra.betelgeus,dec.betelgeus)

def print_info_matahari(jam): # 0 = kira2 jam 12 siang
    print('====================================')
    print('Lokasi dan waktu pengamatan : {} {}'.format(lokasi.name, wita(win_time[jam].value)))
    print('Apakah sudah malam? {}'.format(lokasi.is_night(win_time[jam])))
    print('Matahari terbit dan terbenam pukul {} dan {}'.format(wita((lokasi.sun_rise_time(win_time[jam]) - 5 * u.minute).iso)[-13:],wita((lokasi.sun_set_time(win_time[jam]) + 5 * u.minute).iso)[-13:]))
    print('Bulan terbit dan terbenam pukul {} dan {}'.format(wita((lokasi.moon_rise_time(win_time[jam]) - 5 * u.minute).iso)[-13:],wita((lokasi.moon_set_time(win_time[jam]) + 5 * u.minute).iso)[-13:]))
    print('Altitude dan Iluminasi bulan {} deg dan {} persen'.format(int(lokasi.moon_altaz(win_time[jam]).alt.value),int(lokasi.moon_illumination(win_time[jam]))))
    print('====================================')
def print_info_objek(nama_objek,jam): # 0 = kira2 jam 12 siang
    print('====================================')
    print('Lokasi dan waktu pengamatan : {} {}'.format(lokasi.name,wita(win_time[jam].value)))
    print('Apakah sudah malam? {}'.format(lokasi.is_night(win_time[jam])))
    print('Apakah {} terlihat? {}'.format(nama_objek[0].name,lokasi.target_is_up(win_time[jam],nama_objek[1][jam])))
    print("Altitude : {0.alt:.4} ".format(nama_objek[1][jam]))
    print("Azimut : {0.az:.4}".format(nama_objek[1][jam]))
    print('Waktu terbit : {}'.format(wita((nama_objek[2][jam]-5*u.minute).iso)[-13:]))
    print('Waktu transit : {}'.format(wita(nama_objek[3][jam].iso)[-13:]))
    print('Waktu tenggelam : {}'.format(wita((nama_objek[4][jam]+5*u.minute).iso)[-13:]))
    print('====================================')

# import matplotlib.dates as mdates
# tanggal = mdates.HourLocator()
# fmt = mdates.DateFormatter('%D')
#
# y = [wita(win_time[i].value) for i in range(len(win_time))]
# airmass = spica[1].secz
# alt = alcen[1].alt
# fig,ax = plt.subplots()
# ax.plot(y,alt,'go-')
# # ax.xaxis.set_major_locator(tanggal)
# # ax.xaxis.set_major_formatter(fmt)
# # plt.plot(y,alt,'go-')
# # plt.xlim(delta_md[0].value,delta_md[-1].value)
# ax.set_ylim(alt.min()-2,alt.max()+2)
# plt.gcf().autofmt_xdate()
# plt.show()

def plot(obj,waktu,nama_waktu): #c/ obj = alcen[0]
    plt.rc('font', size=8)
    plot_sky(obj,lokasi,waktu)
    plt.title('{} Time {}'.format(nama_waktu.capitalize(),(obj.name).capitalize()),size=10)
    # plt.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
    plt.show()
    plt.savefig('{}_{}.png'.format(obj.name,nama_waktu),dpi=600)
def save_to_csv(obj): # c/ obj = alcen
    y = [wita(obj[1][i].obstime.value) for i in range(len(obj[1]))]
    star = [{'UT':obj[1][i].obstime.value,'WITA':y[i],'Alt':obj[1][i].alt.value,'Az':obj[1][i].az.value} for i in range(len(win_time))]
    df = pd.DataFrame(star,columns=['UT','WITA','Alt','Az'])
    df.to_csv('{}_night.csv'.format(obj[0].name),index=False)
    print('file {}_night.csv telah disimpan.'.format(obj[0].name))
"""
from astropy.coordinates import get_sun
from astropy.coordinates import get_moon
plt.plot(delta_midnight_2, sunaltazs_may7_to_8.alt, color='y', label='Sun')
# plt.plot(delta_midnight_2, moonaltazs_may7_to_8.alt, color=[0.75] * 3, ls='--', label='Moon')
# plt.plot(delta_midnight_2, betelgeusaltazs_may7_to_8.alt, label='Betelgeuse')
# plt.plot(delta_midnight_2, vegaaltazs_may7_to_8.alt, label='Vega')
plt.fill_between(delta_midnight_2.to('hr').value, 0, 90,
                 sunaltazs_may7_to_8.alt < -0 * u.deg, color='0.5', zorder=0)
plt.fill_between(delta_midnight_2.to('hr').value, 0, 90,
                 sunaltazs_may7_to_8.alt < -18 * u.deg, color='k', zorder=0)
# plt.colorbar().set_label('Azimuth [deg]')
plt.title("Ketinggian Objek Langit Mei 2020")
plt.legend(loc='upper left')
plt.xlim(-12, 12)
plt.xticks(np.arange(13) * 2 - 12)
plt.ylim(0, 90)
plt.xlabel('Selisih jam dari tengah malam (WITA)')
plt.ylabel('Altitude [deg]')
plt.show()
"""
print('Durasi program berjalan: ', datetime.now() - x)