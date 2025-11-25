import os
import asyncio
import json # <--- NECESSÁRIO para ler a lista
from dotenv import load_dotenv

# 1. Carrega a senha
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("❌ ERRO: GOOGLE_API_KEY faltando no .env")
    exit()

from mangaba_ai import MangabaAgent
from sensores import ler_telemetria_avancada

async def iniciar_operacao():
    print("\n" + "="*60)
    print("🍈 MANGABA AI: Central de Monitoramento Geral (Toda Aracaju)")
    print("="*60)

    # --- 1. CRIANDO OS AGENTES ---
    agente_monitor = MangabaAgent(agent_id="Supervisor_Telemetria")
    agente_engenheiro = MangabaAgent(agent_id="Especialista_Tecnico")
    agente_despachante = MangabaAgent(agent_id="Coordenador_Logistica")

    # --- 2. LENDO A LISTA DE DADOS ---
    print("📡 Baixando telemetria de todas as estações...")
    
    dados_brutos_str = ler_telemetria_avancada()
    
    # Converte o texto JSON para uma Lista Python real
    lista_estacoes = json.loads(dados_brutos_str)
    
    print(f"📦 Total de estações detectadas: {len(lista_estacoes)}\n")

    # --- 3. O LOOP (Processando uma por uma) ---
    
    for i, estacao in enumerate(lista_estacoes):
        nome_estacao = estacao.get("local", "Estação Desconhecida")
        
        print(f"▶️ ANALISANDO ESTAÇÃO {i+1}: {nome_estacao.upper()}")
        print("-" * 40)

        # Transforma o dicionário dessa estação específica de volta em texto para a IA ler
        dados_da_vez = json.dumps(estacao, indent=2)

        # PASSO 1: SUPERVISOR
        print("   🤖 Supervisor verificando...")
        prompt_monitor = f"""
        Você é um Supervisor. Regra:
        - OFFLINE: Emergência TI.
        - ONLINE: Analise água e bomba.
        Dados: {dados_da_vez}
        Seja extremamente breve (máximo 1 frase).
        """
        analise = agente_monitor.chat(prompt_monitor)
        print(f"   > Parecer: {analise}")

        # Só acionamos o engenheiro/logística se tiver problema (para não gastar tempo à toa)
        # Se a análise contiver palavras como "Normal", "Adequado", "Operante", a gente pula.
        # Mas para o teste, vamos rodar tudo.

        # PASSO 2: ENGENHEIRO
        print("   🔧 Engenheiro diagnosticando...")
        prompt_engenheiro = f"""
        Com base em: "{analise}" e dados: "{dados_da_vez}".
        Qual a falha técnica? (Se estiver tudo normal, diga "Sem falhas").
        Seja curto.
        """
        diagnostico = agente_engenheiro.chat(prompt_engenheiro)
        
        # PASSO 3: LOGÍSTICA (Só gera OS se tiver problema real)
        # Pequena lógica python para não gerar OS se estiver tudo bem
        if "Sem falhas" not in diagnostico and "Tudo normal" not in analise:
            print("   🚚 Logística gerando OS...")
            prompt_despachante = f"""
            Gere uma OS curtíssima para WhatsApp baseada em: "{diagnostico}".
            Defina: Equipe, Veículo e Peça.
            """
            os_final = agente_despachante.chat(prompt_despachante)
            print(f"   ✅ OS GERADA: {os_final}")
        else:
            print("   ✅ Nenhuma ação logística necessária.")

        print("\n") # Pula linha para a próxima estação

if __name__ == "__main__":
    asyncio.run(iniciar_operacao())
