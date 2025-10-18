# Tradutor de MT:
Este projeto implementa um tradutor de máquinas de Turing que permite converter MTs no modelo de Sipser (fita com início à esquerda) para MTs de fita duplamente infinita e vice-versa.

## Instruções de Execução

1. Escreva sobre o arquivo "MT.in" na pasta do projeto.

2. Execute o script principal dentro da pasta \src:

> python3 main.py

3. O arquivo traduzido será gerado como MT.out na pasta "...\Tradutor de MT", junto ao "MT.in"

***OBS: Não renomeie ou troque o local do arquivo "MT.in"***

## Estrutura do Projeto

<img width="349" height="143" alt="image" src="https://github.com/user-attachments/assets/33f6bc70-14b9-4d8e-82b7-b22f763fd39a" />

* **proofs/**: Contém os arquivos de pré configuração das MTs (MT-DI e MT-SIP)
* **src/**: Contém o código-fonte do tradutor.
* **MT.in**: Arquivo de entrada onde a MT original deve ser escrita, seguindo a sintaxe do simulador online de MTs: Morphett Turing Simulator
* **MT.out**: Arquivo de saída gerado pelo tradutor, contendo a MT traduzida para o modelo oposto.

## Formato do Arquivo de Entrada (MT.in)

Cabeçalho do tipo de máquina

**;S → MT de Sipser (fita com início à esquerda)**

**;I → MT de fita duplamente infinita**

## Regras de Transição para a MT de Entrada
Cada linha deve seguir o formato: [current state] [current symbol] [new symbol] [direction] [new state]

* O estado inicial deve ser sempre 0.

* O estado 0o é reservado para o tradutor e não deve ser usado.

* Comentários na mesma linha de uma transição serão removidos no arquivo de saída.

* Máquinas que escrevem símbolos diferentes de {_, 0, 1} no meio da fita podem não ter tradução funcional, pois o tradutor não gera estados que movam esses símbolos para a direita.

## Observações:

* O tradutor é determinístico e compatível com MTs sobre o alfabeto {0,1}.

* Comentários fora das transições são preservados.

* Movimentos estacionários (*) podem ser utilizados pelo tradutor na MT de saída para manter o comportamento correto da máquina.
