import json
from datetime import datetime

def ler_telemetria_avancada():
    """
    Retorna a lista COMPLETA de todas as estações e seus status atuais.
    """
    
    # 1. Japãozinho (Risco Mecânico)
    dados_japaozinho = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estacao_id": "ETA-JAPAOZINHO-04",
        "local": "Japãozinho",
        "status_conexao": "ONLINE_4G",
        "qualidade_agua": { "turbidez_ntu": 1.8, "ph": 7.1, "cloro": 0.8 },
        "saude_equipamento": {
            "motor_principal": { "vibracao_eixo_x": 14.2, "temperatura_carcaca": 88, "ruido_db": 95 }
        }
    }

    # 2. Jardins (Tudo OK)
    dados_jardins = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estacao_id": "ETA-JARDINS-04",
        "local": "Jardins",
        "status_conexao": "ONLINE_5G",
        "qualidade_agua": { "turbidez_ntu": 1.3, "ph": 7.3, "cloro": 0.9 },
        "saude_equipamento": {
            "motor_principal": { "vibracao_eixo_x": 3.5, "temperatura_carcaca": 50, "ruido_db": 30 }
        }
    }

    # 3. Inácio Barbosa (Perfeito)
    dados_inacio = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estacao_id": "ETA-INACIO-BARBOSA-01",
        "local": "Inácio Barbosa",
        "status_conexao": "ONLINE_FIBRA",
        "qualidade_agua": { "turbidez_ntu": 0.5, "ph": 7.2, "cloro": 1.0 },
        "saude_equipamento": {
            "motor_principal": { "vibracao_eixo_x": 1.2, "temperatura_carcaca": 45, "ruido_db": 40 }
        }
    }

    # 4. Jabotiana (Água Suja)
    dados_jabotiana = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estacao_id": "ETA-JABOTIANA-02",
        "local": "Jabotiana",
        "status_conexao": "ONLINE_4G",
        "qualidade_agua": { "turbidez_ntu": 15.4, "ph": 6.8, "cloro": 0.5 },
        "saude_equipamento": {
            "motor_principal": { "vibracao_eixo_x": 4.0, "temperatura_carcaca": 55, "ruido_db": 60 }
        }
    }

    # 5. Rosa Elze (Mecânica Crítica)
    dados_rosa_elze = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estacao_id": "ETA-ROSA-ELZE-03",
        "local": "Rosa Elze",
        "status_conexao": "ONLINE_RADIO",
        "qualidade_agua": { "turbidez_ntu": 2.5, "ph": 7.0, "cloro": 0.9 },
        "saude_equipamento": {
            "motor_principal": { "vibracao_eixo_x": 18.5, "temperatura_carcaca": 98, "ruido_db": 110 }
        }
    }

    # 6. Orlando Dantas (Sem Sinal)
    dados_orlando = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estacao_id": "ETA-ORLANDO-DANTAS-05",
        "local": "Orlando Dantas",
        "status_conexao": "OFFLINE",
        "mensagem_erro": "TIMEOUT: Gateway não responde (Erro 503)",
        "ultimo_heartbeat": "Há 4 horas atrás",
        "qualidade_agua": {"turbidez_ntu": 0.0, "ph": 0.0, }, 
        "saude_equipamento": {"motor_principal": {"vibracao_eixo_x": 0, "temperatura_carcaca": 0}} 
    }

    # 7. Farolândia (Químico Ácido)
    dados_farolandia = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estacao_id": "ETA-FAROLANDIA-06",
        "local": "Farolândia",
        "status_conexao": "ONLINE_5G",
        "qualidade_agua": { "turbidez_ntu": 1.2, "ph": 5.4, "cloro": 2.5 },
        "saude_equipamento": {
            "motor_principal": { "vibracao_eixo_x": 3.2, "temperatura_carcaca": 52, "ruido_db": 55 }
        }
    }

    # --- LISTA COMPLETA ---
    # Agora retornamos TUDO, não apenas um sorteio
    todas_as_estacoes = [
        dados_japaozinho, 
        dados_jardins, 
        dados_inacio, 
        dados_jabotiana, 
        dados_rosa_elze, 
        dados_orlando, 
        dados_farolandia
    ]
    
    return json.dumps(todas_as_estacoes, indent=2)
