# BRUIT Protocol

**Le canal, pas le slogan.**

TÉMOIN porte le score. BRUIT porte ce que le score a vu : pertes, visibilité, trous ouverts ou fermés. Un CHSH 2.4 à 1 % de pertes n'est pas un CHSH 2.4 à 30 %. CHSH reste sur TÉMOIN. Ce rail n'invente pas un Bell, un photon, ni un labo loophole-free.

Ce dépôt est la version 0. Téléphone + Python. MIT. Voir [INTERDIT.md](INTERDIT.md).

Ce n'est pas TÉMOIN (le score reste sur l'autre rail).
Ce n'est pas QUELLE (l'origine du bit n'est pas un canal).
Ce n'est pas UNFORGE (un sceau de fichier n'est pas une perte).
Ce n'est pas HORIZON (une date n'est pas un trou).
Ce n'est pas un sceau QUANTUM.
Ce rail nomme le canal. Il ne collapse pas MODE. Ce rail ne frappe pas `quantique`.

## Primitive

```
acte TÉMOIN  +  canal  +  trous  →  fiche .bruit.json
```

| Trous | Droit d'écriture |
|---|---|
| `ouverts` | Toujours. Défaut honnête. |
| `fermes` | détection + localité + liberté toutes `fermee` **et** `simule: false`. Sinon : refus. |

Défaut honnête : `trous: ouverts`. Détection / localité / liberté restent `ouverte` sauf déclaration.

`fermes` + `simule: true` : interdit. Un labo logiciel n'est pas loophole-free. Un Job IBM n'est pas une fermeture de trou.

`simule: true` seulement si l'écriture le déclare (`--simule`). Ne pas tamponner `simule` sur un `ouverts` honnête.

La visibilité est un contraste dans [0, 1]. Même classe qu'un CHSH > Tsirelson. > 1 est un mensonge. < 0 est un mensonge. = 1 sans mesure : refus. La visibilité n'est pas un slogan. v0 n'a pas de champ de mesure, donc `visibilite: 1` est refusé. `visibilite` omise, ou dans [0, 1), s'écrit encore (`0.0` est un sans-contraste honnête).

Les ingénieurs DI demandent les pertes. BRUIT répond par écrit.

## Verrous physiques (ce rail)

- BRUIT nomme le canal que TÉMOIN a vu : pertes, visibilité, trous. Un CHSH 2.4 à 1 % de pertes n'est pas un CHSH 2.4 à 30 %. CHSH reste sur TÉMOIN. Ne pas inventer un Bell, un photon, ni un labo loophole-free.
- Défaut honnête : `trous: ouverts`. Toujours. Détection / localité / liberté restent `ouverte` sauf déclaration.
- `trous: fermes` exige détection + localité + liberté toutes `fermee` **et** `simule: false`. Sinon : refus.
- `fermes` + `simule: true` : refus. Un labo logiciel n'est pas loophole-free. Un Job IBM n'est pas une fermeture de trou.
- `simule: true` seulement si l'écriture le déclare (`--simule`). Ne pas tamponner `simule` sur un `ouverts` honnête.
- La visibilité est un contraste dans [0, 1] ; > 1 est un mensonge ; < 0 est un mensonge ; = 1 sans mesure : refus. La visibilité n'est pas un slogan.
- `juger` autorise une fiche qui passe la garde. `flag` : `ouverts` vs `fermes`. Ce rail nomme le canal. Il ne collapse pas MODE. Ne pas frapper `quantique`.
- QUANTUM signe plus tard. Logs hors Git. La fiche JSON n'est pas un sceau QUANTUM.
- Pas UNFORGE, QUELLE, TÉMOIN, ni HORIZON. Pas de token, pas de L1, pas de marketplace « loophole-free », pas d'avis juridique.

Jugement = Carl : `python3 bruit.py ecrire|lire|juger`.

## Comment lancer

```bash
python3 bruit.py ecrire --temoin-id TM-ex
python3 bruit.py ecrire --trous ouverts
python3 bruit.py ecrire --trous fermes --detection fermee --localite fermee --liberte fermee
python3 bruit.py lire examples/ouverts.bruit.json
python3 bruit.py juger examples/ouverts.bruit.json
```

