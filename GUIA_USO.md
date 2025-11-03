# 📚 Guia de Uso - Assistente IA

## 🚀 Início Rápido

### 1. Instalar Ollama (IA Local - Recomendado)

**Por que Ollama?**
- ✅ Totalmente gratuito
- ✅ Funciona offline (privacidade total)
- ✅ Rápido e eficiente

**Como instalar:**

1. Baixe o Ollama: https://ollama.com/download
2. Instale normalmente
3. Abra o terminal e baixe um modelo:

```bash
ollama pull llama3.2:3b
```

### 2. Executar o Assistente

```bash
python assistente_ia.py
```

---

## 🎮 Como Usar

### Gestos Básicos

| Gesto | Ação |
|-------|------|
| ✋ **Mão aberta** (5 dedos) | Ativa o assistente |
| ☝️ **Um dedo** (indicador) | Grava comando de voz (5s) |
| 👊 **Punho fechado** | Desativa o assistente |
| ✌️ **Dois dedos** (paz) | Cancela operação |

### Fluxo de Uso

1. **Ativar**: Mostre a mão aberta → Status fica VERDE
2. **Gravar**: Mostre um dedo → Status fica VERMELHO
3. **Falar**: Diga seu comando em até 5 segundos
4. **Aguardar**: IA processa → Status fica LARANJA
5. **Ouvir**: Resposta aparece na tela e é falada

---

## 💬 Exemplos de Comandos

### Comandos do Sistema

```
"Abrir calculadora"
"Abrir Chrome"
"Que horas são?"
"Que dia é hoje?"
"Aumentar volume"
"Pesquisar Python tutorial"
```

### Perguntas para a IA

```
"Qual é a capital da França?"
"Como fazer café?"
"Explique o que é Python"
"Conte uma piada"
"Qual é a previsão do tempo?" (precisa integração)
```

---

## ⚙️ Configuração Avançada

### Usar OpenAI (Pago)

1. Obter API Key: https://platform.openai.com/api-keys
2. Configurar variável de ambiente:

```bash
# Windows
set OPENAI_API_KEY=sua-chave-aqui

# Linux/Mac
export OPENAI_API_KEY=sua-chave-aqui
```

3. Editar `assistente_ia.py` (linha final):

```python
assistente = AssistenteIA(
    ai_provider="openai",
    ai_model="gpt-4o-mini",  # Ou "gpt-4o"
    use_tts=True
)
```

### Usar Groq (Gratuito com Limites)

1. Obter API Key: https://console.groq.com/keys
2. Configurar:

```bash
# Windows
set GROQ_API_KEY=sua-chave-aqui

# Linux/Mac
export GROQ_API_KEY=sua-chave-aqui
```

3. Editar `assistente_ia.py`:

```python
assistente = AssistenteIA(
    ai_provider="groq",
    ai_model="llama-3.1-8b-instant",
    use_tts=True
)
```

### Desativar Síntese de Voz

```python
assistente = AssistenteIA(
    ai_provider="ollama",
    use_tts=False  # Sem voz
)
```

---

## 🎯 Comandos Customizados Disponíveis

### Navegadores
- "abrir navegador"
- "abrir chrome"
- "abrir firefox"
- "abrir edge"

### Aplicativos
- "abrir calculadora"
- "abrir bloco de notas"
- "abrir explorador"
- "abrir terminal"

### Sistema
- "aumentar volume"
- "diminuir volume"

### Utilidades
- "que horas são"
- "que dia é hoje"
- "tirar screenshot"

### Pesquisa
- "pesquisar [termo]"
- "buscar [termo]"

---

## 🐛 Solução de Problemas

### "IA não disponível"

**Ollama:**
```bash
# Verificar se Ollama está rodando
ollama list

# Se não estiver, baixe o modelo
ollama pull llama3.2:3b
```

**OpenAI/Groq:**
- Verifique se a API Key está correta
- Confirme que a variável de ambiente está configurada

### "TTS não disponível"

Instale as dependências do TTS:
```bash
pip install pyttsx3
```

### "Erro ao gravar áudio"

- Verifique se o microfone está conectado
- No Windows, permita acesso ao microfone
- Liste dispositivos disponíveis executando: `python voice_recognition.py`

### "Whisper demorando muito"

- Use modelo menor: edite `voice_recognition.py`
- Troque `model_size="base"` por `model_size="tiny"`

### "Gesto não detectado"

- Mantenha a mão bem visível para a câmera
- Boa iluminação ajuda muito
- Mantenha distância adequada (30-60cm)

---

## 📊 Comparação de Providers de IA

| Provider | Custo | Velocidade | Precisão | Offline |
|----------|-------|------------|----------|---------|
| Ollama | Grátis | Rápida | Boa | ✅ |
| Groq | Grátis* | Muito Rápida | Excelente | ❌ |
| OpenAI | Pago | Rápida | Excelente | ❌ |

*Groq tem limite gratuito de requisições

---

## 🎓 Dicas de Uso

1. **Fale claramente**: Pronuncie bem as palavras
2. **Ambiente silencioso**: Menos ruído = melhor transcrição
3. **Iluminação**: Ajuda na detecção de gestos
4. **Distância da câmera**: 30-60cm é ideal
5. **Comandos curtos**: Frases diretas funcionam melhor

---

## 🔐 Privacidade

- **Ollama**: Tudo roda localmente, 100% privado
- **OpenAI/Groq**: Dados enviados para servidores externos
- **Áudio**: Arquivos salvos em `temp/`, pode deletar

---

## 📝 Estrutura de Arquivos

```
hand_tracking/
├── assistente_ia.py          # ⭐ Aplicação principal com IA
├── assistente_gestos.py      # Versão sem IA
├── ai_assistant.py           # Módulo de IA conversacional
├── command_executor.py       # Executor de comandos do sistema
├── gesture_recognition.py    # Reconhecimento de gestos
├── voice_recognition.py      # Reconhecimento de voz
└── temp/                     # Áudios temporários
```

---

## 💡 Ideias para Expandir

- [ ] Adicionar mais comandos customizados
- [ ] Integrar com APIs (clima, notícias)
- [ ] Controlar música (Spotify)
- [ ] Controlar apresentações (PowerPoint)
- [ ] Criar perfis de usuário
- [ ] Adicionar reconhecimento facial

---

## 🤝 Ajuda

Problemas? Sugestões?
- Verifique a documentação do Ollama: https://ollama.com/docs
- Teste os módulos individualmente primeiro
- Revise o CLAUDE.md para detalhes técnicos
