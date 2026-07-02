# HFC Geometry Kernel (HGK) Architecture

## Documento mestre de arquitetura

Status: Proposta oficial de referência
Versão: 1.0
Data: 2026-07-01

Este documento define a arquitetura oficial do HFC Geometry Kernel (HGK) como a camada matemática e geométrica do HFC Reverse CAD. Ele serve como referência principal para o desenvolvimento, evolução e integração do kernel ao longo dos próximos anos.

O HGK é responsável por representar, validar, transformar e reconstruir modelos geométricos com rigor matemático, tolerância numérica controlada e compatibilidade com fluxos de engenharia reversa, análise e exportação CAD.

---

## 1. Visão Geral do HGK

O HGK é o núcleo geométrico do HFC Reverse CAD. Sua função é fornecer uma base matemática confiável para:

- representação de formas 3D;
- operações geométricas fundamentais;
- validação de consistência espacial;
- reconstrução de modelos a partir de malhas;
- integração com pipelines de engenharia reversa;
- preparação para interoperabilidade CAD futura.

O kernel deve operar como uma camada independente, sem dependência direta de interface visual, IA ou exportação. Ele deve ser a fonte de verdade da geometria do sistema.

### Organização conceitual

```text
+----------------------------+
| Aplicação / Interface      |
| UI, plugins, workflows     |
+-------------+--------------+
              |
              v
+----------------------------+
| Camadas de alto nível      |
| Reverse, Export, Viewer    |
+-------------+--------------+
              |
              v
+----------------------------+
| HFC Geometry Kernel (HGK)  |
| - Precision                 |
| - Primitives                |
| - Curves / Surfaces        |
| - Topology                  |
| - Reconstruction            |
+----------------------------+
```

---

## 2. Objetivos do Kernel

Os objetivos centrais do HGK são:

1. Fornecer uma base geométrica estável e extensível.
2. Garantir precisão numérica controlada.
3. Suportar a conversão de malhas em representações CAD estruturadas.
4. Isolar matemática geométrica de decisões de aplicação.
5. Permitir evolução gradual sem quebra de contratos principais.
6. Apoiar validação, inspeção, reconstrução e interoperabilidade futura.

O kernel não substitui a intenção do usuário nem a interpretação assistida por IA. Ele garante que toda hipótese geométrica seja avaliada de forma matemática e verificável.

---

## 3. Filosofia de Projeto

A filosofia do HGK é fundamentada em seis princípios:

- Matemática como autoridade final.
- Simplicidade explícita sobre abstração excessiva.
- Modularidade rigorosa.
- Determinismo em operações e resultados.
- Robustez frente a erros numéricos e dados imperfeitos.
- Extensibilidade controlada e compatibilidade futura.

Esses princípios orientam o design de classes, interfaces e fluxos internos.

---

## 4. Arquitetura em Camadas

A arquitetura do HGK deve ser organizada em camadas bem separadas.

### Camada 1 - Núcleo Matemático

Responsável por:

- tolerância e precisão;
- ponto, vetor e matriz;
- transformações rígidas e afins;
- estruturas básicas de cálculo.

### Camada 2 - Geometria Fundamental

Responsável por:

- retas;
- raios;
- planos;
- caixas delimitadoras;
- entidades geométricas elementares.

### Camada 3 - Geometria Superior

Responsável por:

- curvas;
- superfícies;
- volumes;
- entidades de alto nível para análise e reconstrução.

### Camada 4 - Topologia e Reconstrução

Responsável por:

- estruturas B-Rep;
- relações topológicas;
- conversão de malha para formas estruturadas;
- integração com a engenharia reversa.

### Camada 5 - Integração

Responsável por:

- importação e exportação;
- visualização e inspeção;
- integração com IA e pipelines externos.

### Diagrama estrutural

```text
[Interface / Orquestração]
            |
            v
[Integration Layer]
            |
            v
[Topology & Reconstruction]
            |
            v
[Geometry Higher Level]
            |
            v
[Fundamental Geometry]
            |
            v
[Mathematical Core]
```

---

## 5. Núcleo Matemático