Sans labo : `trous: ouverts`. C'est correct. C'est le terrain.

Verrous physiques (stdlib, sans paquet extra) :

```bash
python3 -m unittest discover -s tests -v
```

## Vérifié vs présumé

Les tests verrouillent les lignes ci-dessous. Rien dans ce dépôt n'est un théorème. Rien ici n'est un sceau QUANTUM. Un merge n'est pas un sceau.

| Affirmation | Statut |
|---|---|
| `ecrire` par défaut → `ouverts` + `simule: false` | **vérifié** par les tests de ce rail |
| `ouverts` toujours, pas tamponné `simule: true` | **vérifié** |
| `fermes` sans un trou fermé : refus | **vérifié** |
| `fermes` + `simule: true` : refus | **vérifié** |
| `visibilite > 1` : refus (un mensonge) | **vérifié** |
| `visibilite < 0` : refus (un mensonge) | **vérifié** |
| `visibilite: 1` sans mesure déclarée : refus | **vérifié** |
| `visibilite` omise ou dans [0, 1) s'écrit (`0.0` honnête) | **vérifié** |
| `juger` sur `ouverts` nomme le terrain, pas `quantique` | **vérifié** |
| la fiche JSON n'est pas un sceau QUANTUM | **vérifié** |
| Bell / photon / labo loophole-free inventé | **refusé** |
| signature QUANTUM | **plus tard** — logs hors Git, pas dans ce dépôt |
| EasyCrypt / couche formelle | **pas ici** |
| frapper `quantique` / collapser MODE | **refusé** |

## Ce que v0 refuse

Voir [INTERDIT.md](INTERDIT.md). En bref :

- écrire `fermes` sans détection + localité + liberté fermées
- écrire `fermes` avec `simule: true`
- tamponner `simule: true` sur un `ouverts` honnête
- un Job IBM comme fermeture de trou
- `visibilite > 1` (un mensonge)
- `visibilite < 0` (un mensonge)
- `visibilite: 1` sans mesure
- inventer un Bell, un photon, ou un labo loophole-free
- un token, un L1, un marketplace « loophole-free »
- frapper `quantique` sur ce rail
- collapser MODE depuis BRUIT

Mentir est le seul bug. Le défaut est `ouverts`. C'est le terrain.

## Famille

| Rail | Question |
|---|---|
| [FIGURE](https://github.com/carllaliberte/figure-protocol) | qui |
| [SITUS](https://github.com/carllaliberte/situs-protocol) | où |
| [UNFORGE](https://github.com/carllaliberte/unforge-check) | quoi |
| [QUELLE](https://github.com/carllaliberte/quelle) | d'où le bit |
| [TÉMOIN](https://github.com/carllaliberte/temoin-protocol) | avec quelle force |
| [BRUIT](https://github.com/carllaliberte/bruit-protocol) | ce que le score a vu |
| [HORIZON](https://github.com/carllaliberte/horizon-protocol) | jusqu'à quand le sceau tient |
| [EPSILON](https://github.com/carllaliberte/epsilon-protocol) | avec quel ε |
| [MODE](https://github.com/carllaliberte/mode-protocol) | le collapse des quatre |

MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe **plus tard**. Les logs restent hors Git. Ce dépôt n'est pas un sceau QUANTUM.

## Fichiers

- [`INTERDIT.md`](INTERDIT.md) — ce qu'on ne prétend pas
- [`JUGE.md`](JUGE.md) — ce rail nomme le canal, ne frappe pas `quantique`
- [`schema/bruit.v0.json`](schema/bruit.v0.json)
- [`bruit.py`](bruit.py) — `python3 bruit.py ecrire` / `lire` / `juger`
- [`examples/ouverts.bruit.json`](examples/ouverts.bruit.json) — défaut honnête
- [`tests/test_physics_locks.py`](tests/test_physics_locks.py) — verrous physiques
- [`.github/workflows/physics.yml`](.github/workflows/physics.yml) — CI des tests
