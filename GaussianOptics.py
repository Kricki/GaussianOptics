import math


class GaussianBeam:
    """
    Gaussian beam.

    All units are given in SI units.

    Class attributes:
        :param double wl: Wavelength (in m)
        :param double w_0: Beam waist at focal position (in m)
        :param z_0: Position of focal plane, along beam axis (in m). Default = 0.

    """
    def __init__(self, wl, w_0, z_0=0):
        self._wl = wl
        self._w_0 = w_0
        self._z_0 = z_0

        self._rayleigh_length = self.compute_rayleigh_length()

    @property
    def wl(self):
        return self._wl

    @wl.setter
    def wl(self, val):
        self._wl = val
        self._rayleigh_length = self.compute_rayleigh_length()

    @property
    def w_0(self):
        return self._w_0

    @w_0.setter
    def w_0(self, val):
        self._w_0 = val
        self._rayleigh_length = self.compute_rayleigh_length()

    @property
    def z_0(self):
        return self._z_0

    @z_0.setter
    def z_0(self, val):
        self._z_0 = val
        self._rayleigh_length = self.compute_rayleigh_length()

    @property
    def rayleigh_length(self):
        return self._rayleigh_length

    def compute_rayleigh_length(self):
        """
        Compute the Rayleigh length
        """
        return math.pi*self._w_0**2/self._wl

    def waist_z(self, z):
        """
        Compute beam width at position z.
        :param float z: Position (distance from beam waist)
        :return: Beam width at position z.
        """
        return self._w_0*math.sqrt(1+((z-self._z_0)/self._rayleigh_length)**2)

    def power_aperture(self, power_in, r, z):
        """
        Compute power behind aperture with radius r at a distance z from the beam waist.
        Aperture is centered to the beam.

        See https://en.wikipedia.org/wiki/Gaussian_beam#Power_and_intensity

        :param float power_in: Power before aperture
        :param float r: Radius of aperture
        :param float z: Position of aperture along beam direction with respect to position of beam waist.
        :return: Power behind aperture (in W)
        """
        return power_in*(1-math.exp(-2*r**2/self.waist_z(z)**2))