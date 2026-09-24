# Observability

Repositório de apoio da apresentação sobre fundamentos de telemetria e onde o OpenTelemetry se encaixa nisso. Aqui ficam os conceitos em texto e os exemplos que rodamos ao vivo.

## Logs em todo lugar

Telemetria é o conjunto de sinais que uma aplicação emite. O log é a unidade fundamental desses sinais: toda linguagem tem alguma implementação padrão, e por isso acabamos usando log para tudo.

Localmente ele é excelente. O problema aparece remotamente: com código async ou com duas ou mais réplicas rodando, as linhas de várias execuções se misturam e a leitura fica embaralhada. Fica difícil saber qual linha pertence a qual requisição.

## Traces (rastreio)

A solução para isso é usar traces para acompanhar jornadas.

- O **trace** representa a jornada inteira, com um `trace_id` único.
- Cada **span** descreve um passo dessa jornada, com seu próprio `span_id`.

Com isso conseguimos conectar tudo, desde o front até as consultas no banco de dados, e cada log passa a carregar o trace e o span de onde saiu.

## OpenTelemetry

Existem vários SDKs e provedores de traces, cada um com seu jeito. O OpenTelemetry padroniza esses SDKs, então a forma de instrumentar é a mesma independente de para onde os dados vão.

Alguns pontos importantes:

- A maturidade muda de linguagem para linguagem.
- Em muitos casos não é preciso escrever código extra, a instrumentação automática já resolve. Código manual só entra quando você quer ver algo específico.

## Arquitetura local

A arquitetura que rodamos localmente é bem parecida com a que usamos na nuvem. Tudo passa primeiro por um coletor, que recebe os sinais e traduz para o formato que cada serviço consome.

```
aplicação ──OTLP──> coletor ──> Loki (logs)
                            ──> Tempo (traces)
                            ──> Prometheus (métricas)
                                      │
                                   Grafana
```

### otel-lgtm

Para testar localmente usamos o `grafana/otel-lgtm`, um container com toda essa stack em um lugar só.

Ele é ótimo para demonstração, mas não recomendo para o dia a dia: usa cerca de 1GB de memória, e localmente os logs no console já são excelentes. Aqui a ideia é emular parcialmente a produção.

Para subir:

```sh
cd shared
docker compose up
```

O Grafana fica em http://localhost:3000 e o coletor recebe OTLP nas portas 4317 (gRPC) e 4318 (HTTP).

## Métricas

Em geral, tudo que vira gráfico vem das métricas. Elas trazem dados agregáveis, como quantidade de requisições ou tempo de resposta, e o ideal é que tenham baixa cardinalidade, ou seja, poucos valores diferentes em cada atributo.

## Papel do log

Com traces e métricas, o log continua importante para:

- Erros e warnings
- Auditoria
- Informações longas

De forma geral, o log fica com tudo que não faz parte de uma jornada e sim do ciclo de vida do container.

## Observabilidade e auditoria

No início não é um problema manter as duas coisas juntas, mas com o tempo elas se separam porque os requisitos são diferentes.

- **Resolver problemas**: precisa ser fácil de achar e descritivo no ponto certo.
- **Auditoria**: precisa ser imutável (só adição) e de acesso restrito. Assuma que todos os desenvolvedores podem ler os logs.

## Resumo e recomendações

- Os fundamentos valem para Sentry, Jaeger, Datadog, otel-lgtm, CloudWatch e outros. O que muda é a forma de consultar.
- IA ajuda bastante a montar as consultas.
- Traces servem principalmente para fluxos e análises de curto prazo, não é indicado guardar por muito tempo.
- Não precisa subir o otel-lgtm localmente, não muda muito a vida. Em produção sim, faz diferença.
- FastAPI, uvicorn, Django e Celery têm suas peculiaridades. Na hora de aplicar, confira se o que você quer ver está realmente aparecendo.
- Em projetos novos é bem rápido adicionar e testar, e este repositório fica como demonstração.
- Em projetos antigos ajuda muito a debugar problemas. Se esbarrar em algum que exige mais manutenção, pode valer a pena, principalmente em fluxos ponta a ponta. BackOffice e Portal do Parceiro se beneficiariam muito de traces.
- O Prometheus simplifica o tempo real, e isso vale para produto também. No GED: documentos processados e tamanho dos documentos. No BackOffice: propostas abertas. Tudo sem precisar consultar o banco.
- Observabilidade é extrair valor do monitoramento da telemetria, principalmente para responder perguntas complexas. Com as ferramentas em mãos e os fundamentos, dá para se virar bem :)

## Exemplos

Siga nesta ordem:

1. [single-file](single-file/README.md): logs, traces e envio via OTLP em um script simples.
2. [api](api/README.md): instrumentação automática em uma API FastAPI e métricas.
