from django.shortcuts import render
from deploy.apps.users.models import User


def list_users(request):

	users = User.objects.all()
	template = "index.html"
	context = {
		"users": users
	}
	return render(request, template, context)
