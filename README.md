#Close approach data API test suite
This is an example of a test suite using pytest to run the tests.
The source code is copied from `src` when building the docker image.
Python requirements are in `requirements.txt` and they are installed in the build stage of Dockerfile
Test results are reported as `report.html` file, which is created by `pytest-html`, and placed in the `output` directory, which has to be mounted when running the container.


#Prerequisites
* Docker version 17.05 or higher - needed for multistage build syntax
* Ability to connect to https://ssd-api.jpl.nasa.gov/cad.api

#Build the docker image
```shell
docker build --target test --tag asteroids_test:latest .
```

#Run the tests
```shell
docker run -v "$(pwd)"/output:/output asteroids_test
```

# Analyze the test results
Open `output/report.html` in a browser