O núcleo matemático é a base do HGK. Ele contém os blocos mínimos usados por todos os demais módulos.

### 5.1 PrecisionManager

Responsabilidade:

- centralizar tolerâncias geométricas do sistema;
- comparar valores float de forma segura;
- comparar pontos e vetores com critério numérico consistente;
- fornecer um ponto único de controle para precisão.

Funções esperadas:

- tolerância linear padrão;
- tolerância angular padrão;
- comparação segura entre floats;
- comparação entre pontos;
- comparação entre vetores;
- validação de valores e entradas.

### 5.2 Point3D

Representa um ponto tridimensional imutável no espaço euclidiano.

Responsabilidades:

- armazenar coordenadas x, y, z;
- fornecer distância entre pontos;
- suportar translação;
- permitir conversão para tupla;
- participar de operações geométricas futuras.

### 5.3 Vector3D

Representa um vetor tridimensional imutável.

Responsabilidades:

- armazenar componentes x, y, z;
- calcular módulo;
- normalizar vetores;
- calcular produto escalar e vetorial;
- calcular ângulo entre vetores;
- suportar operações aritméticas básicas.

### 5.4 Matrix4x4

Representa uma matriz 4x4 imutável para transformações espaciais.

Responsabilidades:

- representar transformações homogêneas;
- suportar identidade e construção a partir de linhas;
- fornecer transposição;
- multiplicar matrizes;
- aplicar transformações em Point3D e Vector3D.

### 5.5 Transform3D

Representa transformações espaciais completas, incluindo translação, rotação e escala.

Responsabilidades:

- compor transformações;
- aplicar operações a pontos e vetores;
- manter consistência com o sistema de coordenadas do kernel;
- servir como base para futuras operações de modelagem e reconstrução.

---

## 6. Geometria Fundamental

Esta camada reúne entidades geométricas elementares que serão usadas por curvas, superfícies, topologia e reconstrução.

### 6.1 Line3D

Representa uma reta finita ou infinita no espaço tridimensional.

Responsabilidades:

- definir orientação e posição;
- suportar avaliação de pontos e projeções;
- participar de interseções e validações.

### 6.2 Ray3D

Representa uma semi-reta com origem e direção.

Responsabilidades:

- modelar trajetórias e feixes de direção;
- servir como base para análises de trajetória e projeção.

### 6.3 Plane

Representa um plano geométrico no espaço.

Responsabilidades:

- definir orientação espacial;
- calcular distâncias a pontos;
- participar de operações de interseção e projeção.

### 6.4 BoundingBox

Representa uma caixa delimitadora alinhada aos eixos.

Responsabilidades:

- avaliar limites espaciais de entidades;
- apoiar consultas de proximidade e aceleração espacial;
- participar de filtros de seleção e análise.

---

## 7. Curvas

A camada de curvas deve suportar representações unidimensionais e sua avaliação matemática.

Objetivos:

- representar curvas lineares, poligonais e contínuas por partes;
- fornecer avaliação de tangência e continuidade;
- permitir reconstrução parcial de contornos a partir de malhas;
- preparar a integração com superfícies e B-Rep.

As curvas devem ser tratadas como entidades matematicamente verificáveis e não apenas como sequências de pontos.

---

## 8. Superfícies

A camada de superfícies será responsável por representar entidades bidimensionais e seu relacionamento com o espaço.

Objetivos:

- representar superfícies planas e curvas;
- avaliar normal, orientação e continuidade;
- suportar operações de corte, projeção e análise;
- servir de base para construção de volumes.

Superfícies serão tratadas como estruturas geométricas independentes, com validação própria e suporte a reconstrução futura.

---

## 9. Topologia (B-Rep)

A topologia é uma camada crítica para modelagem CAD e engenharia reversa.

O HGK deve evoluir para suportar estruturas de representação por limite (B-Rep), incluindo:

- vértices;
- arestas;
- faces;
- corpos;
- relações de adjacência e orientação.

A B-Rep permite representar a forma de forma semântica, em vez de apenas por malha ou nuvem de pontos.

### Objetivos da topologia

