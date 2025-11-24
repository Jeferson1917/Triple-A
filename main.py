import os
from crewai import Agent, Task, Crew, LLM # <--- Importando a classe LLM nova
from sensores import ler_telemetria_avancada

# --- 1. CONFIGURAÇÃO DAS CHAVES ---


# --- 1. CONFIGURAÇÃO DO CÉREBRO (GROQ + LLAMA 3) ---
MINHA_CHAVE_GROQ = "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" 

os.environ["GROQ_API_KEY"] = MINHA_CHAVE_GROQ

# TRUQUE: Definimos uma chave falsa da OpenAI para o CrewAI não travar pedindo ela
os.environ["OPENAI_API_KEY"] = "NAO-PRECISA-ISSO-E-UM-TRUQUE"

# --- 2. CONFIGURANDO O CÉREBRO (JEITO NOVO) ---
# O prefixo 'groq/' avisa pro sistema exatamente quem chamar
cerebro_mangaba = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=MINHA_CHAVE_GROQ
)

# --- 3. AGENTES (USANDO O CÉREBRO NOVO) ---
monitor = Agent(
    role='Supervisor de Telemetria',
    goal='Triagem de dados',
    backstory='Se a água estiver ruim, alerte Químicos. Se a máquina vibrar, alerte Mecânica.',
    llm=cerebro_mangaba, # <--- Usando a nova configuração
    verbose=True
)

engenheiro = Agent(
    role='Especialista Preditivo',
    goal='Prever falha',
    backstory='Analise vibração e temperatura. Preveja quando a bomba vai quebrar.',
    llm=cerebro_mangaba,
    verbose=True
)

despachante = Agent(
    role='Logística',
    goal='Criar Ordem de Serviço',
    backstory='Defina equipe, veículo (4x4) e peças para levar.',
    llm=cerebro_mangaba,
    verbose=True
)

# --- 4. TAREFAS ---

print("📡 Lendo sensores simulados...")
dados = ler_telemetria_avancada()

task1 = Task(
    description=f'Analise estes dados: {dados}. A água está potável? A máquina está saudável? Responda resumido.',
    expected_output='Resumo da Situação.',
    agent=monitor
)

task2 = Task(
    description='Diagnóstico da falha mecânica (Vibração 14.2, Temp 88). O que vai quebrar e quando?',
    expected_output='Diagnóstico técnico.',
    agent=engenheiro
)

task3 = Task(
    description='Crie uma Ordem de Serviço para WhatsApp. Inclua: Veículo (Lembre que é estrada de terra), Peças e Prioridade.',
    expected_output='Texto da OS pronto para envio.',
    agent=despachante
)

# --- 5. RODAR ---

equipe = Crew(
    agents=[monitor, engenheiro, despachante],
    tasks=[task1, task2, task3],
    verbose=True
)

print("🚀 INICIANDO SISTEMA MANGABA (Groq)...")
equipe.kickoff()
