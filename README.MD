                                                                      Mangaba AI: Sistema Inteligente de Monitoramento (DESO)

Objetivo do Projeto:
  Este sistema automatiza a análise de telemetria da estação de bombeamento em bairros da cidade de Aracaju. 
  O objetivo é eliminar a necessidade de um humano ficar olhando gráficos o dia todo.
  O sistema lê sensores, identifica problemas (TI, Mecânicos ou Químicos) e gera automaticamente
  uma Ordem de Serviço (O.S.) pronta para ser enviada via WhatsApp para a equipe de campo.

Como Funciona (O Fluxo de 3 Etapas):
O sistema utiliza uma arquitetura de Agentes em Cadeia. Não é apenas uma IA pensando tudo de uma vez; são três "especialistas" conversando entre si sequencialmente:
  1. Entrada de Dados (Sensores):
      O módulo sensores.py simula a leitura de equipamentos reais, retornando um JSON com:
              Conexão: Online/Offline.
              Qualidade da Água: Turbidez (NTU), pH, Cloro.
              Saúde do Equipamento: Vibração do motor, temperatura, tensão elétrica.

  2. O Processamento (Os 3 Agentes):
      Agente 1: O Supervisor (Monitoramento)
              Função: É o primeiro filtro. Ele recebe os dados brutos.
              Lógica: Verifica se está ONLINE ou OFFLINE. Se estiver online, checa se a água está potável e se a bomba não vai explodir.
              Saída: Um parecer geral (ex: "Emergência de TI" ou "Alerta de Turbidez Alta").
      Agente 2: O Engenheiro (Diagnóstico)
              Função: Técnico especialista.
              Entrada: Recebe o parecer do Supervisor + os dados brutos.
              Lógica: Descobre a Causa Raiz. Ele não quer saber se está ruim, ele quer saber por que está ruim (ex: "Rolamento do motor superaqueceu devido a vibração excessiva").
              Saída: Diagnóstico técnico preciso.
      Agente 3: O Despachante (Logística)
              Função: Operacional.
              Entrada: Recebe o diagnóstico do Engenheiro.
              Lógica: Decide quem mandar.
              Regra de Ouro: Sempre manda veículo 4x4 (estrada de terra).
              Define ferramentas e peças de reposição baseadas no problema.
              Saída: Texto final da O.S. formatado para WhatsApp.


  
