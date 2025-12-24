# Monica Voice Agent - Twilio Integration Setup Guide
## One of my major work contributions , I learnt alot while working on Monica it was a game chnager and exposure to deep tech . Always grateful for the opportuanity and A big shoutout thanks to CEO and Founder for his constant support and guidance and my teammate PAVAN NAINI , working alongside him taught me great values and work experince . Thankyou to all other team members -Kshitiz , Anish , Gayatri , Ashutosh ad the manamenet team . 

## Complete Setup Process

### 1. Twilio Account Setup 
You've already completed this step! You have:
- Twilio Account SID
- Auth Token
- A phone number with voice capability

### 2. Configure Your Environment

Create a `.env` file in the project root with your Twilio credentials:

```env
# Copy from .env.sample and fill in your actual values

# Twilio Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_actual_auth_token
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_WEBHOOK_BASE_URL=http://localhost:8000

# Other required settings
DATABASE_URL=postgres://zordie:zordie@db:5432/zordie
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND_URL=redis://redis:6379/0
SECRET_KEY=your-long-random-secret-key
DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 3. Install ngrok (for local testing)

1. Download ngrok: https://ngrok.com/download
2. Extract and run:
   ```bash
   ngrok http 8000
   ```
3. Copy the https URL (e.g., `https://abc123.ngrok.io`)
4. Update `.env`:
   ```env
   TWILIO_WEBHOOK_BASE_URL=https://abc123.ngrok.io
   ```

### 4. Start the Application

```bash
# Start all services with Docker Compose
docker-compose up --build

# Or run locally
python -m uvicorn api_fastapi.app.main:app --host 0.0.0.0 --port 8000
```

### 5. Test the Voice Interview

#### Option A: Using curl
```bash
curl -X POST http://localhost:8000/api/v1/monica/start-call \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Test User",
    "candidate_phone": "+1234567890",
    "position": "software_engineer"
  }'
```

#### Option B: Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/monica/start-call",
    json={
        "candidate_name": "Test User",
        "candidate_phone": "+1234567890",  # Your phone number
        "position": "software_engineer"
    }
)

print(response.json())
# Returns: {"session_id": "monica_abc123", "call_sid": "CA...", "success": true}
```

### 6. Check Interview Status

```bash
# Get current status
curl http://localhost:8000/api/v1/monica/status/{session_id}

# Get final report
curl http://localhost:8000/api/v1/monica/report/{session_id}
```

## How It Works

1. **Start Call**: API receives request with candidate info
2. **Create Session**: Monica creates an interview session
3. **Initiate Call**: Twilio calls the candidate
4. **Ask Questions**: Monica asks interview questions via voice
5. **Record Answers**: Twilio transcribes candidate's responses
6. **Process**: Monica analyzes responses and generates a report

## API Endpoints

### Start Voice Interview
```
POST /api/v1/monica/start-call
```

### Get Interview Status
```
GET /api/v1/monica/status/{session_id}
```

### Get Interview Report
```
GET /api/v1/monica/report/{session_id}
```

### Twilio Webhooks (automatically called by Twilio)
```
POST /api/v1/monica/twiml/start
POST /api/v1/monica/twiml/response
POST /api/v1/monica/twiml/status
POST /api/v1/monica/twiml/recording
```

## Troubleshooting

### Call Not Starting
- Check Twilio credentials in `.env`
- Verify phone number format: `+1234567890`
- Check ngrok is running and URL is correct
- Check Twilio balance (trial accounts have $15 credit)

### Webhooks Not Receiving Data
- Ensure ngrok is running
- Check `TWILIO_WEBHOOK_BASE_URL` is set to ngrok URL
- Look at ngrok web interface: http://127.0.0.1:4040

### Audio Issues
- Ensure FFmpeg is installed
- Check Whisper model is loaded correctly
- Verify TTS engine is configured (Coqui or gTTS)

## Next Steps

1. **Test with your phone number**
2. **Customize interview questions** in `libs/zordie_agents/zordie_agents/monica/inference.py`
3. **Improve sentiment analysis** with better models
4. **Add more features**: recording download, email reports, etc.

## Support

- Twilio Docs: https://www.twilio.com/docs/voice
- Monica Code: `libs/zordie_agents/zordie_agents/monica/`
- API Routes: `api_fastapi/app/routers/monica.py`
