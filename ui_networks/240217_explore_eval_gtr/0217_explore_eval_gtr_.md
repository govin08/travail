

`node_id = '11053'`는 총 4현시로 구성되어 있고, 1현시와 2현시에서 오버랩이 일어난다.

## single ring

<b>`evaluation_green_time_ratio.py`의 368, 369번째 줄</b>

3현시는 오버랩현시에 포함되지 않으므로
$a_3=b_3$
이어야 한다. (단, $a_3$은 A링 3현시의 현시시간.)
그런데
\begin{align*}
a_3&=ag_3+ar_3+ay_3\\
b_3&=bg_3+br_3+by_3
\end{align*}
에서 (단 $ag_3$, $ar_3$, $ay_3$는 각각 A링 3현시의 녹색시간, 적색시간, 황색시간.)
\begin{align*}
ag_3+ar_3+ay_3 &= bg_3+br_3+by_3\\
ag_3 - bg_3 &= -ar_3+br_3 -ay_3+by_3\\
\begin{bmatrix}0\\0\\1\\0\\0\\0\\-1\\0\end{bmatrix}^T
\begin{bmatrix}ag_1\\ag_2\\ag_3\\ag_4\\bg_1\\bg_2\\bg_3\\bg_4\end{bmatrix}
&= (-1)((ar_3+ay_3)-(br_3+by_3))\tag{$*$}
\end{align*}
이어야 한다.
한편
\begin{align*}
\texttt{loss\_lst}
&= \texttt{r\_lst} + \texttt{y_loss\_lst} + \texttt{y\_lst}\\
&=\begin{bmatrix}ar_1\\ar_2\\ar_3\\ar_4\\br_1\\br_2\\br_3\\br_4\end{bmatrix}
+\begin{bmatrix}0.3 \\0.3 \\0.3 \\0.3 \\0.3 \\0.3 \\0.3 \\0.3 \end{bmatrix}
+\begin{bmatrix}ay_1\\ay_2\\ay_3\\ay_4\\by_1\\by_2\\by_3\\by_4\end{bmatrix}
\end{align*}
이다. ($\texttt{y_loss\_lst}$는 편의상 0.3으로 이루어진 벡터로 표현함.)
따라서 식 $(*)$의 우변은
$$
(-1)((ar_3+ay_3)-(br_3+by_3))
=(-1)\begin{bmatrix}0\\0\\1\\0\\0\\0\\-1\\0\end{bmatrix}^T\texttt{loss\_lst}
$$
으로 쓸 수 있고, 따라서 식 $(*)$은 

$$
\begin{bmatrix}0\\0\\1\\0\\0\\0\\-1\\0\end{bmatrix}^T
\begin{bmatrix}ag_1\\ag_2\\ag_3\\ag_4\\bg_1\\bg_2\\bg_3\\bg_4\end{bmatrix}
 = (-1)\begin{bmatrix}0\\0\\1\\0\\0\\0\\-1\\0\end{bmatrix}^T\texttt{loss\_lst}
$$

이다.
A링과 B링의 황색/적색시간이 같으면 ($ar_i=br_i$, $ay_i=by_i$ ; 대부분의 경우에 이것이 성립한다.) 위 식의 우변은 0이다.
이것은 $ag_3=bg_3$이라는 의미이다.

위 식이 `evaluation_green_time_ratio.py`의 368, 369번째 줄의 의미이다.


## dual ring

<b>`evaluation_green_time_ratio.py`의 380, 381번째 줄</b>

1현시와 2현시는 오버랩되므로
$a_1+a_2=b_1+b_2$
이어야 한다.
그러면
\begin{align*}
ag_1+ar_1+ay_1+ag_2+ar_2+ay_2 &= bg_1+br_1+by_1+bg_2+br_2+by_2\\
ag_1 + ag_2 - bg_1 - bg_2 &= -ar_1-ay_1-ar_2-ay_2+br_1+by_1+br_2+by_2\\
\begin{bmatrix}1\\1\\0\\0\\-1\\-1\\0\\0\end{bmatrix}^T
\begin{bmatrix}ag_1\\ag_2\\ag_3\\ag_4\\bg_1\\bg_2\\bg_3\\bg_4\end{bmatrix}
&= (-1)((ar_1+ay_1+ar_2+ay_2)-(br_1+by_1+br_2+by_2))\tag{$**$}
\end{align*}
이어야 한다.
식 $(**)$의 우변은
$$
(-1)((ar_1+ay_1+ar_2+ay_2)-(br_1+by_1+br_2+by_2))
=(-1)\begin{bmatrix}1\\1\\0\\0\\-1\\-1\\0\\0\end{bmatrix}^T\texttt{loss\_lst}
$$
으로 쓸 수 있고, 따라서 식 $(**)$은 

$$
\begin{bmatrix}1\\1\\0\\0\\-1\\-1\\0\\0\end{bmatrix}^T
\begin{bmatrix}ag_1\\ag_2\\ag_3\\ag_4\\bg_1\\bg_2\\bg_3\\bg_4\end{bmatrix}
 = (-1)\begin{bmatrix}1\\1\\0\\0\\-1\\-1\\0\\0\end{bmatrix}^T\texttt{loss\_lst}
$$

이다. 이 식이 `evaluation_green_time_ratio.py`의 380, 381번째 줄의 의미이다.