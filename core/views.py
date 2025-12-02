import google.generativeai as genai
import re
import json
import os
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Transaction, Subscription, Certificate
from .serializers import UserSerializer, TransactionSerializer, SubscriptionSerializer

# GLOBAL MEMORY
CHAT_HISTORY = []

# --- MISSING BODY PARTS (RESTORED) ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

# --- THE NEW BRAIN (RAG + AI) ---
class AIChatView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        # Use the Key from the Cloud Settings (Safe Mode)
        api_key = os.environ.get("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        
        # 1. LOAD KNOWLEDGE BASE (RAG)
        knowledge_text = ""
        try:
            file_path = os.path.join(settings.BASE_DIR, 'core', 'courses.json')
            with open(file_path, 'r') as f:
                data = json.load(f)
                knowledge_text = json.dumps(data, indent=2)
        except Exception as e:
            print(f"Knowledge Error: {e}")
            knowledge_text = "No course data available currently."

        # 2. SYSTEM INSTRUCTION
        system_instruction = f"""
        You are GenB, the assistant for 'The Skill Bridge' in Tshwane.
        
        YOUR KNOWLEDGE BASE (OFFICIAL COURSES):
        {knowledge_text}
        
        YOUR IDENTITY:
        - Use the course list above to answer questions about prices, duration, and content.
        - If asked about a course NOT on the list, say you don't offer it yet.
        - Speak English mixed with Pitori slang (Heita, Sharp, Aweh).
        - Be professional but local.
        
        TASKS:
        1. REGISTRATION: Ask for Username + Email. Output ONLY: ACTION_REGISTER: [Name] [Email]
        2. VERIFICATION: Look for TSB codes.
        3. SALES: Recommend courses from the list above.
        """
        
        model = genai.GenerativeModel('gemini-flash-latest')
        
        user_message = request.data.get('message')
        
        if not user_message:
            return Response({'error': 'No message provided'}, status=400)
            
        try:
            # Update History
            CHAT_HISTORY.append(f"User: {user_message}")
            recent_history = "\n".join(CHAT_HISTORY[-10:])
            
            # Build Prompt
            full_prompt = f"{system_instruction}\n\nHISTORY:\n{recent_history}\n\nUser says: {user_message}"
            print(f"Human: {user_message}")
            
            # Generate
            chat_response = model.generate_content(full_prompt)
            ai_text = chat_response.text.strip()
            final_response = ai_text
            
            # --- LOGIC HANDLERS ---
            
            # HANDLER A: REGISTRATION
            if "ACTION_REGISTER:" in ai_text:
                try:
                    clean_data = ai_text.replace("ACTION_REGISTER:", "").strip()
                    parts = clean_data.split()
                    if len(parts) >= 2:
                        new_username = parts[0]
                        new_email = parts[1]
                        User.objects.create_user(username=new_username, email=new_email)
                        final_response = f"Sharp! Registered {new_username} successfully."
                    else:
                        final_response = "Eish, I need both Username and Email."
                except Exception as e:
                    final_response = "That username is taken, my bra."

            # HANDLER B: CERTIFICATE VERIFICATION
            elif "verify" in user_message.lower() or "check" in user_message.lower():
                match = re.search(r'TSB-[A-Z0-9\-]+', user_message.upper())
                if match:
                    code_to_check = match.group(0)
                    try:
                        cert = Certificate.objects.get(certificate_id=code_to_check)
                        final_response = (
                            f"✅ VERIFIED!\n"
                            f"Student: {cert.user.username}\n"
                            f"Course: {cert.course_name}\n"
                            f"Code: {cert.certificate_id}"
                        )
                    except Certificate.DoesNotExist:
                        final_response = f"❌ INVALID. Code {code_to_check} not found."

            # ----------------------

            CHAT_HISTORY.append(f"GenB: {final_response}")
            print(f"GenB: {final_response}")
            
            return Response({'response': final_response})
            
        except Exception as e:
            print(f"Error: {e}")
            return Response({'error': str(e)}, status=500)

# The Frontend View
def chat_interface(request):
    return render(request, 'core/chat.html')
