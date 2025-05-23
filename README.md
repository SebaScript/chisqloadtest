# ESTADISTICA API

This project provides an API to compute probabilities from the chi-square distribution using both SciPy and a pure-Python algorithm, with load testing setup using Locust.

## Requirements

- Python 3.8+
- pip

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Usage

This API exposes two chi-square endpoints:

**POST /chi2_probabilities** (pure-Python implementation)  
**POST /chi2_scipy** (SciPy implementation)

#### Request Body

A JSON array of objects with the following fields:

- `x` (float, required): value at which to evaluate chi-square CDF  
- `df` (float, optional, default 1): degrees of freedom  
- `lower_tail` (boolean, optional, default false)

#### Response

A JSON array of probabilities corresponding to each input object in order.

#### Examples

Pure algorithm:

```bash
curl -X POST "http://localhost:8000/chi2_probabilities" \
  -H "Content-Type: application/json" \
  -d '[{"x":3.84,"df":1,"lower_tail":true}]'
```

SciPy implementation:

```bash
curl -X POST "http://localhost:8000/chi2_scipy" \
  -H "Content-Type: application/json" \
  -d '[{"x":3.84,"df":1,"lower_tail":true}]'
```

## Load Testing with Locust

This project includes a `locustfile.py` to load test both the pure-Python and SciPy chi-square endpoints.

### Running Locust in UI Mode

1. Ensure the API server is running.
2. Start Locust:

   ```bash
   locust -f locustfile.py --host=http://127.0.0.1:8000
   ```

3. Open the Locust web UI at `http://localhost:8089/`.
4. Enter the number of users, spawn rate (users per second), and click **Start swarming**.

### Running Locust in Headless Mode

```bash
locust -f locustfile.py --host=http://127.0.0.1:8000 \
  --headless --users 100 --spawn-rate 10 --run-time 1m --csv=normal_test
```

- `--users 100`: total number of users to simulate
- `--spawn-rate 10`: rate (per second) to spawn users
- `--run-time 1m`: duration of the test
- `--csv=normal_test`: prefix for CSV report files

### Interpreting Results

- **Requests/sec**: throughput
- **Response Times**: average and percentiles (50%, 95%, 99%)
- **Failures**: number of failed requests

Use these metrics to analyze your API's performance and ensure it meets your requirements.

## Further Improvements

- Add additional statistical distributions
- Integrate CI/CD for automated performance testing
- Containerize the application with Docker 