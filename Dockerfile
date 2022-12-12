FROM python:3.7

# Install dependencies
RUN pip install --upgrade pip
# install pandas
RUN pip install pandas matplotlib yfinance reload

WORKDIR /app
ADD . /app

# Run the application
CMD ["python", "calculate.py"]