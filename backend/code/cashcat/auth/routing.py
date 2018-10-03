def auth_routing(routing):
    routing.add("cashcat.auth.views.LoginView", "login", "/auth/login")
    routing.add("cashcat.auth.views.SignUpView", "sign_up", "/auth/signup")
