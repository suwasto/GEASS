"""Offline acceptance checks against a real HTTP server, with no test dependencies."""

import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal


ROOT = Path(__file__).resolve().parents[1]
CLASSES = {"ABSURD", "INDICATED MARKUP", "SPECIFICATION LOCK", "SPLIT PACKAGE", "NORMAL"}


class ApiAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        cls.base = f"http://127.0.0.1:{port}"
        cls.server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.app:app", "--host", "127.0.0.1", "--port", str(port)],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        cls.addClassCleanup(cls.stop_server)
        for _ in range(100):
            if cls.server.poll() is not None:
                raise RuntimeError("Application exited during startup; run uvicorn directly for diagnostics")
            try:
                cls.request("/api/health")
                return
            except (OSError, urllib.error.URLError):
                time.sleep(0.05)
        raise RuntimeError("Application did not become ready")

    @classmethod
    def stop_server(cls):
        cls.server.terminate()
        try:
            cls.server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            cls.server.kill()
            cls.server.wait(timeout=5)

    @classmethod
    def request(cls, path, body=None):
        data = None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(
            cls.base + path,
            data=data,
            headers={"Content-Type": "application/json"} if body is not None else {},
        )
        try:
            response = urllib.request.urlopen(request, timeout=5)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            content = response.read().decode()
            parsed = json.loads(content) if "application/json" in response.headers.get("Content-Type", "") else content
            return response.status, parsed, response.headers

    def test_http_errors_are_safe_and_parameters_bounded(self):
        for path in (
            "/api/packages?page=0", "/api/packages?page_size=10001",
            "/api/packages?page_size=-1", "/api/packages?page=not-a-number",
            "/api/packages/missing", "/api/tenders/missing", "/api/runs/missing",
        ):
            with self.subTest(path=path):
                status, body, _ = self.request(path)
                self.assertIn(status, (400, 404, 422))
                self.assertNotIn("Traceback", str(body))

    def test_live_run_cannot_be_mistaken_for_fixture_execution(self):
        status, body, _ = self.request("/api/runs", {"mode": "live"})
        self.assertIn(status, (400, 422, 501))
        self.assertNotIn("Traceback", str(body))

    def assert_fixture_provenance(self, value, computed=None):
        envelope = value["provenance"]
        self.assertTrue(envelope["stage"])
        self.assertTrue(envelope["source_id"].startswith("fixture:"))
        self.assertIsNone(envelope["retrieved_at"])
        self.assertTrue(envelope["synthetic"])
        self.assertFalse(envelope["model_asserted"])
        if computed is not None:
            self.assertEqual(envelope["computed"], computed)

    def test_listing_filters_and_paging_are_the_same_public_seam(self):
        status, full, _ = self.request("/api/packages")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(full["total"], 6)
        ids = {row["id_rup"] for row in full["items"]}
        self.assertEqual(len(ids), len(full["items"]))
        for row in full["items"]:
            if row["classification"] is None:
                self.assertEqual(row["evidence_status"], "insufficient_evidence")
                self.assertEqual(row["price_forensics"]["status"], "ungrounded")
            else:
                self.assertIn(row["classification"], CLASSES)
            self.assertTrue(row["classification_reason"])
            self.assertTrue(row["synthetic"])
            self.assert_fixture_provenance(row, False)
        _, first, _ = self.request("/api/packages?page_size=1&page=1")
        _, second, _ = self.request("/api/packages?page_size=1&page=2")
        self.assertEqual(first["total"], full["total"])
        self.assertNotEqual(first["items"][0]["id_rup"], second["items"][0]["id_rup"])
        example = full["items"][0]
        for key, value in (("search", example["id_rup"]), ("region", example["region"]),
                           ("agency", example["satker"]), ("anomaly_class", example["classification"])):
            with self.subTest(filter=key):
                status, filtered, _ = self.request("/api/packages?" + urllib.parse.urlencode({key: value}))
                self.assertEqual(status, 200)
                self.assertIn(example["id_rup"], {row["id_rup"] for row in filtered["items"]})
                if key != "search":
                    field = {"agency": "satker", "anomaly_class": "classification"}.get(key, key)
                    self.assertTrue(all(row[field] == value for row in filtered["items"]))
        _, empty, _ = self.request("/api/packages?search=does-not-exist")
        self.assertEqual(empty["total"], 0)
        self.assertEqual(empty["items"], [])

    def test_money_is_exact_and_evidence_is_explicit(self):
        status, package, _ = self.request("/api/packages/DEMO-001")
        self.assertEqual(status, 200)
        price = package["price_forensics"]
        self.assertEqual(price["status"], "grounded")
        expected = {"implied_unit_price": Decimal("900000"), "benchmark_unit_price": Decimal("600000"),
                    "delta_idr": Decimal("300000"), "delta_percent": Decimal("50")}
        for field, value in expected.items():
            self.assertIsInstance(price[field], str)
            self.assertEqual(Decimal(price[field]), value)
        self.assertEqual(Decimal(price["implied_unit_price"]), Decimal(package["total_pagu"]) / Decimal(price["quantity"]))
        self.assert_fixture_provenance(price, True)
        self.assertTrue(price["source"]["source_id"])
        self.assertTrue(package["supporting_evidence"])
        self.assertTrue(package["counterevidence"])
        self.assertEqual(package["linkage"]["status"], "synthetic_join")

    def test_bundle_abstains_and_missing_join_is_not_invented(self):
        status, package, _ = self.request("/api/packages/DEMO-002")
        self.assertEqual(status, 200)
        price = package["price_forensics"]
        self.assertEqual(price["status"], "ungrounded")
        for field in ("implied_unit_price", "benchmark_unit_price", "delta_idr", "delta_percent"):
            self.assertIsNone(price[field])
        self.assertTrue(price["reason"])
        self.assertEqual(package["linkage"]["status"], "not_linked")
        self.assertIsNone(package["linkage"]["tender_id"])

    def test_inapplicable_benchmark_does_not_publish_a_delta(self):
        status, package, _ = self.request("/api/packages/DEMO-007")
        self.assertEqual(status, 200)
        price = package["price_forensics"]
        self.assertEqual(price["status"], "ungrounded")
        self.assertEqual(Decimal(price["implied_unit_price"]), Decimal("750000"))
        self.assertIsNone(price["benchmark_unit_price"])
        self.assertIsNone(price["delta_idr"])
        self.assertIsNone(price["delta_percent"])
        self.assertTrue(price["reason"])

    def test_anonymization_flag_reaches_all_public_payloads(self):
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.app:app", "--host", "127.0.0.1", "--port", str(port)],
            cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            env={**os.environ, "PYTHONUTF8": "1", "GEASS_ANONYMIZE": "1"},
        )
        try:
            base = f"http://127.0.0.1:{port}"
            for _ in range(100):
                try:
                    with urllib.request.urlopen(base + "/api/health", timeout=1):
                        break
                except urllib.error.URLError:
                    time.sleep(0.05)
            for path in ("/api/packages", "/api/packages/DEMO-001", "/api/tenders/DEMO-T001",
                         "/api/tenders/DEMO-T001/graph", "/api/packages/DEMO-001/dossier?kind=ppid",
                         "/api/packages/DEMO-001/dossier?kind=audit"):
                with self.subTest(path=path), urllib.request.urlopen(base + path, timeout=5) as response:
                    text = response.read().decode()
                    self.assertNotIn("Dinas Contoh", text)
                    self.assertNotIn("Vendor Sintetis", text)
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)

    def test_tender_and_graph_preserve_distinct_participant_identity(self):
        status, tender, _ = self.request("/api/tenders/DEMO-T001")
        self.assertEqual(status, 200)
        self.assert_fixture_provenance(tender, True)
        participants = tender["participants"]
        self.assertEqual(len({row["id"] for row in participants}), 3)
        for row in participants:
            expected = Decimal(row["bid"]) / Decimal(tender["hps"]) * 100
            self.assertLessEqual(abs(Decimal(row["bid_to_hps_percent"]) - expected), Decimal("0.005"))
            if row["evaluation"] == "disqualified":
                self.assertTrue(row["alasan_gugur"])
        status, graph, _ = self.request("/api/tenders/DEMO-T001/graph")
        self.assertEqual(status, 200)
        self.assert_fixture_provenance(graph, True)
        ids = {node["id"] for node in graph["nodes"]}
        self.assertEqual(len(ids), len(graph["nodes"]))
        self.assertTrue({row["id"] for row in participants}.issubset(ids))
        for edge in graph["edges"]:
            self.assertIn(edge["source"], ids)
            self.assertIn(edge["target"], ids)
        self.assertTrue(graph["limitations"])

    def test_dossiers_are_downloadable_synthetic_drafts(self):
        for kind in ("ppid", "audit"):
            with self.subTest(kind=kind):
                status, text, headers = self.request(f"/api/packages/DEMO-001/dossier?kind={kind}")
                self.assertEqual(status, 200)
                self.assertIn("attachment;", headers["Content-Disposition"])
                self.assertIn("text/markdown", headers["Content-Type"])
                self.assertIn("Draf", text)
                self.assertIn("SINTETIS", text)
                self.assertIn("Provenans:", text)
                self.assertIn("fixture:packages.json", text)
                self.assertIn("bukan pernyataan adanya pelanggaran", text)
                self.assertNotIn("terbukti korupsi", text.casefold())
                self.assertIn("300000.00", text)
        status, _, _ = self.request("/api/packages/DEMO-001/dossier?kind=send")
        self.assertEqual(status, 422)

    def test_health_and_run_do_not_claim_cloud_connectivity(self):
        status, health, _ = self.request("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(health["status"], "degraded")
        self.assertEqual(health["mode"], "synthetic_fixture")
        self.assertTrue(health["local_ready"])
        for name in ("sirup", "lpse", "jdih", "bigquery", "gemini", "model_armor", "cloud_trace"):
            self.assertEqual(health["sources"][name]["status"], "not_connected")
        status, run, _ = self.request("/api/runs", {"mode": "fixture"})
        self.assertEqual(status, 201)
        self.assertEqual(run["status"], "completed")
        self.assertEqual(run["mode"], "fixture")
        self.assertEqual(run["model_calls"], 0)
        self.assertGreater(run["package_count"], 0)
        self.assert_fixture_provenance(run, True)
        self.assertTrue(run["spans"])
        self.assertTrue(all(span["source"] == "local_process" for span in run["spans"]))
        status, stored, _ = self.request("/api/runs/" + run["id"])
        self.assertEqual(status, 200)
        self.assertEqual(stored, run)


if __name__ == "__main__":
    unittest.main()
