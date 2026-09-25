**English** · [Português (Brasil)](README.pt-BR.md)

# chunk-boundary-lint

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

`chunk-boundary-lint` is a free, open source tool that checks whether the
first paragraph of each section (H2/H3) in an HTML file still makes sense
on its own when an AI search system extracts only that section, out of
the context of the rest of the page. That is how RAG and generative
answers usually consume content, section by section, not the whole page
at once. It runs locally with the Python standard library only.

Its heuristics are specific to Brazilian Portuguese text: the connective
list, the stopwords and the report are all in Portuguese.

## Contents

- [Background](#background)
- [What it checks](#what-it-checks)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Methodology](#methodology)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Background

Retrieval systems (RAG) that feed AI answers split a page into pieces
("chunks"), usually by section, and retrieve the piece most relevant to
the question, not the whole page. If the first paragraph of a section
opens with "Além disso, isso também ajuda..." ("Besides that, this also
helps..."), that piece makes no sense on its own. `chunk-boundary-lint`
audits exactly that cut point.

## What it checks

1. **Chunk boundary.** The paragraph must not open with a connective that
   depends on what came before ("além disso", "por isso", "também", "no
   entanto"...). If the section is extracted alone, that connective has
   nothing to refer to.
2. **Answer-first.** The paragraph should pick up at least one term from
   its own heading, a sign that the section answers its own topic in the
   first sentence.

It is a sibling of
[`citability-lint`](https://github.com/LucasFerrazSEO/citability-lint),
which audits the paragraph in isolation; this one audits the boundary
between sections.

## Installation

Python 3.9 or newer, standard library only. No external dependencies.

```bash
git clone https://github.com/LucasFerrazSEO/chunk-boundary-lint.git
cd chunk-boundary-lint
```

## Usage

**1. Run it against an HTML file with H2/H3 headings.**

```bash
python chunk_boundary_lint.py artigo.html
```

**2. Read the report.** Real output from an article with two sections
(the first one has a deliberate problem). The tool prints its report in
Brazilian Portuguese.

```
=== chunk-boundary-lint: secoes.html ===
2 seção/seções | OK 1 | ATENÇÃO 2

  ATENÇÃO  "Como funciona o schema markup": 1º parágrafo abre com conectivo "além disso" (a seção não sobrevive sozinha fora de contexto)
  ATENÇÃO  "Como funciona o schema markup": 1º parágrafo não retoma nenhum termo do heading (answer-first)

(Checagem mecânica de fronteira de chunk. Leitura humana continua manual.)
```

The second section of the same file has none of these problems, so it
counts as OK and does not appear in the warning list.

**3. Use `--strict` in CI/CD** to block publishing when a chunk boundary
is broken (exit code 1 if there is any warning):

```bash
python chunk_boundary_lint.py artigo.html --strict
```

## FAQ

**Is chunk-boundary-lint really free?**
Yes. It is open source under the MIT license.

**Does it work with Markdown, or only HTML?**
Only HTML with H2/H3 headings in this version. Convert Markdown to HTML
first (for example with your static site generator's own converter) if
you want to audit a Markdown post.

**Does "answer-first" mean repeating the heading keyword in the
paragraph?**
Not exactly. It means picking up some term related to the heading, by
word stem. It is not a keyword density rule; it is a coherence check
between the question (heading) and the answer (first paragraph).

## Limitations

It covers only Brazilian Portuguese and only HTML with H2/H3 headings.
"Answer-first" is a word-stem heuristic, not semantic synonym matching,
so it can flag a false positive when the section uses a related but
different term from the heading.

## Methodology

A generalization of the chunk boundary check used since 2026 in the
editorial process of [lucasferrazseo.com](https://lucasferrazseo.com).

## Contributing

Bug reports and suggestions are welcome through [GitHub Issues](https://github.com/LucasFerrazSEO/chunk-boundary-lint/issues).

## Author

[Lucas Ferraz](https://lucasferraz.com) is an SEO, website development and Generative Engine Optimization specialist and the founder of [Lucas Ferraz SEO](https://lucasferrazseo.com).

## License

MIT. See [LICENSE](LICENSE).
