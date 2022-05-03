import numpy as np
import uuid

class Boid:
    
    _MIN_SPEED = 7
    _MAX_SPEED = 10
    
    _MARGIN = 100  # when boids get within this distance of the edge, turn 
    _TURN = .75
    
    def __init__(self, position, velocity, bound):
        self._id = uuid.uuid4()  # unique identifier for each boid to help identify others in flock
        self.position = (np.array(position)) * bound
        self.velocity = (np.array(velocity) - 0.5) 
        
        self._bound = bound
    
    def move(self):
        """Move the boid's position by (vx, vy)"""
        self._limit_speed()
        self._maintain_bounds()
        self.position += self.velocity
    
    def _next_position(self):
        """Return the next intended position of the boid."""
        return self.position + self.velocity
        
    def _maintain_bounds(self):
        """Keep boid within bounds of the defined area.
        """
        next_pos = self._next_position()
        upper_margin = self._bound - self._MARGIN
        lower_margin = self._MARGIN
        
        # at least one value will be out of bounds
        single_upper = next_pos > upper_margin
        single_lower = next_pos < lower_margin
        
        # both values would be out of bounds
        both_upper_oob = min(single_upper)
        both_lower_oob = min(single_lower)
        
        # vx and vy need to update - both oob in similar fashion
        if both_upper_oob:
            self.velocity -= self._TURN
        elif both_lower_oob:
            self.velocity += self._TURN
        # vx and/or vy need to update 
        # if both, then both oob in opposite fashion
        elif max(single_upper):
            # go ahead and update lower bound as well
            if max(single_lower):
                self.velocity[np.where(single_lower)] += self._TURN
            self.velocity[np.where(single_upper)] -= self._TURN
        # vx or vy need to update
        elif max(single_lower):
            self.velocity[np.where(single_lower)] += self._TURN
            
    def _limit_speed(self):
        """Normalize velocity vector to not violate speed limits."""
        speed = np.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if speed > self._MAX_SPEED:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self._MAX_SPEED
        elif speed < self._MIN_SPEED:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self._MIN_SPEED
        
class Flock:
    BOUND = 500  # upper bound of area to allow boids in
    _VISION = 20  # radius to define a Boid's neighborhood
    _MIN_SEPARATION = 3  # avoid crowding neighbors - this must be <= visibility range
    
    _SEPARATION = 0.05  # factor to move to avoid collision with neighbors
    _COHERENCE = 0.005  # factor to move to average position of neighbors
    _ALIGNMENT = 0.05  # factor to move to average velocity of neighbors
    
    _AVOIDANCE = 0.05  # factor to adjust by to avoid collisions
    
    def __init__(self, size=15):
        self.size=size # upper limit of positions of Boids
        
        self.flock = np.array(
            [Boid(*np.random.rand(2, 2), self.BOUND) for _ in range(size)]
        )
        self.positions = np.array([b.position for b in self.flock])
        self.velocities = np.array([b.velocity for b in self.flock]) 
        
    def move_flock(self):
        """Move each boid within the flock to its new position."""
        neighborhoods, distances = self._get_neighbors()
        
        # Follow the 3 defined rules to induce behavior
        self.steer_toward_flockmates(neighborhoods)
        self.align_with_flockmates(neighborhoods)
        self.avoid_flockmates(neighborhoods, distances)
        
        for boid in self.flock:
            boid.move()
        self.positions = np.array([b.position for b in self.flock])
        self.velocities = np.array([b.velocity for b in self.flock])
    
    def x_positions(self):
        """Return the x-axis position for each boid as a list."""
        return [p[0] for p in self.positions]
    
    def y_positions(self):
        """Return the y-axis position for each boid as a list."""
        return [p[1] for p in self.positions]
    
    def _get_neighbors(self):
        """For each boid, get a list of all other boids within the radius of visibility."""
        neighborhoods = []
        distances = []
        
        for boid, i in zip(self.flock, range(self.size)):
            dist_from_flock =  np.linalg.norm((boid.position - self.positions), axis=1)
            neighbors_mask = dist_from_flock < self._VISION
            not_self_mask = boid != self.flock
            mask = neighbors_mask & not_self_mask
            
            neighbors = self.flock[np.where(mask)]
            dists = dist_from_flock[np.where(mask)]

            distances.append(dists)
            neighborhoods.append(neighbors)
            
        return neighborhoods, distances
            
    def avoid_flockmates(self, neighborhoods, distances):
        """Avoid collisions with other boids in neighborhood."""
        # for each boid, determine if it is within collision range of another 
        # and avoid collision
        for boid, neighbors, dists in zip(self.flock, neighborhoods, distances):
            too_close_mask = dists < self._MIN_SEPARATION
            collisions = neighbors[np.where(too_close_mask)]
            if collisions.size > 0:
                move_by = np.zeros(2)
                for c in collisions:
                    move_by += boid.position - c.position
                # update boid's velocity to avoid others
                boid.velocity += move_by * self._SEPARATION
            else:
                # no imminent collisions
                pass
                       
    def steer_toward_flockmates(self, neighborhoods):
        """Steer toward average position of other boids in neighborhood."""
        # for each boid, steer to center of mass of all local flockmates
        for boid, neighbors in zip(self.flock, neighborhoods):
            avg_position = np.zeros(2)
            if neighbors.size > 0:
                # get average position of all neighboring boids
                for n in neighbors:
                    avg_position += n.position
                avg_position /= len(neighbors)
                # update position to average
                boid.position += (avg_position - boid.position) * self._COHERENCE
            else:
                # no neighbors to steer toward
                pass
    
    def align_with_flockmates(self, neighborhoods):
        """Match velocity of other boids in neighborhood."""
        # for each boid, match velocity to average of all local flockmates
        for boid, neighbors in zip(self.flock, neighborhoods):
            avg_velocity = np.zeros(2)
            if neighbors.size > 0:
                # get the average velocity of all neighboring boids
                for n in neighbors:    
                    avg_velocity += n.velocity
                avg_velocity /= len(neighbors)
                # update velocity to average
                boid.velocity += (avg_velocity - boid.velocity) * self._ALIGNMENT
            else:
                # no neighbors to align velocity with
                pass
