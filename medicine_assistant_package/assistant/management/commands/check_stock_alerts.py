# assistant/management/commands/check_stock_alerts.py
"""
Management command to check stock levels and send alerts
Run with: python manage.py check_stock_alerts
Can be added to cron job for automated monitoring
"""

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import openai
import os

# Adjust import based on your models
# from inventory.models import Medicine, Batch


class Command(BaseCommand):
    help = 'Check inventory stock levels and generate alerts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--send-email',
            action='store_true',
            help='Send email alerts to administrators',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Print detailed output',
        )

    def handle(self, *args, **options):
        self.stdout.write('Checking inventory stock levels...')
        
        # Import your models
        from inventory.models import Medicine
        
        # Get critical items
        low_stock_items = list(Medicine.objects.filter(
            current_stock__lte=models.F('reorder_level')
        ).values('name', 'current_stock', 'reorder_level'))
        
        out_of_stock = list(Medicine.objects.filter(
            current_stock=0
        ).values('name', 'category'))
        
        expiring_soon = list(Medicine.objects.filter(
            expiry_date__lte=timezone.now() + timedelta(days=30),
            expiry_date__gte=timezone.now()
        ).values('name', 'expiry_date', 'current_stock'))
        
        # Generate AI-powered alert summary
        alert_summary = self.generate_ai_summary({
            'low_stock': low_stock_items,
            'out_of_stock': out_of_stock,
            'expiring_soon': expiring_soon
        })
        
        if options['verbose']:
            self.stdout.write(self.style.SUCCESS('\n' + alert_summary))
        
        # Send email if requested
        if options['send_email'] and (low_stock_items or out_of_stock or expiring_soon):
            self.send_alert_email(alert_summary)
        
        # Summary
        self.stdout.write(self.style.SUCCESS(
            f'\nSummary:'
            f'\n- Low stock items: {len(low_stock_items)}'
            f'\n- Out of stock: {len(out_of_stock)}'
            f'\n- Expiring soon: {len(expiring_soon)}'
        ))
    
    def generate_ai_summary(self, data):
        """Generate AI-powered alert summary"""
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        prompt = f"""Generate a concise, actionable stock alert summary for a pharmacy inventory system.

Data:
- Low stock items: {len(data['low_stock'])}
- Out of stock items: {len(data['out_of_stock'])}
- Expiring soon (30 days): {len(data['expiring_soon'])}

Details:
{data}

Provide:
1. Most urgent items requiring immediate action
2. Brief recommendations
3. Priority order

Keep it under 200 words and actionable."""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a pharmacy inventory specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def send_alert_email(self, summary):
        """Send alert email to administrators"""
        try:
            send_mail(
                subject='[URGENT] Medicine Inventory Alerts',
                message=summary,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=settings.ADMIN_EMAILS,
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Alert email sent successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}'))
