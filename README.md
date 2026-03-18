# Particle_filter

## Introduction

Le filtre particulaire que j'ai choisi de créer me sert à localiser un agent physique dans un espace déjà cartographié.\
Cet agent est doté d'un appareil de mesure. Cet appareil donne une mesure de la distance devant l'agent avec une certaine précision.

je cherche à connaitre la postion de l'agent ainsi que son cap.

## Mise en place

Je vais alors supposer un grand nombre $n$ de couples $(position, cap)$ que l'on nommera particules dans mon espace cartographié.\
cet espace cartographié est représenté sous la forme d'un tableau $I \times J$. 

pour chaque particule $i$ :\
les positions $P_i = (P_{ix}, P_{iy})$ et les cap $\vec{c_i} = (c_{ix}, c_{iy})$ sont tirés aléatoirement\
avec $P_{ix} \in [0, I]$ et $P_{iy} \in [0, J]$\
les caps $\vec{c_i}$ ont pour norme $\lVert \vec{c_i} \rVert = 1$

chaque particule est dotée, comme l'agent d'un "appareil de mesure" virtuel sur son nez, lui permettant de donner avec une certaine précison la distance entre sa position et un obstacle dans la direction de son cap. 

à chaque tour, l'agent va effectuer un déplacement et une mesure.\
les déplacements peuvent être des changements de position ou des changements de cap. (rotation sur soi-même).\
chaque particule effectura le même déplacement et mesurera devant elle.

## Mise en jour des probabilités

On pourra donner une vraissemblance de la mesure de chaque particule comme la gaussienne de l'erreur entre la mesure effectuée par l'agent et celle effectuée par la particule. 

$erreur = v - r$

avec $v =$ mesure de la particule 
et $r =$ mesure de l'agent

d'ou la vraissemblance $L$ de la particule : 

$$L = \frac{1}{\sigma \sqrt{2 \pi}} \exp \left( -\frac{erreur^2}{2 \sigma^2} \right)$$

avec plusieurs mesures, on peut avoir : 

$$L = \prod_{k=1}^K \frac{1}{\sigma \sqrt{2 \pi}} \exp \left( -\frac{erreur_k^2}{2 \sigma^2} \right)$$

chaque particule au départ a une equiprobabilité de correctement représenter l'état de l'agent. on peut alors avoir un à priori unifome sur l'ensemble de ces particules. Au départ, chaque particule à une probabilité $\frac{1}{n}$ de bien représenter l'état de l'agent. 

On met alors à jour notre confiance dans la particule $i$ : 

$$\mathbb{P}(i \mid m) = \frac{L_i(m) \mathbb{P}(\ i\ )}{\sum_{i=1}^n L_i(m) \mathbb{P}(\ i\ )}$$

La probabilité que la particule $i$ représente correctement l'agent sachant la mesure $m$ de l'agent est égale à la vraissemblance de la mesure (ou des mesures) $v_i$ par notre à priori sur la particule (d'abord uniforme, puis se met à jour avec les mesures). 

## Rééchantillonnage

Le rééchantillonnage permet de séléctionner et reproduire les particules ayant le mieux représenté l'état de l'agent.\
on sélectionne $n$ particules avec probabilité proportionnelle à leur poids $\mathbb{P}(\ i\ )$, par séléction/rejet, par roulette... 
on modifie les position $P_i$ de ces particules avec :

$$P_i \leftarrow P_i + \epsilon$$ 

et 

$$\vec{c_i} \leftarrow \frac{\vec{c_i} + \epsilon}{\lVert \vec{c_i} + \epsilon \rVert}$$

avec 

$$\epsilon \sim N(0, \sigma^2)$$

parmi ces particules représentant bien l'état de l'agent, on peut encore favoriser celles qui le représente le mieux en adaptant le $\sigma_i$ de notre $\epsilon_i$ en définissant un $\sigma_{max}$ et adapter $\sigma_i$ comme 

$$\sigma_i = \frac{\sigma_{max}}{1 + \exp \left(w\mathbb{P}(\ i\ ) + b \right)}$$

avec $w$ et $b$ correctement choisis pour que la transition entre $\sigma_{max}$ et $0$ se fassent entre $\min{\mathbb{P}(\ i\ )}$ et $\max{\mathbb{P}(\ i\ )}$

à chaque étape de rééchantillonnage, on peut remettre les $\mathbb{P}(\ i\ )$ à $\frac{1}{n}$ et intégrer aléatoirement une petite quantité de particules aléatoires afin d'éviter une dégénérescence. 










