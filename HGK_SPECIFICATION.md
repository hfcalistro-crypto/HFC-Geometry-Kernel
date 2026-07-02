# HFC Geometry Kernel (HGK)

## Documento oficial de especificação

| Campo | Valor |
| --- | --- |
| Versão do documento | 1.0 |
| Status | Documento oficial preliminar |
| Plataforma tecnológica | HFC Technology Platform |
| Produto principal | HFC Reverse CAD |
| Repositório | hfc-reverse-cad |
| Responsável | Horacio C. |
| Arquitetura | HFC Geometry Kernel (HGK) |
| Tipo de documento | Especificação de engenharia |
| Criado em | 2026-07-01 |
| Última revisão | 2026-07-01 |
| Idioma | Português (Brasil) |

Este documento estabelece a especificação oficial do HFC Geometry Kernel (HGK), o subsistema responsável por representar, validar, transformar e operar modelos geométricos de forma determinística, estável e extensível. O HGK constitui a camada matemática do sistema e deve ser tratado como a fonte de verdade para geometria, topologia e avaliação de consistência em todos os fluxos de engenharia reversa.

---

## 1. Missão do HGK

A missão do HGK é fornecer uma base geométrica confiável para a conversão de malhas 3D em representações CAD estruturadas, garantindo:

- representação precisa de formas e relações espaciais;
- avaliação matemática consistente de entidades geométricas;
- isolamento da lógica geométrica da interface de usuário, IA e pipelines de importação/exportação;
- suporte a reconstrução, validação e interoperabilidade futura;
- desempenho previsível em cenários de análise, inspeção e modelagem paramétrica.

O HGK não substitui a intenção de projeto do usuário nem a interpretação assistida por IA. Ele fornece a camada de verificação matemática que transforma hipóteses em resultados geométricos confiáveis.

---

## 2. Filosofia de projeto

O HGK deve ser concebido com os seguintes princípios fundamentais:

1. Matemática como autoridade final
   - Toda decisão geométrica deve ser sustentada por operações matemáticas verificáveis.
   - A IA pode sugerir interpretações, mas não deve substituir a validação geométrica.

2. Simplicidade explícita
   - A API deve ser clara, previsível e direta, sem esconder complexidade desnecessária.
   - O sistema deve favorecer modelos semânticos simples sobre abstrações excessivas.

3. Modularidade rigorosa
   - Cada componente deve ter responsabilidade única e fronteiras bem definidas.
   - O núcleo geométrico deve permanecer independente de visualização, exportação e lógica de aplicação.

4. Determinismo
   - Operações devem produzir resultados consistentes para os mesmos dados de entrada.
   - Comportamentos dependentes de contexto devem ser explicitamente documentados.

5. Robustez frente a dados imperfeitos
   - O kernel deve tolerar pequenas imprecisões numéricas e malhas incompleta sem perder a estabilidade do fluxo.

6. Extensibilidade controlada
   - Novos tipos de entidade, métodos de avaliação e estratégias de reconstrução devem ser adicionados sem comprometer a coerência do núcleo.

---

## 3. Sistema de coordenadas

O HGK utilizará um sistema de coordenadas cartesiano tridimensional, direito, com eixos ortogonais e orientados conforme a convenção padrão:

- eixo X: direção de referência horizontal;
- eixo Y: direção perpendicular em relação ao plano base;
- eixo Z: eixo vertical ou de profundidade, conforme o contexto de modelagem.

### Regras principais

- O sistema é global e absoluto para o modelo principal.
- Transformações locais podem ser representadas por sistemas de referência associados a entidades ou componentes.
- A orientação do sistema deve ser preservada em todas as operações de rotação e transformação.
- O kernel deve tratar todas as coordenadas como valores espaciais reais em um espaço Euclidiano tridimensional.

### Convenções de uso

- Pontos, vetores e direções devem ser expressos no mesmo referencial a menos que uma transformação explícita seja aplicada.
- Qualquer operação que envolva conversão entre referenciais deve registrar a transformação utilizada.
- A representação de orientação deve ser consistente e compatível com critérios de checagem geométrica.

---

## 4. Unidade interna (mm)

A unidade interna de comprimento do HGK será o milímetro (mm).

### Motivo

- O milímetro é a unidade mais adequada para engenharia mecânica, CAD e processo de reconstrução de modelos físicos.
- Facilita a interoperabilidade com dados industriais e padrões de fabricação.

### Regras de representação

- Todas as coordenadas internas, distâncias, raios, offsets e dimensões devem ser armazenadas e processadas em milímetros.
- Conversões para outras unidades devem ocorrer apenas nas fronteiras do sistema, nunca no núcleo geométrico interno.
- A documentação pública deve explicitar claramente qualquer conversão externa realizada.

---

## 5. Precisão numérica

O HGK deve operar com precisão numérica robusta, utilizando representação de ponto flutuante de alta precisão como base para cálculo interno.

### Padrão esperado

- Uso de aritmética de dupla precisão como padrão de implementação.
- O kernel deve assumir que pequenos desvios numéricos são normais e devem ser tratados por critérios tolerantes.

### Diretrizes

