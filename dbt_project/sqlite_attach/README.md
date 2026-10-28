# sqlite_attach (empty on purpose)

`profiles.yml` points dbt-sqlite's `schema_directory` here. The adapter attaches
every `*.db` file in that folder as an extra schema on each connection.

This project only uses the `main` schema, so the folder stays empty. It used to
point at `data/processed/`, where any extra `.db` file (a backup, a copy for the
dashboard) got attached too, and every dbt command failed with
`malformed database schema`.
