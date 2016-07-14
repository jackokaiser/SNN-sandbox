import nest
import pylab as pl
import numpy as np

'''
parameters
'''

w = 0.5  # coupling strength (pA)
dc_amplitude = 1e2  # amplitude of dc generator (pA)

# neuron parameters
P = {'C_m': 250.,  # capacitance (pF)
     'tau_syn_ex': 0.5,  # synaptic time constant (ms)
     'tau_m': 10.,  # membrane time constant (ms)
     }

# in mV
print 'mean membrane potential caused by DC:', P['tau_m'] / P['C_m'] * dc_amplitude
# The mean effect of the Poisson generator on the membrane potential is tau_m * tau_s / C_m * w * rate
# Thus we can calculate the necessary rate which causes the same mean
# effect as the DC generator
rate = dc_amplitude / w / P['tau_syn_ex'] * 1e3  # 1/s

'''
Create nodes and devices
'''

neuron_dc = nest.Create('iaf_psc_exp', params=P)
neuron_pg = nest.Create('iaf_psc_exp', params=P)
dc = nest.Create('dc_generator', params={'amplitude': dc_amplitude})
pg = nest.Create('poisson_generator', params={'rate': rate})
vm = nest.Create('voltmeter')

'''
Connect network
'''

nest.Connect(dc, neuron_dc)
nest.Connect(pg, neuron_pg, syn_spec={'weight': w})
nest.Connect(vm, neuron_dc)
nest.Connect(vm, neuron_pg)

'''
Simulate
'''

nest.Simulate(100.)

'''
Plotting
'''

# accumulate data
senders = nest.GetStatus(vm)[0]['events']['senders']
times_dc = nest.GetStatus(
    vm)[0]['events']['times'][np.where(senders == neuron_dc)]
vms_dc = nest.GetStatus(vm)[0]['events']['V_m'][np.where(senders == neuron_dc)]
times_pg = nest.GetStatus(
    vm)[0]['events']['times'][np.where(senders == neuron_pg)]
vms_pg = nest.GetStatus(vm)[0]['events']['V_m'][np.where(senders == neuron_pg)]
# plot data
pl.plot(times_dc, vms_dc, label='DC input')
pl.plot(times_pg, vms_pg, label='Poisson input')
pl.legend()
pl.show()
