from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import os
import webbrowser
import subprocess


def index(request):
    return render(request, 'index.html')

def register(request):
   if request.method == 'POST':
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']
      password2 = request.POST['password2']
    
      if password == password2:
          
          if User.objects.filter(email=email).exists():
              messages.info(request,'Email already use')
              return redirect('register')  
            
          elif User.objects.filter(username=username).exists():
              messages.info(request,'Username already exist')
              return redirect('register')
          
          else:
              user = User.objects.create_user(username=username, email=email, password=password)
              user.save()
              return redirect('login')
          
      else:
         messages.info(request,'Password Not Same')  
         return redirect('register')    
      
   return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')  
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
        
    else:
        return render(request, 'login.html')
    
def streamlit_view(request):    
    current_directory = os.path.dirname(os.path.realpath(__file__))
    streamlit_app_path = os.path.join(current_directory, '..', 'scripts', 'streamlit_app.py')

    # Function to run Streamlit app
    def run_streamlit_app():
        subprocess.Popen(['streamlit', 'run', streamlit_app_path])

    # # Run Streamlit app
    run_streamlit_app()

    # Return a response (optional)
    return render(request, 'streamlit_integration.html')

# def streamlit_view2(request):    
#     current_directory = os.path.dirname(os.path.realpath(__file__))
#     streamlit_app_path = os.path.join(current_directory, '..', 'scripts', 'streamlit_app2.py')

#     # Function to run Streamlit app
#     def run_streamlit_app():
#         subprocess.Popen(['streamlit', 'run', streamlit_app_path])

#     # # Run Streamlit app
#     run_streamlit_app()

#     # Return a response (optional)
#     return render(request, 'streamlit_integration1.html')