"""Build an Obsidian vault from graphify-out/graph.json.

The vault lives INSIDE graphify-out/ and only uses data from that folder:
  - graphify-out/graph.json    -> nodes, edges, hyperedges
  - graphify-out/GRAPH_REPORT.md -> community labels (for nicer names)

Generates:
  - graphify-out/nodes/<id>.md
  - graphify-out/communities/<community>.md
  - graphify-out/hyperedges/<id>.md
  - graphify-out/files/<source_file>.md  (groupings, source_file kept as plain text)
  - graphify-out/INDEX.md
  - graphify-out/.obsidian/                (app.json, graph.json, workspace.json)

External project paths (backend/main.py, etc.) are kept as plain text labels,
NOT as hyperlinks, so the vault is self-contained.

Run:
    python scripts/build_obsidian_vault.py
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "graphify-out"
GRAPH_PATH = VAULT / "graph.json"
REPORT_PATH = VAULT / "GRAPH_REPORT.md"


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return value or "untitled"


def wikilink(target_id: str, display: str | None = None) -> str:
    target = slug(target_id)
    if display and display != target:
        return f"[[{target}|{display}]]"
    return f"[[{target}]]"


def edge_confidence(edge: dict) -> tuple[str, float | None]:
    label = (
        edge.get("confidence")
        or edge.get("provenance")
        or edge.get("extraction_type")
        or edge.get("confidence_type")
        or edge.get("type")
        or edge.get("evidence")
        or "UNKNOWN"
    )
    score = edge.get("confidence_score")
    return str(label), score


def write_note(path: Path, frontmatter: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for key, val in frontmatter.items():
        if val is None or val == "":
            continue
        if isinstance(val, list):
            if not val:
                continue
            lines.append(f"{key}:")
            for item in val:
                lines.append(f"  - {item}")
        else:
            text = str(val).replace("\n", " ").strip()
            if any(ch in text for ch in ":#&*!|>%@`") or text == "":
                text = json.dumps(text, ensure_ascii=False)
            lines.append(f"{key}: {text}")
    lines.append("---\n")
    lines.append(body)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    data = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    nodes: list[dict] = data["nodes"]
    edges: list[dict] = data.get("links", data.get("edges", []))
    hyperedges: list[dict] = data.get("graph", {}).get("hyperedges", [])

    nodes_by_id = {n["id"]: n for n in nodes}
    label_for = lambda nid: nodes_by_id.get(nid, {}).get("label", nid)

    community_members: dict[int, list[dict]] = defaultdict(list)
    for n in nodes:
        community_members[n.get("community", -1)].append(n)

    out_edges: dict[str, list[dict]] = defaultdict(list)
    in_edges: dict[str, list[dict]] = defaultdict(list)
    for e in edges:
        s, t = e.get("source"), e.get("target")
        if s:
            out_edges[s].append(e)
        if t:
            in_edges[t].append(e)

    files_to_nodes: dict[str, list[dict]] = defaultdict(list)
    for n in nodes:
        sf = n.get("source_file")
        if sf:
            files_to_nodes[sf].append(n)

    # Clean previous build (only directories we own).
    for sub in ("nodes", "communities", "hyperedges", "files"):
        d = VAULT / sub
        if d.exists():
            for p in d.rglob("*"):
                if p.is_file():
                    p.unlink()

    # ---- Node notes -----------------------------------------------------
    for n in nodes:
        nid = n["id"]
        label = n.get("label", nid)
        community = n.get("community", -1)
        source_file = n.get("source_file")
        source_loc = n.get("source_location")
        file_type = n.get("file_type")

        body_parts = [f"# {label}\n"]

        meta_lines = []
        if source_file:
            loc = f" `{source_loc}`" if source_loc else ""
            meta_lines.append(f"- Source: `{source_file}`{loc}")
        if file_type:
            meta_lines.append(f"- Type: `{file_type}`")
        if community != -1:
            meta_lines.append(
                f"- Community: {wikilink(f'_COMMUNITY_{community}', f'Community {community}')}"
            )
        if meta_lines:
            body_parts.append("\n".join(meta_lines) + "\n")

        outs = out_edges.get(nid, [])
        if outs:
            body_parts.append("## Outgoing\n")
            for e in outs:
                rel = e.get("relation", "related_to")
                conf, score = edge_confidence(e)
                target = e.get("target")
                tlabel = label_for(target) if target else "?"
                score_txt = f" {score:.2f}" if isinstance(score, (int, float)) else ""
                line = f"- --{rel}--> {wikilink(target or '?', tlabel)} _[{conf}{score_txt}]_"
                ev = e.get("evidence")
                if ev and ev not in {"EXTRACTED", "INFERRED", "AMBIGUOUS"}:
                    line += f"\n  > {ev}"
                body_parts.append(line)
            body_parts.append("")

        ins = in_edges.get(nid, [])
        if ins:
            body_parts.append("## Incoming\n")
            for e in ins:
                rel = e.get("relation", "related_to")
                conf, score = edge_confidence(e)
                source = e.get("source")
                slabel = label_for(source) if source else "?"
                score_txt = f" {score:.2f}" if isinstance(score, (int, float)) else ""
                body_parts.append(
                    f"- {wikilink(source or '?', slabel)} --{rel}--> _[{conf}{score_txt}]_"
                )
            body_parts.append("")

        frontmatter = {
            "title": label,
            "id": nid,
            "community": community if community != -1 else None,
            "source_file": source_file,
            "source_location": source_loc,
            "file_type": file_type,
            "tags": [
                "graphify/node",
                f"community/{community}" if community != -1 else None,
                f"type/{file_type}" if file_type else None,
            ],
        }
        frontmatter["tags"] = [t for t in frontmatter["tags"] if t]
        write_note(VAULT / "nodes" / f"{slug(nid)}.md", frontmatter, "\n".join(body_parts))

    # ---- Community notes ------------------------------------------------
    community_labels: dict[int, str] = {}
    if REPORT_PATH.exists():
        report = REPORT_PATH.read_text(encoding="utf-8")
        for m in re.finditer(r"### Community (\d+) - \"([^\"]+)\"", report):
            community_labels[int(m.group(1))] = m.group(2)

    for cid, members in sorted(community_members.items()):
        if cid == -1:
            continue
        cname = community_labels.get(cid, f"Community {cid}")
        body = [f"# {cname}\n", f"Community ID: **{cid}** — {len(members)} nodes\n", "## Members\n"]
        members_sorted = sorted(
            members,
            key=lambda n: len(out_edges.get(n["id"], [])) + len(in_edges.get(n["id"], [])),
            reverse=True,
        )
        for n in members_sorted:
            deg = len(out_edges.get(n["id"], [])) + len(in_edges.get(n["id"], []))
            body.append(f"- {wikilink(n['id'], n.get('label', n['id']))} _({deg} edges)_")
        body.append("")
        write_note(
            VAULT / "communities" / f"{slug('_COMMUNITY_' + str(cid))}.md",
            {
                "title": cname,
                "community": cid,
                "size": len(members),
                "tags": ["graphify/community", f"community/{cid}"],
            },
            "\n".join(body),
        )

    # ---- Hyperedge notes ------------------------------------------------
    for he in hyperedges:
        hid = he.get("id", "hyperedge")
        label = he.get("label", hid)
        rel = he.get("relation", "participate_in")
        conf = he.get("confidence", "UNKNOWN")
        score = he.get("confidence_score")
        src = he.get("source_file")
        body = [f"# {label}\n"]
        if src:
            body.append(f"- Source: `{src}`")
        body.append(f"- Relation: `{rel}`")
        score_txt = f" ({score:.2f})" if isinstance(score, (int, float)) else ""
        body.append(f"- Confidence: {conf}{score_txt}\n")
        body.append("## Participants\n")
        for nid in he.get("nodes", []):
            body.append(f"- {wikilink(nid, label_for(nid))}")
        body.append("")
        write_note(
            VAULT / "hyperedges" / f"{slug(hid)}.md",
            {"title": label, "id": hid, "tags": ["graphify/hyperedge", f"relation/{rel}"]},
            "\n".join(body),
        )

    # ---- File-grouped index notes (source_file as plain text, no link) -
    for source_file, ns in sorted(files_to_nodes.items()):
        body = [f"# {source_file}\n", f"`{source_file}` — {len(ns)} nodes\n", "## Nodes\n"]
        for n in sorted(ns, key=lambda x: x.get("source_location") or ""):
            loc = n.get("source_location") or ""
            body.append(f"- `{loc}` {wikilink(n['id'], n.get('label', n['id']))}")
        body.append("")
        write_note(
            VAULT / "files" / f"{slug(source_file)}.md",
            {"title": source_file, "source_file": source_file, "tags": ["graphify/file"]},
            "\n".join(body),
        )

    # ---- Index / home --------------------------------------------------
    god_node_ids = sorted(
        (n["id"] for n in nodes),
        key=lambda nid: len(out_edges.get(nid, [])) + len(in_edges.get(nid, [])),
        reverse=True,
    )[:15]

    home_lines = [
        "# ACSD - Bóveda de Conocimiento",
        "",
        f"Generada desde `graph.json` — {len(nodes)} nodos, {len(edges)} aristas, "
        f"{len([c for c in community_members if c != -1])} comunidades.",
        "",
        "Abre `graphify-out/` como vault en Obsidian (`Open folder as vault`) y pulsa `Ctrl+G`.",
        "",
        "## God nodes (más conectados)",
    ]
    for nid in god_node_ids:
        n = nodes_by_id[nid]
        deg = len(out_edges.get(nid, [])) + len(in_edges.get(nid, []))
        home_lines.append(f"- {wikilink(nid, n.get('label', nid))} _({deg} edges)_")

    home_lines += ["", "## Comunidades"]
    for cid in sorted(community_members):
        if cid == -1:
            continue
        cname = community_labels.get(cid, f"Community {cid}")
        size = len(community_members[cid])
        home_lines.append(
            f"- {wikilink('_COMMUNITY_' + str(cid), cname)} _({size} nodes)_"
        )

    home_lines += ["", "## Hyperedges"]
    for he in hyperedges:
        home_lines.append(f"- {wikilink(he['id'], he.get('label', he['id']))}")

    home_lines += ["", "## Archivos fuente (agrupaciones)"]
    for source_file in sorted(files_to_nodes):
        home_lines.append(f"- {wikilink(source_file, source_file)}")

    write_note(
        VAULT / "INDEX.md",
        {"title": "ACSD - Graphify Vault", "tags": ["graphify/index"]},
        "\n".join(home_lines),
    )

    # ---- .obsidian config ---------------------------------------------
    obsidian_dir = VAULT / ".obsidian"
    obsidian_dir.mkdir(exist_ok=True)
    (obsidian_dir / "app.json").write_text(
        json.dumps(
            {
                "newLinkFormat": "shortest",
                "useMarkdownLinks": False,
                "alwaysUpdateLinks": True,
                "defaultViewMode": "preview",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (obsidian_dir / "graph.json").write_text(
        json.dumps(
            {
                "collapse-filter": True,
                "search": "",
                "showTags": True,
                "showAttachments": False,
                "hideUnresolved": False,
                "showOrphans": True,
                "collapse-color-groups": False,
                "colorGroups": [
                    {"query": "tag:#graphify/community", "color": {"a": 1, "rgb": 5419488}},
                    {"query": "tag:#graphify/hyperedge", "color": {"a": 1, "rgb": 14701138}},
                    {"query": "tag:#graphify/file", "color": {"a": 1, "rgb": 4521796}},
                    {"query": "tag:#graphify/index", "color": {"a": 1, "rgb": 16766720}},
                ],
                "collapse-display": False,
                "showArrow": True,
                "textFadeMultiplier": 0,
                "nodeSizeMultiplier": 1.2,
                "lineSizeMultiplier": 1,
                "collapse-forces": True,
                "centerStrength": 0.5,
                "repelStrength": 12,
                "linkStrength": 0.9,
                "linkDistance": 220,
                "scale": 0.6,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (obsidian_dir / "workspace.json").write_text(
        json.dumps({"main": {"id": "main", "type": "split"}}, indent=2),
        encoding="utf-8",
    )

    print(f"Vault generated INSIDE: {VAULT}")
    print(f"  nodes:       {len(nodes)}")
    print(f"  edges:       {len(edges)}")
    print(f"  communities: {len([c for c in community_members if c != -1])}")
    print(f"  hyperedges:  {len(hyperedges)}")
    print(f"  files:       {len(files_to_nodes)}")


if __name__ == "__main__":
    main()
