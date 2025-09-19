<script lang="ts">
  import Account from '../components/auth/Account.svelte';

  let { children }: { children: any } = $props();
</script>

<header>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/posts">Posts</a></li>
    </ul>
  </nav>
  <Account />
</header>

{@render children()}

<style>
  ul {
    padding-left: 0;
    display: flex;
    list-style: none;
  }

  ul li {
    margin-left: 20px;
  }

  ul li:first-child {
    margin-left: 0;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
</style>
