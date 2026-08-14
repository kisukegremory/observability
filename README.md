# Observability

Gostaria de criar um repositório para exercitar meu conhecimento de telemetria, simples



# PRD simplificado
1. Criar o repositório com suas dependências em uv
1. Criar uma api em fastapi que retorne um health check
1. Criar um makefile para fazer essa chamada de api (será que existe já algum container que faça isso?)
1. Dockerizar a aplicação e criar comandos para chamar ele de forma simples
1. Instalar o wrapper do opentelemetry
1. Inicializar a aplicação por ele e realizar uma chamada no mesmo
1. Verificar quais variáveis de ambiente podemos setar e brincar com isso
1. Criar o otel-collector.yaml para exportar local
1. Aplicação envia 100% para lá ao invés de console direto
1. Adicionar um span


# Guia de apresentação e manufatura
1. Criar a api em fast api
2. Rodar ela de forma pura 'simple run'
3. Rodar instrumentada local
4. Rodar via compose com jaeger
