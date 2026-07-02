# Architecture

## HFC Core

Camada central do sistema. Coordena configuracoes, contratos internos, erros, estados de processamento e servicos compartilhados.

## Geometry Engine

Responsavel por entidades geometricas, operacoes matematicas, primitivas, curvas, superficies e validacoes geometricas.

## Mesh Engine

Responsavel por carregar, representar, limpar e preparar malhas 3D para processos de engenharia reversa.

## Reverse Engine

Camada dedicada a converter informacoes extraidas de malhas em estruturas CAD parametricas.

## AI Engine

Camada de apoio para sugestoes assistidas por IA. A IA pode sugerir interpretacoes, mas a validacao final pertence aos motores matematicos.

## Viewer

Modulo de visualizacao para inspecao de malhas, geometrias reconstruidas e resultados intermediarios.

## Export Engine

Responsavel por preparar e exportar resultados para formatos CAD e outros formatos tecnicos.

## Plugin Manager

Sistema de extensibilidade para integrar recursos adicionais de forma controlada, modular e compativel com o nucleo do projeto.
