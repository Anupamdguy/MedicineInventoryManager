# 🤖 AI-Powered Medicine Inventory Assistant

A Django-based intelligent assistant that integrates OpenAI's GPT models into your Medicine Inventory Management System for natural language queries, automated stock analysis, and smart alerts.

## ✨ Features

### 1. **Conversational AI Interface**
- Natural language queries about inventory
- Real-time chat with context awareness
- Quick action buttons for common queries
- Conversation history management

### 2. **Automated Stock Analysis**
- AI-generated insights on inventory levels
- Identification of critical stock issues
- Reorder recommendations
- Financial analysis and trends

### 3. **Smart Alerts**
- Automated daily stock checks
- Email notifications for critical items
- Low stock warnings
- Expiry date tracking (30-day window)

### 4. **Natural Language to SQL**
- Convert user questions to database queries
- Safe, read-only query generation
- Django ORM integration

## 🚀 Quick Start

### Installation

```bash
# 1. Clone or copy the assistant files to your Django project
cp -r assistant/ /path/to/your/django/project/

# 2. Install dependencies
pip install openai python-dotenv

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key

# 4. Update Django settings
# Add 'assistant' to INSTALLED_APPS in settings.py

# 5. Update URLs
# Add path('assistant/', include('assistant.urls')) to main urls.py

# 6. Run migrations
python manage.py migrate

# 7. Test the assistant
python test_assistant.py

# 8. Run the server
python manage.py runserver
```

### Access

Visit: `http://localhost:8000/assistant/`

## 📁 Project Structure

```
assistant/
├── views.py                    # Main assistant logic and API endpoints
├── urls.py                     # URL routing
├── models_example.py           # Reference models (adjust to your schema)
├── templates/
│   └── assistant/
│       └── dashboard.html      # Frontend interface
└── management/
    └── commands/
        └── check_stock_alerts.py  # Automated monitoring

Supporting Files:
├── INTEGRATION_GUIDE.md        # Detailed integration instructions
├── test_assistant.py           # Quick test script
├── requirements_assistant.txt  # Python dependencies
└── .env.example               # Environment variables template
```

## 🎯 Key Components

### MedicineAssistant Class

Core functionality in `views.py`:

```python
class MedicineAssistant:
    def chat(user_message, history)           # Conversational interface
    def analyze_stock_levels()                # Generate analysis reports
    def generate_sql_query(user_query)        # NL to SQL conversion
    def get_database_schema()                 # Context for AI
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/assistant/` | GET | Main dashboard UI |
| `/assistant/api/chat/` | POST | Chat with assistant |
| `/assistant/api/analysis/` | GET | Generate stock analysis |
| `/assistant/api/query/` | POST | Natural language queries |

### Management Commands

```bash
# Check stock and generate alerts
python manage.py check_stock_alerts

# With email notifications
python manage.py check_stock_alerts --send-email

# Verbose output
python manage.py check_stock_alerts --verbose
```

## 💬 Usage Examples

### Example 1: Chat Queries

**User**: "What medicines are running low?"

**Assistant**: 
> Based on current stock levels:
> 
> 1. **Paracetamol 500mg** - Only 50 units left (reorder level: 200)
> 2. **Amoxicillin 250mg** - 30 units remaining (reorder level: 150)
> 
> I recommend placing orders for these items soon.

### Example 2: Stock Analysis

Click "Generate Stock Analysis" button:

```
📊 CRITICAL STOCK ALERTS

Immediate Action Required:
• Ibuprofen 400mg - OUT OF STOCK
  → Reorder urgently (suggested qty: 500 units)

Low Stock Items (2):
• Paracetamol 500mg - 50/200 units (75% below level)
• Amoxicillin 250mg - 30/150 units (80% below level)

Expiring Soon (3):
• Cough Syrup ABC - Expires in 10 days (45 units)
  → Consider promotion to clear stock

Total Inventory Value: $45,000
Estimated Restock Cost: $8,500
```

### Example 3: Automated Monitoring

Set up cron job for daily checks:

```bash
# Add to crontab
0 8 * * * cd /path/to/project && source venv/bin/activate && python manage.py check_stock_alerts --send-email
```

Receives daily email with:
- Critical stock alerts
- Items requiring immediate attention
- Prioritized recommendations

## 🔧 Configuration

### Environment Variables

Required in `.env`:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here

