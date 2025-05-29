# MagaluObservatory
Programas e Regras de Observabilidade para Magalu Cloud

<p align="center">
    <img src="magalucloud.png" alt="Diagrama da Arquitetura" width="700"/>
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
| `% memory usage`               | Uso de memória                                 |

<br>

## Monitoramento de BGP

Contempla as principais métricas que devem ser monitoradas em sessões BGP para garantir visibilidade, estabilidade e operação segura de redes com roteamento dinâmico.


| **Métrica**                        | **Descrição**                                                             |
|-----------------------------------|---------------------------------------------------------------------------|
| `Session State`                   | Estado da sessão BGP (Idle, Connect, Active, OpenSent, OpenConfirm, Established) |
| `% received message`              | Taxas de mensagens BGP recebidas                                         |
| `% sent menssages`                | Taxa de mensagens BGP enviadas                                          |
| `% received prefixes`             | Número de prefixos anunciados pelo peer                                  |
| `% advertised prefixes`           | Quantidade de rotas que estão sendo anunciados                             |
| `% received updates`              | taxa de atualizações de rotas recebidas                                 |
| `% sent updates`                  | Atualizações enviadas para os peers                                      |
| `flaps` / `session changes`       | Número de sessões que caíram e subiram novamente                       |
| `% errors`                        | Erros no recebimento/envio de mensagens BGP                           |


<br>







