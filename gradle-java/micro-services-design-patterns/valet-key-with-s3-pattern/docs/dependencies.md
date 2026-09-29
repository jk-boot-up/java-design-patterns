# Dependencies

This project uses the AWS SDK and LocalStack, which the plain Java version of
Valet Key does not. Skipping it loses none of the pattern: the plain version
teaches all of it with nothing installed.

## What Amazon S3 and presigned URLs is

Amazon S3 is object storage: files, called objects, in buckets. A presigned URL is an ordinary web address with extra query parameters: who signed it, when, for how long, which headers are included, and a signature computed with the signer's secret key using AWS Signature Version 4. Anyone holding the URL can make exactly that request until it expires; S3 recomputes the signature and refuses anything else.

## What The AWS SDK presigner is

S3Presigner signs URLs locally, without contacting S3. presignPutObject signs a PUT for one bucket and key; putting a content length in the request makes the size part of the signature.

## What LocalStack is

LocalStack is a local stand-in for AWS services, run in a container. Version 4.14.0 is pinned because later images need an account. Signature checking is turned on with S3_SKIP_SIGNATURE_VALIDATION=0. It does not enforce bucket permissions, which is why an unsigned upload got through.

## Why this project uses them

The plain version shows the idea with its own signing. This version shows the
standard form every cloud offers, signed by the official SDK.

## What to install

Only a JDK, version 21, and a running Docker. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Docker | running; 24 or later |
| LocalStack image | localstack/localstack:4.14.0 |
| AWS SDK for Java (s3) | 2.55.7 |
| Testcontainers | 2.0.5 |

## What it costs

- A container runtime, and a first run that downloads the LocalStack image.
- An emulator that differs from real S3 on permissions.
