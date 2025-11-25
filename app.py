import streamlit as st
import asyncio
import os
import json
from dotenv import load_dotenv

# --- IMPORTAÇÕES DO MANGABA ---
from mangaba_ai import MangabaAgent
from sensores import ler_telemetria_avancada

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Mangaba AI - Monitoramento DESO",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CARREGAR SEGREDOS ---
load_dotenv()
# Tenta pegar a chave do .env ou dos segredos do Streamlit (para nuvem)
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.error("❌ ERRO CRÍTICO: GOOGLE_API_KEY não encontrada. Configure o .env")
        st.stop()

# --- FUNÇÕES DE LÓGICA (O Cérebro) ---

# Cache para não recriar os agentes toda hora que clica num botão
@st.cache_resource
def get_agents():
    # No MangabaAgent, passamos o ID. A API Key ele pega do ambiente.
    monitor = MangabaAgent(agent_id="Supervisor_Telemetria")
    engenheiro = MangabaAgent(agent_id="Especialista_Tecnico")
    despachante = MangabaAgent(agent_id="Coordenador_Logistica")
    return monitor, engenheiro, despachante

# Função ASSÍNCRONA (onde a mágica acontece)
async def processar_ia(dados_str):
    monitor, engenheiro, despachante = get_agents()
    
    # Passo 1
    prompt_monitor = f"""
    Você é um Supervisor de Operações da DESO.
    Sua regra é: Olhe o campo 'status_conexao'.
    - Se for OFFLINE: Declare Emergência de TI.
    - Se for ONLINE: Analise se a água está potável e a bomba saudável.
    Analise estes dados agora: {dados_str}
    """
    # O Mangaba usa .chat() que pode ser síncrono ou assíncrono dependendo da versão.
    # Vamos assumir síncrono para simplificar no Streamlit se a lib permitir,
    # mas como você disse que usa await, vamos manter o await aqui dentro.
    analise = monitor.chat(prompt_monitor) 
    
    # Passo 2
    prompt_eng = f"Com base no parecer '{analise}' e dados '{dados_str}', qual a causa raiz técnica?"
    diagnostico = engenheiro.chat(prompt_eng)
    
    # Passo 3
    prompt_log = f"Com base no diagnóstico '{diagnostico}', crie uma Ordem de Serviço curta para WhatsApp (Veículo 4x4, Peças, Prioridade)."
    os_final = despachante.chat(prompt_log)
    
    return analise, diagnostico, os_final

# Função SÍNCRONA que o Streamlit chama (Wrapper)
def executar_analise(dados_str):
    # Cria um novo loop de eventos para rodar o async dentro do Streamlit
    return asyncio.run(processar_ia(dados_str))

# --- INTERFACE VISUAL (O Corpo) ---

st.title("💧 Sistema Mangaba AI")
st.markdown("**Centro de Controle Operacional - Projeto Piloto Japãozinho (DESO)**")
st.divider()

# Barra Lateral
with st.sidebar:
    st.header("Controle Remoto")
    botao_conectar = st.button("📡 Conectar à Estação Japãozinho", type="primary", use_container_width=True)
    st.info("O sistema simula falhas de sinal e problemas mecânicos aleatoriamente.")

# Lógica do Botão
if botao_conectar:
    
    # 1. Leitura do Sensor
    with st.spinner("📡 Estabelecendo conexão via 4G..."):
        dados_str = ler_telemetria_avancada()
        dados_dict = json.loads(dados_str)
        # Simulando um tempo de resposta
        import time
        time.sleep(1)

    # 2. Exibição do Status
    status = dados_dict.get("status_conexao", "ERRO")
    
    if status == "OFFLINE":
        st.error("### 🚨 ALERTA: ESTAÇÃO OFFLINE")
        st.write(f"**Erro:** {dados_dict.get('mensagem_erro')}")
    else:
        st.success(f"### 🟢 STATUS: {status}")
        # Métricas
        c1, c2, c3 = st.columns(3)
        c1.metric("Turbidez", f"{dados_dict['qualidade_agua']['turbidez_ntu']} NTU")
        c2.metric("Vibração", f"{dados_dict['saude_equipamento']['motor_principal']['vibracao_eixo_x']} mm/s")
        c3.metric("Temp.", f"{dados_dict['saude_equipamento']['motor_principal']['temperatura_carcaca']} °C")

    # 3. Debug (ver JSON)
    with st.expander("📦 Ver Dados Brutos (JSON)"):
        st.json(dados_dict)

    # 4. Processamento da IA
    st.markdown("---")
    st.subheader("🧠 Análise dos Agentes Autônomos")
    
    # Containers para mostrar o progresso
    col1, col2, col3 = st.columns(3)
    box_sup = col1.empty()
    box_eng = col2.empty()
    box_log = col3.empty()

    # Como o MangabaAgent.chat() parece ser síncrono na versão instalada (pelo erro anterior),
    # vamos chamar direto sem asyncio complexo pra ver se resolve seu erro.
    
    with st.spinner("🤖 Agentes trabalhando..."):
        # Instancia agentes
        monitor, engenheiro, despachante = get_agents()

        # --- AGENTE 1 ---
        box_sup.info("Supervisor analisando...")
        res_sup = monitor.chat(f"Analise status e dados: {dados_str}")
        box_sup.success(f"**Supervisor:**\n\n{res_sup}")

        # --- AGENTE 2 ---
        box_eng.info("Engenheiro diagnosticando...")
        res_eng = engenheiro.chat(f"Causa raiz baseada em: {res_sup}?")
        box_eng.warning(f"**Engenheiro:**\n\n{res_eng}")

        # --- AGENTE 3 ---
        box_log.info("Logística gerando OS...")
        res_log = despachante.chat(f"Gere OS para Zap baseada em: {res_eng}. Use veículo 4x4.")
        box_log.success("✅ Logística Concluída")

    # 5. Resultado Final
    st.markdown("### 📱 Ordem de Serviço Final")
    st.info(res_log, icon="📩")

else:
    st.write("Clique no botão ao lado para iniciar.")
