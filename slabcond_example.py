import numpy as np 
import matplotlib.pyplot as plt
import slabcond as sbc

#### defining variables specific to this example
cu110 = {'fs0': 12.4181, 'folder': './cu110_example/', 'area0': 161.4083}
cu110_example = {
    'ibrav':62, # bravis lattice index, defined in grids.py 
    'fs0': cu110['fs0'], # Fermi surface energy
    'fsthick': 0.15, # truncation of electronic state energy in [fs0-fsthick, fs0+fsthick]
    'assume_metal': True, # assume this is a metal
    'isibz': True, # use irreducible Brillouin Zone
    'filinfo': cu110['folder']+'scf.out', # standard output of pw.x, with crystal symmetry matrix
    'filpwc': cu110['folder']+'cond.kf302030.out.all', # output glued together from PWCOND
    'bc': (1,1), # left boundary + right boundary
    'area': cu110['area0'], # volume of unit cell
    'spsym': 'noz', # neglect all symmetry with z-mirror symmetry
    'nqg':None, 
    'ngd': [30,20,30], # fine k and q grid for electron and phonon, respectively
    'filvel': cu110['folder']+'tt_geninterp.kc969_kf302030.dat', # electronic energy and group velocity interpolated from wannier
    'fillw': cu110['folder']+'l_qc969_qf302030.dat', # linewidth from EPW
    'filg2m': cu110['folder']+'fort.qc969_qf302030.709', # transition matrix for iterative algorithm 
    }


if __name__ == '__main__':
    #### an example for unconverged Cu film with (110) surface
    ttkw = cu110_example; NORMCX=3.212e7; NORMCY=4.7306e7

    #### conductivity solver for different film thickness (ISBW)
    fig, ax = plt.subplots()
    for ISBW in [40,80,160,400,800,1200,2000,3000,4000]:
        metal1 = sbc.SlabCond(ngd=ttkw['ngd'], filvel=ttkw['filvel'], fs0=ttkw['fs0'], fsthick=ttkw['fsthick'], assume_metal=ttkw['assume_metal'], isibz=ttkw['isibz'], filinfo=ttkw['filinfo'], fillw=ttkw['fillw'], filpwc=ttkw['filpwc'], bc=ttkw['bc'], area=ttkw['area'], ibrav=ttkw['ibrav'], spsym=ttkw['spsym'],
        slabwidth=ISBW,
        )

        #### electric field direction and normalized bulk conductivity
        EDIR = [1,0]; NORMC = NORMCX
        EDIR = [0,1]; NORMC = NORMCY

        #### generate input for PWCOND
        metal1.writer_pwc_in(cu110['folder']+'cond.ke.kz30')
        #### calculate bulk conductivity
        cond, _, _, _ = metal1.get_conductivity(plot=False, area=ttkw['area'])
        print(cond)

        #### main function to obtain conductivity distribution in film, use ax to plot the normalized conductivity
        rz, cond2 = metal1.get_slabcond(nrz=51, edir=EDIR, ax=ax, normz=False, normc=NORMC, kw={'label': f'{ISBW/10:.2e} A'})
        _cond = np.mean(cond2, axis=0)
        print(ISBW, ":\n", (_cond[0,0]+_cond[1,1])/2, ' S/m')
        print(ISBW, ":\n", f'x: {_cond[0,0]:10.4e}  y: {_cond[1,1]:10.4e} S/m')
        print("boundary:\n", f'x: {(cond2[0,0,0]+cond2[-1,0,0])/2:10.4e}  y: {(cond2[0,1,1]+cond2[-1,1,1])/2:10.4e} S/m')


    plt.ylim(0, 1.4)
    plt.xlabel('slab position (A)')
    plt.ylabel('conductivity (1/ohm/m)')

    plt.legend()
    plt.savefig(cu110['folder']+'normalized_conductivity.png')
    plt.show()
    plt.close()