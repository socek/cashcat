def auth_routing(routing):
    routing.add(
        'PROJECT.auth.views.LoginView',
        'login',
        '/auth/login')
    routing.add(
        'PROJECT.auth.views.SignUpView',
        'sign_up',
        '/auth/signup')
