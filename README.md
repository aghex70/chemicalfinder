## Chemicalfinder API

# Architecture (quick look)
- This application consists of an API implemented using Django & Django Rest Framework connected for persistence purposes to a MongoDB database using Djongo connector.
- The message queue used in this project to execute asynchronous tasks is Celery using Redis as broker.
- For distributed tasks monitoring Flower is being used.
- Finally the project has been developed using container orchestration tools such as Docker and Docker Compose.

# Previous requirements:
- XML patents should be stored in the path "./chemicalfinder/app/chemfinder/patents" in order to be processed.
- Compounds file path must be "./chemicalfinder/app/chemfinder/training/compounds.csv" in order to be processed.

# Workflow (suggested use)
- The application will process a series of XML patents with a defined format. After parsing and recover specific information from these, this information will be stored in the database.
- Afterwards the application will run a basic Named Entity Recognition (NER) in order to categorize fragments, words or sentences.
- Once this basic categorization is persisted in the database, an improved NER will be conducted (ChemNER), using a downloaded model with biomedical data in order to improve the results.
- Finally, the last phase will be the creation and training of a model. To accomplish this task, a dataset consisting of ~41000 chemical compounds has been downloaded, to be provided to the model, generate a TrainedNER and try to achieve the best categorization.

# Installation
- Download docker and docker-compose
- Start the API with the following command:
    docker-compose up --build

# Requests description.
1 - Delete database
curl -X DELETE "http://localhost:8000/api/database/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

2 - Generate patents
curl -X POST "http://localhost:8000/api/patent/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

3 - Retrieve patents
curl -X GET "http://localhost:8000/api/patent/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

4 - Get inventors
curl -X GET "http://localhost:8000/api/inventor/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

5 - Get inventor's patents
curl -X GET "http://localhost:8000/api/inventor/?name=NAME" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

6 - Generate NER (Named Entities Recognizer)
curl -X POST "http://localhost:8000/api/chemner/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

7 - Generate ChemNER
curl -X POST "http://localhost:8000/api/chemner/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

8 - Train model
curl -X POST "http://localhost:8000/api/ner/train/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

9 - Generate TrainedNER
curl -X POST "http://localhost:8000/api/trained_ner/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

10 - Retrieve NER, ChemNER & TrainedNER
curl -X GET "http://localhost:8000/api/ner/?type=ner" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"
curl -X GET "http://localhost:8000/api/ner/?type=chemner" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"
curl -X GET "http://localhost:8000/api/ner/?type=trained_ner" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

11 - Delete NER, ChemNER & TrainedNER
curl -X DELETE "http://localhost:8000/api/ner/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"
curl -X DELETE "http://localhost:8000/api/chemner/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"
curl -X DELETE "http://localhost:8000/api/trained_ner/" -H  "accept: application/json" -H  "X-CSRFToken: DGWmvu5HTcQ87qn98ChgXmHROctvWmwNGK5cAgVkUoxN8I8MijsTJUvFg5mCUEih"

# Helpful links
- Swagger - http://localhost:8000/swagger
- Django Admin - http://localhost:8000/admin/
   - A user is required to enter the admin interface. In order to create one the following commands can be done:
     · docker-compose exec web bash (to enter the container)
     . python manage.py createsuperuser (to create an user)
- Flower - http://localhost:5555/

# Observations and decisions made
- This API has been developed using an Intel i9-9900ks (8 cores and 16 threads) processor with 64GB of RAM in Ubuntu 20.04.1 LTS.
- As stated in the official documentation, Celery number of worker processes/threads can be changed using the --concurrency argument and defaults to the number of CPUs available on the machine. Even though ignoring this parameter should produce the best results as it would use all the available threads, using a configuration with "--concurrency 10" has been far more efficient and faster.
- Regarding this previous point, the process could be sped up using any cloud provider instance to take advantage of servers with bigger compute capability.
- API's authentication and security has not been implemented.
- Biomedical model (en_core_sci_sm) used for ChemNER has been downloaded from https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.3.0/en_core_sci_sm-0.3.0.tar.gz
- CSV compound dataset has been downloaded from https://data.world/alexandra/compounds
- A TrainedNER model using 50 iterations has been generated in the path "/chemicalfinder/app/chemfinder/training/iter50"
- The NER training number of iterations is set to 1 because of the cost of the operation. Feel free to change this parameter.

# Problems unsolved
- Unfortunately, TrainedNER has not brought the expected results, because the training needed words alongside some context, and all I had were mere compounds with no context, producing erroneous results.

