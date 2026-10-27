
# Missão Marte - ECLSS

Projeto acadêmico de Automação de Testes Integrada (ATS13).

## Objetivo

Validar o sistema de controle de recursos do habitat de Marte, incluindo
estoques de oxigênio e água, consumo, racionamento, alertas e solicitações.

## Tecnologias

- Python
- Pytest
- Pytest Mock
- Selenium WebDriver
- Pytest-BDD
- Gherkin
- Pytest-Cov
- GitHub Actions

## Estrutura do projeto

- `src/`: regras de negócio e serviço de telemetria.
- `tests/`: testes unitários, parametrizados, mocks, Selenium e BDD.
- `tests/features/`: cenários escritos em Gherkin.
- `web/`: painel web de controle.
- `.github/workflows/`: pipeline de integração contínua.

## Instalação local

Clone o repositório:

```bash
git clone URL_DO_SEU_REPOSITORIO
cd projeto-missao-marte
```

Crie e ative o ambiente virtual no Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Executar os testes

Execute toda a suíte:

```bash
python -m pytest -v
```

Execute com relatório de cobertura:

```bash
python -m pytest -v --cov=src --cov-report=term-missing
```

Execute somente os testes BDD:

```bash
python -m pytest tests/test_bdd.py -v
```

Execute somente os testes E2E:

```bash
python -m pytest tests/test_selenium_e2e.py -v
```

## Integração contínua

O GitHub Actions executa os testes automaticamente em eventos de push
e pull request, além de permitir execução manual.

## Autor

Carlos Eduardo da Costa Viana
