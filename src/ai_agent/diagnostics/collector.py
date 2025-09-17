import psutil
import subprocess
from typing import Dict, Any
from ..utils.logger import get_logger

logger = get_logger(__name__)

def collect_basic() -> Dict[str, Any]:
    try:
        procs = sorted(psutil.process_iter(['pid','name','cpu_percent','memory_percent']),
                       key=lambda p: p.info.get('cpu_percent', 0) or 0, reverse=True)[:10]
        procs_info = [p.info for p in procs]
    except Exception:
        logger.exception("process collection failed")
        procs_info = []

    def run(cmd):
        try:
            p = subprocess.run(cmd, capture_output=True, text=True)
            return p.stdout if p.returncode == 0 else p.stderr
        except Exception as e:
            logger.debug("cmd failed: %s", e)
            return ""

    df = run(["df", "-h"])
    dmesg = run(["dmesg", "--nolog"])
    journal = run(["journalctl", "-n", "200"])

    return {
        "processes_top": procs_info,
        "df": df,
        "dmesg": dmesg[:20000],
        "journal": journal[:20000]
    }