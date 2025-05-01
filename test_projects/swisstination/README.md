# PM3

Swisstination, a community driven platform that connects travelers with Swiss locals to share the
hidden gems of Switzerland.

**Figma Mockup** (private): [Swisstination](https://www.figma.com/design/urvXgAqmDxbsEfKn5BkssI/Swisstination?node-id=0-1&t=0SFc5bALqQ6yuPlJ-1)

## Dev Setup

Requirements:

- Docker
- Python with Poetry and Poe the Poet
- Node.js

First launch the docker compose file:

```bash
docker compose up -d
```

Install the project dependencies:

```bash
poetry install
npm install
```

Ingest all dummy data:

```bash
poe ingest
```

Start the frontend:

```bash
npm run dev
```

Start Flask backend with environment variables:

```bash
poe dev
```

| Variable                      | Description                  | Default           |
| ----------------------------- | ---------------------------- | ----------------- |
| `SECRET_KEY`                  | Flask secret key             | `very-secret-key` |
| `MONGO_HOST`                  | MongoDB host                 | `localhost`       |
| `MONGO_PORT`                  | MongoDB port                 | `27017`           |
| `MONGO_DB`                    | MongoDB db                   | `swisstination`   |
| `MONGO_COLLECTIONS_AMENITIES` | MongoDB amenities collection | `amenities`       |
| `MONGO_COLLECTIONS_Tours`     | MongoDB tours collection     | `tours`           |
| `MONGO_COLLECTIONS_USERS`     | MongoDB users collection     | `users`           |