- preservar estrutura geométrica;
- permitir edição futura;
- facilitar exportação para formatos CAD;
- sustentar análise de manufatura e inspeção.

---

## 10. Engenharia Reversa

O HGK é a base para a engenharia reversa do HFC Reverse CAD.

A função do kernel nesta etapa é transformar dados discretos, como malhas triangulares, em representações geométricas estruturadas.

### Fluxo esperado

1. leitura de malha STL/OBJ/PLY;
2. análise de topologia e geometria local;
3. identificação de primitivas e superfícies;
4. reconstrução de entidades CAD;
5. validação matemática do resultado;
6. exportação para formatos compatíveis.

O kernel deve apoiar esse fluxo sem depender diretamente de IA para validar ou construir a geometria final.

---

## 11. Importação e Exportação

O HGK deve ser preparado para integração com diferentes formatos e pipelines.

### Importação

- malhas trianguladas;
- dados de nuvem de pontos;
- arquivos de referência de integração futura.

### Exportação

- geometria estruturada;
- entidades de alto nível;
- dados intermediários para visualização e inspeção;
- formatos CAD e técnicos compatíveis.

A camada de importação e exportação deve permanecer externa ao núcleo matemático, preservando a independência do kernel.

---

## 12. Sistema de Precisão

A precisão é uma característica central do HGK.

### Princípios

- uso de ponto flutuante de alta precisão como base interna;
- comparação geométrica baseada em tolerância e proximidade;
- separação entre erro numérico e inconsistência real;
- unidade interna em milímetros.

### Regras principais

- coordenadas internas em mm;
- tolerâncias explícitas e centralizadas;
- comparações não devem depender de igualdade estrita;
- todos os módulos devem respeitar a política de precisão do kernel.

---

## 13. Pipeline de Reconstrução STL → CAD

O pipeline principal do HGK deve seguir um fluxo claro e evolutivo.

```text
[STL / Mesh Input]
        |
        v
[Mesh Validation]
        |
        v
[Geometry Analysis]
        |
        v
[Primitive Detection]
        |
        v
[Surface / Curve Reconstruction]
        |
        v
[Topology Construction]
        |
        v
[CAD-Ready Representation]
```

Esse fluxo serve como referência para futuras implementações de engenharia reversa e reconstrução paramétrica.

---

## 14. Integração com IA

A IA pode atuar como camada de sugestão, classificação e interpretação, mas não deve substituir o núcleo matemático.

### Papel da IA

- sugerir hipóteses de forma;
- auxiliar na classificação de regiões;
- recomendar reconstruções preliminares;
- apoiar navegação e automação de fluxos.

### Papel do HGK

- validar cada hipótese;
- garantir consistência geométrica;
- impedir que interpretações erradas se tornem resultados finais sem verificação.

Essa divisão preserva a confiabilidade técnica do sistema.

---

## 15. Roadmap Técnico

O roadmap do HGK deve ser evolutivo e orientado por maturidade incremental.

### Fase 1 - Fundação

- PrecisionManager
- Point3D
- Vector3D
- Matrix4x4
- Transform3D

### Fase 2 - Geometria básica

- Line3D
- Ray3D
- Plane
- BoundingBox

### Fase 3 - Curvas e superfícies

- curvas simples
- superfícies planas e regradas
- avaliação de continuidade

### Fase 4 - Topologia

- estruturas B-Rep
- relações de adjacência
- fechamento de corpos

### Fase 5 - Engenharia reversa

- reconstrução a partir de malhas
- identificação de primitivas e superfícies
- validação geométrica automatizada

### Fase 6 - Interoperabilidade

- importação/exportação robusta
- integração com formatos CAD e industriais
- expansão de compatibilidade técnica

---

## Conclusão

O HFC Geometry Kernel deve evoluir como uma infraestrutura matemática sólida, modular e preparada para o longo prazo. Este documento serve como referência principal para o desenvolvimento do kernel e para a integração entre geometria, topologia, reconstrução e engenharia reversa.

A continuidade do projeto depende da manutenção dessa arquitetura como guia técnico, sem perder a visão de simplicidade, rigor matemático e compatibilidade futura.
