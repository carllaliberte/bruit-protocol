#!/usr/bin/env python3
"""Physics locks for BRUIT v0. Tests, not a theorem. Not a QUANTUM seal."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import bruit  # noqa: E402


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _refus(fn, *args, **kwargs) -> str:
    with unittest.TestCase().assertRaises(SystemExit) as ctx:
        fn(*args, **kwargs)
    return str(ctx.exception)


def _cli(args, cwd=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "bruit.py"), *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
    )


def _fermes_ok(**extra):
    base = dict(
        trous="fermes",
        detection="fermee",
        localite="fermee",
        liberte="fermee",
        simule=False,
    )
    base.update(extra)
    return bruit.ecrire(**base)


class DefaultEcrireIsOuverts(unittest.TestCase):
    def test_ecrire_default_trous_is_ouverts(self):
        carte = bruit.ecrire()
        self.assertEqual(carte["trous"], "ouverts")
        self.assertEqual(carte["format"], "bruit.v0")
        self.assertEqual(carte["detection"], "ouverte")
        self.assertEqual(carte["localite"], "ouverte")
        self.assertEqual(carte["liberte"], "ouverte")
        self.assertIs(carte["simule"], False)

    def test_ecrire_explicit_ouverts_is_ouverts(self):
        carte = bruit.ecrire(trous="ouverts")
        self.assertEqual(carte["trous"], "ouverts")
        self.assertIs(carte["simule"], False)

    def test_cli_ecrire_default_is_ouverts_and_simule_false(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "carte.bruit.json"
            proc = _cli(["ecrire", "--vers", str(dest)], cwd=tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["trous"], "ouverts")
            self.assertIs(out["simule"], False)
            written = json.loads(dest.read_text(encoding="utf-8"))
            self.assertEqual(written["trous"], "ouverts")
            self.assertIs(written["simule"], False)
            self.assertEqual(written["detection"], "ouverte")
            self.assertEqual(written["localite"], "ouverte")
            self.assertEqual(written["liberte"], "ouverte")

    def test_ouverts_is_always_writable(self):
        carte = bruit.ecrire(trous="ouverts")
        self.assertEqual(carte["trous"], "ouverts")
        jugement = bruit.juger(carte)
        self.assertEqual(jugement["decision"], "allow")
        self.assertEqual(jugement["flag"], "ouverts")
        self.assertEqual(jugement["trous"], "ouverts")


class OuvertsIsNotStampedSimule(unittest.TestCase):
    def test_ecrire_ouverts_does_not_stamp_simule_true(self):
        carte = bruit.ecrire()
        self.assertIs(carte["simule"], False)

    def test_cli_ecrire_ouverts_does_not_stamp_simule_true(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "ouverts.bruit.json"
            proc = _cli(["ecrire", "--trous", "ouverts", "--vers", str(dest)], cwd=tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertIs(out["simule"], False)
            written = json.loads(dest.read_text(encoding="utf-8"))
            self.assertIs(written["simule"], False)

    def test_example_ouverts_is_not_stamped_simule(self):
        carte = json.loads((ROOT / "examples" / "ouverts.bruit.json").read_text(encoding="utf-8"))
        self.assertEqual(carte["trous"], "ouverts")
        self.assertIs(carte["simule"], False)

    def test_presented_card_may_claim_simule_if_not_fermes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "ouverts-soft.bruit.json"
            p.write_text(
                json.dumps(
                    {
                        "format": "bruit.v0",
                        "bruit_id": "BR-soft",
                        "temoin_id": "TM-soft",
                        "trous": "ouverts",
                        "detection": "ouverte",
                        "localite": "ouverte",
                        "liberte": "ouverte",
                        "visibilite": None,
                        "pertes": None,
                        "simule": True,
                        "juridiction": "QC",
                        "langue": "fr-CA",
                        "pose_at": "2026-09-03T00:00:00Z",
                        "note": "carte présentée — simule true",
                    }
                ),
                encoding="utf-8",
            )
            carte = bruit.lire(str(p))
            self.assertIs(carte["simule"], True)
            self.assertEqual(carte["trous"], "ouverts")

    def test_cli_simule_flag_is_a_claim_on_ouverts(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "claimed.bruit.json"
            proc = _cli(
                ["ecrire", "--trous", "ouverts", "--simule", "--vers", str(dest)],
                cwd=tmp,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertIs(out["simule"], True)
            self.assertEqual(out["trous"], "ouverts")


class FermesMissingHoleRefuses(unittest.TestCase):
    def test_ecrire_fermes_without_closing_holes_refuses(self):
        msg = _refus(bruit.ecrire, trous="fermes")
        self.assertIn("refus", msg.lower())
        self.assertIn("fermes", msg.lower())

    def test_ecrire_fermes_missing_each_hole_refuses(self):
        for manque in ("detection", "localite", "liberte"):
            kwargs = dict(
                trous="fermes",
                detection="fermee",
                localite="fermee",
                liberte="fermee",
                simule=False,
            )
            kwargs[manque] = "ouverte"
            msg = _refus(bruit.ecrire, **kwargs)
            self.assertIn("refus", msg.lower(), msg=manque)
            self.assertIn(manque, msg.lower(), msg=manque)

    def test_cli_ecrire_fermes_without_holes_refuses(self):
        proc = _cli(["ecrire", "--trous", "fermes"])
        self.assertNotEqual(proc.returncode, 0)
        blob = (proc.stderr + proc.stdout).lower()
        self.assertIn("refus", blob)
        self.assertIn("fermes", blob)

    def test_lire_fermes_missing_a_hole_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "fermes-trou.bruit.json"
            p.write_text(
                json.dumps(
                    {
                        "format": "bruit.v0",
                        "bruit_id": "BR-trou",
                        "temoin_id": "TM-trou",
                        "trous": "fermes",
                        "detection": "fermee",
                        "localite": "ouverte",
                        "liberte": "fermee",
                        "visibilite": 0.8,
                        "pertes": 0.01,
                        "simule": False,
                        "juridiction": "QC",
                        "langue": "fr-CA",
                        "pose_at": "2026-09-03T00:00:00Z",
                    }
                ),
                encoding="utf-8",
            )
            msg = _refus(bruit.lire, str(p))
            self.assertIn("refus", msg.lower())
            self.assertIn("localite", msg.lower())

    def test_fermes_with_all_holes_closed_writes(self):
        carte = _fermes_ok()
        self.assertEqual(carte["trous"], "fermes")
        self.assertEqual(carte["detection"], "fermee")
        self.assertEqual(carte["localite"], "fermee")
        self.assertEqual(carte["liberte"], "fermee")
        self.assertIs(carte["simule"], False)
        jugement = bruit.juger(carte)
        self.assertEqual(jugement["decision"], "allow")
        self.assertEqual(jugement["flag"], "fermes")


class FermesPlusSimuleRefuses(unittest.TestCase):
    def test_ecrire_fermes_plus_simule_refuses(self):
        msg = _refus(
            bruit.ecrire,
            trous="fermes",
            detection="fermee",
            localite="fermee",
            liberte="fermee",
            simule=True,
        )
        self.assertIn("simule", msg.lower())
        self.assertIn("refus", msg.lower())

    def test_cli_fermes_plus_simule_refuses(self):
        proc = _cli(
            [
                "ecrire",
                "--trous",
                "fermes",
                "--detection",
                "fermee",
                "--localite",
                "fermee",
                "--liberte",
                "fermee",
                "--simule",
            ]
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("simule", (proc.stderr + proc.stdout).lower())

    def test_lire_fermes_plus_simule_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "fermes-simule.bruit.json"
            p.write_text(
                json.dumps(
                    {
                        "format": "bruit.v0",
                        "bruit_id": "BR-sim",
                        "temoin_id": "TM-sim",
                        "trous": "fermes",
                        "detection": "fermee",
                        "localite": "fermee",
                        "liberte": "fermee",
                        "visibilite": 0.8,
                        "pertes": 0.01,
                        "simule": True,
                        "juridiction": "QC",
                        "langue": "fr-CA",
                        "pose_at": "2026-09-03T00:00:00Z",
                    }
                ),
                encoding="utf-8",
            )
            msg = _refus(bruit.lire, str(p))
            self.assertIn("simule", msg.lower())
            self.assertIn("refus", msg.lower())


class VisibiliteOneWithoutMeasureRefuses(unittest.TestCase):
    def test_ecrire_visibilite_one_refuses(self):
        msg = _refus(bruit.ecrire, visibilite=1)
        self.assertIn("refus", msg.lower())
        self.assertIn("visibilite", msg.lower())
        self.assertIn("mesure", msg.lower())

    def test_ecrire_visibilite_one_on_fermes_still_refuses(self):
        msg = _refus(
            bruit.ecrire,
            trous="fermes",
            detection="fermee",
            localite="fermee",
            liberte="fermee",
            visibilite=1.0,
            simule=False,
        )
        self.assertIn("refus", msg.lower())
        self.assertIn("visibilite", msg.lower())

    def test_cli_visibilite_one_refuses(self):
        proc = _cli(["ecrire", "--visibilite", "1"])
        self.assertNotEqual(proc.returncode, 0)
        blob = (proc.stderr + proc.stdout).lower()
        self.assertIn("refus", blob)
        self.assertIn("visibilite", blob)

    def test_lire_visibilite_one_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "vis1.bruit.json"
            p.write_text(
                json.dumps(
                    {
                        "format": "bruit.v0",
                        "bruit_id": "BR-vis1",
                        "temoin_id": "TM-vis1",
                        "trous": "ouverts",
                        "detection": "ouverte",
                        "localite": "ouverte",
                        "liberte": "ouverte",
                        "visibilite": 1,
                        "pertes": None,
                        "simule": False,
                        "juridiction": "QC",
                        "langue": "fr-CA",
                        "pose_at": "2026-09-03T00:00:00Z",
                    }
                ),
                encoding="utf-8",
            )
            msg = _refus(bruit.lire, str(p))
            self.assertIn("refus", msg.lower())
            self.assertIn("visibilite", msg.lower())

    def test_visibilite_below_one_may_write(self):
        carte = bruit.ecrire(visibilite=0.99, pertes=0.3)
        self.assertEqual(carte["visibilite"], 0.99)
        self.assertEqual(carte["pertes"], 0.3)
        self.assertEqual(carte["trous"], "ouverts")


class JugerOuvertsIsTerrainNotQuantique(unittest.TestCase):
    def test_juger_ouverts_note_is_terrain_not_quantique(self):
        jugement = bruit.juger(bruit.ecrire())
        self.assertEqual(jugement["decision"], "allow")
        self.assertEqual(jugement["flag"], "ouverts")
        self.assertIn("terrain", jugement["note"].lower())
        self.assertNotIn("quantique", jugement["note"].lower())
        self.assertNotIn("quantum", jugement["note"].lower())

    def test_cli_juger_example_is_terrain_not_quantique(self):
        example = ROOT / "examples" / "ouverts.bruit.json"
        proc = _cli(["juger", str(example)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "allow")
        self.assertEqual(out["flag"], "ouverts")
        self.assertIn("terrain", out["note"].lower())
        self.assertNotIn("quantique", out["note"].lower())
        self.assertNotIn("Imagine", proc.stdout)

    def test_juger_does_not_collapse_mode(self):
        jugement = bruit.juger(bruit.ecrire())
        self.assertNotIn("mode", jugement)
        self.assertNotIn("quantique", jugement)
        self.assertIn(jugement["flag"], ("ouverts", "fermes"))

    def test_juger_fermes_flags_fermes(self):
        jugement = bruit.juger(_fermes_ok())
        self.assertEqual(jugement["decision"], "allow")
        self.assertEqual(jugement["flag"], "fermes")
        self.assertNotIn("quantique", jugement["note"].lower())


class NoQuantumSealInJson(unittest.TestCase):
    def test_ecrire_json_is_not_a_quantum_seal(self):
        dumped = _dump(bruit.ecrire())
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("quantum seal", dumped.lower())
        self.assertNotIn("Quantum Mode ON", dumped)
        self.assertNotIn("quantique", dumped)

    def test_cli_ecrire_json_is_not_a_quantum_seal(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "carte.bruit.json"
            proc = _cli(["ecrire", "--vers", str(dest)], cwd=tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertNotIn("QUANTUM", proc.stdout)
            written = dest.read_text(encoding="utf-8")
            self.assertNotIn("QUANTUM", written)
            self.assertNotIn("quantique", written)
            self.assertNotIn("Imagine", written)

    def test_cli_lire_json_is_not_a_quantum_seal(self):
        example = ROOT / "examples" / "ouverts.bruit.json"
        proc = _cli(["lire", str(example)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["trous"], "ouverts")
        self.assertIs(out["simule"], False)
        self.assertNotIn("QUANTUM", proc.stdout)
        self.assertNotIn("Imagine", proc.stdout)

    def test_cli_juger_json_is_not_a_quantum_seal(self):
        example = ROOT / "examples" / "ouverts.bruit.json"
        proc = _cli(["juger", str(example)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "allow")
        self.assertEqual(out["flag"], "ouverts")
        self.assertNotIn("QUANTUM", proc.stdout)
        self.assertNotIn("Imagine", proc.stdout)

    def test_example_json_is_not_a_quantum_seal(self):
        text = (ROOT / "examples" / "ouverts.bruit.json").read_text(encoding="utf-8")
        self.assertNotIn("QUANTUM", text)
        self.assertNotIn("Imagine", text)
        self.assertNotIn("quantique", text)

    def test_card_does_not_mint_quantique(self):
        carte = bruit.ecrire()
        self.assertNotIn("quantique", carte)
        self.assertNotIn("mode", carte)
        self.assertNotEqual(carte.get("trous"), "quantique")


class ReadmeDoorCopy(unittest.TestCase):
    def test_readme_has_no_imagine_word(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Imagine", text)
        self.assertNotIn("imagine", text)

    def test_readme_does_not_claim_formal_verification(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("formally verified", text)
        self.assertNotIn("formally-verified", text)
        self.assertNotIn("formellement vérifié", text)

    def test_readme_names_the_public_command_and_the_locks(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("`ouverts`", text)
        self.assertIn("`fermes`", text)
        self.assertIn("python3 bruit.py ecrire", text)
        self.assertIn("python3 bruit.py lire", text)
        self.assertIn("python3 bruit.py juger", text)
        self.assertIn("Verified vs assumed", text)
        self.assertIn("**verified**", text)
        self.assertIn("**later**", text)

    def test_readme_says_ouverts_is_honest_and_does_not_mint_quantique(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Honest default", text)
        self.assertIn("`trous: ouverts`", text)
        self.assertIn("does not mint `quantique`", text)
        self.assertIn("does not collapse MODE", text)

    def test_readme_names_simule_and_visibilite_locks(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("simule", text)
        self.assertIn("visibilite", text)
        self.assertIn("--simule", text)

    def test_copy_on_this_rail_has_no_imagine_word(self):
        for rel in ("README.md", "INTERDIT.md", "JUGE.md", "bruit.py"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("Imagine", text, msg=rel)

    def test_interdit_keeps_the_physics(self):
        text = (ROOT / "INTERDIT.md").read_text(encoding="utf-8")
        self.assertIn("ouverts", text)
        self.assertIn("fermes", text)
        self.assertIn("simule", text)
        self.assertIn("Visibility", text)

    def test_juge_does_not_collapse_mode(self):
        text = (ROOT / "JUGE.md").read_text(encoding="utf-8")
        self.assertIn("canal", text)
        self.assertIn("MODE", text)


class NoInventedLab(unittest.TestCase):
    def test_default_card_has_no_closed_holes(self):
        carte = bruit.ecrire()
        self.assertEqual(carte["trous"], "ouverts")
        self.assertEqual(carte["detection"], "ouverte")
        self.assertEqual(carte["localite"], "ouverte")
        self.assertEqual(carte["liberte"], "ouverte")
        dumped = _dump(carte).lower()
        self.assertNotIn("loophole-free", dumped)
        self.assertNotIn("photon", dumped)

    def test_examples_do_not_publish_closed_holes(self):
        examples = list((ROOT / "examples").glob("*.json"))
        self.assertTrue(examples)
        for path in examples:
            carte = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(carte.get("trous"), "ouverts", msg=path.name)
            self.assertIs(carte.get("simule"), False, msg=path.name)
            text = path.read_text(encoding="utf-8").lower()
            self.assertNotIn("loophole", text, msg=path.name)
            self.assertNotIn("photon", text, msg=path.name)

    def test_repo_copy_does_not_claim_a_loophole_free_lab(self):
        for rel in ("README.md", "INTERDIT.md", "examples/ouverts.bruit.json"):
            text = (ROOT / rel).read_text(encoding="utf-8").lower()
            self.assertNotIn("loophole-free experiment", text, msg=rel)
            self.assertNotIn("loophole-free bell test", text, msg=rel)
            self.assertNotIn("nous avons fermé les trous", text, msg=rel)


if __name__ == "__main__":
    unittest.main()
