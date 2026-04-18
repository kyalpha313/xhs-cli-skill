#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_SAFE_COMMANDS = [
    {
        "name": "status",
        "args": ["status"],
        # 未登录时 status 返回 1 仍然说明命令链路正常。
        "expected_exit_codes": [0, 1],
        "description": "检查当前登录状态",
    },
    {
        "name": "whoami",
        "args": ["whoami"],
        "expected_exit_codes": [0, 1],
        "description": "检查当前账号识别结果",
    },
    {
        "name": "auth_doctor",
        "args": ["auth", "doctor"],
        "expected_exit_codes": [0, 1],
        "description": "检查认证排障链路",
    },
]


DISCOVERY_COMMANDS = [
    {
        "name": "hot",
        "args": ["hot"],
        "expected_exit_codes": [0, 1],
        "description": "检查热榜读取链路",
    },
    {
        "name": "feed",
        "args": ["feed"],
        "expected_exit_codes": [0, 1],
        "description": "检查推荐流读取链路",
    },
]


def collect_env_check(xhs_binary: str) -> dict[str, Any]:
    resolved_binary = shutil.which(xhs_binary)
    if resolved_binary is None and xhs_binary == "xhs":
        return {
            "ok": False,
            "xhs_binary": xhs_binary,
            "checks": [],
            "error": "未找到 `xhs` 可执行文件，请先安装 CLI 并确保它在 PATH 中。",
        }

    binary = resolved_binary or xhs_binary
    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "name": "python_version",
            "ok": sys.version_info >= (3, 10),
            "details": (
                f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            ),
        }
    )

    for name, command in [
        ("xhs_help", [binary, "--help"]),
        ("xhs_auth_help", [binary, "auth", "--help"]),
    ]:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        text = "\n".join(part for part in [proc.stdout, proc.stderr] if part).strip()
        checks.append(
            {
                "name": name,
                "ok": proc.returncode == 0 and bool(text),
                "details": "可执行" if proc.returncode == 0 and bool(text) else "执行失败",
                "returncode": proc.returncode,
            }
        )

    return {
        "ok": all(check["ok"] for check in checks),
        "xhs_binary": binary,
        "checks": checks,
    }


def run_python_json(script_path: Path, script_args: list[str]) -> tuple[int, dict[str, Any]]:
    proc = subprocess.run(
        [sys.executable, str(script_path), *script_args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    payload: dict[str, Any]
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        payload = {
            "ok": False,
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "error": f"无法解析 {script_path.name} 的 JSON 输出。",
        }
    return proc.returncode, payload


def build_command_result(
    root_dir: Path,
    command_spec: dict[str, Any],
    xhs_binary: str,
) -> dict[str, Any]:
    run_xhs_path = root_dir / "scripts" / "run_xhs.py"
    _, payload = run_python_json(
        run_xhs_path,
        ["--xhs-binary", xhs_binary, "--pretty", *command_spec["args"]],
    )
    actual_exit_code = payload.get("exit_code")
    expected_exit_codes = command_spec["expected_exit_codes"]
    command_ok = actual_exit_code in expected_exit_codes
    return {
        "name": command_spec["name"],
        "description": command_spec["description"],
        "expected_exit_codes": expected_exit_codes,
        "ok": command_ok,
        "result": payload,
    }


def print_pretty_report(report: dict[str, Any]) -> None:
    print("xhs-cli-skill smoke check")
    print(f"- overall: {'ok' if report['ok'] else 'failed'}")
    print(f"- root_dir: {report['root_dir']}")
    print(f"- xhs_binary: {report['xhs_binary']}")

    env_report = report["env_check"]
    print(f"- env_check: {'ok' if env_report.get('ok') else 'failed'}")
    env_error = env_report.get("error")
    if env_error:
        print(f"  error: {env_error}")

    for command in report["commands"]:
        status = "ok" if command["ok"] else "failed"
        result = command["result"]
        exit_code = result.get("exit_code")
        print(f"- {command['name']}: {status} - exit_code={exit_code}")
        stderr = (result.get("stderr") or "").strip()
        if stderr:
            first_line = stderr.splitlines()[0]
            print(f"  stderr: {first_line}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run smoke checks for xhs-cli-skill environment and read-only commands."
    )
    parser.add_argument(
        "--xhs-binary",
        default="xhs",
        help="Path or executable name for the xhs CLI. Default: xhs",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON report instead of human-readable output.",
    )
    parser.add_argument(
        "--include-discovery",
        action="store_true",
        help="Also run discovery commands such as hot/feed and optional search.",
    )
    parser.add_argument(
        "--search-query",
        default="AI agent",
        help="Search query used when --include-discovery is enabled. Default: AI agent",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root_dir = Path(__file__).resolve().parent.parent
    env_report = collect_env_check(args.xhs_binary)

    command_specs = list(DEFAULT_SAFE_COMMANDS)
    if args.include_discovery:
        command_specs.extend(DISCOVERY_COMMANDS)
        command_specs.append(
            {
                "name": "search",
                "args": ["search", args.search_query],
                "expected_exit_codes": [0, 1],
                "description": "检查搜索读取链路",
            }
        )

    command_results = [
        build_command_result(root_dir, command_spec, args.xhs_binary)
        for command_spec in command_specs
    ]

    overall_ok = bool(env_report.get("ok")) and all(item["ok"] for item in command_results)
    report = {
        "ok": overall_ok,
        "root_dir": str(root_dir),
        "xhs_binary": args.xhs_binary,
        "env_check": env_report,
        "commands": command_results,
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_pretty_report(report)
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
