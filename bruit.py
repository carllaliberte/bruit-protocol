#!/usr/bin/env python3
"""BRUIT v0 — écrire / lire / juger le canal. Pas de trou fermé inventé."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

FORMAT = "bruit.v0"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _garde(carte: dict) -> None:
    if carte.get("trous") not in ("ouverts", "fermes"):
        raise SystemExit("trous : ouverts | fermes")
    for k in ("detection", "localite", "liberte"):
        if carte.get(k) not in ("ouverte", "fermee"):
            raise SystemExit(k + " : ouverte | fermee")
    vis = carte.get("visibilite")
    if vis is not None and float(vis) == 1:
        raise SystemExit("refus : visibilite = 1 sans mesure. la visibilite n'est pas un slogan")
    if carte["trous"] == "fermes":
        manques = [k for k in ("detection", "localite", "liberte") if carte.get(k) != "fermee"]
        if manques:
            raise SystemExit("refus : trous fermes mais " + ", ".join(manques) + " ouverte")
        if carte.get("simule") is True:
            raise SystemExit("refus : trous fermes + simule. un labo logiciel n'est pas loophole-free")


def ecrire(temoin_id=None, trous="ouverts", detection="ouverte", localite="ouverte", liberte="ouverte", visibilite=None, pertes=None, simule=None, juridiction="QC", langue="fr-CA"):
    trous = (trous or "ouverts").strip().lower()
    if simule is None:
        simule = False
    carte = {
        "format": FORMAT,
        "bruit_id": "BR-" + uuid.uuid4().hex[:12],
        "temoin_id": temoin_id or None,
        "trous": trous,
        "detection": detection,
        "localite": localite,
        "liberte": liberte,
        "visibilite": visibilite,
        "pertes": pertes,
        "simule": bool(simule),
        "juridiction": juridiction,
        "langue": langue,
        "pose_at": _now(),
        "note": "v0 non signée. Logs hors Git.",
    }
    _garde(carte)
    return carte


def lire(chemin: str) -> dict:
    carte = json.loads(Path(chemin).expanduser().read_text(encoding="utf-8"))
    if carte.get("format") != FORMAT:
        raise SystemExit("pas une fiche bruit.v0")
    _garde(carte)
    return carte


def juger(carte: dict) -> dict:
    _garde(carte)
    fermes = carte["trous"] == "fermes"
    return {
        "decision": "allow",
        "flag": "fermes" if fermes else "ouverts",
        "trous": carte["trous"],
        "visibilite": carte.get("visibilite"),
        "pertes": carte.get("pertes"),
        "simule": carte.get("simule"),
        "note": "trois trous fermés déclarés. le canal est borné." if fermes else "trous ouverts. c'est le terrain. cette rail nomme le canal.",
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="bruit")
    sub = p.add_subparsers(dest="cmd", required=True)
    pe = sub.add_parser("ecrire")
    pe.add_argument("--temoin-id", default=None)
    pe.add_argument("--trous", default="ouverts")
    pe.add_argument("--detection", default="ouverte")
    pe.add_argument("--localite", default="ouverte")
    pe.add_argument("--liberte", default="ouverte")
    pe.add_argument("--visibilite", type=float, default=None)
    pe.add_argument("--pertes", type=float, default=None)
    pe.add_argument("--simule", action="store_true", default=False)
    pe.add_argument("--pas-simule", action="store_true", default=False)
    pe.add_argument("--juridiction", default="QC")
    pe.add_argument("--langue", default="fr-CA")
    pe.add_argument("--vers", default="carte.bruit.json")
    pl = sub.add_parser("lire")
    pl.add_argument("fichier")
    pj = sub.add_parser("juger")
    pj.add_argument("fichier")
    args = p.parse_args(argv)
    if args.cmd == "ecrire":
        simule = False if args.pas_simule else (True if args.simule else None)
        carte = ecrire(args.temoin_id, args.trous, args.detection, args.localite, args.liberte, args.visibilite, args.pertes, simule, args.juridiction, args.langue)
        Path(args.vers).write_text(json.dumps(carte, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        out = dict(carte); out["fichier"] = args.vers
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif args.cmd == "lire":
        print(json.dumps(lire(args.fichier), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(juger(lire(args.fichier)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
