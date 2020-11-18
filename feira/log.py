import logging

arquivo_log = "feira.log"

# Criamos o logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Criamos um handler para enviar as mensagens para um arquivo
logger_handler = logging.FileHandler(arquivo_log, mode="a")
logger_handler.setLevel(logging.INFO)


# Especifique a formatação da mensagem
formatacao_data = "%d/%m/%Y %H:%M:%S"
formatacao = logging.Formatter(
    "[%(asctime)-15s - %(levelname)s ] - %(message)s", formatacao_data
)


# Associe esta formatação ao  Handler
logger_handler.setFormatter(formatacao)

# Associe o Handler ao  Logger
logger.addHandler(logger_handler)
