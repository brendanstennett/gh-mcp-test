<script lang="ts">
  import { goto } from '$app/navigation';
  import { type Post } from '$lib/api-types';

  let { data }: { data: { post: Post } } = $props();

  let post = $state<Post>({ ...data.post });
  let loading = $state(false);
  let error = $state('');

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();

    loading = true;
    error = '';

    try {
      const response = await fetch(`/api/v1/posts/${data.post.id}`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(post),
      });

      if (!response.ok) {
        const errorData = await response.json();
        error = errorData.error || 'Failed to update post';
        return;
      }

      goto('/posts');
    } catch (err) {
      error = `An error occurred while updating the post: ${err}`;
    } finally {
      loading = false;
    }
  }

  function handleCancel() {
    goto('/posts');
  }
</script>

<svelte:head>
  <title>Edit Post - {post.title}</title>
</svelte:head>

<div class="container">
  <h1>Edit Post</h1>
  {#if error}
    <div class="error-message">{error}</div>
  {/if}
  <form onsubmit={handleSubmit} class="edit-form">
    <div class="form-group">
      <label for="title">Title</label>
      <input id="title" type="text" bind:value={post.title} disabled={loading} class="form-input" />
    </div>

    <div class="form-group">
      <label for="body">Body</label>
      <textarea id="body" bind:value={post.body} rows="10" disabled={loading} class="form-textarea"
      ></textarea>
    </div>

    <div class="form-group">
      <label class="checkbox-label">
        <input type="checkbox" bind:checked={post.is_published} disabled={loading} />
        Published
      </label>
    </div>

    <div class="form-actions">
      <button type="submit" disabled={loading} class="btn btn-primary">
        {loading ? 'Saving...' : 'Save Changes'}
      </button>
      <button type="button" onclick={handleCancel} disabled={loading} class="btn btn-secondary">
        Cancel
      </button>
    </div>
  </form>
</div>

<style>
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }

  .edit-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  label {
    font-weight: 600;
    color: #374151;
  }

  .form-input,
  .form-textarea {
    padding: 10px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 14px;
  }

  .form-input:focus,
  .form-textarea:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .form-textarea {
    resize: vertical;
    min-height: 120px;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 400;
    cursor: pointer;
  }

  .checkbox-label input[type='checkbox'] {
    width: 18px;
    height: 18px;
    cursor: pointer;
  }

  .error-message {
    color: #dc2626;
    background-color: #fee2e2;
    border: 1px solid #fecaca;
    padding: 10px;
    border-radius: 4px;
    font-size: 14px;
    margin: 0 0 10px;
  }

  .form-actions {
    display: flex;
    gap: 10px;
    margin-top: 10px;
  }

  .btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .btn-primary {
    background-color: #3b82f6;
    color: white;
  }

  .btn-primary:hover:not(:disabled) {
    background-color: #2563eb;
  }

  .btn-secondary {
    background-color: #6b7280;
    color: white;
  }

  .btn-secondary:hover:not(:disabled) {
    background-color: #4b5563;
  }
</style>
