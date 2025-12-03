import os
import json
import google.generativeai as genai
import re
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Transaction, Subscription, Certificate
from .serializers import UserSerializer, TransactionSerializer, SubscriptionSerializer

# GLOBAL MEMORY
CHAT_HISTORY = []

# --- VIEWSETS ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

# --- THE SMART BRAIN ---
class AIChatView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        my_api_key = os.environ.get("GOOGLE_API_KEY")
        if not my_api_key:
            return Response({'error': 'Server Error: API Key missing.'}, status=500)

        genai.configure(api_key=my_api_key)

        # 1. LOAD KNOWLEDGE BASE (The Menu)
        course_data = "No course data available."
        try:
            # Look for the file in the core directory
            file_path = os.path.join(settings.BASE_DIR, 'core', 'courses.json')
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Convert JSON to a string so the AI can read it
                course_data = json.dumps(data, indent=2)
        except Exception as e:
            print(f"Error loading courses: {e}")

        # 2. SYSTEM INSTRUCTION (With the Menu injected)
        system_instruction = f"""
        You are GenB, the assistant for 'The Skill Bridge' in Tshwane.
        IDENTITY: Speak English mixed with Pitori slang. Be professional.
        
        YOUR KNOWLEDGE BASE (COURSE LIST):
        {course_data}
        
        TASKS:
        1. SELL COURSES: If users ask about skills, recommend one of OUR courses from the list above. Quote the exact price and duration.
        2. REGISTRATION: Ask for Username + Email. Output: ACTION_REGISTER: [Name] [Email]
        3. VERIFY: Look for TSB-XXXX codes.
        """
        
        model = genai.GenerativeModel('gemini-flash-latest')
        
        user_message = request.data.get('message')
        
        if not user_message:
            return Response({'error': 'No message provided'}, status=400)
            
        try:
            CHAT_HISTORY.append(f"User: {user_message}")
            recent_history = "\n".join(CHAT_HISTORY[-10:])
            
            full_prompt = f"{system_instruction}\n\nHISTORY:\n{recent_history}\n\nUser says: {user_message}"
            print(f"Human: {user_message}")
            
            chat_response = model.generate_content(full_prompt)
            ai_text = chat_response.text.strip()
            final_response = ai_text
            
            # --- ACTIONS ---
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

            elif "verify" in user_message.lower() or "check" in user_message.lower():
                match = re.search(r'TSB-[A-Z0-9\-]+', user_message.upper())
                if match:
                    code = match.group(0)
                    try:
                        cert = Certificate.objects.get(certificate_id=code)
                        final_response = f"✅ VERIFIED!\nStudent: {cert.user.username}\nCourse: {cert.course_name}\nCode: {cert.certificate_id}"
                    except Certificate.DoesNotExist:
                        final_response = f"❌ INVALID. Code {code} not found."

            # --- END ACTIONS ---

            CHAT_HISTORY.append(f"GenB: {final_response}")
            print(f"GenB: {final_response}")
            
            return Response({'response': final_response})
            
        except Exception as e:
            print(f"Error: {e}")
            return Response({'error': str(e)}, status=500)

def chat_interface(request):
    return render(request, 'core/chat.html')
