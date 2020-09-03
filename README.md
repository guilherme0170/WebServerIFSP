WebServerIFSP
=============

[![Build Status](https://travis-ci.com/alexferl/flask-mysqldb.svg?branch=master)](https://travis-ci.com/alexferl/flask-mysqldb)

(IFSP-SJC) - Projeto de Webserver de Exposição de Propostas de Estágio e Projetos com Empresas

Objetivo do Projeto
-------------------
Esse projeto tem como objetivo a criação de um Webserver para o IFSP de São José dos Campos que sirva como um mural de projetos e propostas de estágio de empresas que tiverem interesse em contactar alunos do IFSP. Essa proposta visa uma diminuição da burocracia entre as empresas e os alunos, e assim conseguir deixar os alunos mais próximos do mundo empresarial, utilizando uma plataforma simples, organizada e funcional.

Arquitetura do Projeto
----------------------
Para a estruturação desse projeto, escolhemos como pilar principal a utilização do Flask, que é uma biblioteca Python que dá uma ótima estrutura para criação de sites. O Banco de Dados escolhido foi o MySQL ue consideramos um banco simples de utilizar e fácil de manejar. Para o FrontEnd, utilizamos o HTML, CSS e o BootsStrap, já o BackEnd ficou todo em Python/Flask.
A imagem abaixo representa de maneira mais visual toda a arquitetura planejada do projeto, que será rodada e containerizada em Docker:

<img src="https://cdn.discordapp.com/attachments/744592913685676155/750875829377958018/Arquitetura_Projeto_Prog.png" width="480" height="360">

Requerimentos
-------------
- MySQL 8.0
- Python 3.8 + Libs:
    * Flask 1.1.2
    * Flask-MyQSLdb 0.2.0
