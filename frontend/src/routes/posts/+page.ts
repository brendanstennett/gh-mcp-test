import type { PageLoad } from './$types.js';

export const load: PageLoad = async ({ fetch, parent }) => {
  // Load posts
  const res = await fetch('/api/v1/posts', {
    credentials: 'include',
  });
  const data = await res.json();

  return {
    posts: data,
  };
};
