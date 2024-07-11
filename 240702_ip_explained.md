통행배정 알고리즘
- $x_{ij}^k$ : 시작존 $i$에서 도착존 $j$로 가는 $k$번째 경로의 통행량
- $t_{ij}^k$ : 시작존 $i$에서 도착존 $j$로 가는 $k$번째 경로의 실제이동시간
- $f_e$ : 링크 $e$의 링크통행량 추정값
- $\bar f_e$ : 링크 $e$의 링크통행량 참값
- $V_{od}$ : 시작존 $o$에서 도착존 $d$로 가는 통행량 추정값
- $\bar V_{od}$ : 시작존 $o$에서 도착존 $d$로 가는 통행량 참값

다음과 같은 최적화 문제를 풂으로써 각 경로에 대한 통행량 $x_{ij}^k$의 최적값을 산출합니다. 이때 선형계획법(linear programming)을 사용합니다.
특히 이 문제는 $x_{ij}^k$가 정수여야 한다는 제약조건이 더 붙기 때문에 정수계획법(integer programming)이라고 말할 수 있습니다.

최적화문제 : 

$$
\begin{align*}
\text{Minimize}\qquad
&L(x)
=M_0\sum_{(i,j)\in OD}\sum_{k=1}^{n_{ij}}t_{ij}^kx_{ij}^k
+M_1\sum_{e\in E}\left|\bar f_e-f_e\right|
+M_2\sum_{(o,d)\in Z^2}\left|\bar V_{od}-V_{od}\right|
+M_3\sum_{\text{inc},\text{out}}\left|\bar\rho_{\text{inc},\text{out}}-\rho_{\text{inc},\text{out}}\right|\\
\text{subject to}\qquad
&x_{ij}^k\ge0
&&\forall i,j,k
\end{align*}
$$

$$
\begin{align*}
\sum_{(i,j)\in OD}\sum_{k=1}^{n_{ij}}t_{ij}^kx_{ij}^k&\text{ : 실제이동시간의 합}\\
\sum_{(i,j)\in OD}\sum_{e\in E}\left|\bar f_e-f_e\right|&\text{ : 링크통행량 오차의 합}\\
\sum_{(o,d)\in Z^2}\left|\bar V_{od}-V_{od}\right|&\text{ : OD통행량 오차의 합}\\
\sum_{\text{inc},\text{out}}\left|\bar\rho_{\text{inc},\text{out}}-\rho_{\text{inc},\text{out}}\right|&\text{ : 회전교통량 오차의 합}
\end{align*}
$$

행렬식 표현

$$
\begin{align*}
\text{Minimize}\qquad
&L(X)
=c^TX\\
\text{subject to}\qquad
&
AX = b
\end{align*}
$$

$$
\begin{align*}
A=
\begin{bmatrix}
P&D_E&0&0
\\
Q&0&D_S&0
\\
U&0&0&D_H
\end{bmatrix}
,\qquad
b
=
\begin{bmatrix}
\bar f\\
\bar V\\
\bar\rho
\end{bmatrix}
,\qquad
c
=
\begin{bmatrix}
M_0T\\M_1\\M_2\\M_3
\end{bmatrix}
,\qquad
X
=
\begin{bmatrix}
x\\ y\\ z\\ w
\end{bmatrix}
\end{align*}
$$

