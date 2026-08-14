<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

</head>

<body>

  <h1>Documentação de Configuração do Ambiente e Serviços (Firebase &amp; Cloud Shell)</h1>

  <h2>1. Seleção do Projeto e Acesso ao Console do Firebase</h2>

  <p>Inicialmente, deve-se acessar o <strong>Console do Firebase</strong> para realizar a seleção e o gerenciamento do projeto que será utilizado durante o processo de configuração do ambiente.</p>

  <p> Após o acesso ao console, seleciona-se o projeto correspondente à aplicação, permitindo a utilização dos recursos e serviços disponibilizados pela plataforma Firebase.</p>

  <img
        width="267"
        height="202"
        alt="Acesso ao Console do Firebase"
        src="https://github.com/user-attachments/assets/733111a5-10ec-4c3b-8419-790d3ea4bc28"
    >

   <hr>

  <h2>2. Abertura do Cloud Shell no Google Cloud / Firebase</h2>

  <p>Após a seleção do projeto, o <strong>Cloud Shell</strong> é inicializado na parte inferior da interface do Google Cloud/Firebase.</p>

  <p> O ambiente de terminal é configurado automaticamente e direcionado para o <strong>ID do projeto selecionado</strong>, permitindo a execução dos comandos necessários para a configuração e manutenção do ambiente.</p>

  <img
        width="317"
        height="226"
        alt="Abertura do Cloud Shell"
        src="https://github.com/user-attachments/assets/2e496d2a-919b-43a5-a0e8-c23329271e31"
    >

  <hr>

  <h2>3. Configuração do Ambiente Virtual em Python no Cloud Shell</h2>

  <p>Para proporcionar o isolamento das dependências utilizadas pela aplicação,é criado um <strong>ambiente virtual em Python</strong> no Cloud Shell.Essa configuração permite organizar as dependências do projeto de forma independente do ambiente principal, contribuindo para a execução controlada das etapas de desenvolvimento, testes e automação.</p>

  <h3>3.1 Criação do ambiente virtual</h3>

   <p>Para criar o ambiente virtual, executa-se o seguinte comando:</p>

  <pre><code>python3 -m venv investetec</code></pre>

  <p>O comando realiza a criação de um ambiente virtual denominado <code>investetec</code>, que será utilizado para a execução das atividades relacionadas ao projeto.</p>

  <img
        width="1007"
        height="238"
        alt="Criação do ambiente virtual"
        src="https://github.com/user-attachments/assets/49b9630c-7457-45a2-ad81-8d2537c0213b"
    >

  <h3>3.2 Verificação dos diretórios existentes</h3>

  <p>Após a criação do ambiente virtual, utiliza-se o comando abaixo para verificar os arquivos e diretórios presentes no ambiente atual:</p>

  <pre><code>ls</code></pre>

  <p>A execução do comando permite verificar a presença do diretório <code>investetec</code> juntamente aos demais arquivos e diretórios existentes no projeto.</p>

  <img
        width="1013"
        height="220"
        alt="Verificação dos diretórios existentes"
         src="https://github.com/user-attachments/assets/f224a006-b255-4e65-a245-b1a3169c74e8"
    >

  <h3>3.3 Ativação do ambiente virtual</h3>

  <p>Para ativar o ambiente virtual previamente criado, executa-se o comando:</p>

  <pre><code>source investetec/bin/activate</code></pre>

  <p>Após a execução, o terminal passa a apresentar o prefixo <code>(investetec)</code>, indicando que o ambiente virtual foi ativado corretamente e está disponível para a execução dos comandos relacionados ao projeto.</p>

   <img
        width="1042"
        height="250"
        alt="Ativação do ambiente virtual"
         src="https://github.com/user-attachments/assets/23b2fb54-73f4-4f8e-aae8-af9b1f7ab87a" 
    >

  <hr>

  <h2>4. Edição de Arquivos e Código no Cloud Shell Editor</h2>

  <p>Para acessar a estrutura de arquivos do projeto e realizar alterações no código-fonte ou nos arquivos de configuração, utiliza-se o <strong>Cloud Shell Editor</strong>.</p>

  <h3>4.1 Acesso ao editor</h3>

  <p>Na interface do Cloud Shell, seleciona-se a opção <strong>"Abrir editor"</strong>, permitindo acessar o ambiente destinado à visualização e edição dos arquivos do projeto.</p>

  <p>O editor possibilita a manipulação de arquivos de código, documentação e configurações necessárias para a implementação do fluxo de CI/CD.</p>

  <img
        width="222"
        height="87"
        alt="Abertura do Cloud Shell Editor"
        src="https://github.com/user-attachments/assets/b9756c53-2b73-4a39-be46-f9e01a1024fd"
    >

  <h3>4.2 Navegação e edição dos arquivos</h3>

  <p>A partir da árvore de arquivos disponibilizada pelo editor, é possível navegar pelos diretórios do projeto, incluindo estruturas como <code>feirascore</code> e <code>tcc-vm-vimi</code>.</p>

  <p>Nesse ambiente, podem ser criados ou modificados os arquivos necessários para a implementação e configuração do fluxo de <strong>CI/CD utilizando GitHub Actions</strong>, além dos arquivos relacionados à configuração dos serviços do Firebase.</p>

  <img
        width="371"
        height="151"
        alt="Estrutura de arquivos do projeto"
        src="https://github.com/user-attachments/assets/085e51e0-19cb-407c-b7ed-cb30d9078c57"
    >

<hr>

  <h2>5. Execução do Servidor de Desenvolvimento</h2>

  <p>Após a configuração do ambiente, realiza-se a inicialização do servidor de desenvolvimento local para possibilitar a validação do código e das integrações antes da realização do processo de deploy.</p>

  <h3>5.1 Execução do script de desenvolvimento</h3>

  <p>No terminal integrado do VS Code, executa-se o seguinte comando:</p>

  <pre><code>source devserver.sh</code></pre>

  <p>Esse comando executa o script <code>devserver.sh</code>, responsável por iniciar a rotina de desenvolvimento local previamente configurada no projeto.</p>

  <img
        width="886"
        height="211"
        alt="Execução do servidor de desenvolvimento"
        src="https://github.com/user-attachments/assets/5504df5a-2d9f-4423-84c7-0569dd366e7d"
    >

  <h3>5.2 Carregamento das configurações no terminal</h3>

  <p> O utilitário <code>source</code> realiza a leitura e execução das instruções presentes no arquivo <code>devserver.sh</code>, aplicando as configurações e variáveis definidas diretamente ao processo do terminal atualmente em execução.</p>

  <p>Dessa forma, as configurações estabelecidas pelo script passam a estar disponíveis no ambiente utilizado para o desenvolvimento.</p>

  <h3>5.3 Inicialização do servidor local</h3>

  <p>Após a execução do script, o ambiente local de desenvolvimento é iniciado, permitindo a realização de testes e validações da aplicação.</p>

  <p>Essa etapa possibilita verificar o funcionamento do código e das integrações configuradas antes da realização do processo de <strong>deploy</strong>, contribuindo para a identificação antecipada de possíveis problemas no ambiente de execução.</p>

</body>
</html>
