# Discord Video Bot

Bot para Discord que busca e baixa vídeos do **YouTube**, **TikTok** e **Kwai**.

## Funcionalidades

- `/buscar <termo>` - Busca vídeos nas 3 plataformas
- `/baixar <url>` - Baixa o vídeo da URL e envia no chat
- `!baixar <url>` - Comando por prefixo (alternativa)

## Como usar localmente

1. Crie um bot em https://discord.com/developers/applications
2. Copie o token do bot
3. Execute com a variável de ambiente:
```
set DISCORD_TOKEN=seu_token_aqui
python main.py
```
Ou no PowerShell:
```
$env:DISCORD_TOKEN="seu_token_aqui"
python main.py
```

## Hospedagem no GitHub (GitHub Secrets)

1. Crie um repositório no GitHub e faça push dos arquivos
2. No repositório vá em **Settings → Secrets and variables → Actions**
3. Adicione um **New repository secret**:
   - **Nome:** `DISCORD_TOKEN`
   - **Segredo:** cole o token do seu bot
4. Para rodar 24/7, conecte o repositório a serviços como:
   - **Railway** (railway.app)
   - **Render** (render.com)
   - **Oracle Cloud** (gratuito)
5. Nestes serviços, adicione `DISCORD_TOKEN` nas variáveis de ambiente (equivalente ao GitHub Secret)

## Comandos

| Comando | Descrição |
|---------|-----------|
| `/buscar <query>` | Busca vídeos por termo |
| `/baixar <url>` | Baixa vídeo da URL |
| `!baixar <url>` | Alternativa por prefixo |
