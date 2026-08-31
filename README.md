# BRUIT Protocol

**Le canal, pas le slogan.**

TÉMOIN porte le score. BRUIT porte ce que le score a vu : pertes, visibilité, trous ouverts ou fermés. Un CHSH 2.4 à 1 % de pertes n'est pas un CHSH 2.4 à 30 %.

Version 0. Téléphone + gratuit. MIT. Voir [INTERDIT.md](INTERDIT.md).

## Primitive

```
acte TÉMOIN  +  canal  +  trous  →  fiche .bruit.json
```

Défaut honnête : `trous: ouverts`. `fermes` exige détection + localité + liberté fermées et `simule: false`.

```bash
python3 bruit.py ecrire --temoin-id TM-ex
python3 bruit.py juger examples/ouverts.bruit.json
```

Les ingénieurs DI demandent les losses. BRUIT répond par écrit.
