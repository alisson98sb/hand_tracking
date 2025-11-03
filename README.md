# 🤖 Assistente Virtual Controlado por Gestos

Sistema de assistente virtual que combina **detecção de gestos manuais via webcam** com **reconhecimento de voz offline (Whisper)** para controle por comandos naturais.

## ✨ Funcionalidades

- 🖐️ **Detecção de Mãos**: Rastreamento em tempo real usando MediaPipe
- 🎯 **Reconhecimento de Gestos**: Identifica gestos específicos (mão aberta, punho, dedos levantados)
- 🎤 **Reconhecimento de Voz**: Transcrição offline em português usando Whisper
- 🔄 **Máquina de Estados**: Sistema inteligente que responde a gestos
- 💬 **Interface Visual**: Feedback em tempo real na tela

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

### 3. Executar o Assistente

```bash
python assistente_gestos.py
```

### 3. Interagir

1. Mostre a **mão aberta** para ativar (status fica verde)
2. Mostre **um dedo** para gravar um comando de voz
3. **Fale seu comando** durante 5 segundos
4. A transcrição aparecerá na tela
5. Feche o **punho** para desativar

Pressione **ESC** para sair.

## 📁 Estrutura do Projeto

```
hand_tracking/
├── assistente_gestos.py      # Aplicação principal integrada
├── gesture_recognition.py    # Módulo de reconhecimento de gestos
├── voice_recognition.py      # Módulo de reconhecimento de voz
├── detect_webcam.py          # Script original de detecção de mãos
├── requirements.txt          # Dependências do projeto
├── CLAUDE.md                 # Documentação para Claude Code
├── prompt.txt                # Roadmap do projeto
└── README.md                 # Este arquivo
```

## 🛠️ Tecnologias

- **Python 3.9+**
- **MediaPipe** - Detecção de mãos e landmarks
- **OpenCV** - Captura e processamento de vídeo
- **OpenAI Whisper** - Reconhecimento de voz offline
- **SoundDevice** - Captura de áudio do microfone
- **NumPy & SciPy** - Processamento de dados

## 📋 Requisitos

- Python 3.9 ou superior
- Webcam funcional
- Microfone funcional
- ~500MB de espaço para modelo Whisper (baixado automaticamente)

## 🎯 Próximos Passos

- [ ] Adicionar IA conversacional (Ollama/OpenAI/Groq)
- [ ] Criar comandos customizados (abrir apps, controlar sistema)
- [ ] Adicionar síntese de voz (TTS)
- [ ] Melhorar interface visual
- [ ] Adicionar mais gestos

## 📝 Notas

- O modelo Whisper é baixado automaticamente na primeira execução (~150MB)
- Modelos ficam em cache: `~/.cache/whisper/`
- Arquivos de áudio temporários ficam em: `temp/`
- Idioma de transcrição configurado para português brasileiro

## 🤝 Contribuindo

Este é um projeto pessoal, mas sugestões são bem-vindas!

## 📄 Licença

Projeto pessoal de estudos.
