# Matriz Jacobiana
## Configuração Reduzida
---

- `utiliza o número mínimo de equações algébricas não-lineares para solução do sistema linear de equações de potência`
- `dimensão NPV+2NPQ x NPV+2NPQ`
    - `NPV equivale ao número de barras tipo 'PV' no sistema elétrico em estudo`
    - `NPQ equivale ao número de barras tipo 'PQ' no sistema elétrico em estudo`
- `vetor de resíduos de potência ativa seguido de vetor de potência reativa`
- `vetor de resíduos de ângulo de fase seguido de vetor de magnitude de tensão, em respeito ao posicionamento dos resíduos de potência ativa e reativa`
- `equações de controle e variáveis de estado novas são adicionadas singularmente à matriz jacobiana`

$$
	\begin{bmatrix}
		\vdots \\
		\Delta P_k \\
		\Delta P_m \\
		\vdots \\ 
		\Delta Q_k \\
		\Delta Q_m \\
		\vdots \\
		\Delta y \\
		\vdots
	\end{bmatrix}
	=
	\begin{bmatrix}
		 & \vdots & \vdots &  & \vdots & \vdots &  & \vdots &  \\
		\cdots & \frac{\partial P_k}{\partial\theta_k} & \frac{\partial P_k}{\partial\theta_m} & \cdots & \frac{\partial P_k}{\partial V_k} & \frac{\partial P_k}{\partial V_m} & \cdots & \frac{\partial P_k}{\partial x} & \cdots\\
		\cdots & \frac{\partial P_m}{\partial\theta_k} & \frac{\partial P_m}{\partial\theta_m} & \cdots & \frac{\partial P_m}{\partial V_k} & \frac{\partial P_m}{\partial V_m} & \cdots & \frac{\partial P_m}{\partial x} & \cdots \\
		 & \vdots & \vdots &  & \vdots & \vdots &  & \vdots &  \\
		\cdots & \frac{\partial Q_k}{\partial\theta_k}& \frac{\partial Q_k}{\partial\theta_m} & \cdots & \frac{\partial Q_k}{\partial V_k} & \frac{\partial Q_k}{\partial V_m} & \cdots & \frac{\partial Q_k}{\partial x} & \cdots \\
		\cdots & \frac{\partial Q_m}{\partial\theta_k} & \frac{\partial Q_m}{\partial\theta_m} & \cdots & \frac{\partial Q_m}{\partial V_k} & \frac{\partial Q_m}{\partial V_m} & \cdots & \frac{\partial Q_m}{\partial x} & \cdots \\
		& \vdots & \vdots &  & \vdots & \vdots &  & \vdots &  \\
		\cdots & \frac{\partial y}{\partial\theta_k}& \frac{\partial y}{\partial\theta_m} & \cdots & \frac{\partial y}{\partial V_k} & \frac{\partial y}{\partial V_m} & \cdots & \frac{\partial y}{\partial x} & \cdots \\
		 & \vdots & \vdots &  & \vdots & \vdots &  & \vdots &  \\
	\end{bmatrix}
	\boldsymbol{\cdot}
	\begin{bmatrix}
		\vdots \\
		\Delta\theta_k \\
		\Delta\theta_m \\
		\vdots \\
		\Delta V_k \\
		\Delta V_m \\
		\vdots \\
		\Delta x \\
		\vdots
	\end{bmatrix}
$$