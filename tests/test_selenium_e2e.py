from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def abrir_painel(driver):
    arquivo = Path("web/painel.html").resolve()
    driver.get(arquivo.as_uri())


def test_solicitacao_oxigenio_aprovada(driver):
    abrir_painel(driver)

    campo = driver.find_element(By.ID, "quantidade")
    campo.send_keys("200")

    driver.find_element(By.ID, "solicitar").click()

    espera = WebDriverWait(driver, 5)

    nivel = espera.until(
        EC.text_to_be_present_in_element(
            (By.ID, "nivel-oxigenio"),
            "800",
        )
    )

    mensagem = espera.until(
        EC.visibility_of_element_located((By.ID, "mensagem"))
    )

    assert nivel is True
    assert mensagem.text == "Solicitação aprovada!"


def test_solicitacao_acima_do_estoque(driver):
    abrir_painel(driver)

    campo = driver.find_element(By.ID, "quantidade")
    campo.send_keys("1500")

    driver.find_element(By.ID, "solicitar").click()

    espera = WebDriverWait(driver, 5)

    mensagem = espera.until(
        EC.visibility_of_element_located((By.ID, "mensagem"))
    )

    assert mensagem.text == "Oxigênio insuficiente."

    nivel = driver.find_element(By.ID, "nivel-oxigenio")
    assert nivel.text == "1000"