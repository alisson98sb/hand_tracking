# 🎤 Lista Completa de Comandos de Voz

## 📌 Como Usar

Basta falar **UMA PALAVRA-CHAVE** que o assistente reconhece automaticamente!

Exemplos:
- Diga apenas: **"CALCULADORA"** → Abre a calculadora
- Diga apenas: **"CHROME"** → Abre o Chrome
- Diga apenas: **"WORD"** → Abre o Word
- Diga apenas: **"POSTMAN"** → Abre o Postman

---

## 🌐 Navegadores

| Comando | Variações Aceitas | Ação |
|---------|-------------------|------|
| **navegador** | "navegador", "abrir navegador" | Abre navegador padrão |
| **chrome** | "chrome", "abrir chrome", "google chrome" | Abre Google Chrome |
| **firefox** | "firefox", "abrir firefox" | Abre Firefox |
| **edge** | "edge", "abrir edge" | Abre Microsoft Edge |

---

## 💼 Aplicativos Microsoft Office

| Comando | Variações Aceitas | Ação |
|---------|-------------------|------|
| **word** | "word", "abrir word", "microsoft word" | Abre Microsoft Word |
| **excel** | "excel", "abrir excel" | Abre Microsoft Excel |
| **powerpoint** | "powerpoint", "abrir powerpoint" | Abre PowerPoint |

---

## 💻 Ferramentas de Desenvolvimento

| Comando | Variações Aceitas | Ação |
|---------|-------------------|------|
| **vscode** | "vscode", "code", "visual studio code", "abrir vscode" | Abre VS Code |
| **postman** | "postman", "abrir postman" | Abre Postman |

---

## 🛠️ Aplicativos do Sistema

| Comando | Variações Aceitas | Ação |
|---------|-------------------|------|
| **calculadora** | "calculadora", "calc", "abrir calculadora" | Abre Calculadora |
| **notepad** | "bloco de notas", "notepad", "abrir bloco de notas" | Abre Bloco de Notas |
| **explorador** | "explorador", "pasta", "arquivos", "abrir explorador" | Abre Explorador de Arquivos |
| **terminal** | "terminal", "cmd", "prompt", "abrir terminal" | Abre Terminal/CMD |

---

## 🔊 Controle de Volume

| Comando | Variações Aceitas | Ação |
|---------|-------------------|------|
| **aumentar volume** | "aumentar volume", "volume alto" | Aumenta o volume |
| **diminuir volume** | "diminuir volume", "volume baixo" | Diminui o volume |
| **silenciar** | "silenciar", "mudo" | Silencia o áudio |

---

## ⏰ Utilidades

| Comando | Variações Aceitas | Ação |
|---------|-------------------|------|
| **horas** | "que horas são", "horas", "hora" | Informa a hora atual |
| **data** | "que dia é hoje", "data", "dia" | Informa a data atual |
| **screenshot** | "tirar screenshot", "screenshot", "print screen" | Captura a tela |

---

## 🔍 Pesquisa na Web

| Comando | Exemplo | Ação |
|---------|---------|------|
| **pesquisar [termo]** | "pesquisar Python tutorial" | Busca no Google |
| **buscar [termo]** | "buscar receita de bolo" | Busca no Google |
| **procurar [termo]** | "procurar restaurantes próximos" | Busca no Google |

---

## 💡 Dicas de Uso

### ✅ Comandos que Funcionam:
- ✅ "calculadora"
- ✅ "chrome"
- ✅ "word"
- ✅ "postman"
- ✅ "vscode"
- ✅ "horas"
- ✅ "pesquisar inteligência artificial"

### ❌ Evite:
- ❌ Frases muito longas
- ❌ Múltiplos comandos de uma vez

### 🎯 Melhor Forma:
**Seja direto! Uma palavra ou frase curta é o suficiente.**

Exemplos perfeitos:
- "Calculadora" → ✅
- "Word" → ✅
- "Chrome" → ✅
- "Que horas são" → ✅

---

## 🚀 Comandos Mais Usados

```
1. calculadora
2. chrome
3. word
4. vscode
5. horas
6. pesquisar [termo]
7. explorador
8. terminal
```

---

## 📝 Adicionar Novos Comandos

Para adicionar comandos personalizados, edite o arquivo `command_executor.py` e adicione no dicionário `self.commands`:

```python
# No método __init__ da classe CommandExecutor
self.commands = {
    # ... comandos existentes ...

    # Seu novo comando
    "spotify": self._open_spotify,
    "abrir spotify": self._open_spotify,
}

# Depois crie a função correspondente
def _open_spotify(self, text):
    """Abre o Spotify"""
    if self.system == "Windows":
        # Caminho do executável do Spotify
        subprocess.Popen([r"C:\Users\...\Spotify.exe"])
        return "Abrindo Spotify"
    return "Spotify não disponível"
```

---

## ⚙️ Requisitos Técnicos

**Para controle de volume** (opcional):
```bash
pip install pycaw comtypes
```

**Para screenshots** (opcional):
```bash
pip install pyautogui
```

---

## 🎓 Exemplos de Uso em Sequência

1. 👋 Mostre a mão aberta → Assistente ativa
2. ☝️ Mostre um dedo → Começa a gravar
3. 🎤 Diga: **"calculadora"**
4. ✅ Calculadora abre!

5. ☝️ Mostre um dedo novamente
6. 🎤 Diga: **"pesquisar receitas de bolo"**
7. ✅ Navegador abre com busca!

8. ☝️ Mostre um dedo
9. 🎤 Diga: **"word"**
10. ✅ Microsoft Word abre!

---

**Divirta-se usando seu assistente virtual! 🚀**
