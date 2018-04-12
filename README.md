**DOCUMENTATION**

LISTE DES OUTILS:

- DissolveOverlay:     
Ce script permet de fusionner des polygones superposés en tenant
             compte d'un champs numérique en particulier, il est possible de choisir . Ex: Le polygon ayant le champs
             FID le plus grand prend le dessus lors de la fusion.

- PlotHistogram:     
Ce script permet de créer un histogram sur la base d'un champs d'
             une feature class.
- ListField: 
Ce script permet de lister tous les champs d'une feature class

- FillGapsMaximumCommonBorder:
Ce script permet de combler les trous à l'intérieur d'un polygone, ou à l'intersection de plusieurs polygones et d'attribuer au nouveau polygone formée les propriétés du polygone partageant la plus longue frontière commune. Il est possible de fixer (en m^2) la surface maximal des trous devant être comblé.

- DeleteAllFeatureFromDatabase:
Permet de vider une personnal geodatabase, sans la supprimer.

Chaque outil est disponible sous forme de script python ou sous forme de toolbox arcgis.
