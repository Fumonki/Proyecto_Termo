import numpy as np


class Perdidas:
    def __init__(self, **kwargs):
        #super().__init__()
        self.D =  kwargs.get('D')
        self.rho =  kwargs.get('rho')
        self.mu =  kwargs.get('mu')
        self.epsilon =  kwargs.get('epsilon')

        #Inician standar
        self.m_dot = 1
        self.V()

    '''Todo lo de abajo se inicializa con la clase'''
    def V(self):
        self.V_dato  = (self.m_dot/(1000 * self.rho)) * (4/(np.pi*self.D**2))
        self.Re()
        
    def Re(self):
        self.Re_dato = (self.rho * self.D * self.V_dato)/self.mu
        self.f()

    def f(self):
        self.f_dato = 0.25/(np.log((self.epsilon/self.D)/3.7 + (5.74/(self.Re_dato**0.9))))**2
        
    '''Parte perdidas fricción'''
    def lf(self, L):
        return (self.f_dato/self.D) * ((self.V_dato**2)/(2*9.81)) * L


    '''Parte singularidades 3K'''
    def lm(self, k1, ki, kd):
        K = (k1/self.Re_dato) + ki*(1 + (kd/((self.D)**0.3)))
        return K * self.V_dato**2/(2*9.81)

            

#class Perdidas_Singular(Perdidas_Largo):
#    def __init__(self, **kwargs):
#        super().__init__()

    
        