import type { User, UserCreate } from '$lib/api-types';
import { browser } from '$app/environment';
import { writable } from 'svelte/store';

// Export types for backward compatibility
export type { User, UserCreate };

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  loading: true,
};

// Create reactive auth store
function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>(initialState);

  return {
    subscribe,

    async init() {
      if (!browser) return;

      update(state => ({ ...state, loading: true }));

      try {
        const user = await getCurrentUser();
        set({
          user,
          isAuthenticated: true,
          loading: false,
        });
      } catch (error) {
        set({ ...initialState, loading: false });
      }
    },

    async login(email: string, password: string) {
      try {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        formData.append('scope', '');

        const response = await fetch('/auth/login', {
          method: 'POST',
          credentials: 'include', // Include cookies
          body: formData,
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || 'Login failed');
        }

        // Get user info after successful login
        const user = await getCurrentUser();

        set({
          user,
          isAuthenticated: true,
          loading: false,
        });

        return { success: true, user };
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Login failed';
        return { success: false, error: message };
      }
    },

    async register(userData: UserCreate) {
      try {
        const response = await fetch('/auth/register', {
          method: 'POST',
          credentials: 'include', // Include cookies
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData),
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || 'Registration failed');
        }

        const user: User = await response.json();
        return { success: true, user };
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Registration failed';
        return { success: false, error: message };
      }
    },

    async logout() {
      try {
        await fetch('/auth/logout', {
          method: 'POST',
          credentials: 'include', // Include cookies
        });
      } catch (error) {
        console.warn('Logout request failed:', error);
      } finally {
        set({ ...initialState, loading: false });
      }
    },
  };
}

async function getCurrentUser(): Promise<User> {
  const response = await fetch('/auth/users/me', {
    credentials: 'include', // Include cookies
  });

  if (!response.ok) {
    throw new Error('Failed to get current user');
  }

  return response.json();
}

// Helper function to get current store value
function get<T>(store: { subscribe: (fn: (value: T) => void) => () => void }): T {
  let value: T;
  const unsubscribe = store.subscribe(val => (value = val));
  unsubscribe();
  return value!;
}

export const authStore = createAuthStore();

// Initialize auth store when module loads
if (browser) {
  authStore.init();
}

// Helper function to check if user is authenticated
export function isAuthenticated(): boolean {
  const state = get(authStore);
  return state.isAuthenticated;
}

// Helper function for making authenticated API requests
export async function authenticatedFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  return fetch(url, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
}

// Legacy compatibility object for existing components
export const authClient = {
  useSession() {
    return {
      subscribe: authStore.subscribe,
    };
  },

  signIn: {
    email: async ({ email, password }: { email: string; password: string }) => {
      const result = await authStore.login(email, password);
      if (result.success) {
        return { data: { user: result.user }, error: null };
      } else {
        return { data: null, error: { message: result.error } };
      }
    },
  },

  signUp: {
    email: async ({ email, password }: { email: string; password: string }) => {
      const result = await authStore.register({
        email,
        password,
        is_active: true,
        is_superuser: false,
        is_verified: false,
      });
      if (result.success) {
        return { data: { user: result.user }, error: null };
      } else {
        return { data: null, error: { message: result.error } };
      }
    },
  },

  signOut: async () => {
    await authStore.logout();
  },
};
