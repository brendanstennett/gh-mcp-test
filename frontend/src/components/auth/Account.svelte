<script lang="ts">
  import { authStore } from '$lib/auth-client';
  import { goto } from '$app/navigation';

  const signOut = async (event: MouseEvent) => {
    event.preventDefault();
    await authStore.logout();
    goto('/');
  };
</script>

<div id="session">
  {#if $authStore.isAuthenticated && $authStore.user}
    <div>
      Welcome, {$authStore.user.email}
      (<a href="/" onclick={signOut}>Sign Out</a>)
    </div>
  {:else}
    <div>
      <a href="/login">Sign In</a>
    </div>
  {/if}
</div>

<style>
  #session {
    margin-right: 0;
  }
</style>
