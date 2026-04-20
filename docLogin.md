<h1> Programação de fluxo de login

<h2> 1- Configurar um projeto e uma conta de serviço do Firebase.</h2>
  
<p> Iremos precisar de:
  
  •Um projeto do Firebase.
  
  •Conta de Serviço: Identidade de acesso gerada automaticamente na criação do projeto.
  
  •Chave de Credenciais: Arquivo de configuração (JSON) necessário para autenticar a comunicação com o SDK.
  </p>
 <h1> Adicionar o SDK</h1>

<p> Aqui será feita a instalação de bibliotecas para habilitar a comunicação entre o servidor e os serviços do Firebase.</p>

<img width="808" height="333" alt="Screenshot1" src="https://github.com/user-attachments/assets/0fe402ad-1313-4d5d-8893-35e0be23068e" />

<h1>Bibliotecas instaladas no servidor:</h1>

<img width="495" height="217" alt="Screenshot" src="https://github.com/user-attachments/assets/19f8f886-512b-4df4-8c03-c92ee98ac86e" />

<h2>2- Inicializar o SDK.</h2>

<p> Após criar o projeto, a conexão com o Firebase pode ser feita de forma automática se o seu sistema estiver rodando nos servidores do próprio Google. Nesse caso, o sistema reconhece as permissões sozinho, sem que você precise configurar senhas ou chaves manualmente. Caso precise ajustar detalhes de serviços específicos (como banco de dados ou arquivos), basta usar uma configuração chamada FIREBASE_CONFIG, que aceita tanto os dados escritos diretamente quanto um link para um arquivo com essas informações.</p>

<img width="815" height="146" alt="Screenshot3" src="https://github.com/user-attachments/assets/ab3b77e0-9a4c-4c5c-b758-41db781d52de" />

 Essa ação, permite que o nosso projeto interaja com os recursos do Firebase.

Com o Admin SDK configurado, é possível realizar tarefas administrativas como gerenciar usuários e autenticações, manipular dados no Realtime Database ou Data Connect, e enviar notificações através do Cloud Messaging.

<h2>3- Utilização do Token de Atualização do OAuth 2.0.</h2>
<p>O Admin SDK também permite a autenticação via token de atualização do Google OAuth2, oferecendo uma alternativa de credencial para acesso aos serviços.</p>

<img width="1002" height="162" alt="Screenshot4" src="https://github.com/user-attachments/assets/c060aad3-1af3-4082-8091-debc323e6456" />

<p>Refresh Token: Uma credencial de longa duração, utilizada para obtermos exclusivamente novos Access Tokens quando eles expirarem, sem a necessidade de autorizações de solicitações para o uso dos recursos.</p>

<h2>4- Inicializar o SDK em ambientes que não são do Google.</h2>
<p>Para ambientes fora da infraestrutura do Google (como o seu computador local ou outros servidores), a autenticação deve ser feita manualmente. Nesses casos, você deve exportar e utilizar um arquivo de chave privada (JSON) da conta de serviço para autorizar o acesso do seu código às APIs do Firebase de forma segura.</p>

Para garantir o acesso seguro em outros servidores, deve-se configurar a seguinte variável:

<img width="988" height="199" alt="Screenshot5" src="https://github.com/user-attachments/assets/cab30658-9c40-4a78-adba-6594ac4903a3" />

<p>Após essas etapas, o Application Default Credentials (ADC) passa a identificar suas credenciais automaticamente, permitindo que o sistema utilize a conta de serviço mesmo em ambientes fora do ecossistema Google.</p>

Inicialize o SDK como mostrado:

<img width="999" height="145" alt="Screenshot6" src="https://github.com/user-attachments/assets/e2507e40-a20d-4b3b-80d6-053808273886" />

<h2>5- Inicializar vários aplicativos.</h2>
<p>Geralmente, basta inicializar um único aplicativo padrão para o projeto. Caso precise acessar serviços adicionais, existem duas formas equivalentes de fazer essa integração.</p>

<img width="1002" height="287" alt="Screenshot7" src="https://github.com/user-attachments/assets/a2de32f9-7c4b-4446-beca-a87e2d1e1a86" />
O comando de inicialização padrão limita-se a um único projeto. Caso a aplicação exija o acesso a múltiplos projetos do Firebase, deve-se instanciá-los individualmente via initialize_app, permitindo a segregação das credenciais e configurações de cada ambiente.

<h2>6- Definir escopos para Realtime Database e Authentication.</h2>
<p>Ao utilizar uma VM do Google Compute Engine com o Application Default Credentials (ADC), é necessário configurar os escopos de acesso para permitir a comunicação com o Realtime Database ou Authentication. Os escopos exigidos devem incluir permissões para userinfo.email e cloud-platform (ou firebase.database), podendo ser verificados ou editados via comandos da interface gcloud.</p>
<img width="797" height="467" alt="Screenshot8" src="https://github.com/user-attachments/assets/16e5cd08-2c97-46dc-b3d7-dc1d20b9d908" />

<h2>7- Como testar com credenciais de usuário final da gcloud</h2>
<p>Ao testar o Admin SDK localmente via gcloud, o Firebase Authentication não aceita as credenciais padrão de usuário final. Para contornar isso, é necessário fornecer o ID do projeto na inicialização e gerar as credenciais usando um ID do cliente OAuth 2.0 próprio (do tipo "app para computador"), em vez do ID padrão da gcloud.</p>

<img width="787" height="128" alt="Screenshot11" src="https://github.com/user-attachments/assets/8c23dd1e-69f7-472c-92d0-1e89eb787f91" />

O ID do projeto pode ser definido explicitamente no código ou via variável de ambiente GOOGLE_CLOUD_PROJECT. O uso da variável é o método mais prático, pois permite testar o código sem precisar de alterações manuais na inicialização.

Para especificar explicitamente o ID do projeto:

<img width="819" height="237" alt="Screenshot10" src="https://github.com/user-attachments/assets/d77d1e2d-e45d-4370-8e14-7689feb4b437" />
