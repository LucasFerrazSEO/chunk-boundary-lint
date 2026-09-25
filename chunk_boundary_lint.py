#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chunk-boundary-lint — checa se o primeiro parágrafo de cada seção (H2/H3) de
um HTML sobrevive sozinho quando um sistema de busca com IA recorta só
aquela seção fora do contexto da página inteira.

O QUE FAZ
    Divide o HTML pelos headings H2/H3 e, para o primeiro parágrafo de cada
    seção, checa duas coisas:

    1. **Fronteira de chunk.** O parágrafo não pode abrir com um conectivo
       que depende do que veio antes ("além disso", "por isso", "também",
       "no entanto"...) — se a seção for recortada sozinha, esse conectivo
       fica sem referente.
    2. **Answer-first.** O parágrafo deveria retomar ao menos um termo do
       próprio heading — é o sinal de que a seção responde à própria
       pergunta/tópico logo na primeira frase, sem forçar o leitor (ou o
       sistema de recuperação) a inferir do resto do texto.

    É irmão do citability-lint (que audita parágrafo isolado); este audita
    a fronteira de seção.

USO
    python chunk_boundary_lint.py artigo.html
    python chunk_boundary_lint.py artigo.html --strict

LIMITAÇÕES
    Cobre só pt-BR e só HTML com H2/H3 (não markdown). "Answer-first" é
    heurística por raiz de palavra (6 caracteres), não sinônimo semântico —
    pode dar falso positivo se a seção usa um termo diferente, mas
    relacionado, do heading.

Autor: Lucas Ferraz (lucasferraz.com) — dependência zero, só biblioteca padrão.
Licença: MIT.
"""
from __future__ import annotations

import argparse
import re
import sys

CONECTIVOS_DEPENDENTES = (
    "além disso", "por isso", "também ", "no entanto", "mas ", "e ",
    "já ", "outro ", "outra ", "assim,", "desse modo", "dessa forma",
    "com isso", "apesar disso", "mesmo assim", "ainda assim", "portanto",
    "logo,", "então ",
)

STOPWORDS_HEADING = set(
    "o a os as um uma umas uns de do da dos das em no na nos nas por para "
    "com sem que qual quais como quando onde quem e ou seu sua seus suas "
    "mais menos muito sobre entre ser é são está estão tem têm deve devem "
    "pode podem vai vão foi hoje ainda cada todo toda pela pelo pelas "
    "pelos meu minha nem não sim isso esse essa este esta".split()
)


def strip_tags(html: str) -> str:
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    return re.sub(r"(?s)<[^>]+>", " ", html)


def normaliza(texto: str) -> str:
    return re.sub(r"\s+", " ", texto).strip()


def extrai_secoes(html: str) -> list[tuple[str, str]]:
    partes = re.split(r"(?is)(<h[23][^>]*>.*?</h[23]>)", html)
    secoes = []
    i = 1
    while i < len(partes):
        heading = normaliza(strip_tags(partes[i]))
        corpo = partes[i + 1] if i + 1 < len(partes) else ""
        secoes.append((heading, corpo))
        i += 2
    return secoes


def primeiro_paragrafo(corpo: str) -> str:
    m = re.search(r"(?is)<p[^>]*>(.*?)</p>", corpo)
    return normaliza(strip_tags(m.group(1))) if m else ""


def termos_significativos(texto: str) -> set[str]:
    palavras = re.findall(r"[a-zà-ÿ0-9]+", texto.lower())
    return {p[:6] for p in palavras if p not in STOPWORDS_HEADING and len(p) >= 3}


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Checa se o 1º parágrafo de cada seção HTML sobrevive fora de contexto."
    )
    ap.add_argument("arquivo", help="arquivo .html")
    ap.add_argument("--strict", action="store_true", help="código de saída 1 se houver qualquer ATENÇÃO")
    args = ap.parse_args()

    try:
        with open(args.arquivo, encoding="utf-8") as fh:
            html = fh.read()
    except OSError as exc:
        print(f"Não consegui ler {args.arquivo}: {exc}", file=sys.stderr)
        sys.exit(2)

    secoes = extrai_secoes(html)
    if not secoes:
        print("Nenhuma seção H2/H3 encontrada no arquivo.", file=sys.stderr)
        sys.exit(2)

    atencoes: list[str] = []
    oks: list[str] = []
    for heading, corpo in secoes:
        p1 = primeiro_paragrafo(corpo)
        if not p1:
            atencoes.append(f"\"{heading[:50]}\": seção sem parágrafo (só lista/tabela/imagem?)")
            continue
        p1_baixo = p1.lower()
        aberto_com_conectivo = next((c for c in CONECTIVOS_DEPENDENTES if p1_baixo.startswith(c)), None)
        if aberto_com_conectivo:
            atencoes.append(
                f"\"{heading[:50]}\": 1º parágrafo abre com conectivo \"{aberto_com_conectivo.strip()}\" "
                "(a seção não sobrevive sozinha fora de contexto)"
            )

        termos_head = termos_significativos(heading)
        termos_par = termos_significativos(p1)
        if termos_head and not (termos_head & termos_par):
            atencoes.append(f"\"{heading[:50]}\": 1º parágrafo não retoma nenhum termo do heading (answer-first)")

        if not aberto_com_conectivo and (not termos_head or (termos_head & termos_par)):
            oks.append(heading)

    print(f"\n=== chunk-boundary-lint: {args.arquivo} ===")
    print(f"{len(secoes)} seção/seções | OK {len(oks)} | ATENÇÃO {len(atencoes)}\n")
    for a in atencoes:
        print("  ATENÇÃO  " + a)
    if not atencoes:
        print("  Nenhum ponto de atenção nas checagens mecânicas.")
    print("\n(Checagem mecânica de fronteira de chunk. Leitura humana continua manual.)")

    sys.exit(1 if (args.strict and atencoes) else 0)


if __name__ == "__main__":
    main()
