from werkzeug.exceptions import BadRequest
from sqlalchemy import and_
from feira.mvc.model import Feira
from feira.db import db
import csv


def criar_feira(feira: Feira):

    if not feira:
        raise BadRequest("Nenhum valor passado para criar uma feira")

    if not "registro" in feira.keys():
        raise BadRequest("O campo registro deve existir")
    
    if not feira["registro"]:
        raise BadRequest("O registro não pode ser vazio")

    if feira['numero'] and not feira['numero'].isdigit():
        raise BadRequest("O numero deve ser vazio ou um número inteiro válido")


    registro_existe = Feira.query.filter(
        Feira.registro == feira["registro"]
    ).first()

    if registro_existe:
        raise BadRequest("O registro da feira já existe")

    nova_feira = Feira(
        registro=feira["registro"],
        nome=feira["nome"].upper(),
        distrito=feira["distrito"].upper(),
        regiao=feira["regiao"].upper(),
        logradouro=feira["logradouro"].upper(),
        numero=feira["numero"],
        bairro=feira["bairro"].upper(),
        referencia=feira["referencia"].upper(),
    )

    db.session.add(nova_feira)
    db.session.commit()
    nova_feira = Feira.query.filter(
        Feira.registro == feira["registro"]
    ).first()
    return nova_feira



def listar_todas_as_feiras():
    return Feira.query.all()


def listar_feiras_por_filtro(filtros: dict):

    filtros_para_query = []

    for chave, valor in filtros.items():
        if chave == "distrito" and valor != "":
            filtros_para_query.append(Feira.distrito == valor.upper())
        if chave == "nome" and valor != "":
            filtros_para_query.append(Feira.nome == valor.upper())
        if chave == "regiao" and valor != "":
            filtros_para_query.append(Feira.regiao == valor.upper())
        if chave == "bairro" and valor != "":
            filtros_para_query.append(Feira.bairro == valor.upper())

    feiras = Feira.query.filter(
        and_(
            *filtros_para_query
        )
    ).all()

    return feiras


def excluir_feira(registro: str):
    feira_para_deletar = Feira.query.filter(Feira.registro == registro).first()

    if not feira_para_deletar:
        raise BadRequest("Não existe nenhuma feira com esse registro")

    db.session.delete(feira_para_deletar)
    db.session.commit()
    return feira_para_deletar

def atualizar_feira(feira: dict, registro: str):
    for chave in feira.keys():
        if chave == "registro":
            raise BadRequest("O campo Registro não pode ser atualizado")

    filtro = Feira.query.filter(Feira.registro == registro)

    if not filtro.first():
        raise BadRequest("Não existe nenhuma feira com esse registro")

    for chave, valor in feira.items():
        feira[chave] = valor.upper()

    filtro.update(feira)
    return filtro.first()



def importar_csv(arquivo):
    with open(arquivo, "r") as arquivo_csv:
        # arquivo = '../DEINFO_AB_FEIRASLIVRES_2014.csv'
        reader = csv.DictReader(arquivo_csv, delimiter=",")
        contador = 0
        feiras_importadas = []
        for collumn in reader:
            feira = Feira(
                registro=collumn["REGISTRO"],
                nome=collumn["NOME_FEIRA"].upper() if collumn["NOME_FEIRA"] else "" ,
                distrito=collumn["DISTRITO"].upper() if collumn["DISTRITO"] else "",
                regiao=collumn["REGIAO5"].upper() if collumn["REGIAO5"] else "",
                logradouro=collumn["LOGRADOURO"].upper() if collumn["LOGRADOURO"] else "",
                numero=collumn["NUMERO"].split(".")[0] if collumn["NUMERO"].split(".")[0].isdigit() else "",
                bairro=collumn["BAIRRO"].upper() if collumn["BAIRRO"] else "",
                referencia=collumn["REFERENCIA"].upper() if collumn["REFERENCIA"] else "",
            )
            feiras_importadas.append(feira)
            contador += 1

        db.session.bulk_save_objects(feiras_importadas)
        db.session.commit()

        return f"Foram importadas {contador} feiras do arquivo {arquivo}"
