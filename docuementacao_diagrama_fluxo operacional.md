<h1 align="center">1. Visão Geral do Sistema</h1>
    
  <p>O sistema possui a fragmentação através de uma arquitetura centralizada baseada em quatro pilares fundamentais:</p>

  **• Identidade e Acesso:** <p>Mecanismos rigorosos de autenticação e segregação de perfis de acesso.<p>
  **• Catálogo de Projetos:** <P>Estrutura para cadastramento, categorização, versionamento e enriquecimento de mídias dos trabalhos.<P>
  **• Conexão & Negócios:** <P>Módulo de interação onde empresas prospectam talentos e formulam propostas de apoio ou investimentos.<P>
  **• Governança:** <P>Módulo de moderação e auditoria acadêmica que assegura a qualidade, a veracidade dos dados e o alinhamento das publicações às diretrizes institucionais.<P>

  <H2>2. Regras de Negócio e Especificação de Domínios</H2>
    <h3>2.1 Domínio 1: Identidade e Acesso</h3>

  <p>O Domínio de Identidade e Acesso gerencia o ciclo de vida dos usuários na plataforma, impondo regras de validação para cada perfil.</p>

  <h3> Diferenciação de Permissões e Perfis Especializados:</h3> <p>A entidade base USUARIO contém as credenciais de autenticação (email, senha_hash) e o controle de estado (status_conta). A especialização ocorre na relação de cardinalidade (1 : 0..1) entre USUARIO e suas extensões: ALUNO, EMPRESA e ADMINISTRADOR.<p>

  <h3> Regra de Validação de Proponente (Aluno)</h3> <p>O cadastro de um perfil de proponente (ALUNO) exige obrigatoriamente a validação de um e-mail institucional pertencente ao domínio @etec.sp.gov.br. A ausência ou invalidação desse domínio impede a atribuição de permissão para submissão de projetos. Além disso, a entidade exige o vínculo com um CURSO ativo.</p>

  <h3>Regra de Validação Corporativa (Empresa)</h3> <p>O cadastro de perfis corporativos/investidores exige a validação formal de documentos jurídicos ou fiscais válidos (CNPJ ou CPF ). Apenas empresas com status ativo e dados validados podem acessar ferramentas de contato direto com os alunos.</p>

  <h3>Mecanismos do Administrador</h3> <p>Perfis cadastrados como ADMINISTRADOR representam docentes, orientadores ou gestores da ETEC, possuindo privilégios para moderação, alteração de status e auditoria de ações no sistema.</p>

  <h2>2.2 Domínio 2: Catálogo de Projetos</h2>

  <p>Este domínio organiza as informações técnicas, conceituais e os materiais demonstrativos dos Trabalhos de Conclusão de Curso.</p>

   <h3 align="center">Regra de Cadastramento e Obrigatoriedade de Campos</h3> <p>Ao submeter um TCC na entidade PROJETO, a plataforma valida a presença obrigatória dos seguintes dados:</p>

  **titulo:**  Nome oficial do projeto.

  **resumo_executivo:**  Descrição conceitual do problema e solução.

  **problema_solucionado:**  Contextualização da dor abordada.
  
  **solucao_proposta:**  Descrição técnica da abordagem desenvolvida.

  **tecnologias_utilizadas:**  Lista descritiva de apoio.

  **link_repositorio / link_video_demonstrativo:**  Referências externas para código-fonte (ex.: GitHub) e demonstração funcional (ex.: YouTube/Vimeo)

  <h3 align="center">Definição de Status Inicial</h3> 
  <p>Todo projeto submetido assume obrigatoriamente e de forma automatizada o status inicial PENDENTE . O projeto nesse estado permanece inacessível na vitrine pública.</p>

  <h3 align="center">Atribuição de Liderança e Equipe</h3>
  <p>O aluno que submete o projeto é registrado como id_aluno_lider. A inclusão de coautores e colaboradores é gerenciada através da entidade associativa PROJETO_INTEGRANTE, que especifica o id_aluno e sua respetiva funcao (ex.: Desenvolvedor, Designer, Documentador).</p>

  <h3 align="center" >Anexos e Tecnologias </h3>
  <p>Um projeto pode associar múltiplos arquivos multimídia através da entidade ANEXO (1:N) e múltiplas linguagens/frameworks via entidade n-para-n PROJETO_TECNOLOGIA, conectando PROJETO e TECNOLOGIA.</p>

  <h2>2.3 Domínio 3: Conexão & Negócios</h2>
  <p>Este domínio provê os meios formais para que o mercado corporativo interaja com os alunos criadores dos projetos</p>

  <h3>Manifestação de Interesse</h3>
  <p>A abordagem de uma empresa a um projeto cadastrado é registrada na entidade MANIFESTACAO_INTERESSE. É fundamental que a empresa esteja com o cadastro validado no Domínio 1.</p>

  <h3>Tipologia de Propostas</h3>
  <p>A manifestação exige a especificação do tipo_proposta, categorizado estritamente em: Oportunidade de Apoio Financeiro/Patrocínio e  Mentoria Técnico-Mercadológica.</p>

  <h3>Disparo de Eventos de Comunicação</h3>
  <p>A criação de um registro em MANIFESTACAO_INTERESSE desencadeia um evento interno que registra uma entrada na entidade NOTIFICACAO, direcionando os detalhes ao id_aluno_lider </p>

  <h2>2.4 Domínio 4: Governança, Moderação e Auditoria</h2>
  <p>O Domínio de Governança garante o controle de qualidade e a rastreabilidade legal das ações executadas na plataforma</p>

