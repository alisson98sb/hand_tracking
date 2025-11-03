# -*- coding: utf-8 -*-
"""
Executor de Comandos Customizados
Mapeia comandos de voz para ações específicas do sistema
"""
import os
import subprocess
import webbrowser
from datetime import datetime
import platform


class CommandExecutor:
    """
    Executa comandos específicos do sistema baseados em palavras-chave
    """

    def __init__(self):
        """Inicializa o executor de comandos"""
        self.system = platform.system()  # Windows, Linux, Darwin (macOS)
        self.command_history = []

        # Mapeamento de comandos com PALAVRAS-CHAVE SIMPLES
        self.commands = {
            # Navegadores - Comandos naturais e diretos
            "navegador": self._open_browser,
            "abrir navegador": self._open_browser,
            "chrome": self._open_chrome,
            "abrir chrome": self._open_chrome,
            "google chrome": self._open_chrome,
            "firefox": self._open_firefox,
            "abrir firefox": self._open_firefox,
            "edge": self._open_edge,
            "abrir edge": self._open_edge,

            # Aplicativos - Palavra única OU comando completo
            "calculadora": self._open_calculator,
            "abrir calculadora": self._open_calculator,
            "calc": self._open_calculator,
            "bloco de notas": self._open_notepad,
            "abrir bloco de notas": self._open_notepad,
            "notepad": self._open_notepad,
            "explorador": self._open_explorer,
            "abrir explorador": self._open_explorer,
            "pasta": self._open_explorer,
            "arquivos": self._open_explorer,
            "terminal": self._open_terminal,
            "abrir terminal": self._open_terminal,
            "cmd": self._open_terminal,
            "prompt": self._open_terminal,

            # Aplicativos Profissionais
            "word": self._open_word,
            "abrir word": self._open_word,
            "microsoft word": self._open_word,
            "excel": self._open_excel,
            "abrir excel": self._open_excel,
            "powerpoint": self._open_powerpoint,
            "abrir powerpoint": self._open_powerpoint,
            "vscode": self._open_vscode,
            "abrir vscode": self._open_vscode,
            "visual studio code": self._open_vscode,
            "code": self._open_vscode,
            "postman": self._open_postman,
            "abrir postman": self._open_postman,

            # Sistema
            "aumentar volume": self._volume_up,
            "volume alto": self._volume_up,
            "diminuir volume": self._volume_down,
            "volume baixo": self._volume_down,
            "silenciar": self._mute,
            "mudo": self._mute,

            # Utilidades
            "que horas são": self._tell_time,
            "horas": self._tell_time,
            "hora": self._tell_time,
            "que dia é hoje": self._tell_date,
            "data": self._tell_date,
            "dia": self._tell_date,
            "tirar screenshot": self._screenshot,
            "screenshot": self._screenshot,
            "print screen": self._screenshot,

            # Pesquisa
            "pesquisar": self._search_web,
            "buscar": self._search_web,
            "procurar": self._search_web,
        }

    def execute(self, command_text):
        """
        Executa um comando baseado no texto transcrito.

        Args:
            command_text (str): Texto do comando de voz

        Returns:
            tuple: (sucesso, mensagem)
        """
        if not command_text:
            return False, "Comando vazio"

        command_lower = command_text.lower().strip()

        # Verificar comandos diretos
        for keyword, action in self.commands.items():
            if keyword in command_lower:
                try:
                    result = action(command_lower)
                    self.command_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "command": command_text,
                        "keyword": keyword,
                        "success": True
                    })
                    return True, result
                except Exception as e:
                    error_msg = f"Erro ao executar '{keyword}': {str(e)}"
                    return False, error_msg

        # Comando não reconhecido
        return False, None

    # ===== NAVEGADORES =====

    def _open_browser(self, text):
        """Abre o navegador padrão"""
        webbrowser.open("https://www.google.com")
        return "Abrindo navegador"

    def _open_chrome(self, text):
        """Abre o Google Chrome"""
        if self.system == "Windows":
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return "Abrindo Chrome"
        webbrowser.open("https://www.google.com")
        return "Abrindo navegador padrão"

    def _open_firefox(self, text):
        """Abre o Firefox"""
        webbrowser.get('firefox').open("https://www.google.com") if 'firefox' else webbrowser.open("https://www.google.com")
        return "Abrindo Firefox"

    def _open_edge(self, text):
        """Abre o Microsoft Edge"""
        if self.system == "Windows":
            subprocess.Popen(["start", "microsoft-edge:"], shell=True)
            return "Abrindo Edge"
        return "Edge não disponível neste sistema"

    # ===== APLICATIVOS =====

    def _open_calculator(self, text):
        """Abre a calculadora"""
        if self.system == "Windows":
            subprocess.Popen(["calc.exe"])
            return "Abrindo calculadora"
        elif self.system == "Darwin":
            subprocess.Popen(["open", "-a", "Calculator"])
            return "Abrindo calculadora"
        return "Calculadora não disponível"

    def _open_notepad(self, text):
        """Abre o bloco de notas"""
        if self.system == "Windows":
            subprocess.Popen(["notepad.exe"])
            return "Abrindo bloco de notas"
        return "Bloco de notas não disponível"

    def _open_explorer(self, text):
        """Abre o explorador de arquivos"""
        if self.system == "Windows":
            subprocess.Popen(["explorer.exe"])
            return "Abrindo explorador de arquivos"
        elif self.system == "Darwin":
            subprocess.Popen(["open", "."])
            return "Abrindo Finder"
        return "Explorador não disponível"

    def _open_terminal(self, text):
        """Abre o terminal"""
        if self.system == "Windows":
            subprocess.Popen(["cmd.exe"])
            return "Abrindo terminal"
        elif self.system == "Darwin":
            subprocess.Popen(["open", "-a", "Terminal"])
            return "Abrindo terminal"
        else:
            subprocess.Popen(["gnome-terminal"])
            return "Abrindo terminal"

    # ===== APLICATIVOS PROFISSIONAIS =====

    def _open_word(self, text):
        """Abre o Microsoft Word"""
        if self.system == "Windows":
            paths = [
                r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
                r"C:\Program Files\Microsoft Office\Office16\WINWORD.EXE",
                r"C:\Program Files (x86)\Microsoft Office\Office16\WINWORD.EXE",
            ]
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return "Abrindo Word"
            return "Word não encontrado. Certifique-se que está instalado."
        return "Word disponível apenas no Windows"

    def _open_excel(self, text):
        """Abre o Microsoft Excel"""
        if self.system == "Windows":
            paths = [
                r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
                r"C:\Program Files\Microsoft Office\Office16\EXCEL.EXE",
                r"C:\Program Files (x86)\Microsoft Office\Office16\EXCEL.EXE",
            ]
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return "Abrindo Excel"
            return "Excel não encontrado. Certifique-se que está instalado."
        return "Excel disponível apenas no Windows"

    def _open_powerpoint(self, text):
        """Abre o Microsoft PowerPoint"""
        if self.system == "Windows":
            paths = [
                r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
                r"C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE",
                r"C:\Program Files (x86)\Microsoft Office\Office16\POWERPNT.EXE",
            ]
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return "Abrindo PowerPoint"
            return "PowerPoint não encontrado. Certifique-se que está instalado."
        return "PowerPoint disponível apenas no Windows"

    def _open_vscode(self, text):
        """Abre o Visual Studio Code"""
        if self.system == "Windows":
            paths = [
                r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getenv("USERNAME")),
                r"C:\Program Files\Microsoft VS Code\Code.exe",
                r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
            ]
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return "Abrindo VS Code"
            # Tentar pelo comando 'code'
            try:
                subprocess.Popen(["code"])
                return "Abrindo VS Code"
            except:
                return "VS Code não encontrado. Certifique-se que está instalado."
        elif self.system == "Darwin":
            subprocess.Popen(["open", "-a", "Visual Studio Code"])
            return "Abrindo VS Code"
        else:
            subprocess.Popen(["code"])
            return "Abrindo VS Code"

    def _open_postman(self, text):
        """Abre o Postman"""
        if self.system == "Windows":
            paths = [
                r"C:\Users\{}\AppData\Local\Postman\Postman.exe".format(os.getenv("USERNAME")),
                r"C:\Program Files\Postman\Postman.exe",
                r"C:\Program Files (x86)\Postman\Postman.exe",
            ]
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return "Abrindo Postman"
            return "Postman não encontrado. Certifique-se que está instalado."
        elif self.system == "Darwin":
            subprocess.Popen(["open", "-a", "Postman"])
            return "Abrindo Postman"
        else:
            subprocess.Popen(["postman"])
            return "Abrindo Postman"

    # ===== SISTEMA =====

    def _volume_up(self, text):
        """Aumenta o volume"""
        if self.system == "Windows":
            # Usar biblioteca pycaw se disponível
            try:
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                current = volume.GetMasterVolumeLevelScalar()
                volume.SetMasterVolumeLevelScalar(min(1.0, current + 0.1), None)
                return "Volume aumentado"
            except:
                return "Controle de volume não disponível (instale: pip install pycaw)"
        return "Controle de volume não disponível neste sistema"

    def _volume_down(self, text):
        """Diminui o volume"""
        if self.system == "Windows":
            try:
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                current = volume.GetMasterVolumeLevelScalar()
                volume.SetMasterVolumeLevelScalar(max(0.0, current - 0.1), None)
                return "Volume diminuído"
            except:
                return "Controle de volume não disponível"
        return "Controle de volume não disponível neste sistema"

    def _mute(self, text):
        """Silencia o áudio"""
        return "Função de silenciar não implementada"

    # ===== UTILIDADES =====

    def _tell_time(self, text):
        """Informa a hora atual"""
        now = datetime.now()
        return f"São {now.hour} horas e {now.minute} minutos"

    def _tell_date(self, text):
        """Informa a data atual"""
        now = datetime.now()
        dias = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
        meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                 "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
        return f"Hoje é {dias[now.weekday()]}, {now.day} de {meses[now.month-1]}"

    def _screenshot(self, text):
        """Tira screenshot"""
        try:
            import pyautogui
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            pyautogui.screenshot(filename)
            return f"Screenshot salva como {filename}"
        except ImportError:
            return "PyAutoGUI não instalado (pip install pyautogui)"

    def _search_web(self, text):
        """Faz busca na web"""
        # Extrair termo de busca
        keywords = ["pesquisar", "buscar", "procurar"]
        search_term = text
        for kw in keywords:
            if kw in text.lower():
                search_term = text.lower().split(kw, 1)[1].strip()
                break

        if search_term:
            url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Pesquisando por: {search_term}"
        return "Termo de busca não encontrado"

    def get_available_commands(self):
        """Retorna lista de comandos disponíveis"""
        return list(self.commands.keys())


# Teste do módulo
if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTE DO EXECUTOR DE COMANDOS")
    print("="*60 + "\n")

    executor = CommandExecutor()

    # Testar alguns comandos
    test_commands = [
        "Que horas são",
        "Que dia é hoje",
        "Abrir calculadora",
        "Pesquisar Python tutorial"
    ]

    for cmd in test_commands:
        print(f"\nComando: {cmd}")
        success, result = executor.execute(cmd)
        if success:
            print(f"[OK] {result}")
        else:
            print(f"[X] Comando nao reconhecido")

    print("\n" + "="*60)
    print("COMANDOS DISPONÍVEIS:")
    print("="*60)
    for cmd in executor.get_available_commands():
        print(f"  - {cmd}")
    print("="*60 + "\n")