- Comparações de igualdade estrita entre valores reais devem ser evitadas.
- Avaliações de posicionamento, alinhamento e interseção devem utilizar critérios de proximidade e tolerância.
- O kernel deve manter estabilidade em operações sucessivas, especialmente em transformações, projeções e consultas topológicas.

### Padrão de referência recomendado

- Erros absolutos e relativos devem ser tratados com limites explícitos.
- O núcleo deve ser capaz de distinguir entre ruído numérico, erro de representação e inconsistência geométrica real.

---

## 6. Objetos geométricos fundamentais

O HGK deve fornecer uma coleção explícita de entidades geométricas fundamentais, organizadas em categorias de representação e relacionamento espacial.

### Entidades primárias

- Ponto 3D
  - Representa uma posição no espaço.
- Vetor 3D
  - Representa magnitude e direção.
- Segmento de reta
  - Representa uma linha limitada por dois extremos.
- Linha infinita
  - Representa uma direção e uma posição de referência.
- Plano
  - Representa uma superfície planar infinita ou limitada.
- Curva
  - Representa uma entidade unidimensional, podendo ser linear, poligonal ou contínua por partes.
- Superfície
  - Representa uma entidade bidimensional, podendo ser planar, cilíndrica, cônica ou de forma livre.
- Volume
  - Representa uma região sólida delimitada por superfícies e/ou fronteiras topológicas.

### Entidades de suporte

- Frame local ou sistema de referência local.
- Transformação affine e transformação rígida.
- Conjuntos de propriedades geométricas, como normal, tangente, curvatura e limites.
- Estruturas de análise espacial para consultas rápidas de proximidade e vizinhança.

### Regras de modelagem

- Cada entidade deve possuir uma identidade lógica e um conjunto de propriedades geométricas bem definidos.
- O kernel deve ser capaz de informar se uma entidade é válida, fechada, limitada, orientada ou degenerada.
- A representação interna deve ser suficientemente rica para permitir análise, reconstrução e exportação futura.

---

## 7. Operações matemáticas

O HGK deve implementar um conjunto de operações matemáticas básicas e avançadas para suporte à geometria, topologia e validação.

### Operações fundamentais

- soma e subtração de vetores;
- produto escalar e produto vetorial;
- normalização de vetores;
- cálculo de distância entre pontos e entre entidades;
- projeção de pontos em retas, planos e curvas;
- cálculo de ângulos e orientação espacial;
- transformações de translação, rotação e escala.

### Operações geométricas

- teste de pertinência espacial;
- criação de interseções entre entidades;
- avaliação de colisão ou proximidade;
- cálculo de limites geométricos e bounding volumes;
- determinação de orientação e consistência topológica;
- avaliação de continuidade entre entidades.

### Regras operacionais

- Operações devem retornar resultados consistentes com a política de tolerância do kernel.
- Operações que não possam ser determinadas devem retornar um estado explícito de indefinição ou não aplicável.
- Erros numéricos devem ser tratados como parte do domínio do kernel, nunca como exceções invisíveis.

---

## 8. Política de tolerâncias

A política de tolerância do HGK deve ser explícita, uniforme e configurável por contexto.

### Princípios

- A comparação geométrica deve ser baseada em proximidade e não em igualdade exata.
- Tolerâncias devem ser suficientemente pequenas para preservar precisão, mas suficientemente grandes para absorver erros numéricos inevitáveis.
- Cada operação deve ser avaliada com base em uma tolerância apropriada ao seu contexto.

### Diretrizes recomendadas

- Tolerância de construção: usada em operações de criação e ajuste inicial.
- Tolerância de validação: usada para checagem de fechamento, coincidência e consistência.
- Tolerância de comparação: usada para decisões de igualdade aproximada.

### Regras de aplicação

- Tolerâncias devem ser expressas em milímetros.
- Valores de tolerância devem ser documentados no ponto de uso.
- O kernel deve evitar depender de valores mágicos dispersos no código.
- O mesmo critério geométrico deve ser aplicado de forma consistente entre entidades equivalentes.

---

## 9. Regras de arquitetura

A arquitetura do HGK deve respeitar as seguintes regras centrais:

1. Separação de responsabilidades
   - Geometria, validação, transformação e topologia devem ser módulos distintos.

2. Dependência unidirecional
   - O núcleo não deve depender de camadas de aplicação, interface ou IA para realizar operações matemáticas fundamentais.

3. Imutabilidade de estruturas de referência
   - Entidades geométricas e dados de entrada devem ser tratados de forma estável, evitando mutações silenciosas.

4. Definição clara de contratos
   - Interfaces públicas devem expressar claramente o que é esperado, o que é retornado e o que pode falhar.

5. Encapsulamento da representação interna
   - A representação interna pode ser complexa, mas a interface externa deve permanecer simples e estável.

6. Tratamento explícito de erros
   - Falhas geométricas, entradas inválidas e inconsistências devem produzir resultados ou exceções bem definidos.

7. Evolução incremental
   - O kernel deve crescer por etapas, com compatibilidade preservada sempre que possível.

---

## 10. Interfaces públicas previstas

