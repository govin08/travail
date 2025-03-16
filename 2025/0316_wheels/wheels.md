제목 : 
prove or disprove : Do wheels of a car always travel the same distance?

본문 :
> Consider the left wheel and the right wheel of a car (say, front wheels). The distances two wheels travel differ when they turn left or right. But, if the car starts traveling towards the north direction and ends traveling towards the same direction, and if the car doesn't rotate fully, then I suspect that the two distances are always the same.

Look at the picture. I'll use **degree of curvature** instead of curvature or radius of curvature, or DOC. The car (1) goes straight (DOC = 0), (2) turns left (DOC= $\pi/3$), (3) goes straight (DOC=0), (4) turns right (DOC= $-\pi/3$). The two wheels travel the same distance at (1) and (3). The right one travels more in (2) and the left one travels more in (4). But in (2) or (4), the difference between two circular arcs depends only on DOC and the distance between the wheels, which is a constant. So (2) and (4) cancel out and two wheels travel exactly the same distance. That is,

$$\delta d = d_1-d_2=r_1\theta-r_2\theta=(r_1-r_2)\theta$$

only depends on $r_1-r_2$ and $\theta$

But it's just the trivial case when the curvature is discontinuous, which is quite unnatural. In fact, the car moves smoothly and the curvature (or the DOC) changes continuously, and I cannot think of the blue and red curves as a combination of circular arcs and line segments.

So the answer is yes in the trivial case shown in the image. But how can I verify that it is still affirmative in the general case?

