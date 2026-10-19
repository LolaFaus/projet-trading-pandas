# 📈 Trader d'un jour

Vous avez 1000 $ et les cours de l'action Amazon depuis 1997.
Par équipe de 2 ou 3, écrivez la stratégie qui fera fructifier ce capital.

## Les règles du jeu

- vous développez votre stratégie sur les cours **jusqu'à fin 2015**
- à la fin de la séance, on la fera tourner sur une **période tenue secrète** :
  le classement final se fait sur la valeur du portefeuille à la fin de cette période
- chaque achat ou vente coûte **0,1 %** de frais : échanger tous les jours n'est pas gratuit
- deux adversaires à battre (tout le vocabulaire est expliqué en tête du notebook) :
  - le *singe* : chaque jour il achète ou vend, au hasard
  - le *buy & hold* : il achète tout le premier jour et ne touche plus à rien
- interdits :
  - regarder le futur (de toute façon `history` ne le contient pas)
  - coder en dur des dates (« tout vendre le 20 septembre 2008 ») : sur la période secrète ça ne servira à rien
  - modifier `trading.py`

## Le matériel

```
project/
├── projet.ipynb     ← l'énoncé : copiez-le en groupe-N.ipynb et travaillez dedans
├── trading.py       le simulateur (classe Stock)
└── data/Amazon.csv  les cours
```

Copiez `projet.ipynb` en `groupe-N.ipynb` (N = votre numéro de groupe), ouvrez-le et suivez-le dans l'ordre : échauffement (~30 min), prise en main du simulateur, stratégie (~1h).

## Le rendu : via git, uniquement

Le rendu, c'est `project/groupe-N.ipynb` complété, et rien d'autre. Pas de mail, pas de clé USB.

1. une personne par équipe *forke* ce dépôt sur GitHub et le clone
2. copiez `project/projet.ipynb` en `project/groupe-N.ipynb` et travaillez dedans ; n'oubliez pas le nom de l'équipe et ses membres dans la première cellule
3. avant de rendre : **Kernel → Restart & Run All**, le notebook doit s'exécuter de bout en bout sans erreur
4. commitez et poussez :

   ```bash
   git add project/groupe-N.ipynb
   git commit -m "groupe N"
   git push
   ```

5. ouvrez une *pull request* vers ce dépôt, intitulée `groupe N`

Seule la cellule « 4. Le rendu » sera évaluée sur la période secrète : sa première ligne sera modifiée, le reste du notebook tournera tel quel.
Un notebook qui plante n'est pas classé.
