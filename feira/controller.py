from werkzeug.exceptions import BadRequest
from sqlalchemy import or_
from feira.model import Feira
from feira.db import db
import csv


def criar_feira(feira: Feira):

    if feira is None:
        raise BadRequest("Nenhum valor passado para criar uma feira")

    registro_existe = Feira.query.filter(
        Feira.registro == feira["registro"]
    ).first()

    if registro_existe:
        raise BadRequest("O registro da feira já existe")

    nova_feira = Feira(
        registro=feira["registro"],
        nome=feira["nome"],
        distrito=feira["distrito"],
        regiao=feira["regiao"],
        logradouro=feira["logradouro"],
        numero=feira["numero"],
        bairro=feira["bairro"],
        referencia=feira["referencia"],
    )
    try:
        db.session.add(nova_feira)
        db.session.commit()
        nova_feira = Feira.query.filter(
            Feira.registro == feira["registro"]
        ).first()
        return nova_feira
    except Exception as e:
        db.session.rollback()
        return e


def listar_todas_as_feiras():
    return Feira.query.all()


def listar_feiras_por_filtro(filtros: dict):

    filtros_para_query = []

    for chave, valor in filtros.items():
        if chave == "distrito" and valor != "":
            filtros_para_query.append(Feira.distrito == valor)
        if chave == "nome" and valor != "":
            filtros_para_query.append(Feira.nome == valor)
        if chave == "regiao" and valor != "":
            filtros_para_query.append(Feira.regiao == valor)
        if chave == "bairro" and valor != "":
            filtros_para_query.append(Feira.bairro == valor)

    feiras = Feira.query.filter(
        or_(
            *filtros_para_query
        )
    ).all()

    return feiras


def excluir_feira(registro: str):
    feira_para_deletar = Feira.query.filter(Feira.registro == registro).first()

    if not feira_para_deletar:
        raise BadRequest("Não existe nenhuma feira com esse registro")

    try:
        db.session.delete(feira_para_deletar)
        db.session.commit()
        return feira_para_deletar
    except Exception as e:
        db.session.rollback()
        return e

def atualizar_feira(feira: dict, registro: str):
    for chave in feira.keys():
        if chave == "registro":
            raise BadRequest("O campo Registro não pode ser atualizado")

    filtro = Feira.query.filter(Feira.registro == registro)
    try:
        filtro.update(feira)

        return filtro.first()

    except Exception as e:
        db.session.rollback()
        return e


def importar_csv(arquivo):
    with open(arquivo, "r") as arquivo_csv:
        # arquivo = '../DEINFO_AB_FEIRASLIVRES_2014.csv'
        reader = csv.DictReader(arquivo_csv, delimiter=",")
        contador = 0
        feiras_importadas = []
        for collumn in reader:
            feira = Feira(
                registro=collumn["REGISTRO"],
                nome=collumn["NOME_FEIRA"],
                distrito=collumn["DISTRITO"],
                regiao=collumn["REGIAO5"],
                logradouro=collumn["LOGRADOURO"],
                numero=collumn["NUMERO"],
                bairro=collumn["BAIRRO"],
                referencia=collumn["REFERENCIA"],
            )
            feiras_importadas.append(feira)
            contador += 1

        db.session.bulk_save_objects(feiras_importadas)
        db.session.commit()

        return f"Foram importadas {contador} feiras do arquivo {arquivo}"
