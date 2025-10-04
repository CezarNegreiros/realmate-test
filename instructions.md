# 📌 Pré-requisitos
Antes de começar, garanta que você tenha os seguintes softwares instalados na sua máquina:

- Docker
- Docker Compose
- Ngrok (para expor sua aplicação localmente)
- Uma instância da Evolution API em execução (que será criada pelo docker compose).

# ⚙️ Configuração Inicial
1. Clone o Repositório
    - Clone este projeto para a sua máquina local.

2. Crie o Arquivo de Ambiente
    - O projeto utiliza um arquivo .env para gerenciar as variáveis de ambiente. Crie o seu a partir do arquivo de exemplo:
``` text
cp .env.example .env
``` 

3. Verifique as Variáveis de Ambiente
    - Abra o arquivo .env e certifique-se de que as variáveis estão corretas para o seu ambiente local. Para a configuração padrão do docker-compose.yml, os valores padrão devem funcionar.
``` text
# .env
DEBUG=True
ALLOWED_HOSTS=localhost
base_url=http://localhost:8000

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=realmate_challenge
DATABASE_USER=realmate_user  
DATABASE_PASSWORD=realmate_password_123
DATABASE_HOST=localhost
DATABASE_PORT=5432

ENV=DEVELOPMENT

DJANGO_SETTINGS_MODULE=realmate_challenge.settings
AUTHENTICATION_API_KEY=realmate_challenge_key

```

# 🚀 Executando a Aplicação
Com o Docker em execução, inicie todos os serviços (banco de dados e aplicação web) com um único comando na raiz do projeto:
``` text
docker-compose up --build
```

- A aplicação estará pronta quando você vir a mensagem Starting development server at http://0.0.0.0:8000/. Deixe este terminal em execução.

# 🔗 Conectando com o WhatsApp (Evolution API + Ngrok)
- Para que a Evolution API possa enviar webhooks para a sua aplicação local, precisamos expor o seu servidor para a internet. Faremos isso com o Ngrok.

## Expor a Aplicação com Ngrok

### Passo 1: Instalação via APT (Recomendado)
- Este método integra o Ngrok ao seu sistema de pacotes, facilitando futuras atualizações.

#### Adicionar a Chave de Segurança
- Abra seu terminal e execute o comando abaixo para adicionar a chave GPG do repositório do Ngrok:

```text
curl -s [https://ngrok-agent.s3.amazonaws.com/ngrok.asc](https://ngrok-agent.s3.amazonaws.com/ngrok.asc) | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
``` 

#### Adicionar o Repositório
- Em seguida, adicione o repositório do Ngrok à sua lista de fontes do sistema:
```text
echo "deb [https://ngrok-agent.s3.amazonaws.com](https://ngrok-agent.s3.amazonaws.com) buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list
```

#### Instalar o Ngrok
Finalmente, atualize a lista de pacotes e instale o Ngrok:

```text
sudo apt update
sudo apt install ngrok
```

- Ao final deste passo, o Ngrok estará instalado no seu sistema.

### Passo 2: Autenticação da Sua Conta

1. **Crie uma Conta**: Se ainda não tiver, crie uma conta gratuita no site do Ngrok.

2. **Copie seu Authtoken**: Faça login no dashboard do Ngrok. Você verá uma seção chamada **"Connect your account"** com um token de autenticação. Copie o comando completo, que será algo como:

```text
ngrok config add-authtoken SEU_TOKEN_LONGO_E_SECRETO_AQUI
```
3. **Execute no Terminal**: Cole o comando que você copiou diretamente no seu terminal e pressione Enter. Isso só precisa ser feito uma vez por máquina.

#### Passo 3: Executando o Ngrok
Com a sua aplicação Django já rodando na porta 8000 (através do docker-compose up), você pode iniciar o túnel do Ngrok.

1. **Abra um Novo Terminal**: Deixe o terminal com o Docker rodando e abra um segundo terminal.

2. **Inicie o Túnel**: Execute o comando para expor a porta 8000:

```text
ngrok http 8000
```

3. **Copie a URL**: O Ngrok exibirá uma tela de status. A informação mais importante é a URL na linha Forwarding. Ela será parecida com isto:
```text
Forwarding      [https://c8b7-2804-14d-5494-7b10-....ngrok-free.app](https://c8b7-2804-14d-5494-7b10-....ngrok-free.app) -> http://localhost:8000
``` 
**Copie a URL que começa com https://. Esta é a URL pública que você usará para configurar o webhook na Evolution API.**

## Configurando o Evolution API

### Acessar o Gerenciador de Instâncias

1. Configure a api key:
No `.venv` você deve colocar um valor em `AUTHENTICATION_API_KEY`, o valor pode ser qualquer um que você preferir

2. Abra no Navegador:
Acesse a URL onde o Manager está exposto. Por padrão, é:
http://localhost:8090/manager

3. Insira a Chave de API:
Você será solicitado a fornecer a chave de API que você configurou no Passo 1 (AUTHENTICATION_API_KEY).

### Criar e Conectar uma Nova Instância
- Uma "instância" representa uma conexão com um número de WhatsApp.

1. Crie a Instância:
- No Manager, clique em `+Instância` para adicionar uma nova instância. Dê a ela um nome descritivo, por exemplo: realmate-tech-test.
- Selecione a integração `Baileys`
- Salve a instância

2. Conecte ao WhatsApp:
- Após criar a instância, ela aparecerá na lista. Clique em "Conectar" ou acesse o endpoint de QR code para essa instância.

- Abra o aplicativo do WhatsApp no seu celular, vá em Aparelhos conectados e escaneie o QR Code exibido.

- Aguarde até que o status da instância mude para CONNECTED.

### Configurando o Webhook

- Coloque a url gerada pelo `ngrok` no campo `url` na seção de `webhooks`. Exemplo:
```text
https://unorderly-catalytical-samson.ngrok-free.dev
```
- Coloque o `/webhook` ao final da `url`
- Em `eventos`, selecione `MESSAGES_UPSERT`
- Salve. Pronto, webhook configurado!