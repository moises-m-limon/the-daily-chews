"use client";

import Post from "./Post";

interface Post {
  id: number;
  username: string;
  imageUrl: string;
  caption: string;
  likes: number;
}

interface FeedProps {
  posts: Post[];
}

export default function Feed({ posts }: FeedProps) {
  return (
    <div className="feed">
      {posts.map((post) => (
        <Post key={post.id} {...post} />
      ))}
    </div>
  );
}
