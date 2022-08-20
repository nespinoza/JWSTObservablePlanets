import datetime
import numpy as np

import jwst_check

def read_table(filename = 'PS_2022.08.19_21.30.25.csv'):

    names, ras, decs = [], [], []

    fin = open(filename, 'r')

    while True:

        line = fin.readline()

        if line != '':

            if line[0] != '#':

                s = line.split(',')

                names.append(s[0])
                ras.append(np.double(s[78]))
                decs.append(np.double(s[79])) 

        else:

            break
    
    return names, ras, decs

# Extract names, ras and decs:
names, ras, decs = read_table()

# Now check observability with jwstcheck:
fout = open('observable_planets.txt', 'w')
fout.write('# Name \t RA \t DEC\n')

for i in range(len(ras)):

    it_has = jwst_check.hasJWST(ras[i], decs[i], 'NIRSpec', datetime.datetime(2022,8,29,0,0), 14)

    if it_has:

        fout.write('{0:} \t {1:.4f} \t {2:.4f}\n'.format(names[i], ras[i], decs[i]))

fout.close()
