# 🤖 Assistente Virtual Controlado por Gestos

Sistema de assistente virtual que combina **detecção de gestos manuais via webcam** com **reconhecimento de voz offline (Whisper)** para controle por comandos naturais.

## ✨ Funcionalidades

### 🤖 Versão com IA (`assistente_ia.py`) - Recomendado
- 🖐️ **Detecção de Mãos**: Rastreamento em tempo real usando MediaPipe
- 🎯 **Reconhecimento de Gestos**: Identifica gestos específicos (mão aberta, punho, dedos levantados)
- 🎤 **Reconhecimento de Voz**: Transcrição offline em português usando Whisper
- 🧠 **IA Conversacional**: Respostas inteligentes (Ollama/OpenAI/Groq)
- 🔊 **Síntese de Voz (TTS)**: Assistente fala as respostas
- ⚙️ **Comandos do Sistema**: Controle do computador por voz
- 🔄 **Máquina de Estados**: Sistema inteligente que responde a gestos
- 💬 **Interface Visual**: Feedback em tempo real na tela

### 🎮 Versão Básica (`assistente_gestos.py`)
- Todas as funcionalidades acima, exceto IA conversacional e TTS
- Ideal para testar o sistema sem dependências de IA

## 🎮 Gestos Disponíveis

| Gesto | Ação |
|-------|------|
| ✋ Mão aberta (5 dedos) | Ativa o assistente |
| ☝️ Um dedo (indicador) | Inicia gravação de voz (5 segundos) |
| 👊 Punho fechado | Desativa o assistente |
| ✌️ Dois dedos (V) | Cancela operação atual |

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Instalar FFmpeg (Necessário para Whisper)

**Windows:** Veja instruções detalhadas em [INSTALAR_FFMPEG.md](INSTALAR_FFMPEG.md)

**Rápido (com Chocolatey):**
```powershell
choco install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
```

**macOS:**
```bash
brew install ffmpeg
```

### 3. Configurar IA (Opcional - apenas para `assistente_ia.py`)

**Opção 1: Ollama (Recomendado - Gratuito e Offline)**
```bash
# Baixar e instalar: https://ollama.com/download
# Depois, baixar um modelo:
ollama pull llama3.2:3b
```

**Opção 2: OpenAI (Pago)**
```bash
export OPENAI_API_KEY='sua-chave-aqui'
```

**Opção 3: Groq (Gratuito com limites)**
```bash
export GROQ_API_KEY='sua-chave-aqui'
```

### 4. Executar o Assistente

**Versão com IA (recomendado):**
```bash
python assistente_ia.py
```

**Versão básica (sem IA):**
```bash
python assistente_gestos.py
```

### 5. Interagir

1. Mostre a **mão aberta** para ativar (status fica verde)
2. Mostre **um dedo** para gravar um comando de voz
3. **Fale seu comando** durante 5 segundos
4. A transcrição aparecerá na tela
5. Feche o **punho** para desativar

Pressione **ESC** para sair.

## 📁 Estrutura do Projeto

```
hand_tracking/
├── assistente_ia.py          # ⭐ Assistente com IA conversacional e TTS
├── assistente_gestos.py      # Assistente básico (sem IA)
├── ai_assistant.py           # Módulo de IA (Ollama/OpenAI/Groq)
├── command_executor.py       # Executor de comandos do sistema
├── gesture_recognition.py    # Módulo de reconhecimento de gestos
├── voice_recognition.py      # Módulo de reconhecimento de voz
├── detect_webcam.py          # Script original de detecção de mãos
├── GUIA_USO.md              # 📚 Guia completo de uso
├── INSTALAR_FFMPEG.md       # Tutorial de instalação do FFmpeg
├── CLAUDE.md                # Documentação para Claude Code
└── README.md                # Este arquivo
```

## 🛠️ Tecnologias

- **Python 3.9+**
- **MediaPipe** - Detecção de mãos e landmarks
- **OpenCV** - Captura e processamento de vídeo
- **OpenAI Whisper** - Reconhecimento de voz offline
- **Ollama / OpenAI / Groq** - IA conversacional
- **pyttsx3** - Síntese de voz (TTS)
- **SoundDevice** - Captura de áudio do microfone
- **NumPy & SciPy** - Processamento de dados

## 📋 Requisitos

- Python 3.9 ou superior
- Webcam funcional
- Microfone funcional
- ~500MB de espaço para modelo Whisper (baixado automaticamente)

## 🎯 Próximos Passos

### ✅ Implementado
- [x] IA conversacional com múltiplos providers (Ollama, OpenAI, Groq)
- [x] Comandos customizados do sistema (abrir apps, volume, pesquisa)
- [x] Síntese de voz (TTS) para respostas da IA
- [x] Interface visual aprimorada com status e feedback
- [x] Documentação completa (GUIA_USO.md)

### 🚀 Melhorias Futuras
- [ ] Suporte a múltiplas mãos simultâneas
- [ ] Gestos personalizáveis pelo usuário
- [ ] Histórico de conversas persistente
- [ ] Integração com APIs externas (clima, notícias)
- [ ] Controle de aplicativos específicos (Spotify, PowerPoint)
- [ ] Reconhecimento facial para perfis de usuário
- [ ] Dashboard web para configuração
- [ ] Suporte a comandos via atalhos de teclado

## 📝 Notas

- O modelo Whisper é baixado automaticamente na primeira execução (~150MB)
- Modelos ficam em cache: `~/.cache/whisper/`
- Arquivos de áudio temporários ficam em: `temp/`
- Idioma de transcrição configurado para português brasileiro

## 🤝 Contribuindo

Este é um projeto pessoal, mas sugestões são bem-vindas!

## 📄 Licença

Projeto pessoal de estudos.
