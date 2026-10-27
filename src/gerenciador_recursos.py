from src.servico_telemetria import ServicoTelemetriaEspacial


class OxigenioInsuficienteError(Exception):
    """Erro lançado quando não há oxigênio suficiente."""


class NivelEmergenciaInvalidoError(Exception):
    """Erro lançado quando o nível de emergência é inválido."""


class GerenciadorRecursosMarte:
    def __init__(self, oxigenio, agua, astronautas, telemetria=None):
        if oxigenio < 0 or agua < 0 or astronautas <= 0:
            raise ValueError(
                "Os recursos devem ser positivos e deve haver astronautas."
            )

        self.oxigenio = oxigenio
        self.agua = agua
        self.astronautas = astronautas
        self.telemetria = telemetria or ServicoTelemetriaEspacial()

    def calcular_consumo_oxigenio(self, consumo_por_astronauta):
        if consumo_por_astronauta < 0:
            raise ValueError("O consumo não pode ser negativo.")

        return consumo_por_astronauta * self.astronautas

    def calcular_consumo_agua(self, consumo_por_astronauta):
        if consumo_por_astronauta < 0:
            raise ValueError("O consumo não pode ser negativo.")

        return consumo_por_astronauta * self.astronautas

    def verificar_oxigenio(self, consumo_diario):
        if consumo_diario < 0:
            raise ValueError("O consumo não pode ser negativo.")

        if self.oxigenio < consumo_diario:
            self.telemetria.disparar_alerta(
                "critico",
                "Oxigênio insuficiente para atender ao consumo diário.",
            )
            raise OxigenioInsuficienteError(
                "Oxigênio insuficiente para atender ao consumo diário."
            )

        return self.oxigenio - consumo_diario

    def calcular_taxa_emergencia(self, nivel):
        taxas = {
            "normal": 0.0,
            "alerta": 0.10,
            "critico": 0.25,
        }

        if nivel not in taxas:
            raise NivelEmergenciaInvalidoError(
                f"Nível de emergência inválido: {nivel}"
            )

        return taxas[nivel]

    def aplicar_racionamento(self, consumo_diario, nivel):
        if consumo_diario < 0:
            raise ValueError("O consumo não pode ser negativo.")

        taxa = self.calcular_taxa_emergencia(nivel)
        return consumo_diario * (1 - taxa)

    def enviar_relatorio_status(self):
        return self.telemetria.enviar_relatorio(
            "operacional",
            self.oxigenio,
            self.agua,
        )
