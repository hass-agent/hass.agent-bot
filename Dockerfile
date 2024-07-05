# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files into the container
COPY discord_bot bot

# Run the bot and flask app

CMD ["sh", "-c", "python bot/bot.py"]
