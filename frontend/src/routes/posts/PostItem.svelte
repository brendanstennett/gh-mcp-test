<script lang="ts">
  import { authStore, type User } from '$lib/auth-client';
  import { type Post } from '$lib/api-types';

  const { post, user }: { post: Post; user?: User } = $props();
</script>

<section>
  <h2>{post.title}</h2>
  <div>{post.body}</div>
  {#if $authStore.isAuthenticated}
    <div class="controls">
      <a href="/posts/edit/{post.id}">Edit</a>
    </div>
  {/if}
</section>

<style>
  .controls {
    margin-top: 5px;
  }
</style>
