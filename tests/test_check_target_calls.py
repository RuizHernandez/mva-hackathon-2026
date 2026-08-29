"""Tests scripts/check_target_calls.py genotype classification logic against
synthetic (non-patient) fixture VCF lines only — never the real controlled
data, which never leaves the local machine."""

import importlib.util
import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_PATH = os.path.join(REPO_ROOT, "scripts", "check_target_calls.py")

spec = importlib.util.spec_from_file_location("check_target_calls", SCRIPT_PATH)
check_target_calls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_target_calls)


class TestGenotypeClassification(unittest.TestCase):
    def test_het(self):
        self.assertEqual(check_target_calls.classify("0/1"), "het")
        self.assertEqual(check_target_calls.classify("0|1"), "het")
        self.assertEqual(check_target_calls.classify("1|0"), "het")

    def test_hom_alt(self):
        self.assertEqual(check_target_calls.classify("1/1"), "hom_alt")

    def test_hom_ref(self):
        self.assertEqual(check_target_calls.classify("0/0"), "hom_ref")

    def test_missing(self):
        self.assertEqual(check_target_calls.classify("./."), "unknown")
        self.assertEqual(check_target_calls.classify(".|0"), "unknown")


class TestCheckAgainstSyntheticVCF(unittest.TestCase):
    """Builds a tiny synthetic VCF (fabricated coordinates/genotypes, not the
    real proband data) to prove the checker finds/classifies matching loci
    and ignores everything else, without ever touching controlled data."""

    def setUp(self):
        import gzip
        import tempfile

        self.tmp = tempfile.NamedTemporaryFile(suffix=".vcf.gz", delete=False)
        self.tmp.close()

        header = "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n"
        lines = [
            "15\t40209701\t.\tT\tG\t100\tPASS\t.\tGT\t0/1\n",   # matches locus 1
            "15\t40220612\t.\tT\tG\t100\tPASS\t.\tGT\t0/1\n",   # matches locus 2
            "1\t123456\t.\tA\tC\t100\tPASS\t.\tGT\t1/1\n",       # unrelated variant
        ]
        with gzip.open(self.tmp.name, "wt") as f:
            f.write(header)
            f.writelines(lines)

        # point the module's target loci at these synthetic coordinates
        check_target_calls.TARGET_LOCI = [
            {"chrom": "15", "pos": 40209701, "ref": "T", "alt": "G", "label": "locus1"},
            {"chrom": "15", "pos": 40220612, "ref": "T", "alt": "G", "label": "locus2"},
        ]

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_finds_both_loci_as_het(self):
        from pathlib import Path
        result = check_target_calls.check(Path(self.tmp.name))
        self.assertEqual(result["locus1"], {"found": True, "genotype_class": "het"})
        self.assertEqual(result["locus2"], {"found": True, "genotype_class": "het"})


if __name__ == "__main__":
    unittest.main()
