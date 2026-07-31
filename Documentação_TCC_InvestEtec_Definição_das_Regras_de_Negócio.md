<h1> Especificação e Amostras de Regras de Negócio (RN)
<br/> 
  
<h1> 1. Contextualização e Introdução Teórica </h1>
  
  <p>No desenvolvimento de sistemas de software, especialmente no contexto de Trabalhos de Conclusão de Curso (TCC), as Regras de Negócio (RN) representam o conjunto de declarações formais que definem ou restringem aspectos do negócio, visando garantir a governança, a coerência operacional e o cumprimento dos objetivos estratégicos da aplicação. Para o projeto InvestEtec, cujo objetivo principal é combater o "problema da gaveta" conectando alunos e projetos acadêmicos a investidores e ao mercado de trabalho, a definição rigorosa das Regras de Negócio atua como elemento articulador entre a concepção do produto e sua implementação técnica nas arquiteturas Back-end (Node.js) e Front-end (React).</p>

 <h1>2. Estrutura Padrão para Especificação de Regras de Negócio</h1>

 <p>Cada Regra de Negócio documentada deve seguir uma estrutura padronizada para evitar ambiguidades entre a equipe de documentação, os desenvolvedores e a banca examinadora. A estrutura contempla os seguintes atributos:</p>

● **Identificador Único (ID)**: Código sequencial (ex.: RN-001) para rastreabilidade nos artefatos de software.

● **Título**: Denominação sucinta do conceito ou da restrição imposta.

● **Descrição Detalhada**: Especificação clara da condição, comportamento ou validação exigida.

● **Atores Impactados**: Perfis de usuários afetados pela regra (Aluno, Empresa/Investidor, Administrador).

</br>

  <h1>3. Amostra de Regras de Negócio do Sistema InvestEtec</h1>

<p>Abaixo apresenta-se o conjunto de amostras de Regras de Negócio mapeadas para os principais módulos funcionais do sistema InvestEtec, detalhadas em formato descritivo estruturado:</p>

<h2>RN-001: Diferenciação de Perfil de Acesso</h2>

  ● **Descrição**: O sistema deve gerenciar estritamente três perfis: Aluno/Proponente, Empresa/Investidor e Administrador. Cada perfil terá permissões restritas em nível de rotas

● **Atores**: Todos os usuários.

<h2>RN-002: Validação do Vínculo Acadêmico</h2>

 ● **Descrição**: O cadastro de perfil Aluno requer validação via e-mail institucional ou verificação do código de matrícula/curso ativo na ETEC Sylvio de Mattos Carvalho.

● **Atores**: Aluno.

<h2>RN-003: Autenticação Corporativa de Investidores</h2>

  ● **Descrição**: Para realizar contatos formais de investimento, a conta empresarial devefornecer CNPJ/CPF válido e confirmação de dados de contato institucional.

 ● **Atores**: Empresa / Investidor.
 
  <h2>RN-004: Campos Mínimos Obrigatórios do Projeto</h2>
  
● **Descrição**: A submissão de um projeto deve obrigatoriamente conter: Título, Resumo/Justificativa, Área Técnica, Lista de Integrantes, Tecnologias Utilizadas e Contato Principal.

● **Atores**: Aluno.

  <h2>RN-005: Designação de Líder do Projeto</h2>
  
  ● **Descrição**: Um projeto pode possuir múltiplos alunos associados, mas exige a atribuição de exatamente 1 (um) Aluno Líder responsável por edições e submissões.

  ● **Atores**: Aluno.

  <h2>RN-006: Moderação Institucional Prévia</h2>

  ● **Descrição**: Todo projeto publicado entra em status 'Pendente', tornando-se público na vitrine virtual somente após homologação e aprovação pelo Administrador/ETEC.
  
  ● **Atores**: Administrador / Aluno.

 <h2>RN-007: Restrição de Acesso Público a Dados Sensíveis</h2>  

   ● **Descrição**: Visitantes não autenticados podem visualizar resumos e informações técnicas de projetos na vitrine, mas não possuem acesso aos dados diretos de contato dos alunos.

   ● **Atores**: Visitante.

 <h2>RN-008: Registro e Histórico de Abordagens de Investimento</h2>   

   ● **Descrição**: Ações de interesse ou solicitações de contato efetuadas por empresas devem ser auditadas e registradas no histórico interno da plataforma.

   ● **Atores**: Empresa / Administrador.

 <h2>RN-009: Proteção de Dados e Alunos Menores de Idade</h2> 

  ● **Descrição**: Para discentes menores de 18 anos, as comunicações institucionais devem prever mediação da coordenação ou autorização expressa do responsável legal (LGPD).

  ● **Atores**: Aluno / Administrador.

 <h2> RN-010: Gestão do Ciclo de Vida do Projeto</h2> 

  ● **Descrição**: Projetos concluídos ou que captaram financiamento podem ser alterados para o status 'Arquivado' ou 'Financiado', mantendo a rastreabilidade histórica no banco de dados.

   ● **Atores**: Aluno / Administrador.

   <h1>4. Recomendações para a Equipe de Desenvolvimento e Documentação</h1>

  **1. Inclusão no Relatório Final do TCC**: Inserir este capítulo na seção de "Análise e Projeto de Sistemas" da monografia. 

  **2. Validação com o Orientador**: Apresentar a lista de regras ao professor orientador para homologação do escopo operacional do sistema.

  **3. Controle de Versão dos Artefatos**: Atualizar os identificadores sempre que houver alteração nos requisitos de negócio acordados com a instituição.
 
   
