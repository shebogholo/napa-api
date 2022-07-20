FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY . .

# # virtual environment
# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv ${VIRTUAL_ENV}
# ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# RUN python3 -m pip install --upgrade pip

RUN pip install -r ./requirements.txt