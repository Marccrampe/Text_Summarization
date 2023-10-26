# Ecoweb Ai Text Summary Service

The application developed enables automatic text summarization using Hugging Face models such as T5, T5rapide and Facebook BART,
models, such as T5, T5rapide and Facebook BART. These models, trained on vast amounts of data, offer the ability to produce
produce accurate summaries from given texts.

This application enables users to submit texts, even very long ones,
to obtain a condensed summary. It uses the natural language processing capabilities of the models
to extract key information and generate a coherent summary.

It supports French texts, while also being able to process English words.
This enables users to work with mixed texts without encountering language problems.

The new version prevents English words from appearing in the summary text during the process, by using a translator as well as a spelling checker.

## Getting started

Simply build the image and run it with the following commands.
The web application can be accessed by typing the following address in your web browser: http::/localhost:7000
or 127.0.0.1:7000
 
## Build and run  the Docker image

```bash
  docker image build -t text-summary-service .

  docker run --name tss -it --rm -p 7000:8000  text-summary-service
```
With these commands, the Docker image will be built and the application launched, allowing users to
to access the text summarization service via the URL provided.

Please note that you may need to change the port number (for example, -p {host-port}:{container-port})
if port 7000 is already in use on your system.
