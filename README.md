Create a flock of `n` Boids with:
- random position at $ (0, 0)<(x, y)<(L, L) $
- random velocity of $ ((v_x, v_y) $

Then follow the 3 rules laid out in: https://www.red3d.com/cwr/boids/
to induce flocking behavior.
- separation (avoid collision with local flockmates)
- cohesion (steer toward average position of local flockmates)
- alignment (steer toward average heading/velocity of local flockmates)
