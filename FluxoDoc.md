<!DOCTYPE html> 
<html lang="pt-BR"> 
  <head> 

   <meta charset="UTF-8"> 

  <meta name="viewport" content="width=device-width, initial-scale=1.0"> 

</head> 

  <body> 



  <h1>Guia Passo a Passo: Criação de Workspace e Conexão de Repositório no Render</h1> 

   <h2>Passo 1: Acesso à Plataforma e Início do Cadastro</h2> 

   <p>  Inicialmente, deve-se acessar o site oficial da plataforma <strong>Render</strong>. Na página inicial, selecione a opção <strong>"Start for free"</strong> para iniciar o processo de cadastro. Caso o projeto esteja sendo migrado de outro provedor, pode-se utilizar a opção <strong>"Migrate to Render"</strong>.</p> 

  <img width="1047" height="871" alt="1" src="https://github.com/user-attachments/assets/d7174156-c0f7-47ed-b61c-a1e53ab141ea" /> 

  <p> O cadastro na plataforma Render pode ser realizado gratuitamente. Para projetos de menor porte, a utilização do plano Hobby não exige, inicialmente, a inserção de cartão de crédito.</p>

  <hr> 

  <h2>Passo 2: Acesso ou Criação de um Novo Workspace</h2> 

  <p>Após acessar a <strong>Dashboard do Render</strong>, deve-se selecionar o nome do Workspace atualmente ativo, localizado no canto superior esquerdo da interface, para abrir o menu de opções.</p> 

  <p>Em seguida, selecione a opção <strong>"+ New Workspace"</strong> para criar um novo ambiente destinado ao gerenciamento isolado do projeto.</p> 

<img width="441" height="327" alt="2" src="https://github.com/user-attachments/assets/d43f2f2a-575b-47f0-a1d2-655e44b33d8f" />
  
<p>A utilização de diferentes Workspaces permite organizar os projetos de maneira independente, facilitando o gerenciamento de <strong>permissões, faturamento (billing) e serviços</strong>.</p> 

  <hr> 

  
<h2>Passo 3: Configuração dos Dados do Workspace</h2> 

  
 <p>Na tela <strong>Workspace Details</strong>, devem ser preenchidas as informações solicitadas para a identificação e configuração do novo Workspace.</p> 

<p>No campo <strong>Name</strong>, informe o nome que será utilizado para identificar o Workspace. Em seguida, verifique o endereço informado no campo <strong>Billing Email</strong>, correspondente ao e-mail associado ao faturamento da conta.</p> 

  <img width="843" height="570" alt="3" src="https://github.com/user-attachments/assets/4333d09e-9923-4c13-8226-f3d02496d2cb" />

<p>Recomenda-se utilizar uma nomenclatura clara e objetiva, permitindo identificar facilmente o projeto ou cliente associado ao Workspace.</p>

   <hr> 


  <h2>Passo 4: Seleção do Plano Hobby</h2> 

  <p>Na etapa de seleção do plano, deve-se confirmar a utilização do <strong>plano Hobby</strong>, disponibilizado gratuitamente pela plataforma. Para prosseguir, selecione a opção <strong>"Plan selected"</strong>.</p> 

  <p>Conforme apresentado na configuração utilizada, o plano possui as seguintes características:</p> 

  <ul> 
  <li><strong>$0/mês</strong>, com recursos computacionais gratuitos dentro dos limites estabelecidos;</li> 

  <li><strong>5 GB</strong> de largura de banda (bandwidth);</li>
  
  <li><strong>2 domínios personalizados</strong>;</li> 

  <li><strong>500 minutos</strong> destinados aos processos de build;</li> 
        
  <li>Possibilidade de realizar deploy de até <strong>25 serviços</strong>.</li> 
 </ul> 

  

<img width="494" height="808" alt="4" src="https://github.com/user-attachments/assets/40fcefcb-1c14-441d-bec8-991320cbee3c" />
  

  <p>O plano Hobby apresenta-se como uma opção adequada para ambientes destinados a <strong>testes, projetos acadêmicos e aplicações de pequeno porte</strong>.</p> 
<hr> 

  

  <h2>Passo 5: Obtenção da URL do Repositório no GitHub</h2> 
  
  <p>Para realizar a integração entre o Render e o projeto, deve-se acessar o repositório correspondente no <strong>GitHub</strong>. No projeto utilizado como referência, o repositório é <code>cherrytech3b2/tcc-vm-investetec</code>.</p> 

  <p>Dentro do repositório, selecione o botão verde <strong>"&lt;&gt; Code"</strong>. Na janela apresentada, selecione a aba <strong>HTTPS</strong> e copie a URL completa do repositório. </p> <pre><code>https://github.com/cherrytech3b2/tcc-vm-investetec.git</code></pre> 

<img width="565" height="454" alt="5" src="https://github.com/user-attachments/assets/b9712282-715a-49ce-9522-d2ef66da7cd1" />

  <p>Para utilizar a opção <strong>Public Git Repository</strong> no Render, é necessário verificar se o repositório do GitHub está configurado como <strong>público</strong>.</p> 

  

  <hr> 


 <h2>Passo 6: Conexão do Repositório Público ao Render</h2> 

  <p>Após obter a URL do repositório, retorne à plataforma Render e acesse a tela destinada à criação de um novo serviço ou processo de deploy.</p> 

  <p>Na interface de configuração, selecione a aba <strong>"Public Git Repository"</strong>.</p> 

  <p>Em seguida, insira no campo correspondente a URL do repositório copiada anteriormente:</p> 

  <img width="3888" height="961" alt="6" src="https://github.com/user-attachments/assets/838228b3-74d8-49f1-835c-812955e51782" />

  <p>Após a inserção da URL, o Render poderá utilizar o repositório especificado como fonte para a configuração do serviço e das etapas posteriores de deploy.</p> 

</body> 
</html> 
