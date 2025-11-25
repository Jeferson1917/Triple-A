import os
import asyncio
from dotenv import load_dotenv

# 1. Carrega a senha do Google
load_dotenv()

# Verificação de segurança
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ ERRO: GOOGLE_API_KEY faltando no .env")
    exit()

from mangaba_ai import MangabaAgent
from sensores import ler_telemetria_avancada

async def iniciar_operacao():
    print("\n--------------------------------------------------")
    print("🍈 MANGABA AI: Sistema de Monitoramento DESO")
    print("--------------------------------------------------")

    # --- 1. CRIANDO OS AGENTES (Usando a assinatura certa!) ---
    
    agente_monitor = MangabaAgent(agent_id="Supervisor_Telemetria")
    agente_engenheiro = MangabaAgent(agent_id="Especialista_Tecnico")
    agente_despachante = MangabaAgent(agent_id="Coordenador_Logistica")

    # --- 2. LENDO DADOS ---
    print("📡 Lendo sensores do Japãozinho...")
    dados = ler_telemetria_avancada()
    print(f"📦 Pacote Recebido: {dados}\n")

    # --- 3. EXECUTANDO O FLUXO (Usando o método .chat()) ---

    # PASSO 1: SUPERVISOR
    print("🤖 1. Supervisor analisando...")
    # Aqui a gente manda a "Personalidade" junto com a ordem
    prompt_monitor = f"""
    Você é um Supervisor de Operações da DESO.
    Sua regra é: Olhe o campo 'status_conexao'.
    - Se for OFFLINE: Declare Emergência de TI.
    - Se for ONLINE: Analise se a água está potável e a bomba saudável.
    
    Analise estes dados agora: {dados}
    """
    analise = agente_monitor.chat(prompt_monitor)
    print(f"> Parecer: {analise}\n")

    # PASSO 2: ENGENHEIRO
    print("🔧 2. Engenheiro diagnosticando...")
    prompt_engenheiro = f"""
    Você é um Especialista Técnico.
    Com base no parecer do supervisor: "{analise}"
    E nos dados brutos: "{dados}"
    
    Qual é a causa raiz técnica? (Ex: Falha de torre 4G? Rolamento estourado? Sensor sujo?)
    Seja técnico e direto.
    """
    diagnostico = agente_engenheiro.chat(prompt_engenheiro)
    print(f"> Diagnóstico: {diagnostico}\n")

    # PASSO 3: LOGÍSTICA
    print("🚚 3. Logística despachando...")
    prompt_despachante = f"""
    Você é o Coordenador de Logística.
    Gere uma ORDEM DE SERVIÇO curta para enviar no WhatsApp do motorista.
    
    Baseado no diagnóstico: "{diagnostico}"
    
    Defina:
    1. Qual equipe mandar (TI ou Mecânica ou Química)?
    2. Qual veículo? (Obrigatório: 4x4, pois é estrada de terra).
    3. Quais peças/ferramentas levar?
    4. Prioridade (Alta/Média).
    """
    os_final = agente_despachante.chat(prompt_despachante)

    print("\n" + "="*50)
    print("✅ ORDEM DE SERVIÇO FINAL (MANGABA AI):")
    print("="*50)
    print(os_final)

if __name__ == "__main__":
    asyncio.run(iniciar_operacao())
