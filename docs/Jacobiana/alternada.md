# Matriz Jacobiana
## Configuração Alternada
---

- `dimensão 2NBUS x 2NBUS`
	- `NBUS equivale ao número de barras do sistema elétrico em estudo`
- `resíduos de potência ativa e reativa alternando em função do número de barramentos do sistema`
- `resíduos de ângulo de fase e magnitude de tensão alternando em respeito ao posicionamento dos resíduos de potencia ativa e reativa`
- `equações de controle e variáveis de estado novas devem ser adicionadas em duplas à matriz jacobiana, em respeito à relação com os resíduos de potência ativa e potência reativa e suas respectivas variáveis de estado`

$$
	\begin{bmatrix}
		\vdots \\
		\Delta P_k \\
		\Delta Q_k \\
		\vdots \\ 
		\Delta P_m \\
		\Delta Q_m \\
		\vdots \\
		\Delta y^P \\
		\Delta y^Q \\
		\vdots
	\end{bmatrix}
	=
	\begin{bmatrix}
		 & \vdots & \vdots &  & \vdots & \vdots &  & \vdots & \vdots &  \\
		\cdots & \frac{\partial P_k}{\partial\theta_k} & \frac{\partial P_k}{\partial V_k} & \cdots & \frac{\partial P_k}{\partial \theta_m} & \frac{\partial P_k}{\partial V_m} & \cdots & \frac{\partial P_k}{\partial x^P} & \frac{\partial P_k}{\partial x^Q} & \cdots\\
		\cdots & \frac{\partial Q_k}{\partial\theta_k} & \frac{\partial Q_k}{\partial V_k} & \cdots & \frac{\partial Q_k}{\partial \theta_m} & \frac{\partial Q_k}{\partial V_m} & \cdots & \frac{\partial Q_k}{\partial x^P} & \frac{\partial Q_k}{\partial x^Q} & \cdots \\
		 & \vdots & \vdots &  & \vdots & \vdots &  & \vdots & \vdots &  \\
		\cdots & \frac{\partial P_m}{\partial\theta_k} & \frac{\partial P_m}{\partial V_k} & \cdots & \frac{\partial P_m}{\partial \theta_m} & \frac{\partial P_m}{\partial V_m} & \cdots & \frac{\partial P_m}{\partial x^P} & \frac{\partial P_m}{\partial x^Q} & \cdots\\
		\cdots & \frac{\partial Q_m}{\partial\theta_k} & \frac{\partial Q_m}{\partial V_k} & \cdots & \frac{\partial Q_m}{\partial \theta_m} & \frac{\partial Q_m}{\partial V_m} & \cdots & \frac{\partial Q_m}{\partial x^P} & \frac{\partial Q_m}{\partial x^Q} & \cdots \\
		 & \vdots & \vdots &  & \vdots & \vdots &  & \vdots & \vdots &  \\
		\cdots & \frac{\partial y^P}{\partial\theta_k} & \frac{\partial y^P}{\partial V_k} & \cdots & \frac{\partial y^P}{\partial \theta_m} & \frac{\partial y^P}{\partial V_m} & \cdots & \frac{\partial y^P}{\partial x^P} & \frac{\partial y^P}{\partial x^Q} & \cdots\\
		\cdots & \frac{\partial y^Q}{\partial\theta_k} & \frac{\partial y^Q}{\partial V_k} & \cdots & \frac{\partial y^Q}{\partial \theta_m} & \frac{\partial y^Q}{\partial V_m} & \cdots & \frac{\partial y^Q}{\partial x^P} & \frac{\partial y^Q}{\partial x^Q} & \cdots \\
		 & \vdots & \vdots &  & \vdots & \vdots &  & \vdots & \vdots &  \\
	\end{bmatrix}
	\boldsymbol{\cdot}
	\begin{bmatrix}
		\vdots \\
		\Delta\theta_k \\
		\Delta V_k \\
		\vdots \\
		\Delta \theta_m \\
		\Delta V_m \\
		\vdots \\
		\Delta x^P \\
		\Delta x^Q \\
		\vdots
	\end{bmatrix}
$$