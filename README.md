# Boutique en ligne

# Contexte

La fraude est un problème majeur de plus en plus préoccupant pour les
institutions financières du monde entier. Les criminels utilisent une grande variété de
méthodes pour attaquer des organisations comme la BNP Paribas, quels que soient
les systèmes, les canaux, les process ou les produits.
Le développement de méthodes de détection de la fraude est stratégique et essentiel
pour les établissements bancaires. Les fraudeurs s'avèrent toujours très créatifs et
ingénieux pour normaliser leurs comportements et les rendre difficilement identifiables.
Une contrainte s'ajoute à cette problématique, la faible occurrence de la fraude dans
la population.
Lien du challenge : https://challengedata.ens.fr/challenges/104

# Application

Afin de simuler une utilisation pratique de notre modèle de détection de fraude,
j’ai créé une application Flask qui sera relié à notre base de données SQL. Les
informations de l’utilisateur et ses commandes seront stockées dans la base puis traité
pour calculer la probabilité de fraude sur chaque commande.
