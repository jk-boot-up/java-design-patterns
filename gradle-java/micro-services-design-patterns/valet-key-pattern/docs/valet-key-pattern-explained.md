# Valet Key, Explained

## The pattern in one sentence

A valet key is a signed, narrow, short-lived permission that lets a client do
one specific thing directly with a storage service, so the application does
not carry the data itself.

## The 5 acts

### 1. Carried by the app

`Shop.uploadThroughApp` receives each photo and sends it on to storage with
the shop's master credential. Ten 2 MB photos make the app server carry
40 MB: every byte in from a customer and out again to storage.

### 2. A valet key

`Shop.valetKey` signs a URL allowing one PUT to `/reviews/R-11/photo.jpg`, for
five minutes, up to 5 MB. The customer's browser uploads the photo straight to
storage, which checks the signature and stores it. The app server carried
only the key: under 200 bytes.

### 3. Only what it allows

The key allows exactly one thing. Using it to read the photo is refused, 403.
Changing the path to overwrite review R-3 breaks the signature, 403. A 6 MB
file is over its limit, 413. And storage without any key refuses, 401.

### 4. Expiry

A key is issued for two tenths of a second and used after four tenths. Storage
refuses it: key expired. Keys stop working on their own.

### 5. The bill

A key is copied into a public chat, and a stranger uses it: storage accepts,
because the key is valid. It cannot be taken back before it expires. Keep keys
short-lived and narrow, and keep signed URLs out of logs.

## The verdict

Use valet keys for large or numerous uploads and downloads that the app does
not need to touch. Sign the method, path, size and expiry, keep lifetimes
short, and keep signed URLs out of logs.

## How to recognise this in code you did not write

- URLs with `X-Amz-Signature`, `sig=` or `se=` parameters.
- An endpoint that returns an upload URL instead of accepting the file.
- Expiring download links.

## Where you have already met this

- Amazon S3 presigned URLs.
- Azure Storage shared access signatures (SAS).
- Google Cloud Storage signed URLs.
- Expiring download links in emails.
