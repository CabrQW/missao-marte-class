import pytest

from pytest_bdd import scenarios, given, when, then, parsers

from src.gerenciador_recursos import (
    GerenciadorRecursosMarte,
    OxigenioInsuficienteError,
)

# Carrega os cenários descritos no arquivo Gherkin.
scenarios("features/solicitacao_oxigenio.feature")


@pytest.fixture
def contexto_bdd():
    return {}


@given(
    parsers.parse(
        "que o habitat possui {oxigenio:d} unidades de oxigênio"
    ),
    target_fixture="contexto_bdd",
)
def preparar_habitat(oxigenio):
    return {
        "habitat": GerenciadorRecursosMarte(
            oxigenio=oxigenio,
            agua=500,
            astronautas=4,
        ),
        "quantidade": 0,
        "aprovada": False,
    }


@when(
    parsers.parse(
        "o astronauta solicita {quantidade:d} unidades de oxigênio"
    )
)
def solicitar_oxigenio(contexto_bdd, quantidade):
    habitat = contexto_bdd["habitat"]
    contexto_bdd["quantidade"] = quantidade

    try:
        habitat.verificar_oxigenio(quantidade)
        habitat.oxigenio -= quantidade
        contexto_bdd["aprovada"] = True
    except OxigenioInsuficienteError:
        contexto_bdd["aprovada"] = False


@then("a solicitação deve ser aprovada")
def verificar_aprovacao(contexto_bdd):
    assert contexto_bdd["aprovada"] is True


@then("a solicitação deve ser recusada por falta de oxigênio")
def verificar_recusa(contexto_bdd):
    assert contexto_bdd["aprovada"] is False


@then(
    parsers.parse(
        "o estoque de oxigênio deve ser {estoque:d} unidades"
    )
)
def verificar_estoque(contexto_bdd, estoque):
    assert contexto_bdd["habitat"].oxigenio == estoque


@then(
    parsers.parse(
        "o estoque de oxigênio deve permanecer em {estoque:d} unidades"
    )
)
def verificar_estoque_inalterado(contexto_bdd, estoque):
    assert contexto_bdd["habitat"].oxigenio == estoque