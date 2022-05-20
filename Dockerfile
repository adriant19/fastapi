
# base image
FROM python:3.9.9

# working directory - to store application code
WORKDIR /usr/src/app

# copy requirements.txt in current folder - to cache so changes wont rerun comamnds
COPY requirements.txt ./

# cache results and run command
RUN pip install --no-cache-dir -r requirements.txt

# copy everything in current container directory (under workdir)
COPY . .

# run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]