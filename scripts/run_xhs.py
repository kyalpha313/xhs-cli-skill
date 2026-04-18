#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from typing import Any


def maybe_parse_json(text: str) -> Any | None:
    stripped = text.strip()
    if not stripped:
        return None
    if not (stripped.startswith("{") or stripped.startswith("[")):
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run xhs commands with structured JSON output."
    )
    parser.add_argument(
        "--xhs-binary",
        default="xhs",
        help="Path or executable name for the xhs CLI. Default: xhs",
    )
    parser.add_argument(
        "--append-json-flag",
        action="store_true",
        help="Append --json to the xhs command before execution.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="Timeout in seconds. Default: 120",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the wrapper JSON result.",
    )
    parser.add_argument(
        "xhs_args",
        nargs=argparse.REMAINDER,
        help="Arguments passed to xhs. Example: auth doctor",
    )
    return parser.parse_args()


def build_missing_binary_result(binary: str, command: list[str]) -> dict[str, Any]:
    return {
        "ok": False,
        "command": command,
        "xhs_binary": binary,
        "exit_code": 127,
        "stdout": "",
        "stderr": f"未找到 `{binary}` 可执行文件，请先安装并确保它在 PATH 中。",
        "stdout_json": None,
    }


def main() -> int:
    args = parse_args()
    xhs_args = list(args.xhs_args)
    if xhs_args and xhs_args[0] == "--":
        xhs_args = xhs_args[1:]

    if not xhs_args:
        print(
            json.dumps(
                {
                    "ok": False,
                    "command": [],
                    "xhs_binary": args.xhs_binary,
                    "exit_code": 2,
                    "stdout": "",
                    "stderr": "请提供至少一个 xhs 子命令参数，例如: status 或 auth doctor。",
                    "stdout_json": None,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 2

    resolved_binary = shutil.which(args.xhs_binary)
    command = [resolved_binary or args.xhs_binary, *xhs_args]
    if args.append_json_flag:
        command.append("--json")

    if resolved_binary is None and args.xhs_binary == "xhs":
        result = build_missing_binary_result(args.xhs_binary, command)
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
        return 127

    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=args.timeout,
            check=False,
        )
        result = {
            "ok": proc.returncode == 0,
            "command": command,
            "xhs_binary": command[0],
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "stdout_json": maybe_parse_json(proc.stdout),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
        return proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        result = {
            "ok": False,
            "command": command,
            "xhs_binary": command[0],
            "exit_code": 124,
            "stdout": stdout,
            "stderr": f"命令执行超时（>{args.timeout} 秒）。\n{stderr}".strip(),
            "stdout_json": maybe_parse_json(stdout),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
        return 124
    except OSError as exc:
        result = {
            "ok": False,
            "command": command,
            "xhs_binary": command[0],
            "exit_code": 126,
            "stdout": "",
            "stderr": str(exc),
            "stdout_json": None,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
        return 126


if __name__ == "__main__":
    raise SystemExit(main())
