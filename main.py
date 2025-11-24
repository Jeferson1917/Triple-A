import os
from dotenv import load_dotenv # <--- Importante para ler o .env
from crewai import Agent, Task, Crew, LLM
from sensores import ler_telemetria_avancada

# --- 1. CARREGAR SEGREDOS ---
load_dotenv() # Isso lê o arquivo .env automaticamente

# Verifica se a chave foi carregada
if not os.getenv("GROQ_API_KEY"):
    print("ERRO: Chave GROQ_API_KEY não encontrada no arquivo .env")
    exit()

# Truque para o CrewAI não reclamar da OpenAI
os.environ["OPENAI_API_KEY"] = "NAO-PRECISA"

# --- 2. CONFIGURANDO O CÉREBRO ---
cerebro_mangaba = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY") # Pega do arquivo .env de forma segura
)

# --- 3. AGENTES ---
monitor = Agent(
    role='Supervisor de Telemetria',
    goal='Triagem de dados',
    backstory='Se a água estiver ruim, alerte Químicos. Se a máquina vibrar, alerte Mecânica.',
    llm=cerebro_mangaba,
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

print("🚀 INICIANDO SISTEMA MANGABA (Groq Seguro)...")
equipe.kickoff()