**1. Estado PENDENTE:** <p>Projeto submetido, aguardando análise no painel do administrador.</p>
**2. Análise Institucional:** <p>O administrador avalia a documentação, o código e os requisitos acadêmicos, registrando parecer na entidade AVALIACAO.</p>
**3. Transição de Estado:**
  <p>• APROVADO : Permite visibilidade imediata na Vitrine Pública.</p>
  <p>• SOLICITOU_AJUSTES : O aluno recebe parecer técnico na entidade AVALIACAO, corrige os dados e ressubmete.</p>
  <p>• REJEITADO : A publicação é negada por descumprimento de diretrizes.</p>

<h3>Auditoria e Histórico</h3> <p>A tabela HISTORICO_STATUS registra cronologicamente todas as transições de fase. A tabela AUDITORIA rastreia ações críticas do sistema capturando usuário, ação, tabela afetada, timestamp e IP.</p>

<h1>3. Modelo Entidade-Relacionamento (DER)</h1>
  <h2>3.1 Legenda de Cardinalidades e Convenções</h2>
  
   **• Chaves Primárias (PK):** <p>Identificadores únicos de cada entidade (id_nomeentidade).</p>
   **• Chaves Estrangeiras (FK):** <p>Atributos que estabelecem os vínculos relacionais entre as tabelas.</p>
   
  **Regras de Cardinalidade Adotadas:**
   **1 : 0..1 —** <p>Um para zero ou um (Especialização / Opcionalidade estrita).</p>
   **1 : N —** <p>Um para muitos (Relacionamento Pai-Filho).</p>
   **N : M—**  <p>Muitos para muitos (Implementado via tabela associativa intermediária).</p>

  <h2>3.2 Apresentação Visual da Modelagem Sanitizada</h2>
  <p>Abaixo apresenta-se o diagrama textual do DER, com as devidas correções de cardinalidade do Usuário, desconexão de Avaliação com Integrantes e remoção da ligação orfã entre Projetos e Notificações:</p>

  <img width="751" height="587" alt="NOI" src="https://github.com/user-attachments/assets/beba713a-b143-453e-915d-5bb58d3f1bde" />
  <br>
  <img width="751" height="587" alt="BOM" src="https://github.com/user-attachments/assets/e7e08beb-237f-44c9-ba5a-1fb863ccbdda" />
  <br>
  <img width="751" height="230" alt="bom" src="https://github.com/user-attachments/assets/b755c020-583a-439c-bfb4-c7fa7d0f3ef7" />

  <h2>3.3 Especificação do Dicionário de Dados</h2>
   <h3>Tabela: USUARIO</h3>
   <img width="782" height="237" alt="tarde" src="https://github.com/user-attachments/assets/06e7de8d-da08-460f-99fb-c18982cf7d0a" />
   <br>
   <h3>Tabela: ALUNO</h3>
   <img width="773" height="169" alt="meio dia" src="https://github.com/user-attachments/assets/acf45f49-cc21-4e99-8e8d-50887c612ab7" />
   <br>
   <h3>Tabela: PROJETO</h3>
   <img width="773" height="241" alt="gliter" src="https://github.com/user-attachments/assets/6521f2f3-4091-44f6-ade1-974cca0032ef" />
   <br>
   <h3>Tabela: AVALIACAO</h3>
   <img width="773" height="171" alt="battaa" src="https://github.com/user-attachments/assets/8159df1f-9611-4db6-ad80-74b498c70f9c" />
   <br>
   <h1>4. Mapeamento Meticuloso do Fluxo Operacional</h1>
     <h2>4.1 Autenticação, Identificação de Perfil e Controle de Acesso</h2>
    <p>O fluxo inicia-se no acesso do usuário à plataforma, seguido da criação da conta base e especialização por perfil:</p>
    
  <img width="770" height="256" alt="melrca" src="https://github.com/user-attachments/assets/b967ed57-3539-413c-b56d-00b8b533cee7" />
  
<h2>4.2 Submissão e Estruturação Técnica do TCC</h2>
 <p>Após a autenticação como Aluno proponente, é liberado o cadastro de projetos:</p>
  <img width="763" height="185" alt="charlie" src="https://github.com/user-attachments/assets/8449fb24-63ef-4894-a89b-26112bb841ac" />

  <h2>4.3 Workflow de Moderação Institucional e Transição de Status</h2>
  <p>Moderação realizada pelos docentes/administradores da instituição:</p>

  <img width="771" height="324" alt="001" src="https://github.com/user-attachments/assets/4928403a-ef2c-4d66-a42d-ddf04f3cdada" />
<h2>4.4 Divulgação na Vitrine Pública e Abordagem Corporativa</h2>
<p>Com o projeto em estado APROVADO , ele é listado na vitrine pública. As empresas autenticadas podem realizar busca por filtros (Curso, Categoria, Tecnologia) e enviar propostas via MANIFESTACAO_INTERESSE. 4.5</p>

  <h2>4.5 Rastreabilidade, Notificação e Auditoria da Plataforma</h2>
 <p>A criação de uma manifestação de interesse gera um evento de disparo para a tabela NOTIFICACAO, alertando o líder do projeto e seu orientador (RESPONSAVEL_ORIENTADOR). Todas as operações críticas da plataforma geram logs em AUDITORIA.</p> 

 <br>

 <img width="1942" height="1606" alt="FluxoOpracional drawio" src="https://github.com/user-attachments/assets/9c2e787d-23a3-4d6d-9a0a-a98b997e97d6" />

  




   

  




  
