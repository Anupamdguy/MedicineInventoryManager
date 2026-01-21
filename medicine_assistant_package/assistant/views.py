# assistant/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum, Count, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import timedelta
import json
import openai
import os
from decimal import Decimal

# Import your models (adjust based on your actual models)
# from inventory.models import Medicine, Supplier, Batch, Transaction


class MedicineAssistant:
    """
    AI Assistant for Medicine Inventory Management
    Handles natural language queries and provides intelligent stock analysis
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def get_database_schema(self):
        """Return database schema for context"""
        return """
        Database Schema:
        
        Medicine Table:
        - id: Primary key
        - name: Medicine name
        - generic_name: Generic/scientific name
        - manufacturer: Manufacturer name
        - category: Medicine category (e.g., Antibiotic, Painkiller)
        - unit_price: Price per unit
        - current_stock: Current quantity in stock
        - reorder_level: Minimum stock level before reorder
        - expiry_date: Expiration date
        - description: Medicine description
        
        Supplier Table:
        - id: Primary key
        - name: Supplier name
        - contact_person: Contact person
        - email: Email address
        - phone: Phone number
        - address: Physical address
        
        Batch Table:
        - id: Primary key
        - medicine: Foreign key to Medicine
        - batch_number: Unique batch identifier
        - quantity: Quantity in batch
        - manufacturing_date: Date manufactured
        - expiry_date: Expiration date
        - supplier: Foreign key to Supplier
        - purchase_date: Date purchased
        
        Transaction Table:
        - id: Primary key
        - medicine: Foreign key to Medicine
        - transaction_type: 'IN' or 'OUT'
        - quantity: Quantity transacted
        - transaction_date: Date of transaction
        - notes: Additional notes
        """
    
    def generate_sql_query(self, user_query):
        """
        Generate SQL query from natural language using GPT-4
        """
        system_prompt = f"""You are an expert SQL query generator for a medicine inventory management system.
        
        {self.get_database_schema()}
        
        Generate SAFE, READ-ONLY SQL queries based on user questions.
        
        Rules:
        1. Only SELECT queries allowed (no INSERT, UPDATE, DELETE, DROP)
        2. Use Django ORM-style queries when possible
        3. Return the query in JSON format with: {{"query_type": "django_orm" or "raw_sql", "query": "the query", "explanation": "brief explanation"}}
        4. For complex aggregations, use raw SQL with proper JOINs
        5. Always include relevant filters and sorting
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_stock_levels(self):
        """
        Automated stock analysis using LLM
        """
        # This would use your actual models
        # For now, showing the structure
        from inventory.models import Medicine
        
        # Get critical stock data
        low_stock = Medicine.objects.filter(
            current_stock__lte=F('reorder_level')
        ).values('name', 'current_stock', 'reorder_level')
        
        expiring_soon = Medicine.objects.filter(
            expiry_date__lte=timezone.now() + timedelta(days=30)
        ).values('name', 'expiry_date', 'current_stock')
        
        out_of_stock = Medicine.objects.filter(current_stock=0).values('name', 'category')
        
        # Prepare data for LLM analysis
        analysis_data = {
            "low_stock_items": list(low_stock),
            "expiring_soon": list(expiring_soon),
            "out_of_stock": list(out_of_stock),
            "total_medicines": Medicine.objects.count(),
            "total_value": Medicine.objects.aggregate(
                total=Sum(F('current_stock') * F('unit_price'))
            )['total']
        }
        
        system_prompt = """You are an expert pharmaceutical inventory analyst.
        Analyze the provided inventory data and provide:
        1. Critical issues that need immediate attention
        2. Recommendations for restocking
        3. Financial insights
        4. Trend observations
        
        Be concise, actionable, and prioritize by urgency.
        Format your response in clear sections with bullet points.
        """
        
        user_prompt = f"""Analyze this medicine inventory data:
        
        {json.dumps(analysis_data, indent=2, default=str)}
        
        Provide a comprehensive analysis with actionable recommendations.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating analysis: {str(e)}"
    
    def chat(self, user_message, conversation_history=None):
        """
        General chat interface for the assistant
        Handles queries, provides insights, and helps with inventory decisions
        """
        if conversation_history is None:
            conversation_history = []
        
        # Get current inventory context
        from inventory.models import Medicine
        
        context_data = {
            "total_medicines": Medicine.objects.count(),
            "low_stock_count": Medicine.objects.filter(
                current_stock__lte=F('reorder_level')
            ).count(),
            "out_of_stock_count": Medicine.objects.filter(current_stock=0).count(),
        }
        
        system_prompt = f"""You are an intelligent assistant for a medicine inventory management system.
        
        Current System Status:
        - Total medicines in database: {context_data['total_medicines']}
        - Items with low stock: {context_data['low_stock_count']}
        - Out of stock items: {context_data['out_of_stock_count']}
        
        {self.get_database_schema()}
        
        Your capabilities:
        1. Answer questions about inventory
        2. Provide stock recommendations
        3. Help with reorder decisions
        4. Analyze trends and patterns
        5. Explain medicine categories and uses
        
        Be helpful, concise, and professional. If you need to query the database, 
        explain what information you need and I'll fetch it for you.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            return {
                "response": assistant_message,
                "conversation_history": messages + [
                    {"role": "assistant", "content": assistant_message}
                ]
            }
        except Exception as e:
            return {
                "response": f"I encountered an error: {str(e)}",
                "conversation_history": conversation_history
            }


# Views
@csrf_exempt
def assistant_chat(request):
    """
    Handle chat messages from the frontend
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            conversation_history = data.get('history', [])
            
            assistant = MedicineAssistant()
            result = assistant.chat(user_message, conversation_history)
            
            return JsonResponse({
                'success': True,
                'response': result['response'],
                'history': result['conversation_history']
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)


@csrf_exempt
def generate_analysis(request):
    """
    Generate automated stock analysis
    """
    if request.method == 'GET':
        try:
            assistant = MedicineAssistant()
            analysis = assistant.analyze_stock_levels()
            
            return JsonResponse({
                'success': True,
                'analysis': analysis
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Only GET requests allowed'}, status=405)


@csrf_exempt
def natural_language_query(request):
    """
    Convert natural language to SQL query and execute
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_query = data.get('query', '')
            
            assistant = MedicineAssistant()
            query_result = assistant.generate_sql_query(user_query)
            
            if 'error' in query_result:
                return JsonResponse({
                    'success': False,
                    'error': query_result['error']
                }, status=400)
            
            # Execute the query (implement based on query_type)
            # This is a simplified version - add proper execution logic
            
            return JsonResponse({
                'success': True,
                'query_info': query_result,
                'message': 'Query generated successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)


def assistant_dashboard(request):
    """
    Render the assistant dashboard page
    """
    return render(request, 'assistant/dashboard.html')
