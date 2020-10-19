import numpy as np
import datetime
import matplotlib.pyplot as plt

from exoctk.contam_visibility import visibilityPA as vpa

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
        if delta[i].days>0 and delta[i].days<days_end:
            ok = True
            break
    return ok
