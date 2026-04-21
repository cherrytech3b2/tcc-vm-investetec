Modelo de dados do Cloud Firestore

O Cloud Firestore é um banco de dados NoSQL focado em documentos que se diferencia dos modelos SQL por não utilizar tabelas ou linhas. Em sua estrutura, os dados são organizados em documentos que obrigatoriamente pertencem a coleções, sendo o sistema otimizado para lidar com grandes volumes de documentos de pequeno porte.

Cada documento funciona como um conjunto de pares chave-valor e pode abrigar desde tipos primitivos até estruturas complexas, como listas, objetos aninhados e subcoleções. Uma característica central do Firestore é a sua natureza implícita: a infraestrutura de coleções e documentos é criada automaticamente pelo banco no momento em que os dados são atribuídos, eliminando a necessidade de uma configuração prévia de esquema.

Documentos

O documento é a unidade básica de armazenamento do Cloud Firestore, funcionando como um registro leve composto por campos mapeados a valores específicos. Cada um desses registros possui um nome exclusivo que o identifica dentro do banco de dados, como no exemplo de um perfil de usuário, onde as informações são estruturadas de forma direta e organizada.

<img width="260" height="152" alt="alovelace" src="https://github.com/user-attachments/assets/cfb5cd83-7c34-43d8-9731-1d8cd373692f" />

No Cloud Firestore, estruturas de dados complexas ou aninhadas dentro de um documento são tecnicamente chamadas de mapas. Essa funcionalidade permite organizar informações de forma mais detalhada e hierárquica, possibilitando, por exemplo, que o nome de um usuário seja subdividido em diferentes componentes dentro de um único campo estruturado.

<img width="247" height="177" alt="alovelace 2" src="https://github.com/user-attachments/assets/30075f62-e2f5-4d4f-b042-c6b33a762fc8" />
Os documentos do Cloud Firestore funcionam essencialmente como registros JSON leves, compartilhando a mesma estrutura básica de organização de dados. As principais distinções residem no suporte a tipos de dados adicionais e na existência de um limite técnico de tamanho para cada documento, mas, na prática, eles podem ser manipulados e compreendidos como se fossem objetos JSON.

Coleções

Os documentos no Cloud Firestore são organizados dentro de coleções, que funcionam como recipientes para agrupá-los. Um exemplo prático dessa estrutura é uma coleção chamada "users", criada especificamente para armazenar e organizar os diversos documentos que representam cada usuário individual do sistema.
<img width="422" height="357" alt="Coleções" src="https://github.com/user-attachments/assets/eca76288-a63c-4df0-a573-b269a2eaaf95" />

<img width="337" height="350" alt="Coleções 2" src="https://github.com/user-attachments/assets/1f764d99-2958-4bdc-ba76-fdb1b73c1212" />

O Cloud Firestore opera de forma independente de esquemas, oferecendo total liberdade para definir campos e tipos de dados em cada documento, mesmo dentro de uma mesma coleção. Apesar dessa flexibilidade, recomenda-se manter um padrão para facilitar consultas futuras.

Estruturalmente, uma coleção é composta exclusivamente por documentos, não podendo conter campos brutos ou outras coleções diretamente. Cada documento possui um nome único dentro de sua coleção, que pode ser definido pelo usuário ou gerado automaticamente pelo sistema. Além disso, a gestão de coleções é dinâmica: elas passam a existir assim que o primeiro documento é criado e desaparecem automaticamente quando o último documento é excluído.

Referências

No Cloud Firestore, a identificação de cada documento é determinada de forma única pela sua localização específica dentro da base de dados. Para interagir com um documento via código — como o exemplo do usuário alovelace dentro da coleção users — é necessário criar uma referência, que funciona como um apontador para esse endereço exato no banco de dados.

<img width="717" height="101" alt="referências" src="https://github.com/user-attachments/assets/a573540f-80be-4d32-b32c-c975514dcd0d" />

Uma referência no Cloud Firestore é um objeto leve que atua exclusivamente como um ponteiro para um local específico no banco de dados. Sua criação é um processo puramente local que não exige a existência prévia de dados nem realiza operações de rede. Além de apontar para documentos individuais, o sistema também permite a criação de referências direcionadas a coleções inteiras.

<img width="727" height="107" alt="referências2" src="https://github.com/user-attachments/assets/7f880e38-0de3-4cdf-9d1a-fa28533be374" />

Para facilitar a programação, o Cloud Firestore permite criar referências a documentos ou coleções utilizando caminhos em formato de string. Esse método utiliza a barra (/) como separador entre os componentes do endereço, permitindo, por exemplo, referenciar o documento alovelace de maneira direta e prática através de sua estrutura de localização no banco de dados.

<img width="720" height="103" alt="referências3" src="https://github.com/user-attachments/assets/52d488c4-3b8c-476c-b6ef-71651d0d9e7b" />


Dados hierárquicos

Para compreender a estrutura hierárquica do Cloud Firestore, pode-se utilizar o exemplo de um aplicativo de chat. Nesse cenário, o sistema organiza os dados criando uma coleção principal chamada rooms, que atua como o recipiente para armazenar as diferentes salas de conversa disponíveis, servindo de base para a construção dos níveis de dados subsequentes.

<img width="402" height="225" alt="Dados hierárquicos" src="https://github.com/user-attachments/assets/8a9f3f7e-1033-4cba-acdb-77c3f8acc9d1" />

Ao planejar o armazenamento de mensagens em um app de chat, o Cloud Firestore recomenda não utilizá-las dentro do documento principal da sala, pois documentos devem permanecer leves e o volume de mensagens pode ser excessivo. A solução ideal é a utilização de subcoleções dentro do documento de cada sala, permitindo organizar grandes quantidades de dados de forma hierárquica sem sobrecarregar o registro principal.

Subcoleções

No cenário de um aplicativo de chat, a estratégia mais eficiente é o uso de subcoleções, que são coleções diretamente vinculadas a um documento específico. Dessa forma, cada documento dentro da coleção principal rooms pode possuir sua própria subcoleção chamada messages, permitindo uma organização clara e isolada dos dados de cada sala.

<img width="425" height="476" alt="Subcoleções" src="https://github.com/user-attachments/assets/73f47771-9cfb-4de5-b46e-11434e5add23" />

Para finalizar a estruturação do exemplo, o Cloud Firestore permite localizar uma mensagem específica dentro de uma subcoleção através de uma referência de caminho. No código, essa referência segue a hierarquia completa: inicia-se na coleção principal de salas, identifica o documento da sala desejada, acessa a subcoleção de mensagens e, por fim, aponta para o documento da mensagem individual.

<img width="777" height="133" alt="Subcoleções2" src="https://github.com/user-attachments/assets/c9379068-daee-4146-b76a-d18018546cde" />

A estrutura do Cloud Firestore exige obrigatoriamente um padrão alternado entre coleções e documentos, o que impede a sobreposição direta de elementos do mesmo tipo. As subcoleções são a ferramenta que permite a hierarquização dos dados, possibilitando que documentos contenham novas coleções e vice-versa. Essa organização facilita o acesso à informação, permitindo tratar uma subcoleção (como as mensagens de uma sala específica) com a mesma simplicidade de uma coleção principal. Além disso, o sistema suporta um alto nível de complexidade, permitindo o aninhamento de dados em até 100 níveis de profundidade.















