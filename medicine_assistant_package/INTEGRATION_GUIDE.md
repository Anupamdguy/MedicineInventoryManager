# AI ASSISTANT INTEGRATION GUIDE
## Medicine Inventory Manager - LLM Assistant Setup

This guide will help you integrate the AI assistant into your existing Django Medicine Inventory Manager.

---

## 📋 TABLE OF CONTENTS
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Integration Steps](#integration-steps)
5. [Testing](#testing)
6. [Production Deployment](#production-deployment)
7. [Usage Examples](#usage-examples)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 PREREQUISITES

- Python 3.8+
- Django 4.0+
- OpenAI API key (get from https://platform.openai.com)
- Your existing Medicine Inventory Manager project

---

## 📦 INSTALLATION

### Step 1: Install Dependencies

```bash
cd /path/to/MedicineInventoryManager
pip install openai>=1.12.0 python-dotenv>=1.0.0
```

### Step 2: Create Assistant App

```bash
python manage.py startapp assistant
```

### Step 3: Copy Files

Copy the following files to your project:

```
assistant/
├── __init__.py
├── views.py              (provided)
├── urls.py               (provided)
├── templates/
│   └── assistant/
│       └── dashboard.html (provided)
└── management/
    └── commands/
        └── check_stock_alerts.py (provided)
```

---

## ⚙️ CONFIGURATION

### Step 1: Update settings.py

Add to your `settings.py`:

```python
# Add 'assistant' to INSTALLED_APPS
INSTALLED_APPS = [
    # ... your existing apps
    'assistant',
]

# Load environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration (for alerts)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@example.com')

# Admin emails for alerts
ADMIN_EMAILS = os.getenv('ADMIN_EMAILS', '').split(',')
```

### Step 2: Update Main URLs

Add to your main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... your existing URLs
    path('assistant/', include('assistant.urls')),
]
```

### Step 3: Create .env File

Create a `.env` file in your project root:

```bash
# .env
OPENAI_API_KEY=sk-your-actual-openai-key-here
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
ADMIN_EMAILS=admin@example.com
```

**Important**: Add `.env` to your `.gitignore`!

---

## 🔗 INTEGRATION STEPS

### Step 1: Update views.py Imports

In `assistant/views.py`, update the model imports to match your actual models:

```python
# Change this line based on your app structure
from inventory.models import Medicine, Supplier, Batch, Transaction

# If your models are in a different app, adjust accordingly
# from pharmacy.models import Medicine, Supplier
```

### Step 2: Customize Database Schema

Update the `get_database_schema()` method in `assistant/views.py` to match your actual database structure. Look at your models and adjust the field names/types accordingly.

### Step 3: Add Navigation Link

Add a link to the assistant in your main navigation template:

```html
<!-- In your base template or navigation -->
<a href="{% url 'assistant:dashboard' %}">
    🤖 AI Assistant
</a>
```

### Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🧪 TESTING

### Test 1: Access the Dashboard

```bash
python manage.py runserver
```

Visit: http://localhost:8000/assistant/

You should see the AI Assistant dashboard with chat interface.

### Test 2: Test Chat Functionality

Try these messages in the chat:
- "What medicines are low on stock?"
- "Show me all antibiotics"
- "How many items are expiring this month?"

### Test 3: Generate Analysis

Click the "Generate Stock Analysis" button. It should produce an AI-generated report.

### Test 4: Test Automated Alerts

```bash
python manage.py check_stock_alerts --verbose
```

---

## 🚀 PRODUCTION DEPLOYMENT

### 1. Security Best Practices

```python
# settings.py - Production settings

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# Use environment variables for sensitive data
SECRET_KEY = os.environ['SECRET_KEY']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Enable CSRF protection
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']
```

### 2. Set Up Automated Alerts (Cron Job)

Add to crontab:

```bash
# Check stock every day at 8 AM and send email alerts
0 8 * * * cd /path/to/project && /path/to/venv/bin/python manage.py check_stock_alerts --send-email
```

Or use Django-cron/Celery for more robust scheduling.

### 3. Rate Limiting (Optional)

Install django-ratelimit:

```bash
pip install django-ratelimit
```

Add to views:

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/m', method='POST')
@csrf_exempt
def assistant_chat(request):
    # ... existing code
```

### 4. Caching (Optional)

Add Redis caching for frequently asked questions:

```python
from django.core.cache import cache

def assistant_chat(request):
    # Check cache first
    cache_key = f"chat_{hash(user_message)}"
    cached_response = cache.get(cache_key)
    
    if cached_response:
        return JsonResponse(cached_response)
    
    # ... generate response
    
    # Cache for 1 hour
    cache.set(cache_key, result, 3600)
```

---

## 💡 USAGE EXAMPLES

### Example 1: Natural Language Queries

**User**: "Show me all medicines that will expire in the next 2 weeks"

**Assistant**: Queries database and returns formatted results with recommendations.

### Example 2: Stock Analysis

**User**: Clicks "Generate Stock Analysis"

**Assistant**: 
- Analyzes current stock levels
- Identifies critical shortages
- Recommends reorder quantities
- Highlights expiring items
- Calculates total inventory value

### Example 3: Automated Alerts

```bash
# Run daily to check stock and send alerts
python manage.py check_stock_alerts --send-email --verbose
```

**Output**:
```
URGENT STOCK ALERTS:

Critical Items:
1. Paracetamol 500mg - OUT OF STOCK
2. Amoxicillin 250mg - Only 50 units (below reorder level of 200)
3. Ibuprofen 400mg - Expires in 10 days (150 units)

Recommendations:
- Reorder Paracetamol immediately (suggested: 500 units)
- Contact supplier for Amoxicillin rush order
- Consider discount promotion for Ibuprofen to clear before expiry
```

---

## 🔍 CUSTOMIZATION OPTIONS

### 1. Modify AI Personality

Edit the system prompt in `views.py`:

```python
system_prompt = f"""You are a friendly and helpful pharmacy assistant.
Use a warm, professional tone. Always prioritize patient safety.
{self.get_database_schema()}
"""
```

### 2. Add Custom Commands

Add to `assistant/views.py`:

```python
def handle_custom_command(self, command, data):
    """Handle special commands like /reorder, /supplier, etc."""
    if command == '/reorder':
        return self.generate_reorder_list()
    elif command == '/supplier':
        return self.find_best_supplier(data)
    # ... add more commands
```

### 3. Add Voice Interface (Future Enhancement)

```javascript
// In dashboard.html
const recognition = new webkitSpeechRecognition();
recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('chatInput').value = transcript;
    sendMessage();
};
```

---

## 🐛 TROUBLESHOOTING

### Issue 1: "Module not found" Error

**Problem**: `ImportError: No module named 'openai'`

**Solution**:
```bash
pip install openai python-dotenv
```

### Issue 2: OpenAI API Key Error

**Problem**: `openai.error.AuthenticationError`

**Solution**:
1. Check your `.env` file has correct API key
2. Verify the key at https://platform.openai.com/api-keys
3. Ensure no extra spaces in the key

### Issue 3: Chat Not Responding

**Problem**: Chat sends message but no response

**Solution**:
1. Check browser console for errors (F12)
2. Verify URL routing is correct
3. Check Django logs for backend errors
4. Ensure CSRF token is properly configured

### Issue 4: Database Query Errors

**Problem**: `FieldError: Cannot resolve keyword`

**Solution**:
Update model imports in `views.py` to match your actual field names:

```python
# Check your actual model fields
from inventory.models import Medicine
print(Medicine._meta.get_fields())  # See all available fields
```

### Issue 5: Email Alerts Not Sending

**Problem**: Alerts generate but no email received

**Solution**:
1. Check email configuration in `.env`
2. For Gmail, enable "App Passwords" in security settings
3. Test email manually:
```python
from django.core.mail import send_mail
send_mail('Test', 'Body', 'from@example.com', ['to@example.com'])
```

---

## 📊 PERFORMANCE OPTIMIZATION

### 1. Database Query Optimization

```python
# Use select_related and prefetch_related
low_stock = Medicine.objects.select_related('supplier').filter(
    current_stock__lte=F('reorder_level')
)
```

### 2. Async Chat (for better UX)

```python
# views.py - Use async views (Django 4.1+)
from django.views.decorators.http import require_http_methods
import asyncio

@require_http_methods(["POST"])
async def assistant_chat_async(request):
    # ... async implementation
```

### 3. Streaming Responses

For long AI responses, implement streaming:

```javascript
// frontend - Use fetch with streaming
const response = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
});

const reader = response.body.getReader();
// ... process stream
```

---

## 🎯 NEXT STEPS

1. **Test thoroughly** with your actual data
2. **Customize prompts** to match your business needs
3. **Add more features**:
   - Inventory forecasting
   - Automatic reorder emails to suppliers
   - Multi-language support
   - Voice commands
   - Mobile app integration
4. **Monitor usage** and iterate based on user feedback
5. **Set up monitoring** (Sentry, logging) for production

---

## 📚 ADDITIONAL RESOURCES

- OpenAI API Docs: https://platform.openai.com/docs
- Django Best Practices: https://docs.djangoproject.com/
- Rate Limiting: https://django-ratelimit.readthedocs.io/

---

## ✅ CHECKLIST

Before going to production:

- [ ] API keys secured in environment variables
- [ ] .env added to .gitignore
- [ ] Database queries optimized
- [ ] Error handling implemented
- [ ] Rate limiting configured
- [ ] Email alerts tested
- [ ] User authentication added to assistant views
- [ ] HTTPS configured
- [ ] Logging set up
- [ ] Backup strategy in place

---

Need help? Create an issue on GitHub or contact support!

**Version**: 1.0.0  
**Last Updated**: January 2025
