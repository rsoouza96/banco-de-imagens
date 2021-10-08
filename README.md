# banco-de-imagens

Este é um projeto em Flask que serve como um banco de imagens. A ideia é que o usuário possa fazer o upload de suas imagens, elas ficaram guardadas e sempre que o usuário precisar fazer o download, elas estarão disponíveis.


#Instalação

A instalação é simples, basta criar um ambiente virtual, rodando os seguintes comandos no seu terminal:
```
$ python -m venv venv
```
```
$ source venv/bin/activate
```
Depois disso, você precisa instalar as dependências que estão no requirements.txt. Para fazer isso basta rodar os comando:
```
$ pip install -r requirements.txt
```

#Rotas
```
| Método | Rota  | Descrição  |

| :---: | :----: | :--------: |

| GET | /download/<file_name> | Baixa um arquivo especifico |

| GET | /download-zip | Baixa todos os arquivos em formato .zip |

| GET | /files | Lista todos os arquivos disponiveis para download |

| GET | /files/<type> | Lista todos os aquivos de um formato especifico disponiveis para download |

| POST | /upload | Enviar um arquivo |
```

#.env
Esse projeto permite algumas configurações no .env, está aplicação por padrão recebe apenas arquivos com no máximo 1mb e com as extensões .png, .jpg, .gif . Entretanto você pode alterar isso.
Caso deseje mudar o tamanho maximo dos arquivos:
```
MAX_CONTENT_LENGTH = 2
```
Caso receber outras extensões, basta passar em formato de lista:
```
ALLOWED_EXTENSIONS = ['png', 'jpg', 'gif']
```

