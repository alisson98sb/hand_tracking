# -*- coding: utf-8 -*-
"""
Assistente Virtual Inteligente Controlado por Gestos
Integra: Gestos + Voz + IA Conversacional + Comandos do Sistema
"""
import cv2
import mediapipe as mp
from gesture_recognition import GestureRecognizer, get_action_from_gesture
from voice_recognition import VoiceRecorder
from ai_assistant import AIAssistant
from command_executor import CommandExecutor
import threading
import time
import pyttsx3


class AssistenteIA:
    """
    Assistente virtual inteligente que combina gestos, voz, IA e TTS
    """

    def __init__(self, ai_provider="ollama", ai_model=None, api_key=None, use_tts=True):
        """
        Inicializa o assistente inteligente.

        Args:
            ai_provider (str): "ollama", "openai", ou "groq"
            ai_model (str): Modelo específico (opcional)
            api_key (str): API key para OpenAI/Groq
            use_tts (bool): Usar síntese de voz para respostas
        """
        # MediaPipe para detecção de mãos
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        # Módulos
        self.gesture_recognizer = GestureRecognizer()
        self.voice_recorder = VoiceRecorder(model_size="base")
        self.command_executor = CommandExecutor()

        # IA Conversacional
        self.ai_assistant = AIAssistant(
            provider=ai_provider,
            model=ai_model,
            api_key=api_key
        )

        # TTS (Text-to-Speech)
        self.use_tts = use_tts
        self.tts_engine = None
        self.tts_is_speaking = False  # Flag para controlar se TTS está falando
        if use_tts:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)  # Velocidade
                self.tts_engine.setProperty('volume', 0.9)  # Volume
                print("[TTS] Síntese de voz ativada")
            except:
                print("[AVISO] TTS não disponível")
                self.tts_engine = None

        # Estados
        self.state = 'IDLE'  # IDLE, ACTIVE, RECORDING, PROCESSING, WAITING
        self.last_gesture = 'NONE'
        self.last_transcription = ""
        self.last_response = ""
        self.voice_model_loaded = False
        self.recording_countdown = 0  # Contador de delay antes de gravar

        # Câmera
        self.camera = cv2.VideoCapture(0)
        self.resolution_x = 1280
        self.resolution_y = 720
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution_x)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution_y)

        # Threading
        self.recording_thread = None
        self.is_recording = False
        self.processing_thread = None
        self.is_processing = False

        print("[ASSISTENTE IA] Inicializado!")
        print(f"[IA] Provider: {ai_provider}, Modelo: {ai_model or 'padrão'}")

    def load_voice_model(self):
        """Carrega o modelo Whisper em background"""
        def load():
            self.voice_recorder.load_model()
            self.voice_model_loaded = True
            print("[WHISPER] Modelo carregado!")

        thread = threading.Thread(target=load, daemon=True)
        thread.start()

    def detect_hands(self, frame):
        """Detecta mãos no frame"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)

        all_hands = []
        if result.multi_hand_landmarks:
            for hand_side, hand_landmarks in zip(result.multi_handedness, result.multi_hand_landmarks):
                hand_info = {}
                coords = []

                for mark in hand_landmarks.landmark:
                    coord_x = int(mark.x * self.resolution_x)
                    coord_y = int(mark.y * self.resolution_y)
                    coord_z = int(mark.z * self.resolution_x)
                    coords.append((coord_x, coord_y, coord_z))

                hand_info['coordenadas'] = coords
                if hand_side.classification[0].label == "Left":
                    hand_info["side"] = "Right"
                else:
                    hand_info["side"] = "Left"

                all_hands.append(hand_info)
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

        return frame, all_hands

    def speak(self, text):
        """Fala um texto usando TTS"""
        if self.tts_engine and self.use_tts:
            def tts_speak():
                self.tts_is_speaking = True
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                # Aguardar 1 segundo extra após terminar de falar
                time.sleep(1.0)
                self.tts_is_speaking = False

            thread = threading.Thread(target=tts_speak, daemon=True)
            thread.start()

    def process_command(self, command_text):
        """
        Processa um comando: primeiro tenta executar comando do sistema,
        depois pergunta para a IA.
        """
        if self.is_processing:
            return

        self.is_processing = True
        self.state = 'PROCESSING'

        def process():
            # 1. Tentar executar comando do sistema
            success, result = self.command_executor.execute(command_text)

            if success:
                print(f"[COMANDO] {result}")
                self.last_response = result
                self.speak(result)
            else:
                # 2. Perguntar para a IA
                print(f"[IA] Processando: {command_text}")
                response = self.ai_assistant.chat(command_text)
                print(f"[IA] Resposta: {response}")
                self.last_response = response
                self.speak(response)

            self.is_processing = False
            self.state = 'ACTIVE'

        self.processing_thread = threading.Thread(target=process, daemon=True)
        self.processing_thread.start()

    def start_recording(self):
        """Inicia gravação de voz"""
        if self.is_recording or not self.voice_model_loaded:
            return

        def record():
            self.is_recording = True
            self.state = 'WAITING'  # Estado de espera
            print("\n[AGUARDANDO] Preparando para gravar...")
            self.speak("Escutando")

            # Aguardar TTS terminar de falar + delay extra
            while self.tts_is_speaking:
                time.sleep(0.1)

            # Countdown visual de 3 segundos
            for i in range(3, 0, -1):
                self.recording_countdown = i
                time.sleep(1.0)

            self.recording_countdown = 0
            self.state = 'RECORDING'
            print("[GRAVANDO] Fale AGORA!")

            texto, arquivo = self.voice_recorder.record_and_transcribe(
                duration=5,
                save_file=True
            )

            self.last_transcription = texto if texto else "Erro na transcrição"
            print(f"[TRANSCRIÇÃO] {self.last_transcription}")

            self.is_recording = False

            # Processar comando
            if texto:
                self.process_command(texto)
            else:
                self.state = 'ACTIVE'

        self.recording_thread = threading.Thread(target=record, daemon=True)
        self.recording_thread.start()

    def process_gesture(self, gesture):
        """Processa gestos e atualiza estado"""
        action = get_action_from_gesture(gesture)

        if action == 'ACTIVATE' and self.state == 'IDLE':
            self.state = 'ACTIVE'
            self.speak("Assistente ativado")
            print("\n[ASSISTENTE] Ativado!")

        elif action == 'DEACTIVATE':
            self.state = 'IDLE'
            self.last_transcription = ""
            self.last_response = ""
            self.speak("Assistente desativado")
            print("\n[ASSISTENTE] Desativado")

        elif action == 'RECORD' and self.state == 'ACTIVE' and self.voice_model_loaded:
            self.state = 'RECORDING'
            self.start_recording()

        elif action == 'CANCEL':
            if self.state == 'RECORDING':
                self.state = 'ACTIVE'
                print("\n[ASSISTENTE] Gravação cancelada")

    def draw_ui(self, frame):
        """Desenha interface visual"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2

        # Cores por estado
        state_colors = {
            'IDLE': (100, 100, 100),
            'ACTIVE': (0, 255, 0),
            'WAITING': (255, 255, 0),  # Amarelo para espera
            'RECORDING': (0, 0, 255),
            'PROCESSING': (255, 165, 0)
        }

        state_labels = {
            'IDLE': "INATIVO",
            'ACTIVE': "ATIVO",
            'WAITING': "AGUARDANDO...",
            'RECORDING': "GRAVANDO AGORA!",
            'PROCESSING': "PROCESSANDO..."
        }

        color = state_colors.get(self.state, (100, 100, 100))
        status = state_labels.get(self.state, "DESCONHECIDO")

        # Barra superior
        cv2.rectangle(frame, (0, 0), (self.resolution_x, 100), (0, 0, 0), -1)

        # Status
        cv2.putText(frame, f"Assistente IA: {status}", (20, 35),
                    font, font_scale, color, thickness)

        # Gesto
        gesture_desc = self.gesture_recognizer.get_gesture_description(self.last_gesture)
        cv2.putText(frame, f"Gesto: {gesture_desc}", (20, 65),
                    font, 0.6, (255, 255, 255), 1)

        # Modelo Whisper
        model_status = "OK" if self.voice_model_loaded else "Carregando..."
        model_color = (0, 255, 0) if self.voice_model_loaded else (0, 165, 255)
        cv2.putText(frame, f"Whisper: {model_status}",
                    (self.resolution_x - 250, 35),
                    font, 0.5, model_color, 1)

        # IA Status
        ai_color = (0, 255, 0) if self.ai_assistant.client else (255, 0, 0)
        ai_status = "OK" if self.ai_assistant.client else "OFF"
        cv2.putText(frame, f"IA ({self.ai_assistant.provider}): {ai_status}",
                    (self.resolution_x - 250, 65),
                    font, 0.5, ai_color, 1)

        # Última transcrição
        if self.last_transcription:
            cv2.rectangle(frame, (10, self.resolution_y - 120),
                          (self.resolution_x - 10, self.resolution_y - 70),
                          (40, 40, 40), -1)
            cv2.putText(frame, f"Voce: {self.last_transcription}",
                        (20, self.resolution_y - 95),
                        font, 0.6, (0, 255, 255), 2)

        # Resposta da IA
        if self.last_response:
            # Quebrar texto longo em múltiplas linhas
            max_chars = 80
            if len(self.last_response) > max_chars:
                response_display = self.last_response[:max_chars] + "..."
            else:
                response_display = self.last_response

            cv2.rectangle(frame, (10, self.resolution_y - 60),
                          (self.resolution_x - 10, self.resolution_y - 10),
                          (20, 20, 60), -1)
            cv2.putText(frame, f"IA: {response_display}",
                        (20, self.resolution_y - 30),
                        font, 0.6, (100, 255, 100), 2)

        # Instruções
        if self.state == 'IDLE':
            cv2.putText(frame, "Mostre a mao aberta para ativar",
                        (20, 90), font, 0.5, (200, 200, 200), 1)
        elif self.state == 'ACTIVE':
            cv2.putText(frame, "Mostre 1 dedo para gravar comando",
                        (20, 90), font, 0.5, (200, 200, 200), 1)

        # CONTADOR VISUAL GRANDE NO CENTRO DA TELA
        if self.recording_countdown > 0:
            # Fundo semi-transparente
            overlay = frame.copy()
            center_x = self.resolution_x // 2
            center_y = self.resolution_y // 2

            # Círculo de fundo
            cv2.circle(overlay, (center_x, center_y), 150, (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

            # Número do contador GIGANTE
            countdown_text = str(self.recording_countdown)
            font_size = 10
            countdown_thickness = 15
            text_size = cv2.getTextSize(countdown_text, font, font_size, countdown_thickness)[0]
            text_x = center_x - text_size[0] // 2
            text_y = center_y + text_size[1] // 2

            # Efeito de brilho (sombra branca)
            cv2.putText(frame, countdown_text, (text_x + 5, text_y + 5),
                        font, font_size, (255, 255, 255), countdown_thickness + 2)
            # Número principal em amarelo
            cv2.putText(frame, countdown_text, (text_x, text_y),
                        font, font_size, (0, 255, 255), countdown_thickness)

            # Texto auxiliar
            helper_text = "Prepare-se para falar..."
            helper_size = cv2.getTextSize(helper_text, font, 1.2, 2)[0]
            helper_x = center_x - helper_size[0] // 2
            cv2.putText(frame, helper_text, (helper_x, center_y + 120),
                        font, 1.2, (255, 255, 255), 2)

        # Indicador de gravação ativa
        elif self.state == 'RECORDING':
            # Indicador piscante de "REC"
            if int(time.time() * 2) % 2 == 0:  # Pisca a cada 0.5s
                cv2.circle(frame, (50, 50), 15, (0, 0, 255), -1)
                cv2.putText(frame, "REC", (70, 55),
                            font, 0.7, (0, 0, 255), 2)

        return frame

    def run(self):
        """Loop principal"""
        print("\n" + "="*70)
        print("ASSISTENTE VIRTUAL INTELIGENTE CONTROLADO POR GESTOS")
        print("="*70)
        print("\nGestos:")
        print("  ✋ Mão aberta     → Ativar assistente")
        print("  ☝️  Um dedo       → Gravar comando (5s)")
        print("  👊 Punho fechado → Desativar")
        print("  ✌️  Dois dedos    → Cancelar")
        print("\nFuncionalidades:")
        print("  • Comandos do sistema (abrir apps, volume, etc)")
        print(f"  • IA conversacional ({self.ai_assistant.provider})")
        print(f"  • Síntese de voz (TTS): {'Ativa' if self.use_tts else 'Desativada'}")
        print("\nPressione 'Esc' para sair")
        print("="*70 + "\n")

        self.load_voice_model()

        try:
            while self.camera.isOpened():
                ret, frame = self.camera.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
                frame, hands = self.detect_hands(frame)

                if hands:
                    hand = hands[0]
                    gesture = self.gesture_recognizer.recognize_gesture(hand)

                    if gesture != self.last_gesture:
                        self.last_gesture = gesture
                        self.process_gesture(gesture)
                else:
                    self.last_gesture = 'NONE'

                frame = self.draw_ui(frame)
                cv2.imshow("Assistente IA por Gestos", frame)

                key = cv2.waitKey(1)
                if key == 27:  # ESC
                    break

        finally:
            self.camera.release()
            cv2.destroyAllWindows()
            print("\nAssistente encerrado.")


if __name__ == "__main__":
    # Configurar aqui o provider de IA
    assistente = AssistenteIA(
        ai_provider="ollama",          # Opcoes: "ollama", "openai", "groq"
        ai_model="deepseek-r1:1.5b",   # Modelo menor (1.1GB) - ideal para pouca RAM
        api_key=None,                  # Necessário para OpenAI/Groq
        use_tts=True                   # Ativar síntese de voz
    )
    assistente.run()
