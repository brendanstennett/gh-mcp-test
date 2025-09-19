import type { PageLoad } from './$types.js';

export const load: PageLoad = async ({ fetch, params }) => {
  const res = await fetch(`/api/v1/posts/${params.id}`, {
    credentials: 'include',
  });
  const data = await res.json();

  if (!res.ok) {
    throw new Error('Post not found');
  }

  return {
    post: data,
  };
};
