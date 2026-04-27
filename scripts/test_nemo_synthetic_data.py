from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from nemo_synthetic_data.cli import main
from nemo_synthetic_data.templates import get_template


class NemoSyntheticDataTests(unittest.TestCase):
    def test_template_registry_contains_bpc(self) -> None:
        template = get_template("bpc_security_events")
        self.assertEqual(template.name, "bpc_security_events")
        self.assertGreaterEqual(len(template.columns), 5)

    @patch.dict("os.environ", {"NVIDIA_API_KEY": "test-key"})
    @patch("nemo_synthetic_data.provider.NemoDataDesignerProvider.validate_environment")
    def test_doctor_runs(self, validate_environment) -> None:
        validate_environment.return_value = {"sdk_loaded": True}
        rc = main(["doctor"])
        self.assertEqual(rc, 0)

    @patch.dict("os.environ", {"NVIDIA_API_KEY": "test-key"})
    @patch("nemo_synthetic_data.provider.NemoDataDesignerProvider.build_manifest")
    def test_export_config(self, build_manifest) -> None:
        build_manifest.return_value = {"columns": [], "model_configs": []}
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "template.json"
            rc = main(
                [
                    "export-config",
                    "api_abuse_patterns",
                    "--output",
                    str(output),
                    "--set",
                    "company_name=PKA",
                ]
            )
            self.assertEqual(rc, 0)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["context"]["company_name"], "PKA")
            self.assertEqual(payload["template"]["name"], "api_abuse_patterns")


if __name__ == "__main__":
    unittest.main()
