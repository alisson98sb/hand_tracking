# -*- coding: utf-8 -*-
"""
Módulo de IA Conversacional
Suporta múltiplos providers: Ollama (local), OpenAI, Groq
"""
import os
import json
from datetime import datetime


class AIAssistant:
    """
    Assistente de IA que processa comandos de voz e gera respostas inteligentes
    """

    def __init__(self, provider="ollama", model=None, api_key=None):
        """
        Inicializa o assistente de IA.

        Args:
            provider (str): "ollama", "openai", ou "groq"
            model (str): Nome do modelo (opcional, usa padrão do provider)
            api_key (str): Chave de API (necessário para OpenAI/Groq)
        """
        self.provider = provider.lower()
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        self.client = None
        self.conversation_history = []

        # Modelos padrão por provider
        self.default_models = {
            "ollama": "llama3.2:3b",  # Modelo rápido e eficiente
            "openai": "gpt-4o-mini",  # Modelo econômico da OpenAI
            "groq": "llama-3.1-8b-instant"  # Modelo rápido do Groq
        }

        self.model = model or self.default_models.get(self.provider, "llama3.2:3b")

        # System prompt em português
        self.system_prompt = """Você é um assistente virtual pessoal prestativo e amigável.
Responda em português brasileiro de forma concisa e clara.
Se não souber algo, admita honestamente.
Mantenha respostas curtas (máximo 2-3 frases) para facilitar a leitura."""

        self._initialize_client()

    def _initialize_client(self):
        """Inicializa o cliente do provider escolhido"""
        if self.provider == "ollama":
            try:
                import ollama
                self.client = ollama
                print(f"[IA] Cliente Ollama inicializado com modelo: {self.model}")
            except ImportError:
                print("[ERRO] Ollama não instalado. Execute: pip install ollama")
                self.client = None

        elif self.provider == "openai":
            try:
                from openai import OpenAI
                if not self.api_key:
                    print("[ERRO] API Key da OpenAI não encontrada.")
                    print("Configure: export OPENAI_API_KEY='sua-chave'")
                    self.client = None
                else:
                    self.client = OpenAI(api_key=self.api_key)
                    print(f"[IA] Cliente OpenAI inicializado com modelo: {self.model}")
            except ImportError:
                print("[ERRO] OpenAI não instalado. Execute: pip install openai")
                self.client = None

        elif self.provider == "groq":
            try:
                from groq import Groq
                if not self.api_key:
                    print("[ERRO] API Key do Groq não encontrada.")
                    print("Configure: export GROQ_API_KEY='sua-chave'")
                    self.client = None
                else:
                    self.client = Groq(api_key=self.api_key)
                    print(f"[IA] Cliente Groq inicializado com modelo: {self.model}")
            except ImportError:
                print("[ERRO] Groq não instalado. Execute: pip install groq")
                self.client = None

        else:
            print(f"[ERRO] Provider '{self.provider}' não suportado")
            self.client = None

    def chat(self, user_message):
        """
        Envia uma mensagem para a IA e recebe resposta.

        Args:
            user_message (str): Mensagem do usuário

        Returns:
            str: Resposta da IA
        """
        if not self.client:
            return "IA não disponível. Verifique a configuração."

        # Adicionar mensagem do usuário ao histórico
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        try:
            response = self._get_response()

            # Adicionar resposta ao histórico
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })

            return response

        except Exception as e:
            error_msg = f"Erro ao comunicar com IA: {str(e)}"
            print(f"[ERRO] {error_msg}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem."

    def _get_response(self):
        """Obtém resposta do provider específico"""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history

        if self.provider == "ollama":
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            return response['message']['content']

        elif self.provider in ["openai", "groq"]:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=150  # Respostas curtas
            )
            return response.choices[0].message.content

        return "Provider não configurado corretamente."

    def reset_conversation(self):
        """Limpa o histórico de conversa"""
        self.conversation_history = []
        print("[IA] Histórico de conversa limpo")

    def get_conversation_summary(self):
        """Retorna resumo da conversa"""
        return {
            "provider": self.provider,
            "model": self.model,
            "message_count": len(self.conversation_history),
            "history": self.conversation_history
        }

    def save_conversation(self, filepath="conversation_history.json"):
        """Salva histórico de conversa em arquivo JSON"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "provider": self.provider,
            "model": self.model,
            "conversation": self.conversation_history
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"[IA] Conversa salva em: {filepath}")

    def load_conversation(self, filepath="conversation_history.json"):
        """Carrega histórico de conversa de arquivo JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.conversation_history = data.get("conversation", [])
            print(f"[IA] Conversa carregada de: {filepath}")
            print(f"[IA] {len(self.conversation_history)} mensagens restauradas")
        except FileNotFoundError:
            print(f"[ERRO] Arquivo não encontrado: {filepath}")
        except Exception as e:
            print(f"[ERRO] Erro ao carregar conversa: {e}")


# Teste do módulo
if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTE DO MÓDULO DE IA CONVERSACIONAL")
    print("="*60 + "\n")

    # Testar com Ollama (local, gratuito)
    print("1. Testando Ollama (local)...")
    ai = AIAssistant(provider="ollama", model="llama3.2:3b")

    if ai.client:
        print("\nPergunta: Olá, como você está?")
        resposta = ai.chat("Olá, como você está?")
        print(f"Resposta: {resposta}\n")

        print("Pergunta: Qual é a capital do Brasil?")
        resposta = ai.chat("Qual é a capital do Brasil?")
        print(f"Resposta: {resposta}\n")

        # Mostrar resumo
        summary = ai.get_conversation_summary()
        print(f"Resumo: {summary['message_count']} mensagens trocadas")
    else:
        print("[AVISO] Ollama não disponível. Para usar:")
        print("  1. Instale: pip install ollama")
        print("  2. Baixe Ollama: https://ollama.com/download")
        print("  3. Execute: ollama pull llama3.2:3b")

    print("\n" + "="*60 + "\n")

    print("Para usar OpenAI ou Groq:")
    print("  OpenAI: ai = AIAssistant(provider='openai', api_key='sua-chave')")
    print("  Groq:   ai = AIAssistant(provider='groq', api_key='sua-chave')")
    print("\n" + "="*60)
