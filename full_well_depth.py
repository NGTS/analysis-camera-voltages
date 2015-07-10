import matplotlib.pyplot as plt
from astropy.io import fits
import seaborn as sns
import numpy as np
import sqlalchemy as sa
import os
from contextlib import contextmanager
import bz2

engine = sa.create_engine('mysql+pymysql://sw@ngtsdb/ngts_ops')

def assess_sky_background_levels():
    files = ['data/122.fits', 'data/168.fits', 'data/223.fits']
    fig1, axis1 = plt.subplots()
    fig2, axis2 = plt.subplots()
    colours = sns.color_palette(n_colors=10)
    for fname, colour in zip(files, colours):
        with fits.open(fname) as infile:
            imagelist = infile['imagelist'].data
        mjd = imagelist['mjd']
        airmass = imagelist['airmass']
        sky = imagelist['skylevel']

        axis1.scatter(airmass, sky, c=mjd, label=fname, color=colour)
        axis2.plot(mjd % 1, sky, '.', label=fname, color=colour)

    axis1.set(xlabel='Airmass', ylabel='Sky level / counts',
            xlim=(1.05, 1.2), ylim=(140, 230))
    for axis in [axis1, axis2]:
        axis.grid(True)
        axis.legend(loc='best')

    optimal_airmass = 1.12
    axis1.axvline(optimal_airmass, ls='--', color='k', alpha=0.8)

    tax = axis2.twinx()
    tax.plot(mjd % 1, airmass, '-')
    tax.set(ylabel='Airmass')
    tax.axhline(optimal_airmass, ls='--', color='k', alpha=0.8)

    for fig in [fig1, fig2]:
        fig.tight_layout()

    return optimal_airmass


def get_image_ids(optimal_airmass):
    out = {}
    files = ['data/122.fits', 'data/168.fits', 'data/223.fits']
    for fname in files:
        with fits.open(fname) as infile:
            imagelist = infile['imagelist'].data

        mjd, airmass, image_id = (imagelist['mjd'], imagelist['airmass'],
                imagelist['image_id'])

        delta = np.abs(airmass - optimal_airmass)
        n_to_pick = 1250
        ind = delta[:n_to_pick].argmin()
        out[fname] = {
                'image_id': image_id[:n_to_pick][ind],
                }

    return out


@contextmanager
def open_file(fname):
    if '.bz2' in fname:
        with bz2.BZ2File(fname) as uncompressed:
            with fits.open(uncompressed) as infile:
                yield infile
    else:
        with fits.open(fname) as infile:
            yield infile



def fetch_image_data(image_id):
    r = engine.execute('''
    select action_id from raw_image_list
    where image_id = %s''', (int(image_id), ))
    action_id = r.first()[0]

    data_root = '/ngts/testdata/paranal'
    path = os.path.join(data_root, 'action{}_observeField'.format(action_id),
            'IMAGE{}.fits.bz2'.format(image_id))

    with open_file(path) as infile:
        return infile[0].data


def image_histogram(image_ids, axis, bins):
    for key in sorted(image_ids.keys()):
        data = image_ids[key]['raw_image_data']
        height, _ = np.histogram(data, bins)

        axis.plot(bins[:-1], height, '-', drawstyle='steps-post', lw=2,
                label=image_ids[key]['label'])
    axis.legend(loc='best')

    axis.set(xscale='log', yscale='log', xlabel='Pixel value', ylabel='Number')
    axis.grid(True, which='both')
