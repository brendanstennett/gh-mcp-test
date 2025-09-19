<script lang="ts">
  import { authStore } from '$lib/auth-client';
  import { goto } from '$app/navigation';

  interface Props {
    redirectOnSuccess?: boolean;
    redirectTo?: string;
    showSignInLink?: boolean;
    onsuccess?: (event: { user: any }) => void;
    onerror?: (event: { message: string }) => void;
  }

  let {
    redirectOnSuccess = true,
    redirectTo = '/',
    showSignInLink = true,
    onsuccess,
    onerror,
  }: Props = $props();

  let email = $state('');
  let password = $state('');
  let confirmPassword = $state('');
  let loading = $state(false);
  let error = $state('');

  const handleSubmit = async (event: Event) => {
    event.preventDefault();

    if (!email || !password || !confirmPassword) {
      error = 'Please fill in all fields';
      return;
    }

    if (password !== confirmPassword) {
      error = 'Passwords do not match';
      return;
    }

    if (password.length < 8) {
      error = 'Password must be at least 8 characters long';
      return;
    }

    loading = true;
    error = '';

    try {
      const result = await authStore.register({
        email,
        password,
        is_active: true,
        is_superuser: false,
        is_verified: false,
      });

      if (!result.success) {
        console.error('Signup error:', result.error);
        error = result.error || 'Sign up failed';
        onerror?.({ message: error });
      } else {
        onsuccess?.({ user: result.user });

        if (redirectOnSuccess) {
          goto(redirectTo);
        }
      }
    } catch (err) {
      console.error('Signup exception:', err);
      error = err instanceof Error ? err.message : 'An unexpected error occurred';
      onerror?.({ message: error });
    } finally {
      loading = false;
    }
  };
</script>

<div class="signup-form">
  {#if error}
    <div class="error" role="alert">
      {error}
    </div>
  {/if}

  <form onsubmit={handleSubmit}>
    <div class="form-group">
      <label for="email">Email:</label>
      <input
        type="email"
        id="email"
        name="email"
        bind:value={email}
        required
        disabled={loading}
        autocomplete="email"
        placeholder="Enter your email"
      />
    </div>

    <div class="form-group">
      <label for="password">Password:</label>
      <input
        type="password"
        id="password"
        name="password"
        bind:value={password}
        required
        disabled={loading}
        autocomplete="new-password"
        placeholder="Enter your password"
        minlength="8"
      />
    </div>

    <div class="form-group">
      <label for="confirm-password">Confirm Password:</label>
      <input
        type="password"
        id="confirm-password"
        name="confirm-password"
        bind:value={confirmPassword}
        required
        disabled={loading}
        autocomplete="new-password"
        placeholder="Confirm your password"
        minlength="8"
      />
    </div>

    <button type="submit" disabled={loading} class="signup-button">
      {#if loading}
        <span class="spinner"></span>
        Creating account...
      {:else}
        Create Account
      {/if}
    </button>
  </form>

  {#if showSignInLink}
    <p class="signin-link">
      Already have an account? <a href="/login">Sign in</a>
    </p>
  {/if}
</div>

<style>
  .signup-form {
    width: 100%;
    max-width: 400px;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #374151;
    font-size: 0.875rem;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 1rem;
    box-sizing: border-box;
    transition: all 0.2s ease-in-out;
    background-color: #ffffff;
  }

  input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  input:disabled {
    background-color: #f9fafb;
    cursor: not-allowed;
    opacity: 0.6;
  }

  input::placeholder {
    color: #9ca3af;
  }

  .signup-button {
    width: 100%;
    padding: 0.75rem 1rem;
    background-color: #10b981;
    color: white;
    border: none;
    border-radius: 0.375rem;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .signup-button:hover:not(:disabled) {
    background-color: #059669;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
  }

  .signup-button:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(16, 185, 129, 0.4);
  }

  .signup-button:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .spinner {
    width: 1rem;
    height: 1rem;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .error {
    background-color: #fef2f2;
    color: #dc2626;
    padding: 0.75rem;
    border-radius: 0.375rem;
    margin-bottom: 1rem;
    border: 1px solid #fecaca;
    font-size: 0.875rem;
  }

  .signin-link {
    text-align: center;
    margin-top: 1.5rem;
    color: #6b7280;
    font-size: 0.875rem;
  }

  .signin-link a {
    color: #10b981;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s ease-in-out;
  }

  .signin-link a:hover {
    color: #059669;
    text-decoration: underline;
  }
</style>
