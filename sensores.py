import json
from datetime import datetime

def ler_telemetria_avancada():
    """
    Simula uma leitura completa da Estação Remota (Japãozinho).
    CENÁRIO: Risco Oculto. Água OK, mas Motor prestes a fundir.
    """
    dados = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estacao_id": "ETA-JAPAOZINHO-04",
        "conectividade": "4G_ESTAVEL", # Sinal está bom hoje
        
        # PARTE 1: O que todo mundo vê (A Água)
        "qualidade_agua": {
            "turbidez_ntu": 1.8,  # Excelente (Meta < 5.0)
            "ph": 7.1,            # Perfeito
            "cloro": 0.8
        },
        
        # PARTE 2: O que só a IA vê (A Saúde da Máquina)
        "saude_equipamento": {
            "motor_principal": {
                "vibracao_eixo_x": 14.2,    # CRÍTICO! (Normal < 4.5 mm/s)
                "temperatura_carcaca": 88,  # ALERTA! (Muito quente)
                "ruido_db": 95              # Barulhento
            }
        }
    }
    return json.dumps(dados, indent=2)