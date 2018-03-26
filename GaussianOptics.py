import math


class GaussianBeam:
    """
    Gaussian beam.

    https://en.wikipedia.org/wiki/Gaussian_beam
    """
    def __init__(self, wl, w_0, z_0=0):
        """

        Parameters
        ----------
        wl : float
            Wavelength of light wave
        w_0 : float
            Beam waist radius at focal position
        z_0 : float
            Position of focal plane, along beam axis. Default = 0.
        """
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
        """Compute beam width at position z along beam axis

        Parameters
        ----------
        z : float
            position (distance from beam waist)

        Returns
        -------
        float
            Beam width at position z

        """
        return self._w_0*math.sqrt(1+((z-self._z_0)/self._rayleigh_length)**2)

    def power_aperture(self, power_in, r, z):
        """Compute power behind aperture with radius r at a distance z from the beam waist.

        Aperture is centered to the beam.
        See https://en.wikipedia.org/wiki/Gaussian_beam#Power_and_intensity

        Parameters
        ----------
        power_in : float
            Power before aperture
        r : float
            Radius of aperture
        z : float
            Position of aperture along beam direction with respect to position of beam waist.

        Returns
        -------
        float
            Power behind aperture (same dimension as power_in)

        """
        return power_in*(1-math.exp(-2*r**2/self.waist_z(z)**2))