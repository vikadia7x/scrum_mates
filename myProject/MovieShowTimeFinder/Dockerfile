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

   ENV SOCIAL_AUTH_TWITTER_KEY = 'QQl3H4qqbiHOIsKpcHCN3ZlmH'
   ENV SOCIAL_AUTH_TWITTER_SECRET = '8kozVUQUITVR3g8PHW43gb1sSI7Iaf8llwpBUctti8IzLMMNC3'

   ENV SOCIAL_AUTH_FACEBOOK_KEY = '314676229128348'  # App ID
   ENV SOCIAL_AUTH_FACEBOOK_SECRET = 'dd9c910c48003e902d8f029f925a3bf5'


   ENV SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '770133029902-gb95pd64gutdkdgvrm73sd5c0p2kc2jv.apps.googleusercontent.com'
   ENV SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'bBetAit4s_JuIG2q-TzlMWPK'

   ENV APP_ID='69f71ca9-d764-4aa5-996b-293c580b7995'
   ENV SECRET_APP_KEY='ocQ7HQP2s5uDE7+/nEWR6Mp3pu1KcAeWbnzS0GILjmE='
   ENV TENANT_ID='41f88ecb-ca63-404d-97dd-ab0a169fd138'
   ENV VAULT_URL='https://showtimefinderkeyvault.vault.azure.net/'

   RUN python /code/manage.py collectstatic --noinput

   #Layer for exposing the app through gunicorn
   EXPOSE 8000
   COPY entrypoint.sh /code/
   WORKDIR /code
   ENTRYPOINT ["sh", "entrypoint.sh"]