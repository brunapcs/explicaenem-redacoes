# explicaENEM Redação On-Demand 
Redação On-Demand is the complete process of: 
  1. Receiveing students texts via google forms 
  2. Fowarding texts to the available revisors (via email)
  3. Receiveing grades and anotations from revisors 
  4. Sending grades and revisions back to students (via email) 
  
## Cloud Functions

The process is executed by  two cloud functions: one responsable for sending 
the students texts to a correspondent revisor and one responable for sending the 
revision/grades back to students. 

The functions are triggered by google Cloud Scheduler everyday at 11 a.m


### Development

You must have acess to explicaENEM's GCP project and the proper ```service acount``` key file. 

Also, you must have a ```.env.yaml``` file with the enviroment variables set: 

 - EMAIL: <only email username (the @ and service provider are not necessary)>
 - SENHA: <email password>
 - REDACOES_SHEET_PROD: <google sheet key>
 - CORRECOES_SHEET_PROD: <google sheet key>

To deploy the cloud functions you must run the following command within the desired function rep <consumer/producer> : 

``` 
$ make deploy
```