# Email Configuration (for alerts)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Admin emails (comma-separated)
ADMIN_EMAILS=admin1@example.com,admin2@example.com
```

### Django Settings

Add to `settings.py`:

```python
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add assistant to installed apps
INSTALLED_APPS = [
    # ... existing apps
    'assistant',
]

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
# ... other email settings
```

## 🎨 Customization

### 1. Modify AI Personality

Edit system prompts in `views.py`:

```python
system_prompt = """You are a friendly pharmacy assistant.
Be warm, professional, and prioritize patient safety.
"""
```

### 2. Add Custom Query Types

Extend the assistant class:

```python
def handle_supplier_query(self, supplier_name):
    # Custom logic for supplier queries
    pass
```

### 3. Customize Dashboard

Edit `templates/assistant/dashboard.html`:
- Change colors in CSS
- Add new quick action buttons
- Modify layout

## 📊 Performance Tips

### 1. Database Optimization

```python
# Use select_related for foreign keys
Medicine.objects.select_related('supplier').filter(...)

# Use prefetch_related for many-to-many
Medicine.objects.prefetch_related('batches').all()
```

### 2. Caching

```python
from django.core.cache import cache

# Cache frequent queries
cache_key = f"low_stock_{date}"
result = cache.get(cache_key)
if not result:
    result = get_low_stock_items()
    cache.set(cache_key, result, 3600)  # 1 hour
```

### 3. Rate Limiting

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/m')
def assistant_chat(request):
    # Limit to 10 requests per minute per IP
    pass
```

## 🔒 Security Best Practices

1. **Never commit `.env`** - Add to `.gitignore`
2. **Use environment variables** for all sensitive data
3. **Implement rate limiting** to prevent abuse
4. **Add authentication** - Require login to access assistant
5. **Validate input** - Sanitize all user inputs
6. **Use HTTPS** in production
7. **Monitor API usage** - Track OpenAI costs

### Adding Authentication

```python
from django.contrib.auth.decorators import login_required

@login_required
def assistant_dashboard(request):
    return render(request, 'assistant/dashboard.html')
```

## 📈 Monitoring & Analytics

### Track Assistant Usage

```python
# Add to views.py
from django.contrib.admin.models import LogEntry

def log_assistant_query(user, query, response):
    LogEntry.objects.create(
        user=user,
        object_repr=query,
        action_flag=1,  # Addition
        change_message=f"Assistant query: {query[:100]}"
    )
```

### Monitor Costs

```python
# Track token usage
def track_openai_usage(response):
    tokens = response.usage.total_tokens
    cost = tokens * 0.002 / 1000  # Approximate cost
    # Log to database or monitoring service
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Chat not responding

**Solution**:
1. Check browser console (F12) for JavaScript errors
2. Verify OpenAI API key in `.env`
3. Check Django logs for backend errors

**Issue**: Import errors for models

**Solution**:
Update imports in `views.py` to match your model location:
```python
from your_app.models import Medicine, Supplier
```

**Issue**: CSRF token errors

**Solution**:
Add to template:
```html
<script>
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
// Add to fetch headers
</script>
```

## 🚀 Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure allowed hosts
- [ ] Set up HTTPS/SSL
- [ ] Enable rate limiting
- [ ] Add authentication
- [ ] Set up logging
- [ ] Configure backups
- [ ] Monitor API costs
- [ ] Test email alerts
- [ ] Set up cron jobs for automated checks

## 📝 API Reference

### POST `/assistant/api/chat/`

**Request**:
```json
{
  "message": "What medicines are low on stock?",
  "history": []  // Optional conversation history
}
```

**Response**:
```json
{
  "success": true,
  "response": "Currently, these medicines are low on stock...",
  "history": [...]  // Updated history
}
```

### GET `/assistant/api/analysis/`

**Response**:
```json
{
  "success": true,
  "analysis": "STOCK ANALYSIS REPORT\n\nCritical Items:..."
}
```

## 🤝 Contributing

To improve this assistant:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use in your projects!

## 🙏 Acknowledgments

- OpenAI for GPT models
- Django community
- Contributors and testers

## 📞 Support

- Read the `INTEGRATION_GUIDE.md` for detailed setup
- Check troubleshooting section above
- Open an issue on GitHub
- Contact: achetia10518@gmail.com

## 🎓 Learning Resources

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Django Documentation](https://docs.djangoproject.com/)
- [LangChain for Django](https://python.langchain.com/)

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Author**: Anupam Chetia

Made with ❤️ for better inventory management