As interfaces públicas do HGK devem ser projetadas para permitir uso por módulos de reconstrução, visualização, validação, exportação e integração futura.

### PrecisionManager como componente oficial

O PrecisionManager é o módulo oficial de gestão de precisão do HGK e deve atuar como a camada central de controle de tolerâncias geométricas do kernel.

#### Responsabilidade do módulo

- centralizar a política de tolerâncias geométricas do sistema;
- fornecer comparações numéricas seguras para valores escalares, pontos e vetores;
- garantir consistência entre operações de validação, reconstrução e análise geométrica;
- oferecer uma base extensível para futuras operações de precisão, orientação e proximidade.

#### API pública prevista

A interface pública do PrecisionManager deve expor, no mínimo:

- inicialização com tolerância linear e angular configuráveis;
- leitura e atualização das tolerâncias padrão;
- comparação segura entre números float;
- comparação entre pontos 3D;
- comparação entre vetores 3D;
- validação explícita de entradas numéricas e estruturas de coordenadas.

#### Tolerâncias padrão

As tolerâncias padrão do módulo devem seguir as regras do HGK:

- tolerância linear padrão em milímetros;
- tolerância angular padrão em radianos;
- comparação baseada em proximidade e não em igualdade estrita;
- suporte a sobrescrita local de tolerância por chamada.

#### Integração com os demais componentes do kernel

O PrecisionManager deve ser utilizado por todos os componentes do HGK que dependam de avaliação numérica, incluindo:

- módulos de validação geométrica;
- operações de interseção e proximidade;
- processos de reconstrução e ajuste de entidades;
- mecanismos de comparação topológica e estrutural.

Sua função é garantir que o kernel opere de forma estável frente a pequenos desvios numéricos, preservando determinismo e robustez sem depender de regras dispersas ou valores mágicos.

### Interfaces conceituais esperadas

- Interface de núcleo geométrico
  - Responsável por coordenar criação, consulta e avaliação de entidades.
- Interface de fábrica geométrica
  - Responsável por construir entidades e estruturas de referência.
- Interface de transformações
  - Responsável por aplicar translação, rotação, escala e composição de transformações.
- Interface de validação geométrica
  - Responsável por verificar integridade, fechamento, orientação e consistência.
- Interface de tolerâncias
  - Responsável por configurar e aplicar políticas de precisão e proximidade.
- Interface de análise espacial
  - Responsável por consultas de proximidade, pertinência e filtragem espacial.

### Princípios de API

- A API deve ser suficientemente abstrata para suportar evolução, mas suficientemente concreta para ser usada diretamente por sistemas de alto nível.
- Operações públicas devem ser legíveis e autoexplicativas.
- A interface deve priorizar clareza sem expor detalhes irrelevantes de implementação.

---

## 11. Estratégia de testes

A estratégia de testes do HGK deve ser rigorosa, orientada por comportamento matemático e por resistência a regressões.

### Objetivos

- Garantir a correção de operações geométricas básicas.
- Proteger a estabilidade numérica em cenários com valores próximos ou degenerados.
- Verificar a consistência entre representação, transformação e avaliação.

### Tipos de teste esperados

- Testes unitários
  - Cobrem operações elementares como distância, projeção, normalização e transformações.
- Testes de regressão
  - Protegem comportamentos críticos já validados contra mudanças futuras.
- Testes de consistência geométrica
  - Verificam propriedades como fechamento, orientação e continuidade.
- Testes de tolerância
  - Confirmam que pequenas variações numéricas não causam falhas indevidas.
- Testes de integração
  - Validam a interação do kernel com pipelines de malha, reconstrução e exportação.

### Critérios de aceitação

- O kernel deve ser testado para entradas válidas e inválidas.
- Operações de fronteira devem ser verificadas com casos degenerados.
- Todos os comportamentos públicos relevantes devem possuir cobertura adequada.

---

## 12. Compatibilidade futura

O HGK deve ser projetado para evolução sem sacrificar estabilidade estrutural.

### Diretrizes de compatibilidade

- Mudanças públicas devem seguir uma política de evolução controlada.
- Novos recursos devem ser adicionados sem exigir reescrita completa de fluxos existentes.
- Recursos antigos devem permanecer suportados quando possível, com depreciação explícita.
- A arquitetura deve permitir a introdução de novos tipos de entidade e algoritmos sem quebrar o contrato principal.

### Estratégia de expansão

- O HGK deve apoiar extensões por meio de módulos bem definidos e sem acoplamento indevido.
- A compatibilidade com cenários futuros de reconstrução paramétrica, análise de fabricação e interoperabilidade CAD deve ser considerada desde a fase inicial.
- A evolução do kernel deve preservar sua função central: fornecer uma base geométrica confiável, estável e matematicamente consistente.

---

## Conclusão

O HGK é a camada fundamental de confiança do sistema HFC Reverse CAD. Sua função não é apenas representar geometria, mas garantir que toda interpretação, reconstrução e validação do modelo seja sustentada por uma base matemática sólida, previsível e extensível. A adoção desta especificação estabelece as bases para um núcleo geométrico profissional, modular e preparado para evolução técnica.
