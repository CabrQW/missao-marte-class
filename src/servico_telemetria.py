class ServicoTelemetriaEspacial:
    """Simula a comunicação com a estação terrestre."""

    def enviar_relatorio(self, status, oxigenio, agua):
        print(
            f"Relatório enviado: status={status}, "
            f"oxigênio={oxigenio}, água={agua}"
        )

    def disparar_alerta(self, nivel, mensagem):
        print(f"ALERTA enviado para a Terra: [{nivel}] {mensagem}")