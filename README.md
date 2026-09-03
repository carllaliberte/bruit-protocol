# BRUIT Protocol

**Le canal, pas le slogan.**

TÉMOIN porte le score. BRUIT porte ce que le score a vu : pertes, visibilité, trous ouverts ou fermés. Un CHSH 2.4 à 1 % de pertes n'est pas un CHSH 2.4 à 30 %. CHSH stays on TÉMOIN. This rail does not invent a Bell, a photon, or a loophole-free lab.

This repository is version 0. Phone + Python. MIT. See [INTERDIT.md](INTERDIT.md).

Ce n'est pas TÉMOIN (le score reste sur l'autre rail).
Ce n'est pas QUELLE (l'origine du bit n'est pas un canal).
Ce n'est pas UNFORGE (un sceau de fichier n'est pas une perte).
Ce n'est pas HORIZON (une date n'est pas un trou).
Ce n'est pas un sceau QUANTUM.
This rail names the canal. It does not collapse MODE. This rail does not mint `quantique`.

## Primitive

```
acte TÉMOIN  +  canal  +  trous  →  fiche .bruit.json
```

| Trous | Droit d'écriture |
|---|---|
| `ouverts` | Toujours. Défaut honnête. Always writable. |
| `fermes` | détection + localité + liberté toutes `fermee` **et** `simule: false`. Sinon : refus. |

Honest default: `trous: ouverts`. Detection / localité / liberté stay `ouverte` unless declared.

`fermes` + `simule: true` : interdit. A software lab is not loophole-free. An IBM job is not hole closure.

`simule: true` only if the write claims it (`--simule`). Do not stamp `simule` on default `ouverts`.

Visibility is a contrast in [0, 1]. Same class as CHSH > Tsirelson. > 1 is a lie. < 0 is a lie. = 1 without measure refuses. Visibility is not a slogan. v0 has no measurement field, so `visibilite: 1` is refused. `visibilite` omitted, or in [0, 1), still writes (`0.0` is honest no-contrast).

Les ingénieurs DI demandent les losses. BRUIT répond par écrit.

## Physics locks (this rail)

- BRUIT names the channel TÉMOIN saw: losses, visibility, holes. A CHSH 2.4 at 1% loss is not a CHSH 2.4 at 30%. CHSH stays on TÉMOIN. Do not invent a Bell, a photon, or a loophole-free lab.
- Honest default: `trous: ouverts`. Always writable. Detection / localité / liberté stay `ouverte` unless declared.
- `trous: fermes` requires detection + localité + liberté all `fermee` **and** `simule: false`. Else refuse.
- `fermes` + `simule: true` refuse. A software lab is not loophole-free. An IBM job is not hole closure.
- `simule: true` only if the write claims it (`--simule`). Do not auto-stamp `simule` on default `ouverts`.
- Visibility is a contrast in [0, 1]; > 1 is a lie; < 0 is a lie; = 1 without measure refuses. Visibility is not a slogan.
- `juger` allows a card that passes the garde. Flag `ouverts` vs `fermes`. This rail names the canal. It does not collapse MODE. Do not mint `quantique`.
- QUANTUM signs later. Logs off Git. The JSON card is not a QUANTUM seal.
- Not UNFORGE, QUELLE, TÉMOIN, or HORIZON. No token, L1, marketplace « loophole-free », or legal opinion.

Judgment = Carl: `python3 bruit.py ecrire|lire|juger`.

## How to run

```bash
python3 bruit.py ecrire --temoin-id TM-ex
python3 bruit.py ecrire --trous ouverts
python3 bruit.py ecrire --trous fermes --detection fermee --localite fermee --liberte fermee
python3 bruit.py lire examples/ouverts.bruit.json
python3 bruit.py juger examples/ouverts.bruit.json
```

Sans labo : `trous: ouverts`. C'est correct. C'est le terrain.

Physics locks (stdlib, no extra packages):

```bash
python3 -m unittest discover -s tests -v
```

## Verified vs assumed

Tests lock the rows below. Nothing in this repository is a theorem. Nothing here is a QUANTUM seal. A merge is not a seal.

| Claim | Status |
|---|---|
| default `ecrire` → `ouverts` + `simule: false` | **verified** by tests on this rail |
| `ouverts` always writable, not stamped `simule: true` | **verified** |
| `fermes` missing a hole refused | **verified** |
| `fermes` + `simule: true` refused | **verified** |
| `visibilite > 1` refused (a lie) | **verified** |
| `visibilite < 0` refused (a lie) | **verified** |
| `visibilite: 1` without a declared measurement refused | **verified** |
| `visibilite` omitted or in [0, 1) writes (`0.0` honest) | **verified** |
| `juger` on `ouverts` names the terrain, not `quantique` | **verified** |
| JSON card is not a QUANTUM seal | **verified** |
| invented Bell / photon / loophole-free lab | **refused** |
| QUANTUM signature | **later** — logs off Git, not in this repo |
| EasyCrypt / formal-layer | **not here** |
| mint `quantique` / collapse MODE | **refused** |

## What v0 refuses

See [INTERDIT.md](INTERDIT.md). In short:

- écrire `fermes` sans détection + localité + liberté fermées
- écrire `fermes` avec `simule: true`
- tamponner `simule: true` sur un `ouverts` honnête
- un Job IBM comme fermeture de trou
- `visibilite > 1` (un mensonge)
- `visibilite < 0` (un mensonge)
- `visibilite: 1` sans mesure
- inventer un Bell, un photon, ou un labo loophole-free
- un token, un L1, un marketplace « loophole-free »
- frapper `quantique` sur cette rail
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
- [`JUGE.md`](JUGE.md) — cette rail nomme le canal, ne frappe pas `quantique`
- [`schema/bruit.v0.json`](schema/bruit.v0.json)
- [`bruit.py`](bruit.py) — `python3 bruit.py ecrire` / `lire` / `juger`
- [`examples/ouverts.bruit.json`](examples/ouverts.bruit.json) — défaut honnête
- [`tests/test_physics_locks.py`](tests/test_physics_locks.py) — verrous physiques
- [`.github/workflows/physics.yml`](.github/workflows/physics.yml) — CI des tests
