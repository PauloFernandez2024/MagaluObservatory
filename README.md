# MagaluObservatory
Programas e Regras de Observabilidade para Magalu Cloud

<p align="center">
    <img src="magalucloud.png" alt="Diagrama da Arquitetura" width="800"/>
</p>
<br>

## 1. Métricas de Rede (Load, Errors, Buffers, Environment)

Estas métricas indicam o volume e o tipo de dados que os equipamentos de rede estão processando, assim como as condições de ambiente. São essenciais para avaliar a carga de trabalho e identificar possíveis gargalos.

| Métrica                        | Descrição                                      |
|--------------------------------|------------------------------------------------|
| `% bandwidth`                  | Tráfego por interfaces e canais                |
| `% errors`                     | Taxa de pacotes com erros (ingress e egress)   |
| `% discards`                   | Taxa de pacotes não processados                |
| `temperature`                  | Alta temperatura reduz vida útil               |
| `fan speede power status`      |	Pode indicar falha de hardware                |
| `link status`                  | Up/Down                                        |
| `% retransmissions`            | Indicativo de perda de pacotes                 |
| `% collisions`                 | Detecção de possíveis problemas (full duplex)  |
| `% cpu utilization`            | Uso de CPU                                     |
| `% memory_usage`               | Uso de memória                                 |

<br>

## Monitoramento de BGP

Contempla as principais métricas que devem ser monitoradas em sessões BGP para garantir visibilidade, estabilidade e operação segura de redes com roteamento dinâmico.


| **Métrica**                        | **Descrição**                                                             |
|-----------------------------------|---------------------------------------------------------------------------|
| `bgp_session_state`               | Estado da sessão BGP (Idle, Connect, Active, OpenSent, OpenConfirm, Established) |
| `bgp_peer_uptime_seconds`         | Tempo que a sessão está ativa                                            |
| `bgp_messages_received_total`     | Total de mensagens BGP recebidas                                         |
| `bgp_messages_sent_total`         | Total de mensagens BGP enviadas                                          |
| `bgp_prefixes_received`           | Número de prefixos anunciados pelo peer                                  |
| `bgp_prefixes_advertised`         | Quantidade de rotas que você está anunciando                             |
| `bgp_updates_received`            | Total de atualizações de rotas recebidas                                 |
| `bgp_updates_sent`                | Atualizações enviadas para os peers                                      |
| `bgp_flaps` / `bgp_session_changes` | Contador de sessões que caíram e subiram novamente                       |
| `bgp_input_errors` / `bgp_output_errors` | Erros no recebimento/envio de mensagens BGP                           |
| `bgp_hold_time`                   | Tempo de inatividade antes da sessão expirar                             |
| `bgp_keepalive_interval`          | Intervalo de envio de keepalives                                         |





