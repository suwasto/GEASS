import unittest

from backend.sources.ssh import parse_page_candidates


class SshParserTests(unittest.TestCase):
    def test_synthetic_single_line_row_keeps_exact_integer_price_and_unit(self):
        rows = parse_page_candidates(
            "KODE REKENING URAIAN SATUAN HARGA\n"
            "5.1.02.01.001.00001 2 2 Bahan contoh kemasan 40 kg zak 63.000\n",
            pdf_page=7, source_id="synthetic:parser-case",
        )
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["listed_price_idr"], 63000)
        self.assertIsInstance(row["listed_price_idr"], int)
        self.assertEqual(row["satuan"], "zak")
        self.assertEqual(row["uraian"], "Bahan contoh kemasan 40 kg")
        self.assertEqual(row["pdf_page"], 7)
        self.assertEqual(row["applicability_status"], "candidate_requires_review")

    def test_headers_multiline_invalid_money_and_zero_are_not_guessed(self):
        text = "\n".join([
            "Bahan bangunan 5.1.02.01.001.00001 2",
            "5.1.02.01.001.00001 2 2 Deskripsi terpotong",
            "lanjutan zak 63.000",
            "5.1.02.01.001.00001 2 2 Contoh zak 63.00",
            "5.1.02.01.001.00001 2 2 Contoh zak 0",
            "5.1.02.01.001.00001 2 2 Contoh zak -500",
        ])
        self.assertEqual(parse_page_candidates(text, pdf_page=7, source_id="synthetic:invalid"), [])

    def test_missing_provenance_rejected(self):
        for page, source in ((0, "synthetic:x"), (1, "")):
            with self.assertRaises(ValueError):
                parse_page_candidates("", pdf_page=page, source_id=source)
