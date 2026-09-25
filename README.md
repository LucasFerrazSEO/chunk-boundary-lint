# chunk-boundary-lint — ferramenta grátis e de código aberto para checar fronteira de chunk em GEO

`chunk-boundary-lint` é uma ferramenta gratuita e de código aberto que
confere se o primeiro parágrafo de cada seção (H2/H3) de um HTML sobrevive
sozinho quando um sistema de busca com IA recorta só aquela seção, fora do
contexto do resto da página — o jeito como RAG e resposta generativa
costumam consumir conteúdo, seção por seção, não a página inteira de uma
vez.

## Por que fronteira de chunk importa em SEO/GEO

Sistemas de recuperação (RAG) que alimentam resposta de IA dividem uma
página em pedaços ("chunks"), geralmente por seção, e recuperam o pedaço
mais relevante para a pergunta — não a página inteira. Se o primeiro
parágrafo de uma seção começa com "Além disso, isso também ajuda...", esse
pedaço, sozinho, não faz sentido nenhum. `chunk-boundary-lint` audita
exatamente esse ponto de corte.

## O que a ferramenta verifica

1. **Fronteira de chunk** — o parágrafo não pode abrir com um conectivo
   que depende do que veio antes ("além disso", "por isso", "também", "no
   entanto"...). Se a seção for recortada sozinha, esse conectivo fica sem
   referente.
2. **Answer-first** — o parágrafo deveria retomar ao menos um termo do
   próprio heading, sinal de que a seção responde ao próprio tópico logo
   na primeira frase.

É irmão do [`citability-lint`](https://github.com/lucasferrazseo/citability-lint),
que audita o parágrafo isolado; este audita a fronteira entre seções.

## Instalação

Só biblioteca padrão do Python (3.9 ou mais recente). Sem dependência
externa.

```bash
git clone https://github.com/lucasferrazseo/chunk-boundary-lint.git
cd chunk-boundary-lint
```

## Como usar, passo a passo

**1. Rode contra um arquivo HTML com headings H2/H3.**

```bash
python chunk_boundary_lint.py artigo.html
```

**2. Leia o relatório.** Exemplo real, de um artigo com duas seções (a
primeira com problema proposital):

```
=== chunk-boundary-lint: secoes.html ===
2 seção/seções | OK 1 | ATENÇÃO 2

  ATENÇÃO  "Como funciona o schema markup": 1º parágrafo abre com conectivo "além disso" (a seção não sobrevive sozinha fora de contexto)
  ATENÇÃO  "Como funciona o schema markup": 1º parágrafo não retoma nenhum termo do heading (answer-first)

(Checagem mecânica de fronteira de chunk. Leitura humana continua manual.)
```

A segunda seção do mesmo arquivo, sem esses problemas, entra na contagem
de OK e não aparece na lista de atenção.

**3. Use `--strict` em CI/CD**, para bloquear publicação com fronteira de
chunk quebrada:

```bash
python chunk_boundary_lint.py artigo.html --strict
```

## Perguntas frequentes

**chunk-boundary-lint é realmente grátis?**
Sim, código aberto sob licença MIT.

**Isso funciona para markdown, ou só HTML?**
Só HTML com heading H2/H3 nesta versão. Converta markdown para HTML antes
(por exemplo, com o próprio conversor do seu gerador de site estático) se
quiser auditar um post em markdown.

**"Answer-first" significa repetir a keyword do heading no parágrafo?**
Não exatamente — significa retomar algum termo relacionado ao heading, por
raiz de palavra. Não é uma regra de densidade de keyword, é uma checagem de
coerência entre pergunta (heading) e resposta (primeiro parágrafo).

## Limitações

Cobre só português brasileiro e só HTML com heading H2/H3. "Answer-first"
é heurística por raiz de palavra, não sinônimo semântico — pode apontar
falso positivo quando a seção usa um termo relacionado, mas diferente, do
heading.

## Método e origem

Generalização da checagem de fronteira de chunk usada desde 2026 no
processo editorial de [lucasferrazseo.com](https://lucasferrazseo.com).

## Autor

[Lucas Ferraz](https://lucasferraz.com) — especialista em SEO, criação de
sites e SEO para IA, fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT — ver [LICENSE](LICENSE).
