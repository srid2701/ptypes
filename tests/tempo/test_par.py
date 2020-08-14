import pytest

from pathlib import Path
from ptypes.tempo import PTypePAR


def test_read(datadir):

    testpath = Path.joinpath(datadir, 'test.par')

    par = PTypePAR(testpath)

    assert par.PSRJ== 'J2144-3933'
    assert par.NAME== 'J2144-3933'
    assert par.RAJ == '21:44:12.060404',   4.500e-05
    assert par.DECJ== '-39:33:56.88504',   3.200e-04

    assert pytest.approx(par.ELONG, 314.60)
    assert pytest.approx(par.ELAT, -24.40)
    assert pytest.approx(par.DM, 3.35)
    assert pytest.approx(par.DM_ERR, 1.000e-02)
    assert pytest.approx(par.PEPOCH, 49016.0000)
    assert pytest.approx(par.F0, 0.11751119527)
    assert pytest.approx(par.F0_ERR, 5.000e-11)
    assert pytest.approx(par.F1, -6.85E-18)
    assert pytest.approx(par.F1_ERR, 7.000e-20)
    assert pytest.approx(par.P0, 8.509827491)
    assert pytest.approx(par.P0_ERR, 3.000e-09)
    assert pytest.approx(par.P1, 4.96E-16)
    assert pytest.approx(par.P1_ERR, 5.000e-18)
    assert pytest.approx(par.DIST_DM, 0.29)
    assert pytest.approx(par.DIST_DM1, 0.27)

    assert par.SURVEY == 'pks70'

    assert pytest.approx(par.PMRA, -57.89)
    assert pytest.approx(par.PMRA_ERR, 8.800e-01)
    assert pytest.approx(par.PMDEC, -155.90)
    assert pytest.approx(par.PMDEC_ERR, 5.400e-01)
    assert pytest.approx(par.S400, 16)
    assert pytest.approx(par.S800, 2.2)
    assert pytest.approx(par.S800_ERR, 0.000e+00)
    assert pytest.approx(par.S1400, 0.8)
    assert pytest.approx(par.W50, 16.5)
    assert pytest.approx(par.W10, 65)
    assert pytest.approx(par.W10_ERR, 1.000e+01)
    assert pytest.approx(par.POSEPOCH, 54100.0)
    assert pytest.approx(par.DMEPOCH, 49016.00)
    assert pytest.approx(par.DIST_AMN, 0.15)
    assert pytest.approx(par.DIST_AMX, 0.18)
    assert pytest.approx(par.DIST_A, 0.16)
    assert pytest.approx(par.AGE, 2.72e+08)
    assert pytest.approx(par.RM,-2)
    assert pytest.approx(par.RM_ERR, 1.000e+01)
    assert pytest.approx(par.PX, 6.05)
    assert pytest.approx(par.PX_ERR, 5.600e-01)

    assert par.DATE == 1996

    assert pytest.approx(par.DIST, 0.16)
    assert pytest.approx(par.DIST1, 0.16)
    assert pytest.approx(par.PMERR_PA, -44.503)
    assert pytest.approx(par.P1_I, 4.05e-16)
    assert pytest.approx(par.AGE_I, 3.33e+08)
    assert pytest.approx(par.BSURF_I, 1.88e+12)
    assert pytest.approx(par.EDOT_I, 2.59e+28)
    assert pytest.approx(par.EDOTD2, 1.2e+30)
    assert pytest.approx(par.R_LUM, 0.41)
    assert pytest.approx(par.R_LUM14, 0.02)
    assert pytest.approx(par.PMTOT, 166.3)
    assert pytest.approx(par.PMTOT_ERR, 6.000e-01)
    assert pytest.approx(par.VTRANS, 126.15)
    assert pytest.approx(par.BSURF, 2.08e+12)
    assert pytest.approx(par.B_LC, 3.16e-02)
    assert pytest.approx(par.SI414, 2.39)
    assert pytest.approx(par.EDOT, 3.2e+28)
    assert pytest.approx(par.RAJD, 326.05025)
    assert pytest.approx(par.DECJD, -39.56580)

    assert par.OSURVEY == '000000004000'

    assert pytest.approx(par.DMSINB, -2.55)
    assert pytest.approx(par.GL, 2.794)
    assert pytest.approx(par.GB, -49.466)
    assert pytest.approx(par.XX, 0.01)
    assert pytest.approx(par.YY, 8.40)
    assert pytest.approx(par.ZZ, -0.12)
    assert pytest.approx(par.PML, -139.2)
    assert pytest.approx(par.PML_ERR, 6.000e-01)
    assert pytest.approx(par.PMB, 82.0)
    assert pytest.approx(par.PMB_ERR, 9.000e-01)

    assert par.EPHVER == 2
    assert par.UNITS  == 'TDB'
