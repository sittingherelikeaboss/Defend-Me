import { LoginForm } from "../LoginForm/LoginForm";
import { Dashboard } from "../Dashboard/Dashboard";

export const nav = [
     { path:     "/",         name: "Home",        element: <LoginForm />,       isMenu: true,     isPrivate: false  },
     { path:     "/login",    name: "Login",       element: <LoginForm />,      isMenu: false,    isPrivate: false  },
     { path:     "/dashboard",  name: "Dashboard",     element: <Dashboard />,    isMenu: true,     isPrivate: true  },
];