# Desafio Mercado Bitcoin

## Instalação das dependencia para execução do projeto e testes
Na raiz do projeto existe o arquivo **Makefile** com comandos para realizar algumas ações no projeto, os comando devem ser executados dentro da pasta raiz. Os comando são:
* make install -> instala as dependências e bibliotecas utilizadas no projeto
* make init_db -> cria o banco de dados **SQLite**
* make import -> executa o script para importação dos dados do arquivo csv
* make format -> formata o código usando a biblioteca **black**
* make test -> Executa os testes com o pytest (**Ao executar os testes sera criado a pasta htmlcov com as informações de cobertura dos testes**)
* make run -> executa a aplicação iniciando o servidor do **Flask** e inicia o banco de dados

## Exemplos das requisições que podem ser feitas

### **Retorna todas as feiras:** GET /feiras/

Exemplo do retorno caso exista informações no banco de dados, caso não tenha retornará uma lista vazia.

**Código:** 200 Ok

```json
[
  {
    "bairro": "VL FORMOSA", 
    "distrito": "VILA FORMOSA", 
    "id": 1, 
    "logradouro": "RUA MARAGOJIPE", 
    "nome": "VILA FORMOSA", 
    "numero": "", 
    "referencia": "TV RUA PRETORIA", 
    "regiao": "LESTE", 
    "registro": "4041-0"
  }, 
  {
    "bairro": "VL ZELINA", 
    "distrito": "VILA PRUDENTE", 
    "id": 2, 
    "logradouro": "RUA JOSE DOS REIS", 
    "nome": "PRACA SANTA HELENA", 
    "numero": "909", 
    "referencia": "RUA OLIVEIRA GOUVEIA", 
    "regiao": "LESTE", 
    "registro": "4045-2"
  }
]
```
Pode ser realizado a busca de feiras pelos campos distrito, nome, região e bairro utilizando query string.

Exemplo: /feiras?distrito=PENHA&nome=PRACA DO CERQUILHO

**Código:** 200 Ok

```json
[
  {
    "bairro": "PENHA", 
    "distrito": "PENHA", 
    "id": 723, 
    "logradouro": "PC DANILO JOSE FERNANDES", 
    "nome": "PRACA DO CERQUILHO", 
    "numero": "", 
    "referencia": "PENHA", 
    "regiao": "LESTE", 
    "registro": "6390-8"
  }
]
```

### **Cria uma feira:** POST /feira

Exemplo de conteúdo para criar a feira:
```json
{
    "registro": "1234-8",
    "nome": "Feira do Gabriel",
    "distrito": "Santo André",
    "regiao": "ABC",
    "logradouro": "Teste",
    "numero": "4321",
    "bairro": "Parque das Nações",
    "referencia": "Teste"
}
```

Exemplo de retorno no caso do cadastro correto:

**Código:** 200 Ok

```json
{
    "bairro": "PARQUE DAS NAÇÕES",
    "distrito": "SANTO ANDRÉ",
    "id": 1,
    "logradouro": "TESTE",
    "nome": "FEIRA DO GABRIEL",
    "numero": "4321",
    "referencia": "TESTE",
    "regiao": "ABC",
    "registro": "1234-9"
}
```

Exemplo de erro ao realizar cadastro e o campo número for uma string com caracteres diferentes de número:

**Código:** 400 Bad Request

```json
{
    "erro": {
        "mensagem": "O numero deve ser vazio ou um número inteiro válido"
    }
}
```
### **Atualiza uma feira:** PUT /feira/:registro/

A feira é atualizada utilizando o seu registro

Exemplo de conteúdo para atualizar o nome de uma feira com o registro 

**URL:** /feira/1234-9
```json
{
    "nome": "Feira Bitcoin",
}
```

Exemplo de retorno ao atualizar com sucesso:

**Código:** 200 Ok

```json
{
    "bairro": "PARQUE DAS NAÇÕES",
    "distrito": "SANTO ANDRÉ",
    "id": 1,
    "logradouro": "TESTE",
    "nome": "FEIRA BITCOIN",
    "numero": "4321",
    "referencia": "TESTE",
    "regiao": "ABC",
    "registro": "1234-9"
}
```

Exemplo de erro ao tentar atualizar uma feira que não existe:

**Código:** 400 Bad Request

```json
{
    "erro": {
        "mensagem": "Não existe nenhuma feira com esse registro"
    }
}
```

### **Excluir uma feira:** DELETE /feira/:registro/

A feira é excluída utilizando o seu registro

Exemplo de retorno ao realizar a exclusão:

**URL:** /feira/1234-9

Exemplo de retorno:

**Código:** 204 No Content

```json
{}
```

Exemplo de erro ao tentar excluír uma feira que não existe:

**Código:** 400 Bad Request

```json
{
    "erro": {
        "mensagem": "Não existe nenhuma feira com esse registro"
    }
}
```