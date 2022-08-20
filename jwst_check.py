import os
import numpy as np
import datetime
import matplotlib.pyplot as plt

from exoctk.contam_visibility import visibilityPA as vpa

from astropy.table import Table
import pyvo as vo

def hasJWST(ra, dec, instrument, tstart, days_end):
    """
    This function returns a boolean (True or False) on the question of whether the target object is 
    observable in a given range of time (defined by tstart and days_end). If target is observable in that 
    range, output will be True; False otherwise.

    Inputs
    ------

    ra: RA in degrees of the target

    dec: DEC in degrees of the target

    instrument: JWST instrument (possibilities: 'NIRISS', 'NIRSpec', 'MIRI', 'NIRCam')

    tstart: datetime.datetime object stating the starting date to check. For example, datetime.datetime(2022,8,1,0,0) indicates August 1st, 2022.

    days_end: Days after tstart you want to check. If you wanted to check 30 days after August 1st, 2022 for instance, days_end would be 30.

    """
    pG, pB, dates, vis_plot, table, badPAs = vpa.using_gtvt(str(ra),
                                                            str(dec),
                                                            instrument)

    delta = (table['Gregorian'].data-tstart)
    ok = False

    for i in range(len(delta)):

        if delta[i].days>=0 and delta[i].days<=days_end:

            ok = True

            break

    return ok

def query_exoplanets(constraints = 'tran_flag=1 and pl_orbper<2', output_filename = 'out.txt'):
    """
    Given a set of `constraints` in SQL format, returns the data for all exoplanets from the NASA Exoplanet Archive. Default constraint is to return all exoplanet data for (a) transiting exoplanets and (b) periods less than 2 days.
    """

    service = vo.dal.TAPService("https://exoplanetarchive.ipac.caltech.edu/TAP")

    if not os.path.exists(output_filename):

        # List of column names: https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html
        sql_query = "SELECT pl_name,ra,dec,pl_rade,pl_bmasse,pl_orbper,pl_eqt,pl_dens,pl_trandep,pl_trandur,sy_jmag,sy_tmag,st_teff,st_rad "+\
                    "FROM ps "+\
                    "WHERE "+constraints

        results = service.search(sql_query)

        # Save to table:
        table = results.to_table()
        table.write(output_filename, format = 'ascii')

    else:

        table = Table.read(output_filename, format = 'ascii')

    return table
