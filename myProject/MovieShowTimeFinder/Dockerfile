FROM ubuntu:16.04

   #Layer for python and gdal support
   RUN apt-get update && apt-get install -y software-properties-common curl \
        && add-apt-repository ppa:ubuntugis/ubuntugis-unstable && apt-get update \
        && apt-get install -y python3-pip libssl-dev libffi-dev python3-gdal \
        && update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
        && update-alternatives --install /usr/bin/pip    pip    /usr/bin/pip3    10 \
        && rm -rf /var/lib/apt/lists/*

   #Begin of mandatory layers for Microsoft ODBC Driver 13 for Linux

   RUN apt-get update && apt-get install -y apt-transport-https wget

   RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
   RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
   RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql unixodbc-dev
   RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools
   RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
   RUN /bin/bash -c "source ~/.bashrc"  

   RUN apt-get update && apt-get install -y \
    python-pip python-dev python-setuptools \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

   RUN apt-get update && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen
   RUN pip install --upgrade pip
    
   #RUN sh -c 'echo "deb [arch=amd64] https://apt-mo.trafficmanager.net/repos/mssql-ubuntu-xenial-release/ xenial main" > /etc/apt/sources.list.d/mssqlpreview.list'
   #RUN apt-key adv --keyserver apt-mo.trafficmanager.net --recv-keys 417A0893
   #RUN apt-get update -y
   #RUN apt-get install -y libodbc1-utf16 unixodbc-utf16 unixodbc-dev-utf16
   #RUN ACCEPT_EULA=Y apt-get install -y msodbcsql
   #RUN apt-get install -y locales
   #End of mandatory layers for Microsoft ODBC Driver 13 for Linux

   RUN apt-get remove -y curl

   #Layers for the django app
   RUN mkdir /code
   WORKDIR /code
   ADD . /code/
   RUN pip install pip --upgrade
   RUN pip install -r requirements.txt
   RUN pip install gunicorn
   RUN pip install whitenoise

   RUN python /code/manage.py collectstatic --noinput

   ENV 

   #Layer for exposing the app through gunicorn
   EXPOSE 8000
   COPY entrypoint.sh /code/
   WORKDIR /code
   ENTRYPOINT ["sh", "entrypoint.sh"]