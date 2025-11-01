# -*- coding: utf-8 -*-
"""
Módulo de reconhecimento de gestos
Identifica gestos específicos das mãos usando os landmarks do MediaPipe
"""


class GestureRecognizer:
    """
    Classe para reconhecer gestos específicos baseados nos landmarks da mão
    """

    def __init__(self):
        """Inicializa o reconhecedor de gestos"""
        pass

    def count_fingers(self, hand):
        """
        Conta quantos dedos estão levantados em uma mão.

        Args:
            hand (dict): Dicionário com informações da mão contendo:
                - 'coordenadas': Lista de 21 landmarks (x, y, z)
                - 'side': 'Left' ou 'Right'

        Returns:
            tuple: (total_dedos_levantados, lista_dedos_status)
                lista_dedos_status: [polegar, indicador, médio, anelar, mínimo]
        """
        if not hand or 'coordenadas' not in hand:
            return 0, [False, False, False, False, False]

        coords = hand['coordenadas']
        fingers = []

        # Verificar polegar (lógica diferente dos outros dedos)
        # Polegar: compara posição X ao invés de Y
        if hand.get('side') == 'Right':
            # Mão direita: polegar levantado se tip (4) está à direita de ip (3)
            thumb_up = coords[4][0] > coords[3][0]
        else:
            # Mão esquerda: polegar levantado se tip (4) está à esquerda de ip (3)
            thumb_up = coords[4][0] < coords[3][0]

        fingers.append(thumb_up)

        # Verificar outros 4 dedos (índice, médio, anelar, mínimo)
        # Landmarks: 8, 12, 16, 20 (tips) comparados com 6, 10, 14, 18 (pips)
        for fingertip in [8, 12, 16, 20]:
            # Dedo levantado se tip está acima (menor Y) que pip
            finger_up = coords[fingertip][1] < coords[fingertip - 2][1]
            fingers.append(finger_up)

        total = sum(fingers)
        return total, fingers

    def recognize_gesture(self, hand):
        """
        Reconhece um gesto específico baseado nos dedos levantados.

        Args:
            hand (dict): Dicionário com informações da mão

        Returns:
            str: Nome do gesto reconhecido ou 'UNKNOWN'
        """
        if not hand:
            return 'NONE'

        total, fingers = self.count_fingers(hand)

        # Gestos específicos
        if total == 0:
            return 'FIST'  # Punho fechado

        elif total == 5:
            return 'OPEN_HAND'  # Mão aberta

        elif total == 1:
            # Verificar qual dedo está levantado
            if fingers[1]:  # Indicador
                return 'ONE_FINGER'
            elif fingers[0]:  # Polegar
                return 'THUMBS_UP'

        elif total == 2:
            # Dois dedos levantados
            if fingers[1] and fingers[2]:  # Indicador + Médio
                return 'PEACE'
            elif fingers[0] and fingers[4]:  # Polegar + Mínimo
                return 'CALL_ME'

        elif total == 3:
            # Três dedos levantados
            if fingers[1] and fingers[2] and fingers[3]:  # Indicador + Médio + Anelar
                return 'THREE'

        elif total == 4:
            # Quatro dedos (sem polegar geralmente)
            if not fingers[0]:
                return 'FOUR'

        return 'UNKNOWN'

    def get_gesture_description(self, gesture):
        """
        Retorna descrição em português do gesto.

        Args:
            gesture (str): Nome do gesto

        Returns:
            str: Descrição do gesto
        """
        descriptions = {
            'NONE': 'Nenhuma mão detectada',
            'FIST': 'Punho fechado',
            'OPEN_HAND': 'Mão aberta',
            'ONE_FINGER': 'Um dedo (indicador)',
            'THUMBS_UP': 'Polegar para cima',
            'PEACE': 'Sinal de paz (V)',
            'CALL_ME': 'Me liga (polegar + mínimo)',
            'THREE': 'Três dedos',
            'FOUR': 'Quatro dedos',
            'UNKNOWN': 'Gesto não reconhecido'
        }
        return descriptions.get(gesture, 'Desconhecido')


# Mapeamento de gestos para ações do assistente
GESTURE_ACTIONS = {
    'OPEN_HAND': 'ACTIVATE',      # Mão aberta = Ativar assistente
    'ONE_FINGER': 'RECORD',       # Um dedo = Iniciar gravação
    'FIST': 'DEACTIVATE',         # Punho = Desativar assistente
    'PEACE': 'CANCEL',            # Dois dedos = Cancelar operação
}


def get_action_from_gesture(gesture):
    """
    Mapeia um gesto para uma ação do assistente.

    Args:
        gesture (str): Nome do gesto

    Returns:
        str or None: Ação correspondente ou None
    """
    return GESTURE_ACTIONS.get(gesture, None)


# Exemplo de uso
if __name__ == "__main__":
    # Teste do reconhecedor
    recognizer = GestureRecognizer()

    # Simular mão com todos os dedos levantados
    test_hand = {
        'side': 'Right',
        'coordenadas': [
            (0, 0, 0),   # 0: pulso
            (10, 10, 0), (20, 20, 0), (30, 30, 0), (50, 20, 0),  # 1-4: polegar (4 é tip)
            (40, 40, 0), (50, 50, 0), (60, 60, 0), (70, 10, 0),  # 5-8: indicador (8 é tip)
            (80, 40, 0), (90, 50, 0), (100, 60, 0), (110, 10, 0), # 9-12: médio (12 é tip)
            (120, 40, 0), (130, 50, 0), (140, 60, 0), (150, 10, 0), # 13-16: anelar (16 é tip)
            (160, 40, 0), (170, 50, 0), (180, 60, 0), (190, 10, 0)  # 17-20: mínimo (20 é tip)
        ]
    }

    total, fingers = recognizer.count_fingers(test_hand)
    gesture = recognizer.recognize_gesture(test_hand)
    description = recognizer.get_gesture_description(gesture)
    action = get_action_from_gesture(gesture)

    print(f"Dedos levantados: {total}")
    print(f"Status dos dedos: {fingers}")
    print(f"Gesto: {gesture} - {description}")
    print(f"Acao: {action}")
