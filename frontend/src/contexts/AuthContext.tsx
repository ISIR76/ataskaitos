import React, { createContext, useContext, useState, useEffect } from "react";
import { client } from "@/api/client";

interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_STORAGE_KEY = "ataskaitos_auth_token";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => {
    // Load token from localStorage on init
    return localStorage.getItem(TOKEN_STORAGE_KEY);
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch current user when token changes
  useEffect(() => {
    const fetchUser = async () => {
      if (!token) {
        setUser(null);
        setIsLoading(false);
        return;
      }

      try {
        const result = await client.GET("/users/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (result.data) {
          setUser(result.data as User);
        } else {
          // Token invalid, clear it
          setToken(null);
          localStorage.removeItem(TOKEN_STORAGE_KEY);
        }
      } catch (err) {
        console.error("Failed to fetch user:", err);
        setToken(null);
        localStorage.removeItem(TOKEN_STORAGE_KEY);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUser();
  }, [token]);

  const login = async (email: string, password: string) => {
    setError(null);
    setIsLoading(true);

    try {
      // Create FormData for login
      const formData = new FormData();
      formData.append("username", email); // FastAPI-Users expects 'username' field
      formData.append("password", password);

      const result = await client.POST("/auth/jwt/login", {
        // @ts-expect-error - FormData is valid for multipart/form-data
        body: formData,
      });

      if (result.data && "access_token" in result.data) {
        const accessToken = (result.data as { access_token: string }).access_token;
        setToken(accessToken);
        localStorage.setItem(TOKEN_STORAGE_KEY, accessToken);
      } else {
        throw new Error("Login failed: No access token received");
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Login failed";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (email: string, password: string) => {
    setError(null);
    setIsLoading(true);

    try {
      const result = await client.POST("/auth/register", {
        body: {
          email,
          password,
        },
      });

      if (result.error) {
        throw new Error("Registration failed");
      }

      // Auto-login after registration
      await login(email, password);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Registration failed";
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem(TOKEN_STORAGE_KEY);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        error,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
