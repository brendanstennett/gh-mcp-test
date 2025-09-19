<script lang="ts">
  import { type Post } from '$lib/api-types';
  import PostItem from './PostItem.svelte';

  let { data }: { data: { posts: Post[] } } = $props();
</script>

<h1>Posts</h1>
{#each data.posts as post}
  <PostItem {post} />
  <hr />
{/each}
