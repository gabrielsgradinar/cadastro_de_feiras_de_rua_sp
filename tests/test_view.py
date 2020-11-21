def test_request_retorna_404(client):
    assert client.get("/url_que_nao_existe").status_code == 404


def test_rota_base(client):
    res = client.get("/")
    assert res.json["mensagem"] == "Hello Mercado Bitcon !"


def test_consulta_feiras_com_dois_filtros(client):
    distrito = "PENHA"
    nome = "VILA NOVA GRANADA"
    res = client.get(f"/feiras?distrito={distrito}&nome={nome}")
    assert res.status_code == 200
    assert res.mimetype == "application/json"
    assert res.json[0]["distrito"] == distrito
    assert res.json[0]["nome"] == nome
    assert len(res.json) == 1


def test_consulta_feiras_com_quatro_filtros(client):
    distrito = "PENHA"
    nome = "VILA NOVA GRANADA"
    regiao = "Leste"
    bairro = "VL NOVA GRANADA"
    res = client.get(
        f"/feiras?distrito={distrito}&nome={nome}&regiao={regiao}&bairro={bairro}"
    )
    assert res.status_code == 200
    assert res.mimetype == "application/json"
    assert res.json[0]["distrito"] == distrito
    assert res.json[0]["nome"] == nome
    assert res.json[0]["regiao"] == regiao.upper()
    assert res.json[0]["bairro"] == bairro
    assert len(res.json) == 1


def test_consulta_todas_as_feiras(client):
    res = client.get("/feiras")
    assert res.status_code == 200
    assert res.mimetype == "application/json"
    assert len(res.json) >= 1


def test_criar_uma_feira(client, mock_feira_criar):
    res = client.post("/feira", json=mock_feira_criar)
    assert res.status_code == 201
    assert res.mimetype == "application/json"
    assert res.json["registro"] == mock_feira_criar["registro"]


def test_erro_ao_criar_uma_feira_com_registro_que_ja_existe(
    client, mock_feira_criar
):
    client.post("/feira", json=mock_feira_criar)

    res = client.post("/feira", json=mock_feira_criar)
    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert res.json["erro"]["mensagem"] == "O registro da feira já existe"


def test_erro_ao_criar_uma_feira_com_nenhuma_informacao(client):
    res = client.post("/feira", json={})
    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert (
        res.json["erro"]["mensagem"]
        == "Nenhum valor passado para criar uma feira"
    )


def test_erro_ao_criar_uma_feira_com_o_registro_vazio(
    client, mock_feira_criar
):
    mock_feira_criar["registro"] = ""
    res = client.post("/feira", json=mock_feira_criar)
    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert res.json["erro"]["mensagem"] == "O registro não pode ser vazio"


def test_erro_ao_criar_uma_feira_com_o_numero_invalido(
    client, mock_feira_criar
):
    mock_feira_criar["numero"] = "invalido"
    res = client.post("/feira", json=mock_feira_criar)
    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert (
        res.json["erro"]["mensagem"]
        == "O numero deve ser vazio ou um número inteiro válido"
    )


def test_erro_ao_criar_uma_feira_sem_o_campo_registro(
    client, mock_feira_criar
):
    del mock_feira_criar["registro"]
    res = client.post("/feira", json=mock_feira_criar)
    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert res.json["erro"]["mensagem"] == "O campo registro deve existir"


def test_atualizar_uma_feira(client):
    dados_para_atualizar = {
        "nome": "Mercado Bitcoin",
        "regiao": "VILA OLIMPIA",
    }
    registro_para_atualizar = "4045-2"
    res = client.put(
        f"/feira/{registro_para_atualizar}", json=dados_para_atualizar
    )
    assert res.status_code == 200
    assert res.mimetype == "application/json"
    assert res.json["registro"] == registro_para_atualizar


def test_erro_ao_atualizar_uma_feira_com_registro_vazio(client):
    dados_para_atualizar = {
        "nome": "Mercado Bitcoin",
        "regiao": "VILA OLIMPIA",
    }
    registro_para_atualizar = " "
    res = client.put(
        f"/feira/{registro_para_atualizar}", json=dados_para_atualizar
    )
    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert (
        res.json["erro"]["mensagem"]
        == "Não existe nenhuma feira com esse registro"
    )


def test_erro_ao_atualizar_uma_feira_com_a_chave_registro_para_atualizar(
    client,
):
    dados_para_atualizar = {
        "registro": "1234",
        "nome": "Mercado Bitcoin",
        "regiao": "VILA OLIMPIA",
    }
    registro_para_atualizar = "1"
    res = client.put(
        f"/feira/{registro_para_atualizar}", json=dados_para_atualizar
    )
    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert (
        res.json["erro"]["mensagem"]
        == "O campo Registro não pode ser atualizado"
    )


def test_excluir_uma_feira(client):
    registro_para_excluir = "4038-0"
    res = client.delete(f"/feira/{registro_para_excluir}")
    assert res.status_code == 204
    assert res.mimetype == "application/json"


def test_erro_ao_excluir_uma_feira_que_nao_existe(client):
    registro_para_excluir = "0000-0"
    res = client.delete(f"/feira/{registro_para_excluir}")
    assert res.status_code == 400
    assert res.mimetype == "application/json"
    assert (
        res.json["erro"]["mensagem"]
        == "Não existe nenhuma feira com esse registro"
    )
