# Discord Video Bot

Bot para Discord que busca e baixa vídeos do **YouTube**, **TikTok**, **Kwai** e analisa produtos **Shopee**.

## Funcionalidades

- `/buscar <termo>` - Busca vídeos no YouTube, TikTok e Kwai
- `/baixar <url>` - Baixa o vídeo da URL e envia MP4 no chat
- `/shopee <produto>` - Busca vídeos de produtos Shopee
- `/produto <link>` - Analisa um link de produto Shopee

## Como usar localmente

```powershell
$env:DISCORD_TOKEN="seu_token_aqui"
python main.py
```

## Deploy grátis no Railway (24/7)

1. Crie uma conta em https://railway.app
2. Clique em **New Project** → **Deploy from GitHub repo**
3. Selecione o repositório `discord-video-bot`
4. Vá em **Variables** e adicione:
   - `DISCORD_TOKEN` = seu token do bot
5. O deploy é automático! O bot fica online 24/7

## Comandos

| Comando | Descrição |
|---------|-----------|
| `/buscar <query>` | Busca vídeos no YouTube, TikTok e Kwai |
| `/baixar <url>` | Baixa vídeo da URL e envia MP4 |
| `/shopee <produto>` | Busca vídeos de produtos na Shopee |
| `/produto <link>` | Analisa link de produto Shopee |
| `!baixar <url>` | Alternativa por prefixo |
