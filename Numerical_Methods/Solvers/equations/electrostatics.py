import numpy as np
import scipy.constants as phys_const

def find_capacitance_per_length(potential_field:np.ndarray,length:float,charge_enclosed:float):
    capacitance = charge_enclosed/potential_field
    cap_per_length = capacitance/(length)
    return cap_per_length

def find_capacitance_per_length(potential_field:np.ndarray,charge_enclosed:float):
    capacitance = charge_enclosed/potential_field
    return capacitance
def energy(potential_field:np.ndarray=None,E_field:np.ndarray=None, length:float=1.0):
    E = np.mean(E_field)
    qs = E_field*phys_const.epsilon_0
    rho = E * phys_const.epsilon_0
    cap_per_length = find_capacitance_per_length(potential_field=potential_field,length=length,charge_enclosed=rho)
    return 0.5*cap_per_length*potential_field**2

def force(energy,distance):
    return energy/distance