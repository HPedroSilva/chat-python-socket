# Chat em Python Utilizando Sockets com Criptografia e Interface Gráfica

Este projeto foi desenvolvido para a disciplina de Sistemas Distribuídos e tem como objetivo criar um sistema de chat distribuído que utilize sockets em Python e criptografia para garantir a segurança das mensagens transmitidas entre os usuários. Além disso, o projeto conta com uma interface gráfica desenvolvida utilizando a biblioteca Tkinter. O projeto foi proposto como trabalho da disciplina, e visa colocar em prática os conceitos aprendidos sobre Sistemas Distribuídos, focando principalmente na utilização de Sockets.

## Funcionalidades

O sistema é capaz de realizar as seguintes funcionalidades:

- Permitir que vários usuários se conectem a um servidor central;
- Permitir que os usuários enviem mensagens uns aos outros;
- Utilizar criptografia para garantir a segurança das mensagens transmitidas;
- Garantir a integridade das mensagens transmitidas para evitar que as mesmas sejam alteradas durante a transmissão;
- Exibir uma interface gráfica para facilitar a interação dos usuários com o sistema.

## Tecnologias utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

- Python: linguagem de programação utilizada para desenvolver o sistema;
- Sockets: tecnologia utilizada para a comunicação entre o servidor e os clientes;
- Tkinter: biblioteca utilizada para criar a interface gráfica do sistema;
- Criptografia: utilizada para garantir a segurança e a integridade das mensagens transmitidas;
- Threads: utilizada para gerenciamento de vários clientes no servidor e para gerenciamento de inteface gráfica.

## Como executar o sistema

Para executar o sistema, siga os seguintes passos:

1. Clone o repositório em sua máquina local;
2. Abra o terminal e navegue até o diretório do projeto;
3. Certifique-se de ter o Python instalado em sua máquina, e instale as dependências do projeto digitanto o seguinte comando: `python -m pip install -r requirements.txt`;
4. Execute o servidor digitando o seguinte comando: `python server.py`;
5. Insira uma porta disponível para o servidor executar (certifique-se de que a porta não está em uso);
6. Execute um ou mais clientes digitando o seguinte comando: `python client.py`;
7. Insira o IP do servidor (utilize o endereço de loopback - 127.0.0.1 caso cliente e servidor estejam na mesma máquina), e a porta utilizada nos servidor para cada cliente;
9. A interface gráfica será aberta e você poderá começar a enviar mensagens para outros usuários conectados ao servidor.
