# TICC

Torneio Intercampi de Computação Competitiva (TICC) do CEFET-MG

### Ambiente virtual
Para executar a aplicação, é recomendada a utilização de um ambiente virtual, por meio do `virtualenvwrapper`.
Após instalar o `virtualenvwrapper`, faça o seguinte comando para criar um ambiente virtual:
```
mkvirtualenv -p python3 ticc
```

Sempre que for executar o projeto, inicie o ambiente virtual:
```
workon ticc
```

### Dependências
Para instalar as dependências da aplicação, utilize o seguinte comando:
```
pip install -r requirements.txt
```

### Preparação do banco de dados
Execute o seguinte comando para criar as relações no seu banco de dados local:
```
./manage.py migrate
```

### Execução
```
./manage.py runserver
```
