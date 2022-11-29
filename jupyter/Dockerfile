FROM jupyter/base-notebook

RUN mkdir -p datos/datos_out

COPY ./data_cleaning.ipynb /home/jovyan/work/
COPY ./requirements.txt /home/jovyan/work/

WORKDIR /home/jovyan/work/
RUN pip install -r requirements.txt

CMD ["jupyter", "notebook", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]