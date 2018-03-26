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

    @staticmethod
    def fiber_coupling_efficiency(mfd, w_x, w_y=None):
        """Compute coupling efficiency into single-mode fiber for given beam waists
        Note: reflection from the fiber facets are not taken into account. For uncoated facets, the reflection losses
        are 8%.

        Parameters
        ----------
        mfd : float
            Mode field diameter of fiber
        w_x : float
            Beam waist along x-axis
        w_y : float
            Beam waist along y-axis. If None (default) a symmetric beam is assumed.

        Returns
        -------
        float
            Theoretical coupling effiency (0...1)
        """
        if w_y is None:
            w_y = w_x

        eff = 1/(4*(mfd/w_x+w_x/mfd)*(mfd/w_y+w_y/mfd))
        return eff

    def fiber_coupling_efficiency_lens(self, mfd, f, w_in=None):
        """Compute coupling efficiency into single-mode fiber using an ideal lens
        Note: reflection from the fiber facets are not taken into account. For uncoated facets, the reflection losses
        are 8%.

        Parameters
        ----------
        mfd : float
            Mode field diameter of fiber
        f : float
            Focal length of lens infront of fiber
        w_in : float
            Beam waist at position of lens

        Returns
        -------
        float
            Theoretical coupling effiency (0...1)
        """
        if w_in is None:
            w_in = self._w_0

        w_lens = 4*self._wl*f/(math.pi*w_in)
        return self.fiber_coupling_efficiency(mfd, w_lens)
