# backend-homework

Backend homework for the new applicants.
The aim of homework is pre filtering the candidates to the next step.

# Running the project

Run in the project's root directory

```bash
docker-compose up
```

# Running importer

Copy the desired `.csv` file into `csv_data` directory. The following command
will pick it up and import it.

```bash
docker-compose run importer <csv_filename>
```

Note: It may take a few seconds until kafka comes alive, so please wait before
using the command above.
