# -*- coding: utf-8 -*-
"""
Assistente Virtual Controlado por Gestos
Integra detecção de mãos, reconhecimento de gestos e reconhecimento de voz
"""
import cv2
import mediapipe as mp
from gesture_recognition import GestureRecognizer, get_action_from_gesture
from voice_recognition import VoiceRecorder
import threading
import time


class AssistenteGestos:
    """
    Assistente virtual que responde a gestos das mãos
    """

    def __init__(self):
        """Inicializa o assistente"""
        # MediaPipe para detecção de mãos
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        # Reconhecedor de gestos
        self.gesture_recognizer = GestureRecognizer()

        # Gravador de voz
        self.voice_recorder = VoiceRecorder(model_size="base")
        self.voice_model_loaded = False

        # Estados do assistente
        self.state = 'IDLE'  # IDLE, ACTIVE, RECORDING
        self.last_gesture = 'NONE'
        self.last_transcription = ""

        # Câmera
        self.camera = cv2.VideoCapture(0)
        self.resolution_x = 1280
        self.resolution_y = 720
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution_x)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution_y)

        # Thread de gravação
        self.recording_thread = None
        self.is_recording = False

        print("Assistente inicializado!")
        print("Carregando modelo Whisper em segundo plano...")

    def load_voice_model(self):
        """Carrega o modelo Whisper em uma thread separada"""
        def load():
            self.voice_recorder.load_model()
            self.voice_model_loaded = True
            print("Modelo Whisper carregado!")

        thread = threading.Thread(target=load, daemon=True)
        thread.start()

    def detect_hands(self, frame):
        """
        Detecta mãos no frame usando MediaPipe.

        Args:
            frame: Frame da câmera

        Returns:
            tuple: (frame_anotado, lista_de_maos)
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)

        all_hands = []
        if result.multi_hand_landmarks:
            for hand_side, hand_landmarks in zip(result.multi_handedness, result.multi_hand_landmarks):
                hand_info = {}
                coords = []

                # Extrair coordenadas dos landmarks
                for mark in hand_landmarks.landmark:
                    coord_x = int(mark.x * self.resolution_x)
                    coord_y = int(mark.y * self.resolution_y)
                    coord_z = int(mark.z * self.resolution_x)
                    coords.append((coord_x, coord_y, coord_z))

                hand_info['coordenadas'] = coords
                # Inverter lado por causa do espelhamento da câmera
                if hand_side.classification[0].label == "Left":
                    hand_info["side"] = "Right"
                else:
                    hand_info["side"] = "Left"

                all_hands.append(hand_info)

                # Desenhar landmarks no frame
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

        return frame, all_hands

    def start_recording(self):
        """Inicia gravação de voz em uma thread separada"""
        if self.is_recording or not self.voice_model_loaded:
            return

        def record():
            self.is_recording = True
            print("\n[GRAVANDO] Fale agora...")
            texto, arquivo = self.voice_recorder.record_and_transcribe(
                duration=5,
                save_file=True
            )
            self.last_transcription = texto if texto else "Erro na transcricao"
            print(f"[TRANSCRICAO] Voce disse: {self.last_transcription}")
            self.is_recording = False
            self.state = 'ACTIVE'  # Voltar para estado ativo

        self.recording_thread = threading.Thread(target=record, daemon=True)
        self.recording_thread.start()

    def process_gesture(self, gesture):
        """
        Processa um gesto e atualiza o estado do assistente.

        Args:
            gesture (str): Nome do gesto reconhecido
        """
        action = get_action_from_gesture(gesture)

        if action == 'ACTIVATE' and self.state == 'IDLE':
            self.state = 'ACTIVE'
            print("\n[ASSISTENTE] Ativado! Mostre um dedo para gravar.")

        elif action == 'DEACTIVATE':
            self.state = 'IDLE'
            self.last_transcription = ""
            print("\n[ASSISTENTE] Desativado.")

        elif action == 'RECORD' and self.state == 'ACTIVE' and self.voice_model_loaded:
            self.state = 'RECORDING'
            self.start_recording()

        elif action == 'CANCEL' and self.state == 'RECORDING':
            self.state = 'ACTIVE'
            print("\n[ASSISTENTE] Gravacao cancelada.")

    def draw_ui(self, frame):
        """
        Desenha interface do usuário no frame.

        Args:
            frame: Frame da câmera

        Returns:
            frame: Frame com UI desenhada
        """
        # Configuração do texto
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2

        # Cor baseada no estado
        if self.state == 'IDLE':
            color = (100, 100, 100)  # Cinza
            status = "INATIVO"
        elif self.state == 'ACTIVE':
            color = (0, 255, 0)  # Verde
            status = "ATIVO"
        elif self.state == 'RECORDING':
            color = (0, 0, 255)  # Vermelho
            status = "GRAVANDO..."

        # Desenhar barra superior
        cv2.rectangle(frame, (0, 0), (self.resolution_x, 80), (0, 0, 0), -1)

        # Status do assistente
        cv2.putText(frame, f"Assistente: {status}", (20, 35),
                    font, font_scale, color, thickness)

        # Gesto atual
        gesture_desc = self.gesture_recognizer.get_gesture_description(self.last_gesture)
        cv2.putText(frame, f"Gesto: {gesture_desc}", (20, 65),
                    font, 0.6, (255, 255, 255), 1)

        # Última transcrição
        if self.last_transcription:
            # Fundo para o texto
            text_size = cv2.getTextSize(self.last_transcription, font, 0.6, 2)[0]
            cv2.rectangle(frame, (10, self.resolution_y - 60),
                          (text_size[0] + 30, self.resolution_y - 10),
                          (0, 0, 0), -1)
            cv2.putText(frame, f"Comando: {self.last_transcription}",
                        (20, self.resolution_y - 30),
                        font, 0.6, (0, 255, 255), 2)

        # Instruções
        if self.state == 'IDLE':
            cv2.putText(frame, "Mostre a mao aberta para ativar",
                        (self.resolution_x - 400, 35),
                        font, 0.5, (200, 200, 200), 1)
        elif self.state == 'ACTIVE':
            cv2.putText(frame, "Mostre 1 dedo para gravar",
                        (self.resolution_x - 350, 35),
                        font, 0.5, (200, 200, 200), 1)

        # Indicador de modelo carregado
        model_status = "OK" if self.voice_model_loaded else "Carregando..."
        model_color = (0, 255, 0) if self.voice_model_loaded else (0, 165, 255)
        cv2.putText(frame, f"Whisper: {model_status}",
                    (self.resolution_x - 200, 65),
                    font, 0.5, model_color, 1)

        return frame

    def run(self):
        """Loop principal do assistente"""
        print("\n" + "="*60)
        print("ASSISTENTE VIRTUAL CONTROLADO POR GESTOS")
        print("="*60)
        print("\nGestos:")
        print("  - Mao aberta (5 dedos) = Ativar assistente")
        print("  - Um dedo (indicador) = Iniciar gravacao de voz")
        print("  - Punho fechado = Desativar assistente")
        print("  - Dois dedos (V) = Cancelar operacao")
        print("\nPressione 'Esc' para sair")
        print("="*60 + "\n")

        # Carregar modelo Whisper em background
        self.load_voice_model()

        try:
            while self.camera.isOpened():
                ret, frame = self.camera.read()
                if not ret:
                    print("Erro ao capturar frame")
                    break

                # Espelhar frame
                frame = cv2.flip(frame, 1)

                # Detectar mãos
                frame, hands = self.detect_hands(frame)

                # Reconhecer gesto
                if hands:
                    hand = hands[0]
                    gesture = self.gesture_recognizer.recognize_gesture(hand)

                    # Só processar se o gesto mudou
                    if gesture != self.last_gesture:
                        self.last_gesture = gesture
                        self.process_gesture(gesture)
                else:
                    self.last_gesture = 'NONE'

                # Desenhar UI
                frame = self.draw_ui(frame)

                # Mostrar frame
                cv2.imshow("Assistente por Gestos", frame)

                # Verificar tecla
                key = cv2.waitKey(1)
                if key == 27:  # ESC
                    break

        finally:
            self.camera.release()
            cv2.destroyAllWindows()
            print("\nAssistente encerrado.")


if __name__ == "__main__":
    assistente = AssistenteGestos()
    assistente.run()
