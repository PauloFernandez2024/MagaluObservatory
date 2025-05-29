## Magalu Cloud - Observability
Programas e Regras de Observabilidade para Magalu Cloud

Serão estabelecidos os principais componentes da arquitetura, com ênfase sobre Coletores e "Rules Engine" permitindo que fórmulas sejam aplicadas sobre as chamadas Macro-Métricas.

<p align="center">
    <img src="magalucloud.png" alt="Diagrama da Arquitetura" width="700"/>
</p>
<br>


## Rules Engine
Criado para permitir total desacoplamento dos códigos associados aos coletores.

<p align="center">
    <img src="rules_engine.png" alt="Diagrama da Arquitetura" width="400"/>
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

## 2. Métricas BGP

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

## 3. Métricas de Servidores

Obtém um conjunto essencial de métricas para monitorar servidores físicos ou virtuais. O acompanhamento contínuo dessas métricas é fundamental para garantir a **disponibilidade**, **desempenho** e **segurança** da infraestrutura.


| **Métrica**                   | **Descrição**                                                                 |
|-------------------------------|-------------------------------------------------------------------------------|
| `% cpu usage`                   | Porcentagem de utilização da CPU (total ou por núcleo)                      |
| `load average`                | Média de carga do sistema nos últimos 1, 5 e 15 minutos                     |
| `% memory usage`                | Percentual de memória RAM utilizada                                         |
| `% swap usage`                  | Uso de memória swap (pode indicar pressão na RAM)                           |
| `% disk usage`                  | Espaço utilizado em disco (por partição ou volume)                           |
| `% disk io read`, `% disk io write` | Taxa de leitura/gravação em disco (MB/s ou IOPS)                          |
| `% filesystem usage`          | Uso do espaço em filesystems                                                       |
| `% bandwidth`                  | Consumo da largur de banada por interface                                    |
| `% network errors`            | Erros e perdas nas interfaces de rede                                  |
| `process_count`               | Número total de processos em execução                                        |
| `open file descriptors`       | Total de arquivos e conexões abertos — pode causar falhas se atingir limite  |
| `temperature`                 | Temperatura da CPU, disco ou GPU (se disponível via sensores)               |
| `fan_speed`, `power_supply_status` | Velocidade das ventoinhas e status da fonte de alimentação            |
| `service availability`        | Disponibilidade de serviços essenciais (via ping, TCP, HTTP, etc.).         |


<br>

## 4. Métricas de Firewalls

Como principais métricas para monitoramento de **firewalls físicos ou virtuais**, essenciais para garantir **segurança**, **desempenho de rede** e **conformidade** com políticas de acesso, detacam-se:


 **Métrica**                           | **Descrição**                                                                 |
|----------------------------------------|-------------------------------------------------------------------------------|
| `cpu_usage`                            | Utilização da CPU — alta carga pode causar latência em inspeções.            |
| `memory_usage`                         | Utilização da RAM — fundamental para análise de pacotes e sessões ativas.    |
| `active connections`                   | Total de conexões ativas no momento.                                         |
| `connections rate`                     | Taxa de criação de novas conexões por segundo.                               |
| `dropped packets`                      | Pacotes descartados por regras, limite ou erro.                              |
| `blocked_connections`                  | Conexões explicitamente bloqueadas pelas regras de firewall.                 |
| `accepted connections`                 | Conexões aceitas (permitidas pelas regras).                                  |
| `interface errors`                     | Erros nas interfaces de rede (CRC, overrun, etc.).                           |
| `active sessions`                      | Número de sessões ativas (SSL/IPSec).                                        |
| `session utilization`                  | Percentual de uso da tabela de sessões.                                      |





