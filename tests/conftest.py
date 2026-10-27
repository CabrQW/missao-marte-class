import pytest 
import os

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.gerenciador_recursos import GerenciadorRecursosMarte

@pytest.fixture(scope="module")
def parametros_habitat():
    """Parâmetros iniciais compartilhados durante o módulo de testes."""
    return {
        "oxigenio": 1000,
        "agua": 500,
        "astronautas": 4,
    }

@pytest.fixture
def habitat(parametros_habitat):
    """Cria um gerenciador limpo para cada teste."""
    gerenciador = GerenciadorRecursosMarte(
        oxigenio=parametros_habitat["oxigenio"],
        agua=parametros_habitat["agua"],
        astronautas=parametros_habitat["astronautas"],
    )

    yield gerenciador

    # Limpeza executada após cada teste.
    gerenciador = None

@pytest.fixture
def driver():
    """Abre o Chrome em modo headless e encerra ao final do teste."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    navegador = webdriver.Chrome(options=options)

    yield navegador

    navegador.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura uma screenshot automaticamente quando um teste falha."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        navegador = item.funcargs.get("driver")

        if navegador is not None:
            pasta = Path("screenshots")
            pasta.mkdir(exist_ok=True)

            nome = f"{item.name}.png"
            caminho = pasta / nome

            navegador.save_screenshot(str(caminho))
            print(f"\nScreenshot da falha salva em: {caminho.resolve()}")