import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

BOUNDS = 1024
FILTER_SIGMA = 12
FRAMES = 30
#np.random.seed(2)

class SimpleParticles():
    ''' Creates a grid filled with particles an a force field with gaussian blur applied to it
    '''
    def __init__(self, bounds, filter_sigma):
        self.particleForceX_unblurred = np.random.random(size=[bounds,bounds])
        self.particleForceX = gaussian_filter(self.particleForceX_unblurred, sigma=filter_sigma)
        self.particleForceY_unblurred = np.random.random(size=[bounds,bounds])
        self.particleForceY = gaussian_filter(self.particleForceY_unblurred, sigma=filter_sigma)
        self.particles = (np.random.random(size=[bounds,bounds]) - 0.4).round()
        
        self.bounds = bounds
        self.filter_sigma = filter_sigma

    def change_force_field(self):
        # for x, particleRow in enumerate(self.particleForceX_unblurred):
        #     for y, particle in enumerate(particleRow):
        #         particle = 1 - particle
        # self.particleForceX = gaussian_filter(self.particleForceX_unblurred, sigma=FILTER_SIGMA)
        # with np.nditer(self.particleForceY_unblurred, op_flags=['readwrite']) as it:
        #     for y in it:
        #         y[...] = 1 - y
        # self.particleForceY = gaussian_filter(self.particleForceY_unblurred, sigma=FILTER_SIGMA)
        self.particleForceX_unblurred = np.random.random(size=[BOUNDS,BOUNDS])
        self.particleForceX = gaussian_filter(self.particleForceX_unblurred, sigma=FILTER_SIGMA)
        self.particleForceY_unblurred = np.random.random(size=[BOUNDS,BOUNDS])
        self.particleForceY = gaussian_filter(self.particleForceY_unblurred, sigma=FILTER_SIGMA)

    def move_particle(self, x, y, recursion=False):
        ''' Moves a particle according to the force exhibited by the force field. 
            If the destination is not free the function gets called recursively and "pushes" the particles forward along the force grid.
            particle values:
                * 1 -> normal value, not changed since last frame was rendered
                * 1.2 -> value once the particle has changed position
                * 1.3 -> value for loops within the system, no movement for this particles 
        '''
        vector = self.get_force_vector(x, y)
        particle_dest = [x + vector[0], y + vector[1]]
        if particle_dest[0] > BOUNDS - 1:
            particle_dest[0] -= BOUNDS
        if particle_dest[1] > BOUNDS - 1:
            particle_dest[1] -= BOUNDS

        particle_dest_value = self.particles[particle_dest[0], particle_dest[1]]
        
        if particle_dest_value == 1.2:
            self.particles[x, y] = 1.2
            return False
    
        if particle_dest_value == 1 or particle_dest_value == 1.3:
            self.particles[x, y] = 1.2
            if self.move_particle(particle_dest[0], particle_dest[1], True) is False:
                self.particles[x, y] = 1.2
                return False

        self.particles[x, y] = 0
        self.particles[particle_dest[0], particle_dest[1]] = 1.2 if recursion else 1.3

    def get_force_vector(self, x, y):
        ''' Calculates the force vector based on the force grid.
        '''
        vector = [0, 0]
        if self.particleForceX[x, y] > 0.5:
            vector[0] = 1
        elif self.particleForceX[x, y] <= 0.5:
            vector[0] = -1
        if self.particleForceY[x, y] > 0.5:
            vector[1] = 1
        elif self.particleForceY[x, y] <= 0.5:
            vector[1] = -1
        return vector

    def render(self, frames):
        ''' Renders the simulation and exports it into "./Export/".
        '''
        for i in range(frames):
            for x, particleRow in enumerate(self.particles):
                for y, particle in enumerate(particleRow):
                    if particle != 0 and particle != 1.3: 
                        self.move_particle(x, y)

            self.particles = self.particles.round()
            plt.imshow(self.particles)
            ax = plt.gca()
            ax.get_yaxis().set_visible(False)
            ax.get_xaxis().set_visible(False)
            plt.savefig(fname=f"./Export/Frame-{i}")
            print(f"Done with Frame {i}")
            if i % 5 == 0:
                self.change_force_field()

if __name__ == "__main__":
    particles = SimpleParticles(BOUNDS, FILTER_SIGMA)
    particles.render(FRAMES)