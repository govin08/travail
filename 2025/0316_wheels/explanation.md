Let $\alpha(s)$ be the location of a trajectory at $s$.
Here, $s$ can be a time or a distance, I don't know yet.

The unit tangent vector $T(s)$ is defined by

$$T(s)=\frac{\alpha'(s)}{||\alpha'(s)||}.$$

Assuming the trajectory moves with unit speed, we have

$$T(s)=\alpha'(s).$$

Note that $s$ menas a time and a distance simulaneously.
The unit normal vector $N(s)$ is defined by

$$N(s)=\frac{T'(s)}{||T'(s)||}$$

The curvature $\kappa(s)$ measures the absolute value of the rate of change of $T(s)$ with respect to the distance(time) $s$;

$$\kappa(s) = \left|\left|\frac{dT}{ds}\right|\right|.$$

We can also write $\kappa(s)=||T'(s)||$.
Here, $\kappa(s)$ is always nonnegative.
To allow for $\kappa(s)$ to have a sign, define $N(s)$ in a different way.
Let $N(s)$ be a unit vector normal to $T(s)$ such that $T(s)$ and $N(s)$ form a positive oriented orthonormal basis.
That is,
$N(s)=\frac{T'(s)}{||T'(s)||}$
if it is turning left and
$N(s)=-\frac{T'(s)}{||T'(s)||}$
if it is turning right.
Defining

$$\kappa(s)=
\begin{cases}
||T'(s)||   &(\text{turning left})\\
-||T'(s)||  &(\text{turning right}),
\end{cases}
$$

we have

$$T'(s) = \kappa(s)N(s),$$

and now $\kappa(s)$ is signed.

Let $\beta_+(s)$ and $\beta_-(s)$ be the positions of the two wheels, respectively.
Let $2\lambda$ be the length of the axle.
We have

$$
\begin{align*}
\beta_+(s)&=\alpha(s)+\lambda N(s)\\
\beta_-(s)&=\alpha(s)-\lambda N(s)
\end{align*}
$$

$$T' = \kappa N$$

---

$0=(T\cdot N)' = T'\cdot N + T\cdot N'=\kappa+T\cdot N'$

$N'=(N'\cdot N)N + (N'\cdot T)T=-\kappa T$
