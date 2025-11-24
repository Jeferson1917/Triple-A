import streamlit as st
import pandas as pd
import numpy as np
import time

# Configuração da Página
st.set_page_config(page_title="DESO FlowMind", page_icon="💧", layout="wide")

# Sidebar - Simulação de Sinal
st.sidebar.image("https://img.icons8.com/color/96/water-factory.png", width=80)
st.sidebar.title("Mangaba Control")
sinal = st.sidebar.toggle("Simular Sinal de Internet", value=False)

# Status do Sistema
if sinal:
    st.success("🟢 SISTEMA ONLINE - Sincronizado com Nuvem ANA/DESO")
else:
    st.warning("🟠 MODO OFFLINE (ZONA DE SOMBRA) - Operando via Edge Computing")
    st.caption("Os dados estão sendo salvos localmente e serão enviados quando o sinal retornar.")

st.title("💧 Monitoramento Estação: ETA-01")

# Métricas (Simuladas)
col1, col2, col3 = st.columns(3)
col1.metric("Turbidez (NTU)", "4.2", "+0.5", delta_color="inverse")
col2.metric("pH", "6.8", "-0.2", delta_color="normal")
col3.metric("Cloro Residual", "1.5 mg/L", "0.0")

# Gráfico em Tempo Real (Fake)
st.subheader("📊 Análise de Sensores (Últimas 24h)")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Turbidez", "pH", "Vazão"])
st.line_chart(chart_data)

# A Mágica da IA (Simulação)
st.divider()
st.subheader("🤖 Agente Relator (Llama 3 via Groq)")

if st.button("Gerar Relatório de Turno"):
    with st.spinner('Analisando dados com IA...'):
        time.sleep(2) # Drama
        st.write("""
        *RELATÓRIO TÉCNICO OPERACIONAL - TURNO MANHÃ*
        
        *1. Status Geral:* A operação segue em conformidade parcial.
        *2. Anomalias:* Detectada leve oscilação de Turbidez às 10:00am.
        *3. Ação do Agente:* O sistema ajustou preventivamente o alerta para a equipe de manutenção.
        *4. Conclusão:* Sugere-se verificação física dos filtros nas próximas 2 horas.
        
        Relatório gerado automaticamente em conformidade com Portaria GM/MS nº 888.
        """)
        st.success("Relatório salvo no dispositivo (Offline).")