#!/usr/bin/env python3
"""Cliente MCP local: consulta herramientas y conserva respuestas fuera de Git."""
import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def consultar(args):
    async with streamable_http_client("http://127.0.0.1:8765/mcp") as (read, write, *_):
        async with ClientSession(read, write) as session:
            await session.initialize()
            if args.tool == "tools":
                response = await session.list_tools()
            else:
                response = await session.call_tool(args.tool, json.loads(args.arguments))
            result = response.model_dump(mode="json", by_alias=True)
            if args.output:
                destination = args.output.resolve()
                root = Path(__file__).resolve().parents[1] / "local"
                if not destination.is_relative_to(root):
                    raise ValueError("Guardar resultados únicamente bajo local/ (excluido de Git)")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(json.dumps({
                    "utc": datetime.now(timezone.utc).isoformat(),
                    "tool": args.tool, "arguments": json.loads(args.arguments),
                    "response": result,
                }, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get("isError") else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", help="Nombre de herramienta MCP, o tools")
    parser.add_argument("arguments", nargs="?", default="{}", help="Argumentos JSON")
    parser.add_argument("--output", type=Path)
    raise SystemExit(asyncio.run(consultar(parser.parse_args())))
