FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}
RUN dnf install -y poppler-utils

COPY lambda-requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r lambda-requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY ./ ./

CMD [ "lambda_handler.lambda_handler" ]