# Análise de Sentimentos com LLM — Projeto do Curso

Aplicação Python que usa a API da OpenAI para analisar comentários de clientes
de um e-commerce fictício.

---

## 1. Pré-requisitos

- **Python 3.9 ou superior**

Confira a versão instalada:

**Windows (PowerShell)**
```powershell
python --version
```

**macOS / Linux**
```bash
python3 --version
```

Se o comando não for reconhecido, instale a partir de [python.org/downloads](https://www.python.org/downloads/).

> **Windows:** na tela de instalação, marque a caixa **"Add Python to PATH"**
> antes de clicar em Install. Sem isso o terminal não encontra o Python.

---

## 2. Criar o ambiente virtual (.venv)

O ambiente virtual isola as bibliotecas deste projeto das bibliotecas do resto
do computador. **Crie o ambiente antes de instalar qualquer coisa.**

Abra o terminal na pasta do projeto e execute:

**Windows (PowerShell)**
```powershell
python -m venv .venv
```

**macOS / Linux**
```bash
python3 -m venv .venv
```

Isso cria uma pasta `.venv` dentro do projeto.

---

## 3. Ativar o ambiente virtual

**Windows (PowerShell)**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Prompt de Comando / cmd)**
```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Deu certo quando aparece `(.venv)` no início da linha do terminal:

```
(.venv) C:\Users\voce\projeto>
```

> **Erro no Windows?** Se aparecer *"a execução de scripts foi desabilitada
> neste sistema"*, rode o comando abaixo uma única vez e tente ativar de novo:
>
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

Para **desativar** o ambiente, em qualquer sistema:

```bash
deactivate
```

---

## 4. Instalar as bibliotecas

Com o ambiente **ativado** (o `(.venv)` precisa estar visível), instale as
dependências:

**Windows (PowerShell)**
```powershell
pip install -r requirements.txt
```

**macOS / Linux**
```bash
pip3 install -r requirements.txt
```

Isso instala:

| biblioteca      | para quê                                  |
|-----------------|-------------------------------------------|
| `openai`        | comunicação com a API da OpenAI            |
| `python-dotenv` | leitura da chave a partir do arquivo `.env`|
| `pandas`        | leitura e análise da base de dados          |
| `pydantic`      | validação das respostas do modelo           |

---

## 5. Obter a chave da API

1. Acesse [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Faça login (ou crie uma conta)
3. Clique em **Create new secret key**
4. **Copie a chave imediatamente** — ela só é exibida uma vez

> A chave começa com `sk-`. Se você perder, não há como recuperá-la: basta
> apagar a antiga e gerar outra.

---

## 6. Configurar a chave no projeto

O projeto lê a chave de um arquivo chamado `.env`, que **você precisa criar**
duplicando o `.env.example`.

**Windows (PowerShell)**
```powershell
Copy-Item .env.example .env
```

**Windows (Prompt de Comando / cmd)**
```cmd
copy .env.example .env
```

**macOS / Linux**
```bash
cp .env.example .env
```

Agora abra o arquivo `.env` no editor e substitua o texto de exemplo pela sua
chave:

```
OPENAI_API_KEY=sk-sua-chave-real-aqui
```

Atenção ao formato:

- **sem** aspas em volta da chave
- **sem** espaços antes ou depois do `=`
- o arquivo se chama exatamente `.env` (com o ponto na frente, sem `.txt`)

> **Nunca compartilhe o arquivo `.env`** nem publique a chave em repositórios.
> O `.env.example` existe justamente para ser compartilhado no lugar dele: ele
> mostra o formato esperado sem expor a chave real.