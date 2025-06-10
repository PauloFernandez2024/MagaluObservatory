## Magalu Cloud - Observability
Programas e Regras de Observabilidade para Magalu Cloud

Serão estabelecidos os principais componentes da arquitetura, com ênfase sobre Coletores e "Rules Engine" permitindo que fórmulas sejam aplicadas sobre as chamadas Macro-Métricasn ou Categorias.

<p align="center">
    <img src="magalucloud.png" alt="Diagrama da Arquitetura" width="700"/>
</p>
<br>


## Rules Engine
Criado para permitir total desacoplamento dos códigos associados aos coletores.

<p align="center">
    <img src="rules.png" alt="Diagrama da Arquitetura" width="400"/>
</p>
<br>

## Arquivos de Configuração e Programas de Apoio

Para um melhor entendimento da solução, serão primeiro definidos os principais arquivos e programas de apoio, responsáveis pela coleta, cálculo, análise e classificação das métricas.
O objetivo destes programas é desacoplar o código dos principais módulos das atividades auxiliares, de tal forma que exclusões ou a adições de novas métricas não alterem os códigos da solução.  

---

### `metrics.yaml`

Arquivo cujo conteúdo define as **categorias** e todas as **métricas dependentes**, cujos os valores são coletados pelos exporters.
Por exemplo, a categoria `bandwidth` possui como dependentes as seguintes métricas:
* `ifHCInOctets`
* `ifHCOutOctets`
* `ifHighSpeed`

Essas métricas são necessárias para calcular o consumo de largura de banda.

---

### `jobs.yaml`

Arquivo de configuração onde são definidos os **jobs do Prometheus**, que especificam as categorias a serem avaliadas e, consequentemente, quais métricas serão coletadas.

Um mesmo conjunto de categorias pode ser utilizado por múltiplos jobs, refletindo cenários onde diferentes dispositivos ou sistemas compartilham o mesmo perfil de métricas.

---

### `formulas.py`

Define como as **categorias** deverão ser calculadas utilizando o conjunto de métricas dependentes definidas em `metrics.yaml`.

O arquivo é dividido em duas seções:

1. **Funções de cálculo** que processam os valores das métricas e retornam o valor da categoria.
2. **Mapa de associação** entre os nomes das categorias e os nomes das respectivas funções implementadas.

---

### `config.yaml`

Arquivo que define os **thresholds** dos valores calculados por categoria, conforme definidos em `formulas.py`.

Cada categoria possui dois thresholds:

* `warning`
* `critical`

Adicionalmente, o campo `score_direction` indica se a categoria possui comportamento **positivo** (maior é melhor) ou **negativo** (maior é pior).

### Exemplo:

Para a categoria `bandwidth`, classificada como score negativo:

* Valor ≥ 90% → `CRITICAL`
* Valor entre 70% e 89.9% → `WARNING`
* Valor < 70% → `OK`

---

### `time_window.py`

Arquivo que define as **janelas de tempo** utilizadas para agrupar as métricas a serem analisadas.

Cada entrada do arquivo representa:

* O **nome da janela** (`5m`, `1h`, `24h`, `30d`)
* O **intervalo de tempo real** em que as métricas serão avaliadas

Por exemplo, a janela `24h` representa a análise das métricas ocorridas nas últimas 24 horas. Essa granularidade permite:

* Avaliações em tempo real (ex: `5m`, `1h`)
* Análises históricas de médio e longo prazo (ex: `24h`, `30d`)

<br>



## 1. Métricas de Rede (Load, Errors, Buffers, Environment)

Estas métricas indicam o volume e o tipo de dados que os equipamentos de rede estão processando, assim como as condições de ambiente. São essenciais para avaliar a carga de trabalho e identificar possíveis gargalos.

| Categoria                      | Descrição                                      |
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


| **Categoria**                     | **Descrição**                                                             |
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


| **Categoria**                   | **Descrição**                                                                 |
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


 **Categoria**                           | **Descrição**                                                                 |
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





