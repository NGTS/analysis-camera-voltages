from astropy.io import fits
from functools import lru_cache
import numpy as np
from contextlib import contextmanager
import matplotlib.pyplot as plt
from scipy import stats
from collections import namedtuple

@contextmanager
def subplots(*args, **kwargs):
    fig, axes = plt.subplots(*args, **kwargs)
    yield (fig, axes)
    fig.tight_layout()

class FluxDifference(namedtuple('FluxDifferenceBase', ['mjd', 'flux'])):
    def plot_lc(self, axis, *args, **kwargs):
        normalise = kwargs.pop('normalise', None)
        if normalise is not None:
            axis.plot(self.mjd % 1, self.flux / np.median(self.flux), '.',
                    *args, **kwargs)
        else:
            axis.plot(self.mjd % 1, self.flux, '.', *args, **kwargs)

class Star(object):

    def __init__(self, mjd, flux, x, y, meta):
        self.mjd = mjd
        self.flux = flux
        self.x = x
        self.y = y
        self.meta = meta

    def normalise(self):
        return self.__class__(self.mjd, self.flux / np.median(self.flux),
                              self.x, self.y, self.meta)

    def plot_lc(self, axis, *args, **kwargs):
        normalise = kwargs.pop('normalise', None)
        if normalise is not None:
            new = self.normalise()
            axis.plot(new.mjd % 1, new.flux, '.', *args, **kwargs)
        else:
            axis.plot(self.mjd % 1, self.flux, '.', *args, **kwargs)

    def binned(self, bins):
        '''
        Bin up by the bins given. The imagelist will no longer make any sense.
        '''
        med_flux, _, _ = stats.binned_statistic(self.mjd % 1, self.flux,
                bins=bins, statistic='median')
        med_mjd, _, _ = stats.binned_statistic(self.mjd % 1, self.mjd % 1,
                bins=bins, statistic='median')
        return self.__class__(med_mjd, med_flux, self.x, self.y, self.meta)


    def __sub__(self, other):
        return FluxDifference(self.mjd, self.flux - other.flux)

    def __truediv__(self, other):
        return FluxDifference(self.mjd, self.flux / other.flux)



class Fits(object):

    def __init__(self, flux, catalogue, imagelist, ccdx, ccdy):
        self.flux = flux
        self.catalogue = catalogue
        self.imagelist = imagelist
        self.ccdx = ccdx
        self.ccdy = ccdy

    @property
    def med_flux(self):
        return np.median(self.flux, axis=1)

    @property
    def frms(self):
        return np.std(self.flux, axis=1) / self.med_flux

    @classmethod
    def from_file(cls, fname):
        with fits.open(fname) as infile:
            flux = infile['flux'].data
            catalogue = infile['catalogue'].data
            imagelist = infile['imagelist'].data
            n_images = len(imagelist)
            ccdx = infile['ccdx'].section[:, n_images // 2]
            ccdy = infile['ccdy'].section[:, n_images // 2]

            return cls(flux, catalogue, imagelist, ccdx, ccdy)

    def plot_frms(self, axis):
        axis.loglog(self.med_flux, self.frms, '.', ms=5)

    def flux_ind(self, *args):
        return self._data_ind('med_flux', *args)

    def frms_ind(self, *args):
        return self._data_ind('frms', *args)

    def ccdx_ind(self, *args):
        return self._data_ind('ccdx', *args)

    def ccdy_ind(self, *args):
        return self._data_ind('ccdy', *args)

    def _data_ind(self, param, min_value, max_value):
        data = getattr(self, param)
        return (data >= min_value) & (data <= max_value)

    def filter_by_star_ind(self, ind):
        new = self.__class__(self.flux[ind], self.catalogue[ind],
                             self.imagelist, self.ccdx[ind], self.ccdy[ind])
        return new

    def stars(self, random=False):
        inds = np.arange(self.flux.shape[0])
        if random:
            np.random.shuffle(inds)

        for i in inds:
            meta = {}
            meta.update({
                col.name: self.imagelist[col.name]
                for col in self.imagelist.columns if col.name.lower() != 'tmid'
            })
            meta.update({
                col.name: self.catalogue[col.name][i]
                for col in self.catalogue.columns
            })
            yield Star(self.imagelist['tmid'], self.flux[i], self.ccdx[i],
                       self.ccdy[i], meta)


def iterate_over_lightcurves(target, comparison):
    paired = zip(target.stars(), comparison.stars())
    with subplots(4, 2, sharex=True) as (fig, axes):
        axes = axes.flatten()
        for (stars, axis) in zip(paired, axes):
            yield (stars[0], stars[1], axis)
            axis.grid(True)

