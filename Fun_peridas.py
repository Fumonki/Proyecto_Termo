import numpy as np


class Perdidas:
    def __init__(self, **kwargs):
        #super().__init__()
        self.D =  kwargs.get('D')
        self.Dnom =  kwargs.get('Dnom')
        self.rho =  kwargs.get('rho')
        self.mu =  kwargs.get('mu')
        self.epsilon =  kwargs.get('epsilon')
        self.V_dato =  kwargs.get('V')
        #Inician standar
        self.m_dot = self.V_dato* self.rho * (np.pi * self.D**2)/4  #m_dot = V * rho * A
        #self.V()
        self.Re()


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
        K = (k1/self.Re_dato) + ki*(1 + (kd/((self.Dnom)**0.3)))
        return K * self.V_dato**2/(2*9.81)


    '''Parte branch'''
    def Branch_Converge(self, flujo_entrada, D_entrada): # = K RUN
        vel_entrada = flujo_entrada/(60000*(np.pi * D_entrada**2/4))  #m/s
        y_b = flujo_entrada/ (flujo_entrada + self.m_dot)  #Ver que esten en mismas unidades flujo de entrada y m_dot
        Beta_b = D_entrada/self.D  #D_entrada es diametro de la tuberia a entrar, self_D es de la tuberia original a la que entra líquido

        if Beta_b <= 0.35:
            C = 1
        else:
            if y_b <= 0.35:
                C = 0.9 * (1 - y_b)
            else:
                C = 0.55

        K_b = C * (1 + 1 * (y_b / Beta_b**2)**2 - 2 * (1 - y_b)**2 - 0 * (y_b / Beta_b)**2)

        return self.Perdida_vel(K_b, K_b, vel_entrada)  
        
            
    def Branch_Diverge(self, flujo_salida, D_salida):
        vel_salida = flujo_salida/(60000*(np.pi * D_salida**2/4))  #m/s
        flujo_salida = flujo_salida/60000 * self.rho
        y_b = (self.m_dot)/flujo_salida  #Ver que esten en mismas unidades flujo de entrada y m_dot
        Beta_b = D_salida/self.D  #D_entrada es diametro de la tuberia a entrar, self_D es de la tuberia original a la que entra líquido

        if Beta_b <= 0.4:
            M = 0.4
        else:
            if y_b <= 0.5:
               M = 2*(2*y_b-1)
            else:
                M = 0.3*(2*y_b-1)

        if Beta_b <= 2/3:
            G = 1
            H = 1
        else:
            G = 1+0.3*y_b**2
            H = 0.3

        

        K_b = G*(1 + H * (y_b / Beta_b**2)**2 )
        K_m = M*y_b**2
        return self.Perdida_vel(K_b, K_m, vel_salida) #No retorna la perdida directamente, ya que depende de la velocidad de la rama madre y la rama saliente
    

    def Perdida_vel(self, K_b, K_m, vel_salida):
        self.Kb = K_b
        self.vel_salida = vel_salida
        return K_b * vel_salida**2/(2*9.81) + K_m *self.V_dato**2/(2*9.81)  #Retorna la perdida de la rama madre y la rama saliente, ya que depende de la velocidad de ambas ramas
    
    def Arreglo_ida(self):
        return self.Kb * self.vel_salida**2/(2*9.81)
    
        