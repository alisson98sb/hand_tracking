# 🎬 Instalação do FFmpeg (Necessário para Whisper)

O Whisper precisa do FFmpeg para processar arquivos de áudio.

## 🪟 Windows - Método Rápido

### Opção 1: Chocolatey (Recomendado)

1. **Instalar Chocolatey** (se não tiver):
   - Abra PowerShell como Administrador
   - Execute:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Instalar FFmpeg**:
   ```powershell
   choco install ffmpeg
   ```

3. **Reiniciar terminal** e testar:
   ```bash
   ffmpeg -version
   ```

### Opção 2: Download Manual

1. **Baixar FFmpeg**:
   - Acesse: https://www.gyan.dev/ffmpeg/builds/
   - Baixe: `ffmpeg-release-essentials.zip`

2. **Extrair e Configurar**:
   - Extraia para: `C:\ffmpeg`
   - Adicione ao PATH:
     - Pesquise "Variáveis de Ambiente" no Windows
     - Edite "Path" do Sistema
     - Adicione: `C:\ffmpeg\bin`

3. **Reiniciar terminal** e testar:
   ```bash
   ffmpeg -version
   ```

### Opção 3: Scoop

```powershell
scoop install ffmpeg
```

## 🐧 Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

## 🍎 macOS

```bash
# Homebrew
brew install ffmpeg
```

## ✅ Verificar Instalação

Após instalar, execute:

```bash
ffmpeg -version
```

Deve mostrar algo como:
```
ffmpeg version 6.0 Copyright (c) 2000-2023 the FFmpeg developers
...
```

## 🔄 Depois de Instalar

1. **Feche e reabra** o terminal
2. Execute o assistente novamente:
   ```bash
   python assistente_ia.py
   ```

## ⚠️ Problemas Comuns

### "ffmpeg não encontrado"
- Reinicie o terminal/computador
- Verifique se o PATH foi configurado corretamente
- Teste com `where ffmpeg` (Windows) ou `which ffmpeg` (Linux/Mac)

### "Permissão negada"
- Execute PowerShell como Administrador
- Use `sudo` no Linux/Mac

## 🆘 Alternativa sem FFmpeg

Se não conseguir instalar FFmpeg, você pode:
1. Usar apenas comandos do sistema (não usa Whisper)
2. Usar API de transcrição online (Azure, Google Cloud Speech)

---

**Após instalar, teste novamente o assistente!** 🚀
