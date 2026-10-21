# Project 2 — Scenario A: Secure 5G Web Application

## Architecture

- The 5G UE connects through the existing Open5GS/UERANSIM network.
- Nginx provides the HTTPS gateway at `10.20.6.20`.
- Django runs privately at `10.20.8.20`.
- Django is isolated from the N6 network.
- Nginx redirects HTTP to HTTPS and supports TLS 1.2 and TLS 1.3.

## Prerequisites

- Docker Engine and Docker Compose
- Existing Project 1 N6 Docker network named `project1-n6`
- OpenSSL

## 1. Configure the secret key

Create a local `.env` file in the terminal:

```bash
printf 'DJANGO_SECRET_KEY=%s\n' "$(openssl rand -hex 32)" > .env
chmod 600 .env
```

## 2. Generate the local CA certificate

Generate the CA private key:

```bash
openssl genrsa -out certs/ca.key 2048
chmod 600 certs/ca.key
```

Generate the CA certificate:

```bash
openssl req -x509 -new -key certs/ca.key -sha256 -days 365 \
  -config certs/ca-openssl.cnf -out certs/ca.crt
```

## 3. Generate the Nginx server certificate

Generate the server private key and certificate request:

```bash
openssl genrsa -out certs/server.key 2048
chmod 600 certs/server.key

openssl req -new -key certs/server.key \
  -out certs/server.csr -subj "/CN=10.20.6.20"
```

Sign the server certificate:

```bash
openssl x509 -req -in certs/server.csr \
  -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial \
  -out certs/server.crt -days 365 -sha256 \
  -extfile certs/server.ext
```

Verify the certificate:

```bash
openssl verify -CAfile certs/ca.crt certs/server.crt
```

Expected result: `certs/server.crt: OK`

Keep `certs/ca.key` secure. Never commit private keys.

## 4. Start the application

Ensure the existing `project1-n6` Docker network is available, then run these commands in the terminal:

```bash
docker compose up -d --build
docker compose exec django python manage.py migrate
docker compose ps
```

To create an administrator account if needed:

```bash
docker compose exec django python manage.py createsuperuser
```

## 5. Test HTTPS

Run this command in the terminal:

```bash
curl --cacert certs/ca.crt \
  --resolve 10.20.6.20:443:127.0.0.1 \
  https://10.20.6.20/health/
```

The expected response contains the service name `project2-django`, status `ok`, and project name `Telecommunication Security`.

## Important

- `.env` and generated certificate files are excluded from Git.
- Keep private keys secure.
- This project uses a local CA, not a publicly trusted certificate authority.
