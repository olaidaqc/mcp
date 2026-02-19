import unittest
from pathlib import Path
import tempfile

from web_mcp_manager.engine.logs import LogSink


class TestLogSink(unittest.TestCase):
    def test_log_sink_appends_to_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "runtime.log"
            sink = LogSink(log_file)
            sink.write("hello")
            self.assertEqual(log_file.read_text(encoding="utf-8").strip(), "hello")


if __name__ == "__main__":
    unittest.main()
