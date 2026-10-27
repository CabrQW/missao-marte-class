import pytest

from src.gerenciador_recursos import (
    GerenciadorRecursosMarte,
    OxigenioInsuficienteError,
    NivelEmergenciaInvalidoError,
)


def test_calcular_consumo_oxigenio(habitat):
    resultado = habitat.calcular_consumo_oxigenio(10)
    assert resultado == 40


def test_verificar_oxigenio_suficiente(habitat):
    resultado = habitat.verificar_oxigenio(100)
    assert resultado == 900


def test_oxigenio_insuficiente():
    habitat = GerenciadorRecursosMarte(50, 500, 4)

    with pytest.raises(OxigenioInsuficienteError):
        habitat.verificar_oxigenio(100)


def test_nivel_emergencia_invalido(habitat):
    with pytest.raises(NivelEmergenciaInvalidoError):
        habitat.calcular_taxa_emergencia("desconhecido")


def test_aplicar_racionamento(habitat):
    resultado = habitat.aplicar_racionamento(100, "critico")
    assert resultado == 75


@pytest.mark.parametrize(
    "astronautas, consumo_individual, esperado",
    [
        (1, 10, 10),
        (2, 10, 20),
        (4, 10, 40),
        (6, 15, 90),
    ],
)
def test_consumo_por_quantidade_de_astronautas(
    astronautas, consumo_individual, esperado
):
    habitat = GerenciadorRecursosMarte(1000, 500, astronautas)

    resultado = habitat.calcular_consumo_oxigenio(consumo_individual)

    assert resultado == esperado


@pytest.mark.parametrize(
    "nivel, taxa_esperada",
    [
        ("normal", 0.0),
        ("alerta", 0.10),
        ("critico", 0.25),
    ],
)
def test_taxas_de_emergencia(habitat, nivel, taxa_esperada):
    assert habitat.calcular_taxa_emergencia(nivel) == taxa_esperada


@pytest.mark.parametrize(
    "consumo, nivel, esperado",
    [
        (100, "normal", 100),
        (100, "alerta", 90),
        (100, "critico", 75),
        (200, "critico", 150),
    ],
)
def test_cotas_de_racionamento(habitat, consumo, nivel, esperado):
    assert habitat.aplicar_racionamento(consumo, nivel) == esperado


@pytest.mark.parametrize(
    "consumo",
    [-1, -10],
)
def test_consumo_negativo_invalido(habitat, consumo):
    with pytest.raises(ValueError):
        habitat.calcular_consumo_oxigenio(consumo)


def test_alerta_enviado_quando_oxigenio_insuficiente(mocker):
    telemetria = mocker.Mock()

    habitat = GerenciadorRecursosMarte(
        oxigenio=50,
        agua=500,
        astronautas=4,
        telemetria=telemetria,
    )

    with pytest.raises(OxigenioInsuficienteError):
        habitat.verificar_oxigenio(100)

    telemetria.disparar_alerta.assert_called_once_with(
        "critico",
        "Oxigênio insuficiente para atender ao consumo diário.",
    )


def test_relatorio_enviado_com_dados_corretos(mocker):
    telemetria = mocker.Mock()

    habitat = GerenciadorRecursosMarte(
        oxigenio=1000,
        agua=500,
        astronautas=4,
        telemetria=telemetria,
    )

    habitat.enviar_relatorio_status()

    telemetria.enviar_relatorio.assert_called_once_with(
        "operacional",
        1000,
        500,
    )


def test_nao_envia_alerta_quando_oxigenio_e_suficiente(mocker):
    telemetria = mocker.Mock()

    habitat = GerenciadorRecursosMarte(
        oxigenio=1000,
        agua=500,
        astronautas=4,
        telemetria=telemetria,
    )

    resultado = habitat.verificar_oxigenio(100)

    assert resultado == 900
    telemetria.disparar_alerta.assert_not_called()
