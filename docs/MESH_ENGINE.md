# Mesh Engine - Sprint 2

## Objetivo

A Sprint 2 estabelece uma implementacao proprietaria inicial do Mesh Engine, com leitura basica de malhas, validacao de integridade e estatisticas essenciais para os proximos fluxos de engenharia reversa.

## Escopo implementado

- Carregamento inicial de OBJ, STL ASCII e PLY ASCII.
- Excecoes de dominio para arquivos invalidos, formatos nao suportados e malhas corrompidas.
- Snapshot imutavel dos dados carregados.
- Calculo de bounds por eixo.
- Estatisticas de vertices, triangulos, arestas e formato.
- Limpeza segura de estado apos falhas de carregamento.

## Fora de escopo nesta sprint

- STL binario.
- Reparacao automatica de malhas.
- Simplificacao ou remalhamento.
- Deteccao de primitivas CAD.
- Dependencias externas de processamento geometrico.

## Politica proprietaria

Este modulo faz parte do HFC Reverse CAD, software proprietario. Nenhuma licenca open source e concedida para seu uso, copia, modificacao ou distribuicao.
