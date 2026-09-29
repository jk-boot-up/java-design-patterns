# Session Guide — Valet Key with Amazon S3 Pattern

## Learning Objectives

By the end of the session you can:

- Sign an S3 presigned PUT URL with the AWS SDK.
- Upload directly from a client with only the URL.
- Explain which changes break the signature.
- Keep presigned URLs short-lived and narrow.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Through the app server | 7 min |
| 0:17 | Act 2: A presigned URL | 7 min |
| 0:24 | Act 3: That, and nothing else | 7 min |
| 0:31 | Act 4: The key runs out | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Compare act one's 40 MB with act
two's under 2 KB. Open `Storage.presignedPut`: one request, one signature.
End on act three's refusals and the honest note about LocalStack.

## Exercises

1. Sign a GET URL for the uploaded photo and share it for one minute.
2. Add a content type to the signature and upload with the wrong one.
3. Run the same code against a real S3 bucket and try the unsigned upload again.
