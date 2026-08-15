<h1 align="center">Domínio 1: Identidade e Acesso</h1>
<p>Gerencia o ciclo de vida dos usuários, autenticação e a diferenciação de perfis no sistema.</p>

<p><b>📄 Tabela: USUARIO</b><br>
Tabela base para autenticação e perfis.</p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_usuario` | PK | Identificador único do usuário |
| `email` | Único | E-mail para login |
| `senha_hash` | Requerido | Hash de segurança da senha |
| `status_conta` | Requerido | Estado atual da conta |
| `tipo_perfil` | Requerido | Define o perfil (Aluno, Empresa, Administrador) |

<p><b>📄 Tabela: ALUNO</b><br>
Especialização de USUARIO.</p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_aluno` | PK / FK | Vínculo com USUARIO(id_usuario) |
| `nome_completo` | Requerido | Nome completo do estudante |
| `id_curso` | FK | Vínculo com o curso ativo (CURSO) |
| `email_institucional` | Domínio Obrigatório | E-mail corporativo (@etec.sp.gov.br) |

<p><b>📄 Tabela: EMPRESA</b><br>
Especialização de USUARIO.</p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_empresa` | PK / FK | Vínculo com USUARIO(id_usuario) |
| `cnpj_cpf` | Documento Fiscal | CNPJ ou CPF para validação |
| `status_validacao` | Requerido | Estado da validação da empresa (Ativo/Validado) |

<p><b>📄 Tabela: ADMINISTRADOR</b><br>
Especialização de USUARIO (Docentes, orientadores ou gestores da ETEC).</p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_administrador` | PK / FK | Vínculo com USUARIO(id_usuario) |

<h2> Domínio 2: Catálogo de Projetos</h2>
<p>Organiza as informações técnicas, conceituais e arquivos multimídia dos Trabalhos de Conclusão de Curso (TCC).</p>

<p><b>📄 Tabela: PROJETO</b></p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_projeto` | PK | Identificador único do projeto |
| `titulo` | Requerido | Título do projeto |
| `resumo_executivo` | Requerido | Breve apresentação do projeto |
| `problema_solucionado` | Requerido | Descrição do problema abordado |
| `solucao_proposta` | Requerido | Detalhamento da solução |
| `tecnologias_utilizadas` | Texto / Resumo | Visão geral das tecnologias |
| `link_repositorio` | URL | Link do repositório (ex.: GitHub) |
| `link_video_demonstrativo` | URL | Link do vídeo (ex.: YouTube, Vimeo) |
| `status_projeto` | Default: PENDENTE | Estado atual da submissão |
| `id_aluno_lider` | FK | Referência ao ALUNO(id_aluno) responsável |

<p><b>📄 Tabela: PROJETO_INTEGRANTE</b><br>
Tabela associativa de coautores do projeto.</p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_projeto` | FK | Referência a PROJETO(id_projeto) |
| `id_aluno` | FK | Referência a ALUNO(id_aluno) |
| `funcao` | Requerido | Papel no projeto (ex.: Desenvolvedor, Designer) |

<p><b>📄 Tabela: ANEXO</b></p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_anexo` | PK | Identificador único do anexo |
| `id_projeto` | FK | Referência a PROJETO(id_projeto) |
| `arquivo_multimidia` | Referência/URL | Caminho ou ponteiro para o arquivo armazenado |

<p><b>📄 Tabela: TECNOLOGIA</b></p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_tecnologia` | PK | Identificador único da tecnologia |
| `nome_tecnologia` | Requerido | Nome da ferramenta/linguagem |

<p><b>📄 Tabela: PROJETO_TECNOLOGIA</b><br>
Tabela associativa N:M entre projetos e tecnologias.</p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_projeto` | FK | Referência a PROJETO(id_projeto) |
| `id_tecnologia` | FK | Referência a TECNOLOGIA(id_tecnologia) |

<h2> Domínio 3: Conexão & Negócios</h2>
<p>Provê os meios para que empresas validadas e investidores interajam com os alunos criadores dos projetos.</p>

<p><b>📄 Tabela: MANIFESTACAO_INTERESSE</b></p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_manifestacao` | PK | Identificador único da manifestação |
| `id_empresa` | FK | Referência a EMPRESA(id_empresa) |
| `id_projeto` | FK | Referência a PROJETO(id_projeto) |
| `tipo_proposta` | Enum / Restrição | Apoio Financeiro/Patrocínio ou Mentoria Técnico-Mercadológica |

<h2> Domínio 4: Governança, Moderação e Auditoria</h2>
<p>Garante o controle de qualidade acadêmica, moderação e a rastreabilidade legal das ações no sistema.</p>

<p><b>📄 Tabela: AVALIACAO</b></p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_avaliacao` | PK | Identificador único da avaliação |
| `id_projeto` | FK | Referência a PROJETO(id_projeto) |
| `id_administrador` | FK | Referência a ADMINISTRADOR(id_administrador) |
| `parecer_tecnico` | Texto | Feedback técnico para os estudantes |
| `decisao_status` | Enum | APROVADO, SOLICITOU_AJUSTES ou REJEITADO |

<p><b>📄 Tabela: NOTIFICACAO</b></p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_notificacao` | PK | Identificador único da notificação |
| `id_aluno_lider` | FK | Referência ao aluno líder destinatário |
| `id_orientador` | FK | Referência ao orientador responsável destinatário |
| `mensagem` | Texto | Conteúdo disparado após registro em MANIFESTACAO_INTERESSE |

<p><b>📄 Tabela: HISTORICO_STATUS</b></p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_historico` | PK | Identificador único do registro de histórico |
| `id_projeto` | FK | Referência a PROJETO(id_projeto) |
| `status_anterior` | Requerido | Estado prévio do projeto |
| `status_novo` | Requerido | Estado atualizado do projeto |
| `data_transicao` | Timestamp | Data e hora da mudança |

<p><b>📄 Tabela: AUDITORIA</b></p>

| Campo | Tipo / Restrição | Descrição |
| :---: | :--------------: | :-------: |
| `id_auditoria` | PK | Identificador único da auditoria |
| `id_usuario` | FK | Referência a USUARIO(id_usuario) responsável pela ação |
| `acao_executada` | Requerido | Descrição da operação realizada |
| `tabela_afetada` | Requerido | Nome da tabela modificada |
| `timestamp` | Timestamp | Data e hora do evento |
| `ip_origem` | Requerido | Endereço IP do cliente |
