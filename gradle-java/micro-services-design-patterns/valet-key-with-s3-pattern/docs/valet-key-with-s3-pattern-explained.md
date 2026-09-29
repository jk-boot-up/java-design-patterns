# Valet Key with Amazon S3, Explained

## The pattern in one sentence

With S3, a valet key is a presigned URL: a signed, expiring permission for
one request, checked by the storage service.

## The 5 acts

### 1. Through the app server

Each review photo goes to the shop's app server, which writes it to S3 with
its own credentials. Ten 2 MB photos mean forty megabytes through the app
server: every byte in, and every byte out again.

### 2. A presigned URL

The shop's server uses the AWS SDK's presigner to sign a URL allowing one PUT
of reviews/R-11/photo.jpg, exactly 2,000,000 bytes, for five minutes. The
browser uploads straight to S3 and gets HTTP 200; the object is stored with
all 2,000,000 bytes. The app server carried only the URL, under 2 KB.

### 3. That, and nothing else

S3 checks the signature against exactly what is asked. Reading the photo with
the upload URL: 403. Editing the URL to point at review R-3: 403. Sending a 6
MB file with it: 403, because the size was signed. An upload with no
signature at all gets through here only because LocalStack does not enforce
bucket permissions; real S3 would refuse it with 403.

### 4. The key runs out

The time of signing and the lifetime are part of what is signed. A URL valid
for one second, used after two, is refused with 403.

### 5. The bill

A valid URL is pasted into a public chat, and a stranger uses it: HTTP 200,
and ten bytes are stored. Whoever holds the key can use it until it expires.
Keep keys short-lived and narrow, keep them out of logs, and sign with
credentials that can be revoked if one leaks.

## The verdict

Use presigned URLs for large uploads and downloads the app need not see. Sign
the method, object and size, keep lifetimes short, keep URLs out of logs, and
test permissions against the real service.

## How to recognise this in code you did not write

- `S3Presigner.presignPutObject(...)` or `presignGetObject(...)`.
- URLs with `X-Amz-Signature` and `X-Amz-Expires`.
- Upload endpoints that return a URL instead of accepting the file.

## Where you have already met this

- Amazon S3 presigned URLs and presigned POST policies.
- Google Cloud Storage signed URLs and Azure Blob Storage SAS tokens.
- Download links in emails that stop working after a day.
