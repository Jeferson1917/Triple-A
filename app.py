import streamlit as st
import os
import json
import time
from dotenv import load_dotenv

# --- IMPORTAÇÕES DO MANGABA ---
from mangaba_ai import MangabaAgent
from sensores import ler_telemetria_avancada

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Mangaba AI - Monitoramento Geral",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CARREGAR SEGREDOS ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.error("❌ ERRO CRÍTICO: GOOGLE_API_KEY não encontrada.")
        st.stop()

# --- CACHE DOS AGENTES ---
@st.cache_resource
def get_agents():
    monitor = MangabaAgent(agent_id="Supervisor_Telemetria")
    engenheiro = MangabaAgent(agent_id="Especialista_Tecnico")
    despachante = MangabaAgent(agent_id="Coordenador_Logistica")
    return monitor, engenheiro, despachante

# --- INTERFACE VISUAL ---

st.title("💧 Central de Controle - Mangaba AI")
st.markdown("**Monitoramento em Tempo Real da Rede de Abastecimento (DESO)**")
st.divider()

# --- BARRA LATERAL (CONTROLE) ---
with st.sidebar:
    st.header("📡 Conexão com a Rede")
    
    # Botão para buscar os dados de TODAS as estações
    if st.button("🔄 Atualizar Telemetria da Rede", type="primary", use_container_width=True):
        with st.spinner("Buscando dados de todas as estações via 4G/5G..."):
            # 1. Lê a lista completa
            dados_json_str = ler_telemetria_avancada()
            lista_dados = json.loads(dados_json_str)
            
            # 2. Salva no "Estado da Sessão" do Streamlit (Memória)
            st.session_state['dados_rede'] = lista_dados
            st.session_state['ultima_atualizacao'] = time.strftime("%H:%M:%S")
            st.success(f"{len(lista_dados)} Estações Encontradas!")
            time.sleep(1)

    # Mostra quando foi a última atualização
    if 'ultima_atualizacao' in st.session_state:
        st.caption(f"Última leitura: {st.session_state['ultima_atualizacao']}")
    
    st.markdown("---")
    st.info("Sistema conectado ao Mangaba AI (Groq LPU).")

# --- ÁREA PRINCIPAL (DASHBOARD) ---

