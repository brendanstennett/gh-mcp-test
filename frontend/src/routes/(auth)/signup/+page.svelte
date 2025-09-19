<script lang="ts">
  import { authClient } from '$lib/auth-client';
  import { goto } from '$app/navigation';
  import SignUpForm from '$lib/../components/auth/SignUpForm.svelte';

  const session = authClient.useSession();

  $effect(() => {
    if ($session?.data) {
      goto('/');
    }
  });

  const handleSignUpSuccess = (event: { user: any }) => {
    goto('/');
  };

  const handleSignUpError = (event: { message: string }) => {
    console.error('Sign up error:', event.message);
  };
</script>

<svelte:head>
  <title>Sign Up</title>
</svelte:head>

<div class="container">
  <div class="form-wrapper">
    <h1>Create Account</h1>
    <p class="subtitle">Sign up for a new account</p>

    <SignUpForm onsuccess={handleSignUpSuccess} onerror={handleSignUpError} />
  </div>
</div>

<style>
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    padding: 1rem;
  }

  .form-wrapper {
    background: white;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow:
      0 20px 25px -5px rgba(0, 0, 0, 0.1),
      0 10px 10px -5px rgba(0, 0, 0, 0.04);
    width: 100%;
    max-width: 420px;
    backdrop-filter: blur(10px);
  }

  h1 {
    text-align: center;
    margin-bottom: 0.5rem;
    color: #1f2937;
    font-size: 1.875rem;
    font-weight: 700;
  }

  .subtitle {
    text-align: center;
    margin-bottom: 2rem;
    color: #6b7280;
    font-size: 1rem;
  }

  @media (max-width: 640px) {
    .container {
      padding: 0.5rem;
    }

    .form-wrapper {
      padding: 1.5rem;
    }

    h1 {
      font-size: 1.5rem;
    }
  }
</style>
