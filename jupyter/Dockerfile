FROM jupyter/base-notebook

COPY ./data_cleaning.ypynb /home/jovyan/work/
COPY ./requirements.txt /home/jovyan/work/

WORKDIR /home/jovyan/work/
RUN mkdir final_dataset
RUN pip -r install requirements.txt

CMD ["jupyter", "notebook", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]