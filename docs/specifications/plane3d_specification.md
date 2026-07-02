# Plane3D Specification

## 1. Objetivo da classe

A classe `Plane3D` representa um plano geométrico infinito no espaço tridimensional. Ela fornece uma abstração matemática para definir orientação e posição de uma superfície plana, permitindo cálculos de distância, projeção, normalização e interseção com outros elementos geométricos do kernel.

## 2. Responsabilidades

- representar um plano no espaço 3D com uma posição e uma orientação bem definidas
- armazenar e validar os parâmetros de definição do plano
- calcular a distância de um `Point3D` ao plano
- projetar pontos e vetores sobre o plano
- determinar se pontos ou vetores estão contidos, paralelos ou ortogonais ao plano
- fornecer um sistema de normalização e consistência de sinal para a representação do plano
- suportar transformações afins através de `Transform3D` / `Matrix4x4`

## 3. Relação com Point3D

- `Plane3D` é definida, em parte, a partir de um ponto de apoio no plano, geralmente um `Point3D`.
- `Point3D` serve como referência de posição para calcular a equação do plano e para determinar se um ponto pertence ao plano.
- Operações comuns envolvendo `Point3D` incluem:
  - calcular distância perpendicular do ponto ao plano
  - projetar um ponto sobre o plano
  - validar a inclusão de um ponto com base na tolerância de precisão do kernel

## 4. Relação com Vector3D

- A orientação do plano é definida por um vetor normal unitário, representado por `Vector3D`.
- `Vector3D` é usado para:
  - armazenar a direção normal do plano
  - calcular projeções de vetores e pontos
  - avaliar paralelismo entre o plano e outros vetores ou planos
  - derivar a orientação do plano a partir de duas direções tangenciais, quando aplicável
- A classe deve garantir que o vetor normal esteja normalizado e represente um único sentido consistente.

## 5. Relação com Transform3D

- `Transform3D` permite transformar a posição e a orientação do plano via operações afins.
- `Plane3D` deve expor métodos para aplicar um `Transform3D` e gerar um novo plano transformado.
- Transformações devem afetar corretamente tanto a origem de referência quanto o vetor normal.
- A aplicação de transformações homogêneas deve preservar a propriedade de plano, incluindo reflexões e rotações.

## 6. Relação com Matrix4x4

- `Transform3D` é representado internamente por `Matrix4x4`.
- `Plane3D` pode ser convertido em ou derivado de uma matriz de transformação quando a aplicação a uma superfície ou espaço local for necessária.
- Para transformações diretas, `Plane3D` deve suportar a aplicação de uma `Matrix4x4` equivalente ao `Transform3D`.
- A matriz 4x4 também é útil para converter o plano em coordenadas homogêneas e para composições de transformações entre sistemas de referência.

## 7. Forma matemática do plano

A forma matemática do plano deve ser definida com rigor e consistência:

- Equação cartesiana geral: `ax + by + cz + d = 0`
- Vetor normal: `n = (a, b, c)` com norma unitária
- Distância de um ponto `P(x, y, z)` ao plano: `distance = n dot P + d`
- Ponto de referência: qualquer `Point3D` `P0` no plano satisfaz `n dot P0 + d = 0`
- Representação alternativa: `Plane3D(n, P0)` onde `n` é o vetor normal e `P0` é um ponto no plano

A classe deve manter coerência entre essas representações e normalizar a forma interna para evitar ambiguidades de sinal.

## 8. Métodos públicos previstos

A interface pública proposta para `Plane3D` deve incluir, no mínimo:

- `__init__(self, normal: Vector3D, point: Point3D)`
- `from_coefficients(cls, a: float, b: float, c: float, d: float) -> "Plane3D"`
- `from_points(cls, p1: Point3D, p2: Point3D, p3: Point3D) -> "Plane3D"`
- `normal(self) -> Vector3D`
- `point_on_plane(self) -> Point3D`
- `distance_to_point(self, point: Point3D) -> float`
- `project_point(self, point: Point3D) -> Point3D`
- `is_point_on_plane(self, point: Point3D, tolerance: float | None = None) -> bool`
- `is_parallel_to(self, other: "Plane3D") -> bool`
- `is_orthogonal_to(self, other: "Plane3D") -> bool`
- `intersect_with_plane(self, other: "Plane3D") -> "Line3D" | None`
- `apply_transform(self, transform: Transform3D) -> "Plane3D"`
- `apply_matrix(self, matrix: Matrix4x4) -> "Plane3D"`
- `to_coefficients(self) -> tuple[float, float, float, float]`
- `to_string(self) -> str`

Métodos auxiliares previstos:

- `normalize(self) -> "Plane3D"`
- `flip(self) -> "Plane3D"`
- `signed_distance_to_point(self, point: Point3D) -> float`

## 9. Casos de uso

- validar que uma face geométrica está corretamente orientada no espaço
- projetar pontos de nuvem ou malha para estimar uma superfície plana local
- calcular a distância de um ponto a um plano de referência em análises de inspeção
- construir planos de corte para seções ou alinhamento geométrico
- suportar operações de reconstrução de superfícies planas em engenharia reversa
- determinar interseções entre planos para extração de arestas e linhas de contorno

## 10. Estratégia de testes

A estratégia de testes deve cobrir:

- criação de planos a partir de coeficientes e pontos
- validação da normalização do vetor normal
- cálculo de distância e sinal correto para pontos acima e abaixo do plano
- projeção de pontos e verificação de pontos projetados no plano
- comparação de pontos com tolerância para decisões de inclusão
- transformações com `Transform3D` e `Matrix4x4`
- casos degenerateis: pontos colineares em `from_points`, vetores nulos ou normais inválidos
- consistência de sinal após `flip` e `normalize`
- interseção de planos paralelos, coincidentes e intersectantes

Testes devem ser herméticos, determinísticos e baseados em tolerância numérica controlada.

## 11. Critérios de desempenho

- instânciação e validação devem ser rápidas para uso em malhas e análise local
- operações de distância e projeção devem ser O(1)
- transformações devem evitar cópias desnecessárias de dados quando possível, retornando instâncias derivadas sem estado mutável
- a normalização deve ser estável numericamente e tratar casos de magnitude muito pequena com validações claras
- a implementação deve manter desempenho aceitável para algoritmos que iteram sobre centenas de milhares de pontos ou planos

## 12. Compatibilidade futura

- projetar a API para facilitar extensões a outras entidades geométricas como `Surface3D` ou `PlaneSegment`
- manter o plano como entidade imutável para permitir uso seguro em pipeline multithread
- permitir representação dual de plano (coeficientes e normal/ponto) sem quebra de compatibilidade
- garantir que mudanças internas de precisão não alterem contratos públicos de comparação e distância
- documentar limites de uso, incluindo casos de planos degenerados e aproximação numérica
- preservar a possibilidade de derivar `Plane3D` a partir de dados de malha, nuvem de pontos e algoritmos de detecção de primitives
