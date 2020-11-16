from werkzeug.exceptions import HTTPException
from sqlalchemy import or_
from model import Feira
from db import db
import csv


class RegistroNaoPodeAtualizar(HTTPException):
    code = 400
    description = "Registro não pode ser atualizado"


class NenhumaFeiraParaExcluir(HTTPException):
    code = 400
    description = "Não existe nenhum feira com esse registro"


def criar_feira(feira: Feira):
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

    filtros_para_query = {
        "distrito": filtros["distrito"]
        if "distrito" in filtros.keys()
        else "",
        "regiao": filtros["regiao"] if "regiao" in filtros.keys() else "",
        "nome": filtros["nome"] if "nome" in filtros.keys() else "",
        "bairro": filtros["bairro"] if "bairro" in filtros.keys() else "",
    }

    feiras = Feira.query.filter(
        or_(
            Feira.distrito == filtros_para_query["distrito"],
            Feira.nome == filtros_para_query["nome"],
            Feira.regiao == filtros_para_query["regiao"],
            Feira.bairro == filtros_para_query["bairro"],
        )
    ).all()

    return feiras


def excluir_feira(registro: str):
    feira_para_deletar = Feira.query.filter(Feira.registro == registro).first()

    if not feira_para_deletar:
        raise NenhumaFeiraParaExcluir()

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
            raise RegistroNaoPodeAtualizar()

    filtro = Feira.query.filter(Feira.registro == registro)
    try:
        filtro.update(feira)

        return filtro.first()

    except Exception as e:
        db.session.rollback()
        return e


def importar_csv(arquivo):
    with open(arquivo, 'r') as arquivo_csv:
            # arquivo = '../DEINFO_AB_FEIRASLIVRES_2014.csv'
            reader = csv.DictReader(arquivo_csv, delimiter=',')
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
            
            return f'Foram importadas {contador} feira do arquivo {arquivo}'