# Canvassy - Railway Deployment

Canvassy is configured to run on Railway with a persistent volume.

## 1. Deploy the repository

Create a Railway project and deploy this GitHub repository.

## 2. Add the app password

In the Canvassy service, add this Railway variable:

```text
APP_PASSWORD=<your password>
```

Do not commit the password to GitHub.

## 3. Add persistent storage

Attach a Railway Volume to the Canvassy service and set the mount path to:

```text
/data
```

Railway automatically supplies `RAILWAY_VOLUME_MOUNT_PATH=/data` to the app.

On the first application startup, Canvassy copies the repository's
`data_final.csv` into `/data/data_final.csv`. After that, all canvassing
updates are read from and written to the persistent copy.

Do not wipe/delete the Railway volume during the campaign unless you have
backed up the canvassing data.

## 4. Generate a public domain

In Railway, open the service Settings and generate a public domain.
Use that URL on the phone and add it to the phone's Home Screen if desired.

## Local development

Nothing changes for local development. If `RAILWAY_VOLUME_MOUNT_PATH` is not
set, Canvassy reads and writes the repository's local `data_final.csv`.
The existing `.streamlit/secrets.toml` can still provide `APP_PASSWORD`
locally.

Run locally with:

```bash
streamlit run app.py
```

## Important backup

The live campaign results on Railway are stored in the volume copy of
`data_final.csv`, not the GitHub seed file. Periodically download a backup of
`/data/data_final.csv` from the Railway volume.
