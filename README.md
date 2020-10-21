# NLP sobre el Boletin Oficial

La idea inicial es poder parsear dia a dia las contrataciones que se publican en el Boletin Oficial de la Argentina, identificar las empresas/personas que son parte de cada publicacion usando NLP y el padron de AFIP, guardar esos datos (db, json) y publicarlo en twitter.

### Tecnologias

- Parsing: Beautiful Soup
- Identificacion de Empresas/Personas: Spacy + Expresiones Regulares
- MySQL
- Tweepy
- Docker 

### Resultados?

En este [repositorio](https://github.com/fsartoris/boletin_contrataciones) estan los resultados del proceso diario. 

En esta [cuenta de twitter](https://twitter.com/bot_gov) se pueden ver las publicaciones diarias.

License
----

MIT