# Só mostra o dashboard se já tiver dados carregados
if 'dados_rede' in st.session_state:
    lista = st.session_state['dados_rede']
    
    # 1. SELETOR DE ESTAÇÃO (O Pulo do Gato)
    # Cria uma lista só com os nomes dos bairros para o menu
    opcoes_bairros = [estacao['local'] for estacao in lista]
    
    col_sel, col_vazio = st.columns([1, 2])
    with col_sel:
        bairro_selecionado = st.selectbox("📍 Selecione a Estação para Analisar:", opcoes_bairros)

    # 2. FILTRAR OS DADOS (Pega só o dicionário do bairro escolhido)
    # Isso procura na lista o item que tem o nome igual ao selecionado
    dados_estacao = next(item for item in lista if item["local"] == bairro_selecionado)
    
    # Transforma de volta em texto para a IA ler
    dados_str_ia = json.dumps(dados_estacao, indent=2)

    # --- EXIBIÇÃO DOS DADOS DA ESTAÇÃO ESCOLHIDA ---
    
    st.markdown(f"### Status: {bairro_selecionado.upper()}")
    
    status = dados_estacao.get("status_conexao", "ERRO")
    
    # Lógica Visual (Verde ou Vermelho)
    if status == "OFFLINE":
        st.error(f"### 🚨 ESTAÇÃO OFFLINE")
        st.write(f"**Erro:** {dados_estacao.get('mensagem_erro')}")
        st.write(f"**Último contato:** {dados_estacao.get('ultimo_heartbeat')}")
    else:
        st.success(f"### 🟢 CONEXÃO ESTÁVEL ({status})")
        
        # Métricas (Gauges)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Turbidez", f"{dados_estacao['qualidade_agua']['turbidez_ntu']} NTU")
        c2.metric("pH", dados_estacao['qualidade_agua']['ph'])
        c3.metric("Vibração", f"{dados_estacao['saude_equipamento']['motor_principal']['vibracao_eixo_x']} mm/s")
        c4.metric("Temp.", f"{dados_estacao['saude_equipamento']['motor_principal']['temperatura_carcaca']} °C")

    with st.expander("📦 Ver JSON Bruto"):
        st.json(dados_estacao)

    st.divider()

    # --- BOTÃO DA IA (Só roda para a estação selecionada) ---
    # --- BOTÃO DA IA ---
    if st.button(f"🤖 Acionar IA para Analisar {bairro_selecionado}", type="secondary"):
        
        st.subheader("🧠 Diagnóstico Inteligente Detalhado")
        
        col1, col2, col3 = st.columns(3)
        box_sup = col1.empty()
        box_eng = col2.empty()
        box_log = col3.empty()

        with st.spinner("Processando Agentes..."):
            monitor, engenheiro, despachante = get_agents()

            # --- PASSO 1: SUPERVISOR (Agora falante e detalhista) ---
            box_sup.info("Supervisor analisando telemetria...")
            
            prompt_monitor = f"""
            Você é um Supervisor Sênior da DESO. Faça uma ANÁLISE TÉCNICA DETALHADA destes dados:
            {dados_str_ia}

            Sua tarefa:
            1. Analise item por item (Turbidez, pH, Vibração, Temperatura).
            2. Explique POR QUE está bom ou ruim (compare com os limites ideais).
            3. Cite os valores exatos que estão chamando atenção.
            
            NO FINAL DO TEXTO, dê o veredito obrigatório usando uma destas tags:
            - Se 'status_conexao' for OFFLINE -> Escreva: "VEREDITO: CRITICO (Sem Sinal)"
            - Se houver qualquer valor fora do padrão -> Escreva: "VEREDITO: ALERTA (Problema Detectado)"
            - Se tudo estiver perfeito -> Escreva: "VEREDITO: OK (Operação Normal)"
            """
            res_sup = monitor.chat(prompt_monitor)
            
            # Mostra o texto completo (agora ele vai falar bastante)
            if "OK" in res_sup and "ALERTA" not in res_sup:
                box_sup.success(f"**Relatório do Supervisor:**\n\n{res_sup}")
            else:
                box_sup.error(f"**Relatório do Supervisor:**\n\n{res_sup}")

            # --- DECISÃO LÓGICA (Python procura a palavra chave no texto grande) ---
            tem_problema = "ALERTA" in res_sup or "CRITICO" in res_sup or "OFFLINE" in status

            if tem_problema:
                # --- PASSO 2: ENGENHEIRO ---
                box_eng.info("Engenheiro investigando causa raiz...")
                prompt_eng = f"""
                O Supervisor reportou um problema técnico:
                "{res_sup}"
                
                Como Engenheiro Especialista, analise a CAUSA RAIZ.
                - Não repita os dados. Explique o que está acontecendo fisicamente ou quimicamente.
                - Ex: Se a vibração é 14mm/s, explique que o rolamento está prestes a gripar.
                - Estime o tempo até a falha total.
                """
                res_eng = engenheiro.chat(prompt_eng)
                box_eng.warning(f"**Parecer de Engenharia:**\n\n{res_eng}")

                # --- PASSO 3: LOGÍSTICA ---
                box_log.info("Logística preparando despacho...")
                prompt_log = f"""
                Baseado no diagnóstico técnico: "{res_eng}".
                
                Gere uma ORDEM DE SERVIÇO profissional para WhatsApp.
                Formato:
                🚨 *URGENTE: MANUTENÇÃO DESO*
                📍 Local: {bairro_selecionado}
                🔧 Equipe: [TI / Mecânica / Química]
                🚙 Veículo: [4x4 ou Leve]
                🛠 Peças: [Listar peças prováveis]
                ⚠️ Prioridade: [Alta/Imediata]
                """
                res_log = despachante.chat(prompt_log)
                
                box_log.success("✅ **Logística Concluída**")
                st.info(f"📱 **MENSAGEM PARA EQUIPE:**\n\n{res_log}")
                
            else:
                # Se estiver tudo OK
                box_eng.success("✅ Engenharia: Monitoramento passivo (Sem anomalias).")
                box_log.success("✅ Logística: Frota em stand-by.")
                
    
