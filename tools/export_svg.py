#!/usr/bin/env python3
"""Export the deliberately small Mermaid flowchart subset in this atlas to SVG.

Mermaid .mmd files are the single editable source. Graphviz SVG is a convenience
export, not an additional authoritative diagram definition. Requires `dot`.
"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'diagrams' / 'mermaid'
OUTPUT = ROOT / 'diagrams' / 'svg'
OUTPUT.mkdir(exist_ok=True)
NODE = re.compile(r'([A-Za-z][A-Za-z0-9_]*)\["([^"]+)"\]|([A-Za-z][A-Za-z0-9_]*)\{"([^"]+)"\}')
EDGE = re.compile(r'^\s*([A-Za-z][A-Za-z0-9_]*)(?:\["[^"]+"\]|\{"[^"]+"\})?\s*(<-->|-->|-\.->)(?:\|([^|]+)\|)?\s*([A-Za-z][A-Za-z0-9_]*)')

def quote(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'

def render(path):
    content=path.read_text(encoding='utf-8')
    lines=[line.strip() for line in content.splitlines() if line.strip()]
    direction='LR' if lines[0]=='flowchart LR' else 'TB'
    if lines[0] not in ('flowchart LR','flowchart TD'):
        raise ValueError(f'Unsupported flowchart direction: {path}')
    nodes={}
    edges=[]
    for line in lines[1:]:
        for match in NODE.finditer(line):
            if match.group(1):
                nodes[match.group(1)]=(match.group(2),False)
            else:
                nodes[match.group(3)]=(match.group(4),True)
        match=EDGE.match(line)
        if match:
            src, kind, label, dst=match.groups()
            edges.append((src,dst,kind,label))
        elif '-->' in line or '<-->' in line or '-.->' in line:
            raise ValueError(f'Unsupported Mermaid edge in {path}: {line}')
    for src,dst,_,_ in edges:
        if src not in nodes or dst not in nodes:
            raise ValueError(f'Missing node label for {src} or {dst} in {path}')
    dot=['digraph G {',f'rankdir={direction};','graph [pad="0.25", nodesep="0.40", ranksep="0.55", bgcolor="white", outputorder="edgesfirst", fontname="DejaVu Sans"];', 'node [fontname="DejaVu Sans", fontsize=11, style="rounded,filled", shape="box", color="#AABBC9", fillcolor="#F2F6FA", fontcolor="#183149", penwidth=1.2, margin="0.16,0.12"];', 'edge [color="#5C8299", arrowsize=0.7, penwidth=1.3, fontname="DejaVu Sans", fontsize=9, fontcolor="#496679"];']
    for key,(label,decision) in nodes.items():
        opts=', shape="diamond", fillcolor="#E5F1EE"' if decision else ''
        dot.append(f'{quote(key)} [label={quote(label)}{opts}];')
    for src,dst,kind,label in edges:
        extra=[]
        if kind=='<-->': extra+=['dir=both']
        if kind=='-.->': extra+=['style=dashed']
        if label: extra += [f'label={quote(label)}']
        dot.append(f'{quote(src)} -> {quote(dst)}' + ((' ['+', '.join(extra)+']') if extra else '')+';')
    dot.append('}')
    proc=subprocess.run(['dot','-Tsvg','-o',str(OUTPUT / f'{path.stem}.svg')],input='\n'.join(dot),text=True,capture_output=True)
    if proc.returncode:
        raise RuntimeError(f'{path}: {proc.stderr}')
    return len(nodes),len(edges)

if __name__ == '__main__':
    files=sorted(SOURCE.glob('*.mmd'))
    for f in files:
        n,e=render(f)
        print(f'{f.stem}: {n} nodes, {e} edges')
    print(f'Exported {len(files)} SVGs')
