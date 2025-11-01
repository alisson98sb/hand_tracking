import sounddevice as sd
import whisper
import numpy as np
from scipy.io.wavfile import write
import os
from datetime import datetime


class VoiceRecorder:
    """
    Classe responsável pela gravação de áudio e transcrição usando Whisper.
    """

    def __init__(self, sample_rate=16000, model_size="base"):
        """
        Inicializa o gravador de voz.

        Args:
            sample_rate (int): Taxa de amostragem do áudio (padrão: 16000 Hz, recomendado para Whisper)
            model_size (str): Tamanho do modelo Whisper ("tiny", "base", "small", "medium", "large")
                             - tiny: mais rápido, menos preciso
                             - base: equilíbrio entre velocidade e precisão
                             - small: melhor precisão, mais lento
        """
        self.sample_rate = sample_rate
        self.model_size = model_size
        self.model = None
        self.is_recording = False
        self.audio_data = None

        # Criar diretório temp se não existir
        if not os.path.exists("temp"):
            os.makedirs("temp")

    def load_model(self):
        """
        Carrega o modelo Whisper. Esta operação pode demorar alguns segundos
        na primeira execução, pois faz o download do modelo.
        """
        if self.model is None:
            print(f"Carregando modelo Whisper '{self.model_size}'...")
            self.model = whisper.load_model(self.model_size)
            print("Modelo carregado com sucesso!")

    def record_audio(self, duration=5, device=None):
        """
        Grava áudio do microfone por uma duração específica.

        Args:
            duration (int): Duração da gravação em segundos (padrão: 5)
            device (int): ID do dispositivo de áudio (None usa o padrão do sistema)

        Returns:
            numpy.ndarray: Dados de áudio gravados
        """
        print(f"Gravando áudio por {duration} segundos...")
        self.is_recording = True

        try:
            # Gravar áudio
            self.audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,  # Mono
                dtype='float32',
                device=device
            )
            sd.wait()  # Aguardar conclusão da gravação
            self.is_recording = False
            print("Gravação concluída!")
            return self.audio_data

        except Exception as e:
            self.is_recording = False
            print(f"Erro ao gravar áudio: {e}")
            return None

    def save_audio(self, audio_data=None, filename=None):
        """
        Salva os dados de áudio em um arquivo WAV.

        Args:
            audio_data (numpy.ndarray): Dados de áudio (usa self.audio_data se None)
            filename (str): Nome do arquivo (gera automaticamente se None)

        Returns:
            str: Caminho do arquivo salvo
        """
        if audio_data is None:
            audio_data = self.audio_data

        if audio_data is None:
            print("Nenhum áudio para salvar!")
            return None

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"temp/comando_{timestamp}.wav"

        # Normalizar e converter para int16
        audio_normalized = np.int16(audio_data * 32767)
        write(filename, self.sample_rate, audio_normalized)
        print(f"Áudio salvo em: {filename}")
        return filename

    def transcribe_audio(self, audio_file=None, language="pt"):
        """
        Transcreve um arquivo de áudio usando Whisper.

        Args:
            audio_file (str): Caminho do arquivo de áudio (usa o último gravado se None)
            language (str): Idioma do áudio (padrão: "pt" para português)

        Returns:
            dict: Resultado da transcrição contendo:
                - text: texto transcrito
                - segments: segmentos detalhados
                - language: idioma detectado
        """
        # Carregar modelo se ainda não foi carregado
        if self.model is None:
            self.load_model()

        if audio_file is None:
            print("Erro: Nenhum arquivo de áudio especificado!")
            return None

        if not os.path.exists(audio_file):
            print(f"Erro: Arquivo '{audio_file}' não encontrado!")
            return None

        print(f"Transcrevendo áudio...")
        try:
            result = self.model.transcribe(audio_file, language=language)
            print(f"Transcrição concluída: \"{result['text']}\"")
            return result

        except Exception as e:
            print(f"Erro ao transcrever áudio: {e}")
            return None

    def record_and_transcribe(self, duration=5, save_file=True, language="pt"):
        """
        Método conveniente que grava áudio e transcreve em uma única operação.

        Args:
            duration (int): Duração da gravação em segundos
            save_file (bool): Se True, salva o arquivo de áudio
            language (str): Idioma do áudio

        Returns:
            tuple: (texto_transcrito, caminho_arquivo)
        """
        # Gravar áudio
        audio_data = self.record_audio(duration)
        if audio_data is None:
            return None, None

        # Salvar áudio
        audio_file = self.save_audio(audio_data)
        if audio_file is None:
            return None, None

        # Transcrever
        result = self.transcribe_audio(audio_file, language)
        if result is None:
            return None, audio_file

        # Deletar arquivo temporário se não for necessário mantê-lo
        if not save_file:
            try:
                os.remove(audio_file)
                print(f"Arquivo temporário removido: {audio_file}")
            except Exception as e:
                print(f"Erro ao remover arquivo: {e}")

        return result['text'], audio_file

    def list_audio_devices(self):
        """
        Lista todos os dispositivos de áudio disponíveis no sistema.
        Útil para escolher um microfone específico.
        """
        print("\n=== Dispositivos de áudio disponíveis ===")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:  # Apenas dispositivos de entrada
                print(f"[{i}] {device['name']} - {device['max_input_channels']} canais")
        print("=========================================\n")
        return devices


# Exemplo de uso
if __name__ == "__main__":
    # Criar instância do gravador
    recorder = VoiceRecorder(model_size="base")

    # Listar dispositivos de áudio disponíveis (opcional)
    # recorder.list_audio_devices()

    # Carregar modelo Whisper (pode demorar na primeira vez)
    recorder.load_model()

    print("\nPronto para gravar!")
    print("Pressione Enter para iniciar a gravação de 5 segundos...")
    input()

    # Gravar e transcrever
    texto, arquivo = recorder.record_and_transcribe(duration=5, save_file=True)

    if texto:
        print(f"\n=== RESULTADO ===")
        print(f"Texto transcrito: {texto}")
        print(f"Arquivo salvo em: {arquivo}")
    else:
        print("Falha na transcrição.")
